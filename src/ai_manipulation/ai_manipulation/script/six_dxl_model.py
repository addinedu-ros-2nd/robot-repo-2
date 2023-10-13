from math import exp
import os
import rclpy
import select
import sys
import threading

import numpy as np
from multiprocessing import Process
import argparse
import os
import platform
import sys
from pathlib import Path
import torch
import cv2
import time

from ultralytics.utils.plotting import Annotator, colors, save_one_box

from ai_manipulation.utils.models.common import DetectMultiBackend
from ai_manipulation.utils.utils.dataloaders import IMG_FORMATS, VID_FORMATS, LoadImages, LoadScreenshots, LoadStreams
from ai_manipulation.utils.utils.general import (LOGGER, Profile, check_file, check_img_size, check_imshow, check_requirements, colorstr, cv2,
                           increment_path, non_max_suppression, print_args, scale_boxes, strip_optimizer, xyxy2xywh)
from ai_manipulation.utils.utils.torch_utils import select_device, smart_inference_mode
from ai_manipulation.utils.utils.utils import ARUCO_DICT

import joblib
import json
import random
from sklearn.linear_model import LinearRegression
import scipy.stats as stats

from array import array
from std_msgs.msg import Float64MultiArray
# from open_manipulator_msgs.msg import KinematicsPose, OpenManipulatorState
# from open_manipulator_msgs.srv import SetJointPosition, SetKinematicsPose
from rclpy.node import Node
# from rclpy.qos import QoSProfile
# from sensor_msgs.msg import JointState

if os.name == 'nt':
    import msvcrt
else:
    import termios
    import tty

import subprocess

package_name = 'ai_manipulation'
output = subprocess.check_output(["ros2", "pkg", "prefix", package_name], text=True)
workspace_path = output.split("/install")[0]

# Params
states_backup = os.path.join(workspace_path, "src", package_name, package_name, "datas/openmanipulator_states.json")
acts_backup = os.path.join(workspace_path, "src", package_name, package_name, "datas/openmanipulator_acts.json")
model_backup = os.path.join(workspace_path, "src", package_name, package_name, "datas/openmanipulator_weight.pkl")
k_path = os.path.join(workspace_path, "src", package_name, package_name, "utils/calibration_matrix.npy")
d_path = os.path.join(workspace_path, "src", package_name, package_name, "utils/distortion_coefficients.npy")
random_state_gen_num = 16
angle_gap_origin = 0.09  # radian
angle_gap = 0.07
path_time = 0.4  # second
state_size = 6
action_size = 4
threshold = 0.11 # scenario ending thres
INF = 999999999999

present_joint_angle = [0.0, 0.0, 0.0, 0.0, 0.0]
goal_joint_angle = [0.0, 0.0, 0.0, 0.0, 0.0]
prev_goal_joint_angle = [0.0, 0.0, 0.0, 0.0, 0.0]
present_kinematics_pose = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
goal_kinematics_pose = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
prev_goal_kinematics_pose = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

e = """
Communications Failed
"""

def pose_esitmation(frame, aruco_dict_type, matrix_coefficients, distortion_coefficients):

    '''
    frame - Frame from the video stream
    matrix_coefficients - Intrinsic matrix of the calibrated camera
    distortion_coefficients - Distortion coefficients associated with your camera

    return:-
    frame - The frame with the axis drawn on it
    '''

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.aruco_dict = cv2.aruco.Dictionary_get(aruco_dict_type)
    parameters = cv2.aruco.DetectorParameters_create()

    corners, ids, rejected_img_points = cv2.aruco.detectMarkers(gray, cv2.aruco_dict, parameters=parameters)
    # print(f"ids : {ids}")
    # If markers are detected
    tvec = [[[INF, INF, INF]]]
    if len(corners) > 0:
        for i in range(0, len(ids)):
            # print("coners :", corners[i])
            # Estimate pose of each marker and return the values rvec and tvec---(different from those of camera coefficients)
            rvec, tvec, markerPoints = cv2.aruco.estimatePoseSingleMarkers(corners[i], 0.02, matrix_coefficients,
                                                                       distortion_coefficients)
            # print(f"rotation vector : {rvec}")
            # print(f"translation vector : {tvec.shape}\n")
            # distance = np.sqrt(tvec[0][0][0]**2 + tvec[0][0][1]**2 + tvec[0][0][2]**2)

            # Draw a square around the markers
            cv2.aruco.drawDetectedMarkers(frame, corners)

    return tvec[0][0]

@smart_inference_mode()
def run(
        weights=os.path.join(workspace_path, "src", package_name, package_name, "utils/best.pt"),  # model path or triton URL
        source="2",  # file/dir/URL/glob/screen/0(webcam)
        imgsz=(640, 480),  # inference size (height, width)
        conf_thres=0.3,  # confidence threshold
        iou_thres=0.3,  # NMS IOU threshold
        max_det=1000,  # maximum detections per image
        device='',  # cuda device, i.e. 0 or 0,1,2,3 or cpu
        view_img=False,  # show results
        classes=None,  # filter by class: --class 0, or --class 0 2 3
        agnostic_nms=False,  # class-agnostic NMS
        augment=False,  # augmented inference
        visualize=False,  # visualize features
        line_thickness=3,  # bounding box thickness (pixels)
        hide_labels=False,  # hide labels
        hide_conf=False,  # hide confidences
        half=False,  # use FP16 half-precision inference
        dnn=False,  # use OpenCV DNN for ONNX inference
        vid_stride=1,  # video frame-rate stride
):
    global tvec, xy_list, cam_activate, object_num
    source = str(source)
    is_file = Path(source).suffix[1:] in (IMG_FORMATS + VID_FORMATS)
    is_url = source.lower().startswith(('rtsp://', 'rtmp://', 'http://', 'https://'))
    webcam = source.isnumeric() or source.endswith('.streams') or (is_url and not is_file)
    screenshot = source.lower().startswith('screen')
    if is_url and is_file:
        source = check_file(source)  # download

    # Load model
    device = select_device(device)
    model = DetectMultiBackend(weights, device=device, dnn=dnn, fp16=half)
    stride, names, pt = model.stride, model.names, model.pt
    imgsz = check_img_size(imgsz, s=stride)  # check image size

    # Dataloader
    view_img = check_imshow(warn=True)
    dataset = LoadStreams(source, img_size=imgsz, stride=stride, auto=pt, vid_stride=vid_stride)
    bs = len(dataset)
    vid_path, vid_writer = [None] * bs, [None] * bs

    # Run inference
    model.warmup(imgsz=(1 if pt or model.triton else bs, 3, *imgsz))  # warmup
    seen, windows, dt = 0, [], (Profile(), Profile(), Profile())
    for path, im, im0s, vid_cap, s in dataset:
        with dt[0]:
            im = torch.from_numpy(im).to(model.device)
            im = im.half() if model.fp16 else im.float()  # uint8 to fp16/32
            im /= 255  # 0 - 255 to 0.0 - 1.0
            if len(im.shape) == 3:
                im = im[None]  # expand for batch dim

        # Inference
        with dt[1]:
            visualize = increment_path(save_dir / Path(path).stem, mkdir=True) if visualize else False
            pred = model(im, augment=augment, visualize=visualize)

        # NMS
        with dt[2]:
            pred = non_max_suppression(pred, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det)

        # 탐지된 물체 정보 처리
        for i, det in enumerate(pred):  # per image
            seen += 1
            if webcam:  # batch_size가 1 이상인 경우
                p, im0, frame = path[i], im0s[i].copy(), dataset.count
                s += f'{i}: '
            else:
                p, im0, frame = path, im0s.copy(), getattr(dataset, 'frame', 0)
            
            # aruco marker tvec
            aruco_dict_type = ARUCO_DICT["DICT_5X5_100"]
            k = np.load(k_path)
            d = np.load(d_path)
            tvec = pose_esitmation(im0, aruco_dict_type, k, d)

            p = Path(p)  # 경로를 Path 객체로 변환
            s += '%gx%g ' % im.shape[2:]  # print string
            gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
            annotator = Annotator(im0, line_width=line_thickness, example=str(names))
            
            object_num = []
            xy_list = []
            if len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_boxes(im.shape[2:], det[:, :4], im0.shape).round()

                # Print results
                for c in det[:, 5].unique():
                    n = (det[:, 5] == c).sum()  # detections per class
                    s += f"{n} {names[int(c)]}{'s' * (n > 1)}, "  # add to strin
               

                def map_value(value, from_min, from_max, to_min, to_max):
                    from_range = from_max - from_min
                    to_range = to_max - to_min
                    scaled_value = (value - from_min) / from_range
                    mapped_value = to_min + (scaled_value * to_range)
                    return mapped_value


                # cls 변수는 클래스 인덱스를 나타내며, names 리스트에서 클래스 이름을 가져옵니다
                for *xyxy, conf, cls in reversed(det):
                    if view_img:  # 이미지에 바운딩 박스 그리기
                        c = int(cls)  # 정수형 클래스
                        label = None if hide_labels else (names[c] if hide_conf else f'{names[c]} {conf:.2f}') # 라벨 표시 여부
                        annotator.box_label(xyxy, label, color=colors(c, True)) # 이미지에 바운딩 박스와 라벨 추가
                        if names[c] == 'shoe_lace' :  # 원하는 클래스 리스트
                            tmp_list = torch.tensor(xyxy).view(1, 4).view(-1).tolist()

                            x_pixel = np.mean([tmp_list[0], tmp_list[2]])
                            y_pixel = np.mean([tmp_list[1], tmp_list[3]])
                                                
                            # print(f"{names[c]} Center (x, y): {x_pixel:.2f}, {y_pixel:.2f} \n")
                            xy_list.append((x_pixel, y_pixel))

                        object_num = len(xy_list)
                        print("object detect {0}".format(len(names[c])))

            cam_activate = True

            # Stream resultscomplete
            im0 = annotator.result()
            if view_img:
                # im0 = cv2.flip(im0, -1)  # -1은 상하좌우 반전을 의미합니다

                if platform.system() == 'Linux' and p not in windows:
                    windows.append(p)
                    cv2.namedWindow(str(p), cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)  # allow window resize (Linux)
                    cv2.resizeWindow(str(p), im0.shape[1], im0.shape[0])
                cv2.imshow(str(p), im0)
                cv2.waitKey(1)  # 1 millisecond

class Agent():
    def __init__(self):
        self.states             = []
        self.acts               = []
        self.state_size         = state_size
        self.action_size        = action_size
        self.learning_rate      = 0.001
        self.brain              = self._build_model()
    
        if os.path.isfile(states_backup):
            with open(states_backup, 'r') as json_file:
                self.states = json.load(json_file)
        if os.path.isfile(acts_backup):
            with open(acts_backup, 'r') as json_file:
                self.acts = json.load(json_file)

    def _build_model(self):
        # Neural Net for Deep-Q learning Model
        model = LinearRegression()

        if os.path.isfile(model_backup):
            model = joblib.load(model_backup)
        return model

    def backup(self):
        joblib.dump(self.brain, model_backup)
        with open(states_backup, 'w') as json_file:
            json.dump(self.states, json_file)
        with open(acts_backup, 'w') as json_file:
            json.dump(self.acts, json_file)

    def generate_random_pose(self, pose, prob_mean, bad_pose):
        global xy_list
        wait_box_detection()
        random_values = [0] * 4
        random_values[0] = np.random.uniform(pose[0] - 0.5 * angle_gap, pose[0] + 0.5 * angle_gap)
        random_values[0] = stats.norm.rvs(loc=pose[0] + ((xy_list[0][0] + xy_list[1][0]) / 2 - 320) * 0.001, scale=0.07 * angle_gap, size=1)[0]
        # print(((xy_list[0][0] + xy_list[1][0]) / 2 - 320) * 0.01)
        while True:
            time.sleep(0.03)
            not_bad = True
            for idx in range(1,3):
                if prob_mean[idx] == pose[idx]:
                    random_values[idx] = np.random.uniform(pose[idx] - angle_gap, pose[idx] + angle_gap)
                else:
                    while True:
                        tmp = stats.norm.rvs(loc=prob_mean[idx], scale=0.4 * angle_gap, size=1)[0]
                        if (pose[idx] - angle_gap < tmp and tmp < pose[idx] + angle_gap):
                            break
                    random_values[idx] = tmp
            # suppress unwanted camera angle movement
            random_values[3] = np.random.uniform(pose[3] - 1.0 * angle_gap, pose[3])
            for each in bad_pose:
                if np.linalg.norm(np.array(random_values) - np.array(each)) < 0.02:
                    prob_mean = pose.copy()
                    not_bad = False
            if not_bad:
                break
        return random_values
    
    def remember(self, state, act):
        self.states.append(state)
        self.acts.append(act)
    
    def learn(self):
        self.brain.fit(self.states, self.acts)
    
    def predict(self, state):
        return self.brain.predict(state)

class TeleopKeyboard(Node):
    settings = None

    def __init__(self):
        super().__init__('teleop_keyboard')
        self.goal_joint_state_publisher = self.create_publisher(Float64MultiArray, 'goal_joint_states', 10)
        self.goal_joint_state_publisher

        self.joint_state_subscription = self.create_subscription(
            Float64MultiArray,
            'present_joint_states',
            self.joint_state_callback,
            10)
        self.joint_state_subscription

    def send_goal_joint_space(self):
        msg = Float64MultiArray()
        msg.data = array('d', goal_joint_angle.copy())
        self.goal_joint_state_publisher.publish(msg)

    def joint_state_callback(self, msg):
        global present_joint_angle
        present_joint_angle = list(msg.data).copy()
        print("I heard:", present_joint_angle)



# Here  -  seokwon
#####################################################################################################

    def searching_action(self):
    # if object can't detect 
        while (len(object_num) == 0): 
            goal_joint_angle[0] -= -0.005      # 11번 모터가 1.5부터 -1.5까지 서칭
            
            # 오브젝트가 감지가 안될때 처음 대기 상태로 복귀
            if (goal_joint_angle[0] == -1.5):
                goal_joint_angle[0] = 3.0
                goal_joint_angle[1] = 0.377
                goal_joint_angle[2] = 0.084
                goal_joint_angle[3] = 0.985
                self.send_goal_joint_space(self.pathtime)
            pass


        
            # x 좌표만 신경 쓴것
            # 오브젝트가 1개만 감지 될 때 (그 방향으로 카메라를 돌려서 오브젝트를 더 찾는다)
                # -70 < center_x <-30 일때가 실행가능 범위 안에 들어온 것이다.
            while (len(object_num) == 1) :
                if (object_num[0][2] <= 30):
                    if (-70 > center_x ): # -70 보다 센터값이 작으면 왼쪽에 있으니까 카메라도 왼쪽으로 가야함
                        goal_joint_angle[0] += 0.005
                    elif ( 70 < center_x ): # 70보다 센터값이 크면 오른쪽에 있으니까 카메라도 오른쪽으로 가야함
                        goal_joint_angle[0] -= 0.005
                else:
                    continue

                # 보류
                # # 아래의 경우는 시야에 1짝만 있는 상황으로 1짝만 픽업하든가 해야한다.    
                # elif (-30 < center_x < 0): # -30 ~0 사이의 값이면 거의 중앙에서 살짝 왼쪽이니까 카메라를 살짝 오른쪽으로 돌린다.
                #     goal_joint_angle[0] += 0.005 
                # elif (0 < center_x < 30):
                #     goal_joint_angle[0] -= 0.005

            # 오브젝트가 2개 감지 될 때
            #object_num -> 오브젝트 넘버, 오브젝트 중앙좌표 x , 앞과 동일하고 y
            while (len(object_num) >= 2) :
                if ((object_num[0][2] + object_num[1][2]) <=40):
                    if ((object_num[0][1] + object_num[1][1]) < -30): # 두 합이 -값이면 왼쪽으로 옮겨야하 한다.
                        goal_joint_angle[0] += 0.005
                    elif ((object_num[0][1] + object_num[1][1]) > 30):
                        goal_joint_angle[0] -= 0.005
                    # 두개의 x 좌표 합이 0에서 30사이면 카메라 중잉이라고 보면 된다.
                    elif (0 < abs(object_num[0][1] + object_num[1][1]) < 30):
                        # 신발 잡는 함수 실행
                        if ((object_num[0][2] + object_num[1][2]) >10):
                            self.searching_after_action_far()
                        elif ( -50 <(object_num[0][2] + object_num[1][2]) < 10):
                            self.searching_after_action_nomal()
                        elif ((object_num[0][2] + object_num[1][2]) < -50):
                            self.searching_after_action_close()
                else:
                    continue



###############################################################################################################

def wait_box_detection():
    while (len(xy_list) != 2):
        # print("Detection Failed!", len(xy_list))
        time.sleep(0.5)

def wait_arrive():
    time.sleep(0.1)
    while True:
        tmp_dist = np.sqrt(np.sum(np.fromiter(((p2 - p1)**2 for p1, p2 in zip(goal_joint_angle[:4], present_joint_angle[:4])), dtype=float)))
        if tmp_dist == 0:
            break
    time.sleep(0.1)

def main():
    global tvec, xy_list, cam_activate, goal_joint_angle

    rclpy.init()
    teleop_keyboard = TeleopKeyboard()
    t2 = threading.Thread(target=rclpy.spin, args=(teleop_keyboard,), daemon=True)
    t2.start()


    prev_goal_joint_angle = [0.03221359848976135, -0.5783107876777649, 0.1457281857728958, 1.902136206626892, 0., 0.023769033551216123]

    goal_joint_angle = prev_goal_joint_angle.copy()

    while True:
        goal_joint_angle[:4] = [-0.33221359848976135, -0.5783107876777649, 0.1457281857728958, 1.902136206626892]
        teleop_keyboard.send_goal_joint_space()
        time.sleep(1)
        goal_joint_angle[:4] = [0.33221359848976135, -0.5783107876777649, 0.1457281857728958, 1.902136206626892]
        teleop_keyboard.send_goal_joint_space()
        time.sleep(1)
    teleop_keyboard.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
from ultralytics import YOLO
import cv2

import numpy as np

from ultralytics.utils import ASSETS
from ultralytics.models.yolo.pose import PosePredictor







def calculate_angle(joint1, joint2, joint3): 
    # 어깨 골반 무릎 순서
    # 하지만 사실 점 3개를 해도 된다
    # 5,6 어깨
    # 11, 12 골반
    # 13, 14 무릎
    

    vector1 = np.squeeze(np.array(joint1.cpu())) - np.squeeze(np.array(joint2.cpu()))
    vector2 = np.squeeze(np.array(joint3.cpu())) - np.squeeze(np.array(joint2.cpu()))

    dot_product = np.dot(vector1, vector2)
    magnitude1 = np.linalg.norm(vector1)
    magnitude2 = np.linalg.norm(vector2)

    cosine_theta = dot_product / (magnitude1 * magnitude2)
    angle = np.arccos(np.clip(cosine_theta, -1.0, 1.0))

    return np.degrees(angle)


# # 어깨, 골반, 무릎으로 이루어진 각을 계산
# angle = calculate_angle(shoulder, pelvis, knee)

# # 각이 특정 값보다 작으면 앉은 상태로 간주
# threshold_angle = 90  # 예시값. 실제로는 실험을 통해 적절한 값을 찾아야 합니다.

# if angle < threshold_angle:
#     print("앉은 상태입니다.")
# else:
#     print("서 있는 상태입니다.")






# model = YOLO("yolo8s.pt")
model = YOLO("yolov8n-pose.pt")

cap = cv2.VideoCapture(0)
# cap = cv2.VideoCapture("/home/seokwon/Desktop/RNN_data/2023-11-06_16-06-45.avi") #  보는 시점 기준 정중앙에 서있음
# cap = cv2.VideoCapture("/home/seokwon/Desktop/RNN_data/2023-11-10_11-23-00.avi") # 보는 시점 기준 오른쪽에 서있음





while cap.isOpened() :
    ret, frame = cap.read()

    if ret :
        results = model(frame)
        for result in results:
            for keypoints in result.keypoints:
                try:
                    xyn = keypoints.xyn
                    # print("Keypoints [5] :", xyn[5])
                    # print("Keypoints [11] :", xyn[11])
                    # print("Keypoints [13] :", xyn[13])
                    if xyn.size == 0 :
                        print("fail")
                        continue


                    selected_keypoints = xyn[0, [5, 11, 13], :]
                    shoulder = xyn[0, [5], :]
                    hip = xyn[0, [11], :]
                    knee = xyn[0, [13], :]
                    print("Keypoints 어깨, 골반, 무릎:", selected_keypoints)

                    angle = calculate_angle(shoulder, hip, knee)


                    # 각이 특정 값보다 작으면 앉은 상태로 간주
                    threshold_angle = 120  # 예시값. 실제로는 실험을 통해 적절한 값을 찾아야 합니다.

                    if angle < threshold_angle:
                        print("앉은 상태입니다.")
                    else:
                        print("서 있는 상태입니다.")

                except IndexError as e:
                    print(f"IndexError: {e}")
                    continue

        cv2.imshow("Results", results[0].plot()) 

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
cap.release()





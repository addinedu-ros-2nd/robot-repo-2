import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import Int32MultiArray
from cv_bridge import CvBridge
import numpy as np
import cv2
from ultralytics import YOLO

class DetectPoseNode(Node):
    def __init__(self):
        super().__init__('detect_pose_node')

        self.declare_parameter('rgb_topic', '/camera/color/image')
        self.declare_parameter('conf', 0.5)
        self.declare_parameter('device', 'cpu')

        self.rgb_topic = self.get_parameter('rgb_topic').value
        self.conf = self.get_parameter('conf').value
        self.device = self.get_parameter('device').value

        self.colcor_subscriber = self.create_subscription(
            Image,
            self.rgb_topic,
            self.color_image_callback,
            10
        )
        self.pose_publisher = self.create_publisher(
            Int32MultiArray,
            '/person_pose_acting',
            10
        )

        self.cv_bridge = CvBridge()

        self.model = YOLO('yolov8n-pose.pt')

        # self.visualization = True

    def calculate_angle(self, joint1, joint2, joint3): 
        # 어깨 골반 무릎 순서
        # 하지만 사실 점 3개를 해도 된다
        # 5,6 어깨
        # 11, 12 골반
        # 13, 14 무릎
        # 각도 계산
        vector1 = np.squeeze(np.array(joint1.cpu())) - np.squeeze(np.array(joint2.cpu()))
        vector2 = np.squeeze(np.array(joint3.cpu())) - np.squeeze(np.array(joint2.cpu()))

        dot_product = np.dot(vector1, vector2)
        magnitude1 = np.linalg.norm(vector1)
        magnitude2 = np.linalg.norm(vector2)

        cosine_theta = dot_product / (magnitude1 * magnitude2)
        angle = np.arccos(np.clip(cosine_theta, -1.0, 1.0))

        return np.degrees(angle)



    def color_image_callback(self, msg):
        color_image = self.cv_bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        
        results = self.model.predict(color_image, conf=self.conf, device=self.device) # detect
        # result = results[0].boxes.data.cpu().numpy()
        # keypoints = result.keypoints
        
        for result in results :
            for idx, keypoints in enumerate(result.keypoints):
                try:
                    xyn = keypoints.xyn
                    if xyn.size == 0:
                        continue

                    # selected_keypoints = xyn[0, [5, 11, 13], :]
                    shoulder = xyn[0, [5], :] # joint1
                    hip = xyn[0, [11], :]     # joint2
                    knee = xyn[0, [13], :]    # joint3

                    angle = self.calculate_angle(shoulder, hip, knee)

                    threshold_angle = 120
                    
                    if angle < threshold_angle:
                        msg = Int32MultiArray()
                        msg.data = [1] # 'sit'
                        self.pose_publisher.publish(msg)
                    else:
                        msg = Int32MultiArray()
                        msg.data = [2] # 'stand'
                        self.pose_publisher.publish(msg)

                except IndexError as e :
                    continue




        print('activating')
        cv2.imshow("YOLOv8 Skeleton keypoint", color_image)
        cv2.waitKey(1)

def main(args=None):
    rclpy.init(args=args)
    node = DetectPoseNode()
    rclpy.spin(node)
    rclpy.shutdown()
if __name__ == '__main__':
    main()
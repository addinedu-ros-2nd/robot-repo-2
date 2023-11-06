import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import Int32MultiArray
from cv_bridge import CvBridge
import numpy as np
import cv2
from ultralytics import YOLO

class DetectNode(Node):
    def __init__(self):
        super().__init__('detect_node')
        self.colcor_subscriber = self.create_subscription(
            Image,
            '/camera/color/image_raw',#이미지 토픽
            self.color_image_callback,
            10
        )
        self.detect_publisher = self.create_publisher(
            Int32MultiArray,
            '/person_detect',
            10
        )
        self.cv_bridge = CvBridge()
        self.model = YOLO('yolov8n.pt')
    def color_image_callback(self, msg):
        color_image = self.cv_bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        person_tracking = self.model.track(color_image, persist=True, conf=0.5, classes=0)[0]
        tracking_info = []
        # 박스를 사용하여 원본 이미지에 "person" 객체를 그리기
        if person_tracking.boxes.id==None:
            return
        for box in person_tracking.boxes:
            x1, y1, x2, y2 = box.data.tolist()[0][:4]
            x1, y1, x2, y2 = map(round, [x1, y1, x2, y2])
            tracking_info.extend([int(box.id[0]), x1, y1, x2, y2])
            cv2.rectangle(color_image, (x1, y1), (x2, y2), (0, 0, 255), 4)
            # 텍스트를 박스 위에 추가 (배경을 빨간색으로, 글자를 흰색으로)
            text = "ID: " + str(int(box.id[0])) + ", Acc: " + str(float(box.data[0][-2]))[:4]
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 1
            font_thickness = 2
            text_size, _ = cv2.getTextSize(text, font, font_scale, font_thickness)
            text_x = x1 - 2  # 텍스트를 그릴 x 좌표
            text_y = y1 - 2  # 텍스트를 그릴 y 좌표 (박스 위에 위치)
            # 텍스트 배경 박스를 그리기
            cv2.rectangle(color_image, (text_x, text_y - text_size[1]), (text_x + text_size[0], text_y), (0, 0, 255), cv2.FILLED)
            # 텍스트를 흰색으로 그리기
            cv2.putText(color_image, text, (text_x, text_y), font, font_scale, (255, 255, 255), font_thickness)
        cv2.imshow("YOLOv8 Tracking", color_image)
        cv2.waitKey(1)
        if len(tracking_info) > 0:
            msg = Int32MultiArray()
            msg.data = tracking_info
            self.detect_publisher.publish(msg) #/person_detect으로 퍼블리시
def main(args=None):
    rclpy.init(args=args)
    node = DetectNode()
    rclpy.spin(node)
    rclpy.shutdown()
if __name__ == '__main__':
    main()

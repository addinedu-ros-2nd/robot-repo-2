import open3d as o3d
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, CameraInfo
from std_msgs.msg import Float32, Int32MultiArray
from cv_bridge import CvBridge
import numpy as np

class DistNode(Node):
    def __init__(self):
        super().__init__('dist_node')
        self.camera_info_subscription = self.create_subscription(
            CameraInfo,
            '/camera/color/camera_info',
            self.camera_info_callback,
            10
        )
        self.depth_subscriber_ = self.create_subscription(
            Image,
            '/camera/depth/image_rect_raw',
            self.depth_image_callback,
            10
        )
        self.detect_subscriber = self.create_subscription(
            Int32MultiArray,
            '/person_detect',
            self.detect_callback,
            10
        )
        self.dist_publisher = self.create_publisher(
            Float32,
            '/person_dist',
            10
        )
        self.cv_bridge = CvBridge()
        self.depth_image = None
        self.intrinsics = None

        # Open3D 시각화 엔진 초기화
        self.vis = o3d.visualization.Visualizer()
        self.vis.create_window()
        self.pcd = o3d.geometry.PointCloud()
        self.vis.add_geometry(self.pcd)

    def camera_info_callback(self, msg):
        fx = msg.k[0]  # Focal length x
        fy = msg.k[4]  # Focal length y
        cx = msg.k[2]  # Principal point x
        cy = msg.k[5]  # Principal point y
        self.intrinsics = o3d.camera.PinholeCameraIntrinsic(
            msg.width, msg.height, fx, fy, cx, cy
        )

    def depth_image_callback(self, msg):
        self.depth_image = self.cv_bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')
        self.depth_image = np.array(self.depth_image, dtype=np.float32)

        depth_scale = 100  # depth 이미지의 스케일을 적절히 설정 (millimeter를 meter로 변환)
        if self.intrinsics is not None:
            depth_image_o3d = o3d.geometry.Image(self.depth_image)
            self.pcd = o3d.geometry.PointCloud.create_from_depth_image(
                depth_image_o3d,
                self.intrinsics,
                depth_scale=depth_scale
            )
            self.vis.clear_geometries()  # 이전 포인트 클라우드를 지우고 새로운 것을 추가
            self.vis.add_geometry(self.pcd)
            # self.vis.update_geometry(self.pcd)
            self.vis.poll_events()
            self.vis.update_renderer()

    def detect_callback(self, msg):
        pass
        # tmp = msg.data
        # humans = np.reshape(tmp, (-1,6))#배열을 (x,6)로 만들기
        # if self.depth_image is not None:
        #     id = 0
        #     for i in humans:
        #         x1, y1, x2, y2, conf, cls = i
        #         depth_list = [] #박스안의 depth정보 리스트
        #         id += 1
        #         for y in range(y1, y2):
        #             for x in range(x1, x2):
        #                 pixel_value = self.depth_image[y, x]
        #                 depth_list.append(pixel_value)
        #         if len(depth_list)> 0: # 리스트 길이가 0이면 평균 구할때 분모가 0이된다
        #             depth_list.sort()
        #             rm_list=int(len(depth_list)/4)
        #             depth_list = depth_list[rm_list:rm_list*3] # sort를 하고 노이즈를 제거한다
        #             # 평균 계산
        #             total = sum(depth_list)
        #             length = len(depth_list)
        #             average = total / length
        #             distance_cm = round(average * 0.1, 4) #cm단위로 변환
        #             self.dist_publish(distance_cm, id) #publish함수
    def dist_publish(self, dist, id):
        msg = Float32()
        msg.data = dist
        self.get_logger().info("id:{0} person distance is {1}cm".format(id, msg.data))
        self.dist_publisher.publish(msg)
    def __del__(self):
        self.vis.destroy_window()
def main(args=None):
    rclpy.init(args=args)
    node = DistNode()
    rclpy.spin(node)
    rclpy.shutdown()
if __name__ == '__main__':
    main()
import os
import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, CameraInfo
from std_msgs.msg import Int32MultiArray
from cv_bridge import CvBridge
import numpy as np
import time

class PointCloudVisualizer(Node):
    def __init__(self):
        super().__init__('point_cloud_visualizer')
        self.seg_subscriber = self.create_subscription(
            Int32MultiArray,
            '/person_seg_tracking',
            self.seg_callback,
            10
        )
        self.depth_subscriber_ = self.create_subscription(
            Image,
            '/camera/depth/image_rect_raw',
            self.depth_image_callback,
            10
        )
        self.camera_info_subscription = self.create_subscription(
            CameraInfo,
            '/camera/depth/camera_info',
            self.camera_info_callback,
            10
        )
        self.cv_bridge = CvBridge()
        self.color_image = None
        self.depth_image = None
        self.intrinsics = None
        self.seg = None
        self.set_intrinsics = False

        self.vis = o3d.visualization.Visualizer()
        self.vis.create_window()
        opt = self.vis.get_render_option()
        opt.background_color = np.asarray([0, 0, 0])
        self.pcd = o3d.geometry.PointCloud()
        self.vis.add_geometry(self.pcd)

    def seg_callback(self, msg):
        self.seg = np.array(msg.data[1:307201]).astype(np.uint8)

    def camera_info_callback(self, msg):
        fx = msg.k[0]
        fy = msg.k[4]
        cx = msg.k[2]
        cy = msg.k[5]
        if not self.set_intrinsics:
            self.intrinsics = o3d.camera.PinholeCameraIntrinsic(
                msg.width, msg.height, fx, fy, cx, cy
            )
            self.set_intrinsics = True

    def depth_image_callback(self, msg):
        self.depth_image = self.cv_bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')
        self.depth_image = np.array(self.depth_image, dtype=np.float32)
        if self.seg is not None:
            self.depth_image = self.depth_image * self.seg.reshape(self.depth_image.shape[0], self.depth_image.shape[1])
            print()
        depth_scale = 1.0   

        if self.intrinsics is not None:
            depth_image_o3d = o3d.geometry.Image(self.depth_image)
            self.pcd = o3d.geometry.PointCloud.create_from_depth_image(
                depth_image_o3d,
                self.intrinsics,
                depth_scale=depth_scale,
                # depth_trunc=1.0,
                # stride=2,
                project_valid_depth_only=True,
            )
            self.pcd.transform([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0],
                           [0, 0, 0, 1]])
            self.vis.reset_view_point(True)
            ctr = self.vis.get_view_control()
            ctr.unset_constant_z_far()
            ctr.unset_constant_z_near()
            ctr.scale(1000.0)
            # ctr.set_lookat([0, 0, 0])  # 원점을 중심으로
            # ctr.set_up([0, 0, 1])  # 위를 향하도록
            # ctr.set_front([0, -1, 0])  # 앞을 향하도록
            # ctr.set_constant_z_far(10.0)
            # ctr.set_constant_z_near(10.9)
            # ctr.rotate(x, y, x0, y0)
            # ctr.rotate(0.0, 180.0)
            # ctr.change_field_of_view(step=-90)
            self.vis.clear_geometries()
            self.vis.add_geometry(self.pcd)
            # self.vis.update_geometry(self.pcd)
            self.vis.update_renderer()
            self.vis.poll_events()
            time.sleep(0.1)

def main(args=None):
    rclpy.init(args=args)
    node = PointCloudVisualizer()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()

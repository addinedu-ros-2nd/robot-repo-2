import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from my_talker_listener_package.pyqt_app import MyMainWindow
from PyQt5.QtWidgets import QApplication

class TalkerNode(Node):

    def __init__(self):
        super().__init__('talker_node')
        self.publisher_ = self.create_publisher(String, 'chatter', 10)
        self.timer_ = self.create_timer(1, self.timer_callback)
        self.msg_ = String()
        self.i = 0

        # Initialize PyQt5 application
        self.app = QApplication([])
        self.window = MyMainWindow()
        self.window.show()

    def timer_callback(self):
        self.msg_.data = f'Hello ROS 2 {self.i}'
        self.publisher_.publish(self.msg_)
        self.window.update_label(self.msg_.data)  # Update the label in the PyQt5 GUI
        self.get_logger().info(f'Publishing: "{self.msg_.data}"')
        self.i += 1

def main(args=None):
    rclpy.init(args=args)
    node = TalkerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

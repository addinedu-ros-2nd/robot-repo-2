import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class TalkerNode(Node):

    def __init__(self):
        super().__init__('talker_node')
        self.publisher_ = self.create_publisher(String, 'test', 10)
        self.timer_ = self.create_timer(1, self.timer_callback)
        self.msg_ = String()
        self.i = 0

    def timer_callback(self):
        self.msg_.data = f'Hello ROS 2 {self.i}'
        self.publisher_.publish(self.msg_)
        self.get_logger().info(f'Publishing: "{self.msg_.data}"')
        self.i += 1

def main(args=None):
    rclpy.init(args=args)
    node = TalkerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

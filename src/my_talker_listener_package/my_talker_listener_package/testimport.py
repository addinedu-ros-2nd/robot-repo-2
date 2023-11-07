import my_talker_listener_package.talker as talk
import rclpy

def main():
    rclpy.init()
    node = talk.TalkerNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
    print('hello')


import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QTimer

class ListenerNode(Node):

    def __init__(self):
        super().__init__('listener_node')
        self.subscription_ = self.create_subscription(String, 'chatter', self.listener_callback, 10)
        self.subscription_
        self.init_qt()

    def listener_callback(self, msg):
        data = msg.data
        self.label.setText(f'Received: {data}')

    def init_qt(self):
        self.app = QApplication([])
        self.window = QMainWindow()
        self.window.setWindowTitle("ROS 2 Listener")
        self.window.setGeometry(100, 100, 400, 200)
        self.central_widget = QWidget()
        layout = QVBoxLayout()
        self.label = QLabel("Data from ROS: ")
        layout.addWidget(self.label)
        self.central_widget.setLayout(layout)
        self.window.setCentralWidget(self.central_widget)
        self.window.show()

    def start(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.process_events)
        self.timer.start(10)  # 10ms 마다 이벤트 처리

    def process_events(self):
        rclpy.spin_once(self)

def main(args=None):
    rclpy.init(args=args)
    node = ListenerNode()
    node.start()  # PyQt5 이벤트 루프와 ROS 2 이벤트 루프를 시작
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

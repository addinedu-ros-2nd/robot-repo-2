import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Int32, Bool
from PyQt5.QtCore import QTimer
import time
import threading




# ros ver
from_class = uic.loadUiType("src/my_new_package/my_new_package/shoebotVer.0.01.ui")[0]
# #python ver
# from_class = uic.loadUiType("basic.ui")[0]

class Listen(Node):
    def __init__(self):
        super().__init__('listener_node')
        self.subscriptionchatter_ = self.create_subscription(String, 'chatter', self.listener_callback, 10)
        self.subscriptionchatter_
        self.subscriptionFaceID_ = self.create_subscription(Int32, 'FaceID', self.FaceID_callback, 10)
        self.subscriptionFaceID_
        self.subscriptionFaceID2_ = self.create_subscription(Bool, 'FaceID2', self.FaceID2_calback, 10)
        self.subscriptionFaceID2_
#===publisher
        self.publishermoro_ = self.create_publisher(String, 'moro', 10)
        #퍼블리셔리슨에서확인# self.timer_ = self.create_timer(1, self.moro_pub)
        self.publisherroboarm_= self.create_publisher(String, 'roboarm', 10)
        #퍼블리셔리슨에서확인# self.timer_ = self.create_timer(1, self.moro_pub)
        self.i = 0
       
    def moro_pub(self):
        msg_ = String()
        msg_.data = f"moro {self.i}"
        self.publishermoro_.publish(msg_)
        #publshing 확인
        self.get_logger().info(f'moroPublishing: "{msg_.data}"')
        self.i += 1
  
    def roboarm(self):
        msg_ = String()
        msg_.data = f"roboarm {self.i}"
        self.publisherroboarm_.publish(msg_)
        #publshing 확인
        self.get_logger().info(f'roboarmPublishing: "{msg_.data}"')
        self.i += 1


   
    def FaceID_callback(self, msg):
        global FaceID
        FaceID = msg.data
    def listener_callback(self, msg):
        global chatter
        chatter = msg.data
        # self.get_logger().info(f'I heard: "{msg.data}"')
    def FaceID2_calback(self, msg):
        global FaceID2
        FaceID2 = msg.data

class WindowClass(QMainWindow, from_class) :
    def __init__(self, node):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Shoebot_Ver.0.1!")
        self.rosButton.clicked.connect(self.on_button_clicked)

#auto trigger===
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.auto_refresh)
        self.timer.start(500)  # 1000ms (1초) 마다 타이머 이벤트 발생

        # self.pushButton_1.clicked.connect(self.button1_Clicked)
        # self.pushButton_2.clicked.connect(self.button2_Clicked)
        # self.pushButton_3.clicked.connect(self.button3_Clicked)
        # self.pushButton_4.clicked.connect(self.button4_Clicked)
        # self.pushButton_5.clicked.connect(self.button5_Clicked)
        # self.pushButton_6.clicked.connect(self.button6_Clicked)
        # self.pushButton_7.clicked.connect(self.button7_Clicked)
        # self.pushButton_8.clicked.connect(self.button8_Clicked)
        # self.pushButton_9.clicked.connect(self.button9_Clicked)
        # self.pushButton_10.clicked.connect(self.button10_Clicked)
        # self.rosButton.clicked.connect(self.rosButton1_Clicked)  # Connect to ROS Button 1
        # self.rosButton_2.clicked.connect(self.rosButton2_Clicked)  # Connect to ROS Button 2
        
        # self.rosButton_2.clicked.connect(self.on_button_clicked2)
        self.rosMobile.clicked.connect(self.get_trigger)
        self.rosMobile2.clicked.connect(lambda: self.mobileactive(node))

    def get_trigger(self):
        self.lineEdit_3.setText(str(FaceID2))
        self.roslog.append('FaceID2 worked')

    def mobileactive(self, node):

        if FaceID2 == True:
            self.lineEdit_4.setText('모바일로봇움직여')
            node.moro_pub()
            # #publisher만들것을 여기서 싸줘야함
            self.lineEdit_5.setText('morocall')
            time.sleep(2)
            node.roboarm()
            self.lineEdit_6.setText('roboarm')
            
        else:
            self.lineEdit_4.setText('신호없으니움직이지마')
            self.lineEdit_5.setText('')
            self.lineEdit_6.setText('')
        
        return self.roslog.append('mobilemoro_active')
    
       


    # def on_button_clicked2(self):
    #     self.lineEdit_2.setText(str(FaceID)),
    #     self.roslog.append('FaceID :' + str(FaceID))

    def auto_refresh(self):
        # 타이머 이벤트 발생 시 버튼 클릭 시뮬레이션
        self.rosButton.click()
        # self.rosButton_2.click()
        self.rosMobile.click()
        self.rosMobile2.click()
        
    def on_button_clicked(self):
        self.lineEdit.setText(chatter)
        self.roslog.append('chatter :' + chatter)

def main():
    rclpy.init()
    node = Listen()
    app = QApplication(sys.argv)
    myWindows = WindowClass(node)
    thread1 = threading.Thread(target=rclpy.spin, args=[node], daemon=False)
    thread1.start()
    myWindows.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
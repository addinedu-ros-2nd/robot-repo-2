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

import random




# ros ver
from_class = uic.loadUiType("src/my_new_package/my_new_package/shoebotVer.0.01.ui")[0]
# #python ver
# from_class = uic.loadUiType("basic.ui")[0]

class Listen(Node):
    def __init__(self):
        super().__init__('listener_node')

        self.subscriptiont_faceidget_ = self.create_subscription(Int32, 'testfaceid', self.testfaceid_callback, 10)
        self.subscriptiont_faceidget_
        # self.subscription_faceidsecond_ = self.create_subscription(Int32, 'testfaceid_second', self.testfaceidsec_callback, 10)
        # self.subscription_faceidsecond_
        
        self.subscription_minibotfinished_ = self.create_subscription(String, 'minibot_finished', self.minibotfin_callback, 10)
        self.subscription_minibotfinished_
        self.subscription_roboarmfinished_ = self.create_subscription(String, 'roboarm_finished', self.roboarmfin_callback, 10)
        self.subscription_roboarmfinished_


        # 실제 페이스 아이디 쓰는 서브스크립션
        # self.subscriptionFaceID_ = self.create_subscription(Int32, 'FaceID', self.FaceID_callback, 10)
        # self.subscriptionFaceID_
#===publisher
        self.publisherminibotgohome_ = self.create_publisher(String, 'minibotgohome', 10)
        self.publisherroboarmgo_ = self.create_publisher(String, 'roboarmactive', 10)
        self.publisherroboarmgo2_ = self.create_publisher(String, 'roboarmactive2', 10)
        self.publisherminibotgo_ = self.create_publisher(Int32, 'minibotgo', 10)
        self.publisherminibotgobutton_ = self.create_publisher(String, 'minibotgobtn', 10)
        # self.publisherroboarm_= self.create_publisher(Bool, 'roboarm', 10)
# 타임순서로 만들기 사람이한명 왔다고 가정한후에 숫자 1을 줄거임 후에 (0~5까지줘야함)
    def testfaceid_callback(self, msg):
        global testfaceid
        testfaceid = msg.data
# 미니봇이 도착한후에 퍼블리셔를 주고 받는 함수 이거 를 받으면 finish로 받게된다면 msg가 무조건 에스를 주고 그다음
# 이것 을 받은 친구가 다음동작을 확인후에 동작을 하면됩니다.
    def minibotfin_callback(self, msg):
        global minibotfin
        minibotfin = msg.data
        if msg.data == 'finish':
            self.get_logger().info('Received minibotfin pub worked')
        else:
            self.get_logger().info('no work minibot checking now')

    # 로보암이 이용후에 퍼블리셔를 주고 받는 함수 이거 를 받으면 finish로 받게된다면 msg가 무조건 에스를 주고 그다음
# 이것 을 받은 친구가 다음동작을 확인후에 동작을 하면됩니다.
    def roboarmfin_callback(self, msg):
        global roboarmfin
        roboarmfin = msg.data
        if msg.data == 'finish':
            self.get_logger().info('Received roboarmfin pub worked')
        else:
            self.get_logger().info('no work roboarm hecking now')


#publisher 관련함수임 auto function(왜냐면 testfaceid가 값을줌)
#애는 qaplication에 함수안에 함수를 넣어서 자동 실행하게금만듬
# 타임순서 2번은 미니봇이 testfaceid 1번 을 가져가고 1번을 받는 동작이지 움직일수도있고아닐수도있음
    def minibot_pub(self, testfaceid):
        msg = Int32()
        msg.data = testfaceid
        # num = get_location(movingloc)
        self.publisherminibotgo_.publish(msg)
        self.get_logger().info(f'Publishing: "{testfaceid}"')

# 이 두개의 함수는 특정 행동을 해주려는 것이고 => 퍼블리셔로 발행 노드로 해서 람다 값으로 줘서
#클릭으로 이루어주면된다. 
    def minibotgobtn(self):
        msg = String()
        msg.data = 'minibotgoanybtn'
        self.publisherminibotgohome_.publish(msg)
        self.get_logger().info(f'Publising: {msg.data}"')

    def minibotgohome(self):
        msg = String()
        msg.data = 'minibotgohome'
        self.publisherminibotgohome_.publish(msg)
        self.get_logger().info(f'Publising: {msg.data}"')

    def roboarmgo(self):
        msg = String()
        msg.data = 'roboarmactive'
        self.publisherroboarmgo_.publish(msg)
        self.get_logger().info(f'Publising: {msg.data}"')

    def roboarmgo2(self):
        msg = String()
        msg.data = 'roboarmactive2'
        self.publisherroboarmgo2_.publish(msg)
        self.get_logger().info(f'Publising: {msg.data}"')


# #주는 것은 불 값으로 줌 트루 라면 트루로 받고 있고 실행할것이다.
#     def roboarm(self):
#         self.msg_ = Bool()
#         self.msg_.data = bool(random.getrandbits(1))
#         self.publisherroboarm_.publish(self.msg_)

#다른상황에 대해서{face id 에 두번
# list 정리해서 하는 것에대해서 
# } 두번 만약에 페이스 아이디 두번 이면 어떻게할까에서 기현
    # def testfaceidsec_callback(self, msg):
    #     global testfaceidsec
    #     testfaceidsec = msg.data
    # 
 
    # 실제 FaceID 이용할떄 이 콜백을 사용하면 됨
    # def FaceID_callback(self, msg):
    #     global FaceID
    #     FaceID = msg.data


class WindowClass(QMainWindow, from_class) :
    def __init__(self, node):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Shoebot_Ver.0.1!")
        

#auto trigger===
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.auto_refresh)
        self.timer.start(1000) 
         # 1000ms (1초) 마다 타이머 이벤트 발생
         # 어투 콜백을 하지말고 손으로 일일히하자
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
        # self.rosButton.clicked.connect(self.on_button_clicked)
        # self.rosMobile.clicked.connect(self.testfaceidcheck)
        self.minibot_finishedbtn.clicked.connect(self.minibotfin)
        self.roboarm_finishedbtn.clicked.connect(self.roboarmfin)
    
        self.minibotbtn.clicked.connect(lambda: self.minibotgogo(node))
        self.minibotbackbtn.clicked.connect(lambda: self.minibothome(node))
        self.robotactivebtn.clicked.connect(lambda: self.roboactive(node))
        self.robotactivebtn2.clicked.connect(lambda: self.roboactive2(node))
        
        #auto mover get testfaceid and active something
        self.rosMobile2.clicked.connect(lambda: self.mainmobile(node, testfaceid))

# each button have trigger publihser
    def minibotgogo(self,node):
        node.minibotgobtn()

    def minibothome(self,node):
        node.minibotgohome()
    
    def roboactive(self,node):
        node.roboarmgo()

    def roboactive2(self,node):
        node.roboarmgo2()


    def minibotfin(self):
        if minibotfin == 'finish':
            self.lineEdit_4.setText('minibot_done')
        else:
           self.lineEdit_4.setText('minibot_NOTDone')
        
 
    def roboarmfin(self):
        if roboarmfin == 'finish':
            self.lineEdit_5.setText('roboarm_done')
        else:
            self.lineEdit_5.setText('roboarm_NOTDone')
            
   

    def testfaceidcheck(self):
        self.lineEdit_3.setText(str(testfaceid))
        # faceId INt 32 로 받아온것을 str로 반환
        # self.roslog.append('testfaceid worked')
        # faceID 받아오는거 확인 


        

    #pyqt에서 버튼 클릭하면* ui 를 왜쓰는가? 람다써서 connect(lambda: self.{func}(node))
    # #ui 가 되면됨. 
    # def mainmobile(self, node, testfaceid):
    #     if testfaceid ==0:
    #         self.lineEdit_4.setText('홈위치에갈것')
    #         self.lineEdit_5.setText('')
    #         self.lineEdit_6.setText('')
    #         self.minibotbackbtn.clicked.connect(lambda: self.minibothome(node))
    #         self.lineEdit_4.setText('go to home now')
    #         self.roslog.append('go to home now')

    #         self.minibot_finishedbtn.clicked.connect(self.minibotfin)    
    #     elif minibotfin == 'finish':
    #         self.lineEdit_4.setText('미니봇피니쉬받음')
    #         self.roslog.append('미니봇피니쉬받음')
    #         self.lineEdit_5.setText('로보암에게 연결')
    #         self.roslog.append('로보암에게 연결')
    #         self.robotactivebtn.clicked.connect(lambda: self.roboactive(node))
    #         self.roboarm_finishedbtn.clicked.connect(self.roboarmfin)
    #         if roboarmfin == 'finish':
    #             self.lineEdit_5.setText('로보암 피니쉬받음')
    #             self.roslog.append('로보암 피니쉬받음')
    #             self.lineEdit_4.setText('미니봇실행')
    #             self.roslog.append('미니봇실행')

    #             if testfaceid == 1:
    #                 self.minibotbtn.clicked.connect(lambda: self.minibotgogo(node(testfaceid)))
    #                 self.minibot_finishedbtn.clicked.connect(self.minibotfin)
    #                 if minibotfin == 'finish':
    #                     self.lineEdit_4.setText('미니봇피니쉬받음2')
    #                     self.roslog.append('미니봇피니쉬받음2')
    #                     self.lineEdit_5.setText('로보암에게 연결2')
    #                     self.roslog.append('로보암에게 연결2')
    #                     self.robotactivebtn2.clicked.connect(lambda: self.roboactive2(node))        
    #                     self.roboarm_finishedbtn.clicked.connect(self.roboarmfin)
    #                     if roboarmfin == 'finish':
    #                         self.lineEdit_5.setText('로보암 피니쉬받음2')
    #                         self.roslog.append('로보암 피니쉬받음2')
    #                         self.lineEdit_4.setText('미니봇실행2')
    #                         self.roslog.append('미니봇실행2')
    #                         self.minibotbackbtn.clicked.connect(lambda: self.minibothome(node))
    #                         self.minibot_finishedbtn.clicked.connect(self.minibotfin)
    #                         if minibotfin == 'finish':
    #                             self.lineEdit_4.setText('미니봇피니쉬받음3')
    #                             self.roslog.append('미니봇피니쉬받음3')
    #                             self.lineEdit_5.setText('completed')
    #                             self.roslog.append('completed')
    #                             self.lineEdit_6.setText('completed')

    #                         else:
    #                             return self.lineEdit_3.setText('works?') 
          
            # elif testfaceid == 2:
            #     node.roboarmgo()
            #     node.minibotbtn({num})
            # elif testfaceid == 3:
            #     node.roboarmgo()
            #     node.minibotbtn({num})
            # elif testfaceid == 4:
            #     node.roboarmgo()
            #     node.minibotbtn({num})
            # elif testfaceid == 5:
            #     node.roboarmgo()
            #     node.minibotbtn({num})
            # pass
                


    # def mobileactive(self, node, testfaceid):
    #     if testfaceid == 0:
    #         self.lineEdit_4.setText('신호없으니움직이지마')
    #         self.lineEdit_5.setText('')
    #         self.lineEdit_6.setText('')
    #         pass
    #     elif testfaceid in range(1, 6):


    #         self.lineEdit_4.setText(f'Go to {testfaceid} section')

    #         node.minibot_pub(testfaceid)
    #         self.lineEdit_5.setText('minibotwhatyoudoing')
    #         time.sleep(0) # 움직임과 미니봇 사이에 콜을 2초 단위로 줘야한다.
    #         # node.roboarm()
    #         # self.lineEdit_6.setText('roboarm')
    #     else:
    #         self.lineEdit_4.setText('')
    #         self.lineEdit_5.setText('')
    #         self.lineEdit_6.setText('')
        
    #     return self.roslog.append('minibot_active')
    
       


    # # def on_button_clicked2(self):
    #     self.lineEdit_2.setText(str(FaceID)),
    #     self.roslog.append('FaceID :' + str(FaceID))

    def auto_refresh(self):
    #     # 타이머 이벤트 발생 시 버튼 클릭 시뮬레이션
    #     self.rosButton.click()
    #     # self.rosButton_2.click()
    #     self.rosMobile.click()
        self.rosMobile2.click()

    # def on_button_clicked(self):
    #     self.lineEdit.setText('')
        # self.roslog.append('')

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
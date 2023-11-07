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


from my_new_package.sound import play_sound # pip install pygame plz





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
        self.setWindowTitle("Shoebot_Ver.0.45!")
        

#auto trigger===
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.auto_refresh)
        self.timer.start(500)  # 1000ms (1초) 마다 타이머 이벤트 발생

        self.pushButton_1.clicked.connect(self.button1_Clicked)
        self.pushButton_2.clicked.connect(self.button2_Clicked)
        self.pushButton_3.clicked.connect(self.button3_Clicked)
        self.pushButton_4.clicked.connect(self.button4_Clicked)
        self.pushButton_5.clicked.connect(self.button5_Clicked)
        self.pushButton_6.clicked.connect(self.button6_Clicked)
        self.pushButton_7.clicked.connect(self.button7_Clicked)
        self.pushButton_8.clicked.connect(self.button8_Clicked)
        self.pushButton_9.clicked.connect(self.button9_Clicked)
        self.pushButton_10.clicked.connect(self.button10_Clicked)
       # Connect to ROS Button 1
         # Connect to ROS Button 2
        self.rosButton.clicked.connect(self.on_button_clicked)
        self.rosButton_2.clicked.connect(self.on_button_clicked2)
        self.rosMobile.clicked.connect(self.get_trigger)
        self.rosMobile2.clicked.connect(lambda: self.mobileactive(node))


##============================lineedit log & statue 

        self.logEdit.returnPressed.connect(self.addText)
        self.enter.clicked.connect(self.addTextClicked)
        self.Error.clicked.connect(self.error12)

##===========================================================time function
    def start_count(self):
        self.count=0
        self.timer = self.startTimer(1000)

    def timerEvent(self,event):
        self.count += 1
        self.lcdNumber.display(self.count)

    ##====================================================================log fucuntion

    def error12(self):
        msg = "===============Error==============="
        self.textEdit.setText(msg)
        self.log.append(msg)
        play_sound('07_에러효과음.mp3')
    def addText(self):
        input = self.logEdit.text()
        self.logEdit.clear()
        self.log.append(input)
    def addTextClicked(self):
        input = self.logEdit.text()
        self.logEdit.clear()
        self.log.append(input)    

##=========================================action function
    def button1_Clicked(self):
        Action1 = "사람이 들어오는 action  → 컴퓨터는 사람이 들어왔다라고 인식"
        self.textEdit.setText(Action1)
        self.log.append(Action1)
        play_sound('01_인식되었습니다.wav')
        
    def button2_Clicked(self):
        Action2 = "사람이들어와서 카메라로 찍는 action 컴퓨터는 사람에대해서 얼굴만 가져와서 찍음"
        self.textEdit.setText(Action2)
        self.log.append(Action2)
    def button3_Clicked(self):
        Action3 = "카메라로 찎은 데이터를 기록하는 action 컴퓨터는 사람에 얼굴을 가져와서 1번이라고 기록 하고 *"
        self.textEdit.setText(Action3)
        self.log.append(Action3)

    def button4_Clicked(self):
        Action4 = "메뉴플레이터를 작동, 메뉴플레이터는 신발인식후 신발을 들어올리는 action 까지"
        self.textEdit.setText(Action4)
        self.log.append(Action4)
        play_sound('03_신발정리중입니다.wav')
    def button5_Clicked(self):
        Action5 = "미니봇은 신발을 들고 간다고 가정하고 , 이때 신발장 근처로 움직이는 action 하기"
        self.textEdit.setText(Action5)
        self.log.append(Action5)   
    def button6_Clicked(self):
        Action6 = "신발장 근처로 이동하는 action 이후에 manuplator로 신발장에 두는 action 하기"
        self.textEdit.setText(Action6)
        self.log.append(Action6)  
        play_sound('06_움직임효과음.mp3')
    def button7_Clicked(self):
        Action7 = "3번에 있는 데이터 1번 기록에 신발장 위치 데이터 기록 해서 하나로 묶기"
        self.textEdit.setText(Action7)
        self.log.append(Action7)
        play_sound('01_인식되었습니다.wav')
    def button8_Clicked(self):
        Action8 = "미니봇은 다시 금 홈으로 돌아가기"
        self.textEdit.setText(Action8)
        self.log.append(Action8)
        play_sound('04_귀환중입니다.wav')
    def button9_Clicked(self):
        Action9 = "다시 1번이 아니라 n+1번으로 할수 있게끔 하기"
        self.textEdit.setText(Action9)
        self.log.append(Action9)
    def button10_Clicked(self):
        Action10 = "초기화 기능 넣기"
        self.textEdit.setText(Action10)
        self.log.append(Action10)
        play_sound('05_대기중입니다.wav')




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
    
       #face iD give number
    def on_button_clicked2(self):
        self.lineEdit_2.setText(str(FaceID)),
        self.roslog.append('FaceID :' + str(FaceID))

    def auto_refresh(self):
        # 타이머 이벤트 발생 시 버튼 클릭 시뮬레이션
        self.rosButton.click()
        self.rosButton_2.click()
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
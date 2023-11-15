# ShoeBot
![Title drawio](https://github.com/addinedu-ros-2nd/robot-repo-2/assets/140477778/86723d3a-4c09-41ea-a812-f5b6df4cb52a)
-----------
# Member
-----
### 오세찬

manipulator control ROS2 cpp package 작성

Human 3D trajectory estimation system 구현

### 김동우 [github link](https://github.com/DongUKim)

2D point & shoot SLAM 맵 구현 및 Mobile robot 제어

shoe pick & place를 위한 joint angle 데이터 생성 및 딥러닝 모델을 이용한 데이터 증강


### 김명섭

Face recognition library를 활용한 얼굴인식 및 ID 관리 system 구현

YOLOv8-Pose, LSTM, Tensor Flow의 CNN을 활용하여 Human Pose estimation LSTM 모델 구현

### 백세진

귀 후비후비

### 최석원

배 벍벍 긁을 위한 월동 준비

shoe detection를 위한 YOLOv3 학습모델 구축

YOLOv8-Pose,Tensor Flow를 활용하여 Human Pose estimation decision tree모델과 LSTM 모델 구현


### 왕한세


shoe detection를 위한 YOLOv3 학습모델 구축

MoveIt을 활용한 6-DOF manipulator URDF 구현 및 제어

Digital Twin

화장실 가서 맨날 cry

# Demo Video
----

[https://youtu.be/70jTAGOszJk?si=234ndFWIfTjO60wj](https://youtu.be/70jTAGOszJk?si=B9b1eJ4xAqf_m7qv)


## Project Summary
----
Face recognition으로 사람 얼굴을 구별

YOLOv3 모델을 이용해 신발을 detecting 후 Robotics의 open_manipulator을 이용해 신발을 집어 Mobile robot을 이용해 신발장까지 운반하는 시스템

Pose estimation으로 행동예측을 하여 Mobile robot을 회피기동
## Scenario
----
![시퀀스다이어그램-스테이트전이 (2)](https://github.com/addinedu-ros-2nd/robot-repo-2/assets/140477778/5a99e0b4-a979-45f4-9dea-5e57a060ab19)
## System Configuration
----
![ShoeBot_Diagram-Page-4 drawio](https://github.com/addinedu-ros-2nd/robot-repo-2/assets/140477778/f5ffd09c-155c-4951-af13-9e8d26a2af4c)
## Manipulator Motion Planning
----
### Motion Planning Part Summary
manipulator가 신발을 감지 한 후에 신발을 집고 주행로봇이나 신발장에 올리기 위해 필요한 동작을 구현하는 단계

### Motion Planning Part Technology
Language: Python, C++
Library:

Python - math, os, rclpy, threading, numpy, multiprocessing, platform, sys, pathlib, torch, cv2, time, json, ultralytics.utils, ai_manipulation.utils, joblib, random, sklearn.linear_model, scipy.stats, array, std_msgs.msg, rclpy.node, subprocess

C++ - Dynamicxel, cstdlib, chrono, functional, memory, string, rclcpp, std_msgs

Hardware:
Open-manipulator, Object detecting camera, shoe’s mockup with formboard

### cpp controller 실행코드
```
ros2 run dynamixel_workbench_toolbox dxl_controller control
```

cpp controller 실행코드(읽기전용)
```
ros2 run dynamixel_workbench_toolbox dxl_controller
```

model 생성 코드 실행
```
ros2 run ai_manipulation six_dxl_model
```

현재 pose를 확인 할 수 있는 topic
```
ros2 topic echo /present_joint_angle
```


## Face Recognition
----

## Pose Estimation
----

## Mobile Robot
-----
# Improvements expected in the future
a=text

세진이형

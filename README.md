<img src="https://github.com/addinedu-ros-2nd/robot-repo-2/assets/140477778/86723d3a-4c09-41ea-a812-f5b6df4cb52a" width= "110%" height="110%"/>


# Why?
<img src="https://github.com/addinedu-ros-2nd/robot-repo-2/assets/140477778/6d90a1c4-a6e6-44a0-bfa7-9022e40e8950" width="30%" height="30%"/>


직접 손으로 정리하시겠습니까?

아니면 shoebot이 정리해드릴까요?

## Project Introduce
----
shoebot은 사람의 손이 없어도 신발을 집어, 신발장에 정리해두는 친절한 로봇입니다.

# Demo Video
----

![image](https://github.com/addinedu-ros-2nd/robot-repo-2/assets/140477778/e05c57b4-476a-476e-943d-8dc229365a41)(https://www.youtube.com/watch?v=70jTAGOszJk)


## Project Keyword
----
1. Manipulator pick & place
2. Deeplearning
3. Autonomous driving
4. ROS2

   
## Project Summary
----
Face recognition으로 사람 얼굴을 구별

YOLOv3 모델을 이용해 신발을 detecting 후 Robotics의 open_manipulator을 이용해 신발을 집어 Mobile robot을 이용해 신발장까지 운반하는 시스템

Pose estimation으로 행동예측을 하여 Mobile robot을 회피기동
## Scenario
----
<img src="https://github.com/addinedu-ros-2nd/robot-repo-2/assets/140477778/5a99e0b4-a979-45f4-9dea-5e57a060ab19" width="30%" height="30%"/>


## System Configuration
----
<img src="https://github.com/addinedu-ros-2nd/robot-repo-2/assets/140477778/f5ffd09c-155c-4951-af13-9e8d26a2af4c" width="30%" height="30%"/>


## Manipulator Motion Planning
----
### Motion Planning Part Summary
manipulator가 신발을 감지 한 후에 신발을 집고 주행로봇이나 신발장에 올리기 위해 필요한 동작을 구현하는 단계

### Motion Planning Part language & library
Language: Python, C++
Library:

Python - math, os, rclpy, threading, numpy, multiprocessing, platform, sys, pathlib, torch, cv2, time, json, ultralytics.utils, ai_manipulation.utils, joblib, random, sklearn.linear_model, scipy.stats, array, std_msgs.msg, rclpy.node, subprocess

C++ - Dynamicxel, cstdlib, chrono, functional, memory, string, rclcpp, std_msgs

Hardware:
Open-manipulator, Object detecting camera, shoe’s mockup with formboard

### Motion Planning Part technology 

#### Custom cpp package 

1. 6-DOF 제어
2. dynamic cell control table 관찰

#### YOLOv3 신발객체탐지 모델

1. 모형신발을 사용하여 학습
2. 450개의 사진

#### 자가학습 시스템 구축

1. shoe pick & place 를 위한 pose를 manipulator 스스로 학습하도록 모델을 구축

#### MoveIt를 활용한 manipulator 제어





## Face Recognition
----


## Pose Estimation
----



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

YOLOv8-Pose, LSTM, Tensor Flow의 CNN을 활용하여 Human Pose estimation 을 위한 LSTM 모델 구현

### 백세진

PyQT를 활용하여 GUI생성, ROS연결 통신

### 최석원

shoe detection를 위한 YOLOv3 학습모델 구축

YOLOv8-Pose,Tensor Flow를 활용하여 Human Pose estimation 을 위한 decision tree모델과 LSTM 모델 구현


### 왕한세


shoe detection를 위한 YOLOv3 학습모델 구축

MoveIt을 활용한 6-DOF manipulator URDF 구현 및 제어

Digital Twin

화장실 가서 맨날 cry
## Mobile Robot
-----
# Improvements expected in the future


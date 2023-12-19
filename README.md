# How to run ROS1_noetic 

## 환경설정
<pre><code>source /opt/ros/noetic/setup.bash</code></pre>

<pre><code>source devel/setup.bash</code></pre>


## ROS1 noetic DOMAIN, URI 통일하기
<pre><code>export ROS_MASTER_URI=http://localhost:11311</code></pre>
<pre><code>export ROS_ID=45</code></pre>

## Rviz 실행
<pre><code>roslaunch open_manipulator_description open_manipulator_rviz.launch</code></pre>

## Gazebo 실행
<pre><code>roslaunch open_manipulator_gazebo open_manipulator_gazebo.launch</code></pre>

## 컨트롤러 GUI 실행
<pre><code>roslaunch open_manipulator_control_gui open_manipulator_control_gui.launch</code></pre>

## Moveit 실행
<pre><code>roslaunch open_manipulator_controller open_manipulator_controller.launch use_platform:=false use_moveit:=true</code></pre>
### 가제보에서 실행할 때는 use_platform = false

## rqt
<pre><code>rqt</code></pre>

## Gazebo, Rviz 연동 실행
<pre><code>roslaunch open_manipulator_controllers joint_trajectory_controller.launch</code></pre>

## Manipulator 연결
<pre><code>roslaunch open_manipulator_controller open_manipulator_controller.launch</code></pre>

## Rviz와 manipulator를 연동하여 Joint_angle 값 받아오기 (Digital Twin)
<pre><code>roslaunch open_manipulator_description open_manipulator_rviz.launch</code></pre>
<pre><code>roslaunch open_manipulator_controller open_manipulator_controller.launch</code></pre>

### Joint_angle 토픽 구독 취소, manipulator 모터 제어 풀기
<pre><code>rosservice call /set_actuator_state "set_actuator_state: false”</code></pre>



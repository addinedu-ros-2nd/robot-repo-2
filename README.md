# IoT-repo-3

## 1. Development environment
1-1. OS : Ubuntu 22.04
1-2. Meta OS : ROS2 Humble Hawksbill

## 2. How to use
### 2-1. Install ROS Packages
<pre><code>
</code></pre>
<pre><code>$ sudo apt install ros-humble-rqt* ros-humble-joint-state-publisher</code></pre>

### 2-2. Clone git Repository

<pre><code>
$ cd ~
$ git clone <repository_url> colcon_ws
$ cd ~/colcon_ws && colcon build --symlink-install
</code></pre>

### 2-3. USB Latency Timer Setting
The initial USB latency time is 16ms. Utilizing the command provided, the USB latency will be adjusted to 1ms, followed by a confirmation of the new USB latency configuration.

'''
$ chmod +x ~/colcon_ws/install/open_manipulator_x_controller/lib/open_manipulator_x_controller/create_udev_rules
$ ros2 run open_manipulator_x_controller create_udev_rules
$ cat /sys/bus/usb-serial/devices/ttyUSB0/latency_timer # terminal output : 1
'''

### 2-4. Setup Bash

'''
$ source ~/.bashrc
$ source /opt/ros/humble/setup.bash
$ source ~/colcon_ws/install/local_setup.sh
'''

### 2-5. Basic Operation
Terminal #1 : Enables control of the Openmanipulator

'''$ ros2 launch open_manipulator_x_controller open_manipulator_x_controller.launch.py'''

Terminal #2 : Can control using keyboard

'''$ ros2 run open_manipulator_x_teleop teleop_keyboard'''

Terminal #3 : Load Openmanipulator on RViz

'''$ ros2 launch open_manipulator_x_description open_manipulator_x_rviz.launch.py'''

Terminal #4 : Check Openmanipulator setting

'''$ ros2 topic pub /option std_msgs/msg/String "data: print_open_manipulator_x_setting"


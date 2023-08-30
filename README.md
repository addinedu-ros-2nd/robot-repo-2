# 1. Project Summary

## 1-1. Development environment
- OS : Ubuntu 22.04
- ROS version : ROS2 Humble Hawksbill

# 3. How to use
## 3-1. Install ROS Packages

<pre><code>$ sudo apt install ros-humble-rqt* ros-humble-joint-state-publisher</code></pre>

## 3-2. Clone git Repository

<pre><code>$ cd ~
$ git clone https://github.com/addinedu-amr-3rd/IoT-repo-3.git colcon_ws
$ cd ~/colcon_ws && colcon build --symlink-install</code></pre>

## 3-3. USB Latency Timer Setting
The initial USB latency time is 16ms. Utilizing the command provided, the USB latency will be adjusted to 1ms, followed by a confirmation of the new USB latency configuration.

<pre><code>$ chmod +x ~/colcon_ws/install/open_manipulator_x_controller/lib/open_manipulator_x_controller/create_udev_rules
$ ros2 run open_manipulator_x_controller create_udev_rules
$ cat /sys/bus/usb-serial/devices/ttyUSB0/latency_timer # terminal output : 1</code></pre>

# 4. Run examples

## 4-1. Setup Bash

You need to run the following command every time you open the terminal.

<pre><code>$ source ~/.bashrc
$ source /opt/ros/humble/setup.bash
$ source ~/colcon_ws/install/local_setup.sh</code></pre>

## 4-2. OpenManipulator grabbing shoes

<pre><code>$ ros2 run dynamixel_workbench_toolbox save_dxl_info</code></pre>

## 4-3. OpenManipulator basic examples

Here is a list of executable files for the basic Dynamixel examples:
|filenames--|
|------|
|bps_change|ping|
|bulk_read_write|position|
|current_based_position|read_write|
|find_dynamixel|reboot|
|id_change|reset|
|mode_change|sync_read_write|
|model_scan|sync_write|
|monitor|velocity|

<pre><code>$ ros2 run dynamixel_workbench_toolbox "executable_file_name"</code></pre>

Don't forget to replace <file_name> with the actual name of the file you want to execute.

## 4-4.OpenManipulator controlled via keyboard
Terminal #1 : Enables control of the Openmanipulator

<pre><code>$ ros2 launch open_manipulator_x_controller open_manipulator_x_controller.launch.py</code></pre>

Terminal #2 : Can control using keyboard

<pre><code>$ ros2 run open_manipulator_x_teleop teleop_keyboard</code></pre>

Terminal #3 : Load Openmanipulator on RViz

<pre><code>$ ros2 launch open_manipulator_x_description open_manipulator_x_rviz.launch.py</code></pre>

Terminal #4 : Check Openmanipulator setting

<pre><code>$ ros2 topic pub /option std_msgs/msg/String "data: print_open_manipulator_x_setting"
</code></pre>

## 4-3

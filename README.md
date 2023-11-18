### 1. Turn on the realsense camera
<pre><code>ros2 launch realsense2_camera rs_launch.py depth_module.profile:=640x480x30 rgb_camera.profile:=640x480x30</code></pre>

### 2. Human Pose Estimation LSTM + Seg 
<pre><code>ros2 launch depth_example merge_lstm_seg.launch.py</code></pre>


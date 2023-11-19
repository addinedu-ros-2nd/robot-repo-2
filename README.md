### 1. Turn on the realsense camera
<pre><code>ros2 launch realsense2_camera rs_launch.py depth_module.profile:=640x480x30 rgb_camera.profile:=640x480x30</code></pre>

### 2. Human tracking data streaming
<pre><code>ros2 run depth_example yolov8_seg_tracking</code></pre>

### 3. Danger alarm with point cloud viewer
<pre><code>ros2 run realsense_human_tracking human_pcl</code></pre>

### 4. Basic human tracking node
<pre><code>ros2 run depth_example basic_tracking</code></pre>

### 5. Basic distance node
<pre><code>ros2 run depth_example basic_distance</code></pre>

### 1. Turn on the realsense camera
<pre><code>
ros2 launch realsense2_camera rs_launch.py depth_module.profile:=640x480x30 rgb_camera.profile:=640x480x30
</code></pre>

### 2. Basic human tracking node
<pre><code>
ros2 run depth_example basic_tracking
</code></pre>

### 3. Basic distance node
<pre><code>
ros2 run depth_example basic_distance
</code></pre>

### 4. Human tracking data streaming
<pre><code>
ros2 run depth_example Streaming_for_loop_with_tracking
</code></pre>


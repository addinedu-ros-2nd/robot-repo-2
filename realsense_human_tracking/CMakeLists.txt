cmake_minimum_required(VERSION 3.8)
project(realsense_human_tracking)

# Default to C++14
#if(NOT CMAKE_CXX_STANDARD)
set(CMAKE_CXX_STANDARD 14)
#endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(pcl_conversions REQUIRED)
find_package(PCL REQUIRED)
#find_package(realsense2 REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(OpenCV REQUIRED)
find_package(cv_bridge REQUIRED)

include_directories(${PCL_INCLUDE_DIRS} include)
link_directories(${PCL_LIBRARY_DIRS})
add_definitions(${PCL_DEFINITIONS})

# find dependencies
find_package(ament_cmake REQUIRED)
# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

add_executable(human_pcl src/human_pcl.cpp)
target_link_libraries( human_pcl
  ${PCL_LIBRARIES}
)
ament_target_dependencies( human_pcl
  rclcpp
  std_msgs
  sensor_msgs
  OpenCV
  cv_bridge
)
add_executable(color_image src/color_image.cpp)
ament_target_dependencies(color_image rclcpp std_msgs sensor_msgs OpenCV cv_bridge)
add_executable(pcl_visualizer_demo src/pcl_visualizer_demo.cpp)
target_link_libraries( pcl_visualizer_demo ${PCL_LIBRARIES})
add_executable(pcl_dbscan src/pcl_dbscan.cpp)
target_link_libraries( pcl_dbscan
  ${PCL_LIBRARIES}
)
ament_target_dependencies(pcl_dbscan rclcpp std_msgs sensor_msgs OpenCV cv_bridge)
add_executable(testing src/test.cpp)
ament_target_dependencies(testing rclcpp std_msgs sensor_msgs OpenCV cv_bridge)


install(TARGETS
 human_pcl
 color_image
 pcl_visualizer_demo
 pcl_dbscan
 testing
 DESTINATION lib/${PROJECT_NAME}
)

ament_package()

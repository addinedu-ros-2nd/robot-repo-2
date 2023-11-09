#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/image.hpp"
#include "std_msgs/msg/float32.hpp"
#include "std_msgs/msg/int32_multi_array.hpp"
#include "cv_bridge/cv_bridge.h"
#include "opencv2/opencv.hpp"

#include <iostream>
#include <thread>
#include <pcl/common/angles.h> // for pcl::deg2rad
#include <pcl/features/normal_3d.h>
#include <pcl/io/pcd_io.h>
#include <pcl/visualization/pcl_visualizer.h>
#include <pcl/console/parse.h>

pcl::visualization::PCLVisualizer::Ptr simpleVis (pcl::PointCloud<pcl::PointXYZ>::ConstPtr cloud){
  // --------------------------------------------
  // -----Open 3D viewer and add point cloud-----
  // --------------------------------------------
  pcl::visualization::PCLVisualizer::Ptr viewer (new pcl::visualization::PCLVisualizer ("3D Viewer"));
  viewer->setBackgroundColor (0, 0, 0);
  viewer->addPointCloud<pcl::PointXYZ> (cloud, "sample cloud");
  viewer->setPointCloudRenderingProperties (pcl::visualization::PCL_VISUALIZER_POINT_SIZE, 1, "sample cloud");
  viewer->addCoordinateSystem (1.0);
  viewer->initCameraParameters ();
  return (viewer);
}

class DistNode : public rclcpp::Node {
    rclcpp::Subscription<sensor_msgs::msg::Image>::SharedPtr depth_subscription_;
    rclcpp::Subscription<sensor_msgs::msg::Image>::SharedPtr color_subscription_;
    rclcpp::Subscription<std_msgs::msg::Int32MultiArray>::SharedPtr detect_subscription_;
    rclcpp::Publisher<std_msgs::msg::Float32>::SharedPtr dist_publisher_;
    cv_bridge::CvImagePtr cv_ptr;
    cv::Mat depth_image_;

    public:
        DistNode() : Node("dist_node") {
            depth_subscription_ = this->create_subscription<sensor_msgs::msg::Image>(
                "/camera/depth/image_rect_raw",
                10,
                std::bind(&DistNode::depthImageCallback, this, std::placeholders::_1)
            );
            color_subscription_ = this->create_subscription<sensor_msgs::msg::Image>(
                "/camera/color/image_raw",
                10,
                std::bind(&DistNode::colorImageCallback, this, std::placeholders::_1)
            );
            detect_subscription_ = this->create_subscription<std_msgs::msg::Int32MultiArray>(
                "/person_box_tracking",
                10,
                std::bind(&DistNode::detectCallback, this, std::placeholders::_1)
            );
            dist_publisher_ = this->create_publisher<std_msgs::msg::Float32>(
                "/person_dist",
                10
            );
        }

    private:
        pcl::PointCloud<pcl::PointXYZ>::Ptr point_cloud_ptr = std::make_shared<pcl::PointCloud<pcl::PointXYZ>>();
        // pcl::PointCloud<pcl::PointXYZRGB>::Ptr point_cloud_ptr = std::make_shared<pcl::PointCloud<pcl::PointXYZRGB>>();
        pcl::visualization::PCLVisualizer::Ptr viewer = simpleVis(point_cloud_ptr);

        void colorImageCallback(const sensor_msgs::msg::Image::ConstPtr msg) {}
        void depthImageCallback(const sensor_msgs::msg::Image::ConstPtr msg) {
            cv_ptr = cv_bridge::toCvCopy(msg);
            depth_image_ = cv_ptr->image;
            depth_image_.convertTo(depth_image_, CV_32F);

            point_cloud_ptr = std::make_shared<pcl::PointCloud<pcl::PointXYZ>>();
            for (int y = 0; y < depth_image_.rows; y++) {
                for (int x = 0; x < depth_image_.cols; x++) {
                    pcl::PointXYZ point;
                    // pcl::PointXYZRGB point;

                    // Access depth value at (x, y)
                    float depth = depth_image_.at<float>(y, x);

                    // Check if the depth value is valid (e.g., not NaN)
                    if (depth > 0) {
                        // Set point coordinates
                        point.x = depth;  // x-coordinate is the depth value
                        point.y = x;
                        point.z = y;
                        // point.r = ;
                        // point.g = ;
                        // point.b = ;

                        point_cloud_ptr->points.push_back(point);
                    }
                }
            }
            point_cloud_ptr->width = point_cloud_ptr->size ();
            point_cloud_ptr->height = 1;
            viewer->updatePointCloud(point_cloud_ptr, "sample cloud");
            viewer->spinOnce (100);
            std::this_thread::sleep_for(std::chrono::milliseconds(100));
        }

        void detectCallback(const std_msgs::msg::Int32MultiArray::SharedPtr msg) {
            std::vector<int> tmp = msg->data;
            std::vector<std::vector<unsigned int>> humans;
            unsigned int cols = 5;
            for (size_t i = 0; i < sizeof(tmp); i += cols) {
                std::vector<unsigned int> human(tmp.begin() + i, tmp.begin() + i + cols);
                humans.push_back(human);
            }

            if (tmp.size() != 0 && !depth_image_.empty()) {
                for (const auto &human : humans) {
                    unsigned int id = human[0];
                    unsigned int x1 = human[1];
                    unsigned int y1 = human[2];
                    unsigned int x2 = human[3];
                    unsigned int y2 = human[4];

                    std::vector<float> depth_list;

                    // for (int x = x1; x < x2; x++) {
                    //     for (int y = y1; y < y2; y++) {
                    //         // printf("%f\n", depth_image_.at<float>(y, x));
                    //         // float pixel_value = depth_image_.at<float>(y, x);
                    //         // depth_list.push_back(pixel_value);
                    //     }
                    // }
                    // printf("hello\n");

                    // if (!depth_list.empty()) {
                    //     std::sort(depth_list.begin(), depth_list.end());
                    //     int rm_list = depth_list.size() / 4;
                    //     depth_list.erase(depth_list.begin(), depth_list.begin() + rm_list);
                    //     depth_list.erase(depth_list.begin() + rm_list * 2, depth_list.end());

                    //     float total = std::accumulate(depth_list.begin(), depth_list.end(), 0.0);
                    //     float average = total / depth_list.size();
                    //     float distance_cm = std::round(average * 10000) / 10000.0;
                    //     distPublish(distance_cm, id);
                    // }
                }
            }
        }

        void distPublish(float dist, int id) {
            std_msgs::msg::Float32::SharedPtr msg;
            msg->data = dist;
            dist_publisher_->publish(*msg);
            RCLCPP_INFO(this->get_logger(), "id:%d person distance is %.4f cm", id, msg->data);
        }
};

int main(int argc, char *argv[]) {
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<DistNode>());
    rclcpp::shutdown();
    return 0;
}

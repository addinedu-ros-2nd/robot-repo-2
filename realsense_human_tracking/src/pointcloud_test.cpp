#include <rclcpp/rclcpp.hpp>
#include <sensor_msgs/msg/camera_info.hpp>
#include <sensor_msgs/msg/image.hpp>
#include <sensor_msgs/msg/point_cloud2.hpp>
// #include <pcl_conversions/pcl_conversions.h>
#include <pcl/point_cloud.h>
#include <pcl/point_types.h>
#include <pcl/filters/passthrough.h>
#include <pcl/visualization/cloud_viewer.h>

class DepthToPointCloudNode : public rclcpp::Node
{
public:
    DepthToPointCloudNode() : Node("depth_to_pointcloud_node")
    {
        camera_info_subscription_ = this->create_subscription<sensor_msgs::msg::CameraInfo>(
            "/camera/depth/camera_info", 10,
            std::bind(&DepthToPointCloudNode::cameraInfoCallback, this, std::placeholders::_1)
        );

        depth_image_subscription_ = this->create_subscription<sensor_msgs::msg::Image>(
            "/camera/depth/image_rect_raw", 10,
            std::bind(&DepthToPointCloudNode::depthImageCallback, this, std::placeholders::_1)
        );

        pointcloud_publisher_ = this->create_publisher<sensor_msgs::msg::PointCloud2>(
            "/camera/depth/pointcloud", 10
        );
    }

private:
    void cameraInfoCallback(const sensor_msgs::msg::CameraInfo::SharedPtr msg)
    {
        // Process CameraInfo message, extract intrinsic parameters if needed
    }

    void depthImageCallback(const sensor_msgs::msg::Image::SharedPtr msg)
    {
        // Process depth image and create a point cloud
        pcl::PointCloud<pcl::PointXYZ> point_cloud;

        // Convert depth image to point cloud
        pcl::PassThrough<pcl::PointXYZ> pass;
        pass.setInputCloud(point_cloud.makeShared());
        pass.setFilterFieldName("z");
        pass.setFilterLimits(0.0, 10.0);
        pass.filter(point_cloud);

        // Publish the point cloud
        sensor_msgs::msg::PointCloud2 pointcloud_msg;
        pcl::toROSMsg(point_cloud, pointcloud_msg);
        pointcloud_msg.header = msg->header;
        pointcloud_publisher_->publish(pointcloud_msg);

        // Visualize the point cloud (optional)
        pcl::visualization::CloudViewer viewer("Point Cloud Viewer");
        viewer.showCloud(point_cloud.makeShared());
        viewer.spinOnce();
    }

    rclcpp::Subscription<sensor_msgs::msg::CameraInfo>::SharedPtr camera_info_subscription_;
    rclcpp::Subscription<sensor_msgs::msg::Image>::SharedPtr depth_image_subscription_;
    rclcpp::Publisher<sensor_msgs::msg::PointCloud2>::SharedPtr pointcloud_publisher_;
};

int main(int argc, char *argv[])
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<DepthToPointCloudNode>());
    rclcpp::shutdown();
    return 0;
}

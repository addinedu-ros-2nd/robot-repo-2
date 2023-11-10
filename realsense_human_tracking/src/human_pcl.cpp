#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/image.hpp"
#include "std_msgs/msg/float32.hpp"
#include "std_msgs/msg/int32_multi_array.hpp"
#include "sensor_msgs/msg/camera_info.hpp"
#include "cv_bridge/cv_bridge.h"
#include "opencv2/opencv.hpp"
#include <cmath>
#include <iostream>
#include <thread>
#include <pcl/common/angles.h>
#include <pcl/features/normal_3d.h>
#include <pcl/io/pcd_io.h>
#include <pcl/visualization/pcl_visualizer.h>
#include <pcl/console/parse.h>

pcl::visualization::PCLVisualizer::Ptr rgbVis (pcl::PointCloud<pcl::PointXYZRGB>::ConstPtr cloud){
  // --------------------------------------------
  // -----Open 3D viewer and add point cloud-----
  // --------------------------------------------
  pcl::visualization::PCLVisualizer::Ptr viewer (new pcl::visualization::PCLVisualizer ("3D Viewer"));
  viewer->setBackgroundColor (0, 0, 0);
  pcl::visualization::PointCloudColorHandlerRGBField<pcl::PointXYZRGB> rgb(cloud);
  viewer->addPointCloud<pcl::PointXYZRGB> (cloud, rgb, "sample cloud");
  viewer->setPointCloudRenderingProperties (pcl::visualization::PCL_VISUALIZER_POINT_SIZE, 3, "sample cloud");
  viewer->addCoordinateSystem (1.0);
  viewer->initCameraParameters ();
  return (viewer);
}

void removeOutliers(cv::Mat& mat) {
    // 평균과 표준 편차 계산
    cv::Scalar mean, stddev;
    cv::meanStdDev(mat, mean, stddev);
    float threshold = 10 / pow(mean[0], 1.0 / 5.0);
    printf("%f, %f, %f\n", mean[0], stddev[0], threshold);

    // Z-score를 계산하고, 임계값 이상인 값을 0으로 설정
    mat.forEach<float>([&](float& pixel, const int* position) -> void {
        double zScore = (pixel - mean[0]) / stddev[0];
        if (std::abs(zScore) > threshold) {
            pixel = 0.0;
        }
    });
}

void removeOutline(cv::Mat& mat) {
    // mat 크기
    cv::Mat clonedMat = mat.clone();
    int rows = clonedMat.rows;
    int cols = clonedMat.cols;

    // 5x5 크기의 커널
    int kernelSize = 2;
    cv::Mat kernel = cv::Mat::zeros(kernelSize, kernelSize, CV_32F);

    // 매트릭스 전체를 2칸씩 띄엄띄엄 돌면서 처리
    for (int i = 0; i < rows - kernelSize; i += 2) {
        for (int j = 0; j < cols - kernelSize; j += 2) {
            // 5x5 커널 영역 가져오기
            cv::Mat regionOfInterest = mat(cv::Rect(j, i, kernelSize, kernelSize));

            // 커널 안에 0이 하나라도 있으면 해당 커널의 값을 모두 0으로 만듦
            if (cv::countNonZero(regionOfInterest <= 10) > 0) {
                kernel.copyTo(clonedMat(cv::Rect(j, i, kernelSize, kernelSize)));
            }
        }
    }
}

cv::Mat human_filter(cv::Mat depth_image_, cv::Mat mat_human){
    cv::Mat result;
    mat_human.convertTo(mat_human, CV_32F);
    cv::multiply(depth_image_, mat_human, result);
    return result;
}

struct rs2_intrinsics {
    float         ppx;       /**< Horizontal coordinate of the principal point of the image, as a pixel offset from the left edge */
    float         ppy;       /**< Vertical coordinate of the principal point of the image, as a pixel offset from the top edge */
    float         fx;        /**< Focal length of the image plane, as a multiple of pixel width */
    float         fy;        /**< Focal length of the image plane, as a multiple of pixel height */
    float         coeffs[5]; /**< Distortion coefficients */
};

static void rs2_deproject_pixel_to_point(pcl::PointXYZRGB& point, const struct rs2_intrinsics * intrin, int pixel_x, int pixel_y, float depth) {
    float x = (pixel_x - intrin->ppx) / intrin->fx;
    float y = (pixel_y - intrin->ppy) / intrin->fy;
    // if Distortion Model == Brown Conrady
    // float r2  = x*x + y*y;
    // float f = 1 + intrin->coeffs[0]*r2 + intrin->coeffs[1]*r2*r2 + intrin->coeffs[4]*r2*r2*r2;
    // float ux = x*f + 2*intrin->coeffs[2]*x*y + intrin->coeffs[3]*(r2 + 2*x*x);
    // float uy = y*f + 2*intrin->coeffs[3]*x*y + intrin->coeffs[2]*(r2 + 2*y*y);
    // x = ux;
    // y = uy;
    point.y = depth * x;
    point.z = depth * y;
    point.x = depth;
    point.r = 255;
    point.g = std::round(255 - 255 * depth / 5);
    point.b = std::round(255 - 255 * depth / 5);
}

class DistNode : public rclcpp::Node {
    public:
        DistNode() : Node("dist_node") {
            camera_info_subscriber_ = create_subscription<sensor_msgs::msg::CameraInfo>(
                "/camera/depth/camera_info",
                10,
                std::bind(&DistNode::cameraInfoCallback, this, std::placeholders::_1)
            );
            depth_subscription_ = this->create_subscription<sensor_msgs::msg::Image>(
                "/camera/depth/image_rect_raw",
                10,
                std::bind(&DistNode::depthImageCallback, this, std::placeholders::_1)
            );
            // color_subscription_ = this->create_subscription<sensor_msgs::msg::Image>(
            //     "/camera/color/image_raw",
            //     10,
            //     std::bind(&DistNode::colorImageCallback, this, std::placeholders::_1)
            // );
            seg_subscription_ = this->create_subscription<std_msgs::msg::Int32MultiArray>(
                "/person_seg_tracking",
                10,
                std::bind(&DistNode::segCallback, this, std::placeholders::_1)
            );
        }

    private:
        rclcpp::Subscription<sensor_msgs::msg::CameraInfo>::SharedPtr camera_info_subscriber_;
        rclcpp::Subscription<sensor_msgs::msg::Image>::SharedPtr depth_subscription_;
        // rclcpp::Subscription<sensor_msgs::msg::Image>::SharedPtr color_subscription_;
        rclcpp::Subscription<std_msgs::msg::Int32MultiArray>::SharedPtr seg_subscription_;
        rclcpp::Publisher<std_msgs::msg::Float32>::SharedPtr dist_publisher_;
        cv_bridge::CvImagePtr cv_ptr;
        cv::Mat color_image_;
        cv::Mat depth_image_;
        rs2_intrinsics intrinsics;
        pcl::PointCloud<pcl::PointXYZRGB>::Ptr point_cloud_ptr = std::make_shared<pcl::PointCloud<pcl::PointXYZRGB>>();
        pcl::visualization::PCLVisualizer::Ptr viewer = rgbVis(point_cloud_ptr);

        // void colorImageCallback(const sensor_msgs::msg::Image::ConstPtr msg) {
        //     color_image_.create(msg->height, msg->width, CV_8UC3);
        //     color_image_.data = const_cast<unsigned char *>(msg->data.data());
        //     // color_image_.step = msg->step;
        //     cv::cvtColor(color_image_, color_image_, cv::COLOR_RGB2BGR);
        // }

        void cameraInfoCallback(const sensor_msgs::msg::CameraInfo::SharedPtr msg) {
            intrinsics.ppx = msg->k[2];
            intrinsics.ppy = msg->k[5];
            intrinsics.fx = msg->k[0];
            intrinsics.fy = msg->k[4];
            intrinsics.coeffs[0] = msg->d[0];
            intrinsics.coeffs[1] = msg->d[1];
            intrinsics.coeffs[2] = msg->d[2];
            intrinsics.coeffs[3] = msg->d[3];
            intrinsics.coeffs[4] = msg->d[4];
        }

        void depthImageCallback(const sensor_msgs::msg::Image::ConstPtr msg) {
            cv_ptr = cv_bridge::toCvCopy(msg);
            depth_image_ = cv_ptr->image;
            depth_image_.convertTo(depth_image_, CV_32F);
        }

        void segCallback(const std_msgs::msg::Int32MultiArray::SharedPtr msg) {
            if (depth_image_.rows <= 0) {
                return;
            }
            std::vector<int> tmp = msg->data;
            unsigned int len = depth_image_.rows * depth_image_.cols + 1;
            unsigned int count = tmp.size() / len;

            for (size_t i = 1; i <= count; i++) {
                std::vector<int> human(tmp.begin() + len * (i - 1) + 1, tmp.begin() + len * i);
                cv::Mat mat_human(human);
                mat_human.convertTo(mat_human, CV_8U);
                mat_human = mat_human.reshape(1, depth_image_.rows);
                cv::Mat result = human_filter(depth_image_, mat_human);
                // statistical outlier removal -> Failed!!
                removeOutliers(result);
                // removeOutline(result);
                // removeOutliers(result);

                point_cloud_ptr = std::make_shared<pcl::PointCloud<pcl::PointXYZRGB>>();
                for (int y = 0; y < result.rows; y++) {
                    for (int x = 0; x < result.cols; x++) {
                        float depth = result.at<float>(y, x) / 1000;
                        // cv::Vec3b pixel = color_image_.at<cv::Vec3b>(y, x);
                        // int blue = pixel[0];
                        // int green = pixel[1];
                        // int red = pixel[2];
                        if (depth > 0) {
                            pcl::PointXYZRGB point;
                            rs2_deproject_pixel_to_point(point, &intrinsics, x, y, depth);
                            point_cloud_ptr->points.push_back(point);
                        }
                    }
                }
            }

            point_cloud_ptr->width = point_cloud_ptr->size ();
            point_cloud_ptr->height = 1;
            viewer->updatePointCloud(point_cloud_ptr, "sample cloud");
            viewer->spinOnce(100);
            std::this_thread::sleep_for(std::chrono::milliseconds(100));
        }
};

int main(int argc, char *argv[]) {
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<DistNode>());
    rclcpp::shutdown();
    return 0;
}

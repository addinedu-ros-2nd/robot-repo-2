#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/image.hpp"
#include "std_msgs/msg/float32.hpp"
#include "std_msgs/msg/int32_multi_array.hpp"
#include "cv_bridge/cv_bridge.h"
#include "opencv2/opencv.hpp"

class DistNode : public rclcpp::Node {
    rclcpp::Subscription<sensor_msgs::msg::Image>::SharedPtr depth_subscription_;
    rclcpp::Subscription<std_msgs::msg::Int32MultiArray>::SharedPtr detect_subscription_;
    rclcpp::Publisher<std_msgs::msg::Float32>::SharedPtr dist_publisher_;
    std::shared_ptr<cv_bridge::CvImage> cv_bridge_;
    cv_bridge::CvImagePtr cv_ptr;
    // cv_bridge::CvBridge bridge;
    cv::Mat depth_image_;
    public:
        DistNode() : Node("dist_node") {
            depth_subscription_ = this->create_subscription<sensor_msgs::msg::Image>(
                "/camera/depth/image_rect_raw",
                10,
                std::bind(&DistNode::depthImageCallback, this, std::placeholders::_1)
            );

            detect_subscription_ = this->create_subscription<std_msgs::msg::Int32MultiArray>(
                "/person_detect",
                10,
                std::bind(&DistNode::detectCallback, this, std::placeholders::_1)
            );

            dist_publisher_ = this->create_publisher<std_msgs::msg::Float32>(
                "/person_dist",
                10
            );


            printf("hello!\n");
        }

    private:
        void depthImageCallback(const sensor_msgs::msg::Image::SharedPtr msg) {
            cv_ptr = cv_bridge_->imgMsgToCv(msg, "passthrough");
            depth_image_ = cv_ptr->image;
            depth_image_.convertTo(depth_image_, CV_32F);
            // cv_bridge::CvImagePtr cv_ptr;
            // cv_ptr = cv_bridge::toCvCopy(msg, sensor_msgs::image_encodings::TYPE_32FC1);
            // depth_image_ = cv_ptr->image;
        }

        void detectCallback(const std_msgs::msg::Int32MultiArray::SharedPtr msg) {
            std::vector<int> tmp = msg->data;
            std::vector<std::vector<int>> humans;
            int cols = 5;
            for (size_t i = 0; i < sizeof(tmp); i += cols) {
                std::vector<int> human(tmp.begin() + i, tmp.begin() + i + cols);
                humans.push_back(human);
            }

            if (tmp.size() != 0 && !depth_image_.empty()) {
                for (const auto &human : humans) {
                    int id = human[0];
                    int x1 = human[1];
                    int y1 = human[2];
                    int x2 = human[3];
                    int y2 = human[4];

                    std::vector<float> depth_list;

                    std::cout << depth_image_.size() << "\n";

                    ////////// Fix here!!!!
                    for (int y = y1; y < y2; y++) {
                        for (int x = x1; x < x2; x++) {
                            std::cout << depth_image_.at<float>(y, x) << "\n";
                            // float pixel_value = depth_image_.at<float>(y, x);
                            // depth_list.push_back(pixel_value);
                        }
                    }

                //     if (!depth_list.empty()) {
                //         std::sort(depth_list.begin(), depth_list.end());
                //         int rm_list = depth_list.size() / 4;
                //         depth_list.erase(depth_list.begin(), depth_list.begin() + rm_list);
                //         depth_list.erase(depth_list.begin() + rm_list * 2, depth_list.end());

                //         float total = std::accumulate(depth_list.begin(), depth_list.end(), 0.0);
                //         float average = total / depth_list.size();
                //         float distance_cm = std::round(average * 10000) / 10000.0;
                //         distPublish(distance_cm, id);
                //     }
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

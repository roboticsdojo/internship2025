#include <chrono>   // For time intervals like 500ms
#include <memory>  // For shared_ptr
#include "rclcpp/rclcpp.hpp"  // Core ROS 2 C++ client library
#include "std_msgs/msg/string.hpp"  // Message type used in the publisher

using namespace std::chrono_literals;  // Enables use of 500ms directly

class Talker : public rclcpp::Node {
public:
    Talker() : Node("talker_node"), count_(0) {
        publisher_ = this->create_publisher<std_msgs::msg::String>("chatter", 10);
        timer_ = this->create_wall_timer(500ms, std::bind(&Talker::publish_message, this));
    }

private:
    void publish_message() {
        auto message = std_msgs::msg::String();
        message.data = "Hello ROS2! Count: " + std::to_string(count_++);
        RCLCPP_INFO(this->get_logger(), "Publishing: '%s'", message.data.c_str());
        publisher_->publish(message);
    }

    rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
    rclcpp::TimerBase::SharedPtr timer_;
    int count_;
};

int main(int argc, char * argv[]) {
    rclcpp::init(argc, argv);  // Initialize ROS
    rclcpp::spin(std::make_shared<Talker>());   // Run node
    rclcpp::shutdown();  // Clean up
    return 0;
}

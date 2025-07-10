#include "rclcpp/rclcpp.hpp"

class MyRobotNode : public rclcpp::Node
{
public:
    MyRobotNode() : Node("my_robot_node")
    {
        RCLCPP_INFO(this->get_logger(), "My Robot Node has been started.");
    }
};

int main(int argc, char *argv[])
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<MyRobotNode>());
    rclcpp::shutdown();
    return 0;
}

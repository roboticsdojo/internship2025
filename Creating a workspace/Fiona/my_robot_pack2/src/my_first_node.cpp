#include "rclcpp/rclcpp.hpp"
using namespace std;

class MyFirstNode : public rclcpp::Node
{
public:
    MyFirstNode() : Node("first_node")
    {
        timer_ = this->create_wall_timer(
            chrono::seconds(1),
            bind(&MyFirstNode::timer_callback, this));
    }

private:
    void timer_callback()
    {
        RCLCPP_INFO(this->get_logger(), "Timer callback executed!");
    }

    rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char * argv[])
{
    rclcpp::init(argc, argv);
    rclcpp::spin(make_shared<MyFirstNode>());
    rclcpp::shutdown();
    return 0;
}

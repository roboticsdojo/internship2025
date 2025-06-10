import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class TalkerNode(Node):

    def __init__(self):
        super().__init__('talker_node')
        self.publisher = self.create_publisher(
            String,
            'talker',
            10
        )
        timer_period = 0.5
        self.timer = self.create_timer(
            timer_period, self.timer_callback
        )

    def timer_callback(self):
        msg = String()
        msg.data = 'Hello!'
        self.publisher.publish(msg)
        self.get_logger().info(f'published:{msg.data}')


def main(args=None):
    rclpy.init(args=args)

    talker_node = TalkerNode()

    rclpy.spin(talker_node)

    talker_node.destroy_node()
    rclpy.shutdown()
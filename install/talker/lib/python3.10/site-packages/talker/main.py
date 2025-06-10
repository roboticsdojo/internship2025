import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class TalkerNode(Node):

    def __init__(self):
        super().__init__('talker_node')
        self.publisher = self.create_publisher(
            string,
            'talker',
            10
        )
        timer period = 0.5
        self.timer = self.create_timer(
            timer_period, self.timer_callback
        )

    def timer_callback(self):
        msg = string()
        msg.data = 'Hello!'
        self.publisher.publish(msg)


def time_callback(self):
    rclpy.init(args=args)

    talker_node = TalkerNode()

    rclpy.spin(talker_node)

    rclpy.shutdown()    
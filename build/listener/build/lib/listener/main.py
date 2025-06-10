import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class ListenerNode(Node):

    def __init__(self):
        super().__init__('listener_node')
        self.subscriber = self.create_subscription(
            string,
            'talker',
            10
        )

    def listener_callback(self, msg):
        self.get_logger().info('msg: %s' %msg.data)


def main(args=None):
    rclpy.init(args=args)

    listener_node = ListenerNode()

    rclpy.spin(istener_node)

    rclpy.shutdown()    
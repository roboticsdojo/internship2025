# Import the ROS 2 Python client library
import rclpy
from rclpy.node import Node

# Import the standard message type: String
from std_msgs.msg import String

# Define a custom node class that inherits from Node
class TalkerNode(Node):

    def __init__(self):
        super().__init__('talker_node') # Initialize the node with the name 'talker'
        # Create a publisher on the topic 'chatter' with queue size 10
        self.publisher = self.create_publisher(
            String,
            'talker',
            10
        )
        timer_period = 0.5 # Create a timer that calls a function every 0.5 second
        self.timer = self.create_timer(
            timer_period, self.timer_callback
        )

    # The function that gets called every 0.5 second
    def timer_callback(self):
        msg = String() # Create a message of type String
        msg.data = 'Hello!' # Set its data
        self.publisher.publish(msg)# Publish the message
        self.get_logger().info(f'published:{msg.data}') # Log the event


# The main entry point of the node
def main(args=None):
    rclpy.init(args=args) # Initialize ROS 2

    talker_node = TalkerNode() # Create an instance of the node

    rclpy.spin(talker_node) # Keep the node running

    talker_node.destroy_node() # Clean up
    rclpy.shutdown() # Shutdown ROS 2
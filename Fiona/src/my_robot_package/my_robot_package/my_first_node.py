#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

class MyFirstNode(Node):
    def __init__(self):
        super().__init__('first_node')  # Initialize the node with a name
        self.create_timer(1.0, self.time_callback)  # Timer calls time_callback every second

    def time_callback(self):
        self.get_logger().info('Timer callback executed!')

def main(args=None):
    rclpy.init(args=args)  # Initialize the ROS 2 Python client library

    node = MyFirstNode()  # Instantiate your node class

    rclpy.spin(node)  # Keep the node alive

    rclpy.shutdown()

if __name__ == '__main__':
    main()

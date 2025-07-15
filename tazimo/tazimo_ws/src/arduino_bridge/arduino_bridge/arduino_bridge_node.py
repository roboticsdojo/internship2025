#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import JointState
import serial
import math

class ArduinoBridge(Node):
    def __init__(self):
        super().__init__('arduino_bridge_node')
        
        # Serial setup (adjust port/baudrate)
        self.serial_port = '/dev/ttyUSB0'  # Arduino serial port
        self.baudrate = 9600
        self.serial = serial.Serial(self.serial_port, self.baudrate, timeout=1)
        self.get_logger().info(f"Connected to Arduino on {self.serial_port}")
        
        # Robot parameters (adjust for your hardware)
        self.WHEEL_RADIUS = 0.0325  # meters
        self.WHEEL_SEPARATION = 0.022  # meters
        self.TICKS_PER_REVOLUTION = 136 # Encoder ticks per wheel revolution
        
        # Subscriber for velocity commands
        self.cmd_vel_sub = self.create_subscription(
            Twist, '/cmd_vel', self.cmd_vel_callback, 10)
        
        # Publishers
        self.odom_pub = self.create_publisher(Odometry, '/odom', 10)
        self.joint_pub = self.create_publisher(JointState, '/joint_states', 10)
        
        # Odometry state
        self.x = 0.0  # Robot position (meters)
        self.y = 0.0
        self.th = 0.0  # Robot orientation (radians)
        self.last_time = self.get_clock().now()
        
        # Timer for reading serial data (50Hz)
        self.timer = self.create_timer(0.02, self.read_serial)

    def cmd_vel_callback(self, msg):
        # Convert Twist (linear.x, angular.z) to left/right wheel speeds
        left_speed = msg.linear.x - (msg.angular.z * self.WHEEL_SEPARATION / 2)
        right_speed = msg.linear.x + (msg.angular.z * self.WHEEL_SEPARATION / 2)
        
        # Send to Arduino (format: "V<left>,<right>\n")
        command = f"V{left_speed:.2f},{right_speed:.2f}\n"
        self.serial.write(command.encode())

    def read_serial(self):
        if self.serial.in_waiting:
            line = self.serial.readline().decode('utf-8').strip()
            
            # Parse encoder data (format: "E<left_ticks>,<right_ticks>\n")
            if line.startswith('E'):
                try:
                    left_ticks, right_ticks = map(int, line[1:].split(','))
                    self.process_encoder_data(left_ticks, right_ticks)
                except ValueError:
                    self.get_logger().warn("Malformed encoder data")

    def process_encoder_data(self, left_ticks, right_ticks):
        # Calculate wheel displacements (in meters)
        left_dist = (2 * math.pi * self.WHEEL_RADIUS) * (left_ticks / self.TICKS_PER_REVOLUTION)
        right_dist = (2 * math.pi * self.WHEEL_RADIUS) * (right_ticks / self.TICKS_PER_REVOLUTION)
        
        # Update odometry (differential drive model)
        current_time = self.get_clock().now()
        dt = (current_time - self.last_time).nanoseconds / 1e9
        self.last_time = current_time
        
        # Compute linear and angular displacement
        linear = (left_dist + right_dist) / 2
        angular = (right_dist - left_dist) / self.WHEEL_SEPARATION
        
        # Update pose
        self.x += linear * math.cos(self.th)
        self.y += linear * math.sin(self.th)
        self.th += angular
        
        # Publish odometry
        self.publish_odometry(linear / dt, angular / dt)
        # Publish joint states (for RViz)
        self.publish_joint_states(left_ticks, right_ticks)

    def publish_odometry(self, linear_vel, angular_vel):
        odom_msg = Odometry()
        odom_msg.header.stamp = self.get_clock().now().to_msg()
        odom_msg.header.frame_id = 'odom'
        odom_msg.child_frame_id = 'base_link'
        
        # Pose (position + orientation)
        odom_msg.pose.pose.position.x = self.x
        odom_msg.pose.pose.position.y = self.y
        odom_msg.pose.pose.orientation.z = math.sin(self.th / 2)
        odom_msg.pose.pose.orientation.w = math.cos(self.th / 2)
        
        # Twist (velocity)
        odom_msg.twist.twist.linear.x = linear_vel
        odom_msg.twist.twist.angular.z = angular_vel
        
        self.odom_pub.publish(odom_msg)

    def publish_joint_states(self, left_ticks, right_ticks):
        joint_msg = JointState()
        joint_msg.header.stamp = self.get_clock().now().to_msg()
        joint_msg.name = ['left_wheel_joint', 'right_wheel_joint']
        joint_msg.position = [
            (left_ticks / self.TICKS_PER_REVOLUTION) * 2 * math.pi,
            (right_ticks / self.TICKS_PER_REVOLUTION) * 2 * math.pi
        ]
        self.joint_pub.publish(joint_msg)

def main():
    rclpy.init()
    node = ArduinoBridge()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

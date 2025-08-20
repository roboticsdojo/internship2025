# #!/usr/bin/env python3
# import rclpy
# from rclpy.node import Node
# from rclpy.parameter import Parameter
# from geometry_msgs.msg import Twist, TransformStamped
# from nav_msgs.msg import Odometry
# from sensor_msgs.msg import JointState
# from tf2_ros import TransformBroadcaster
# import serial
# import math
# import numpy as np
# from collections import deque
# from threading import Lock

# class VelocityFilter:
#     """Competition-grade velocity smoothing filter"""
#     def __init__(self, window_size=5):
#         self.window = deque(maxlen=window_size)
#         self.lock = Lock()
        
#     def filter(self, value):
#         with self.lock:
#             self.window.append(value)
#             if len(self.window) < 3:  # Wait for sufficient samples
#                 return value
#             return np.median(self.window)

# class ArduinoBridge(Node):
#     def __init__(self):
#         super().__init__('arduino_bridge_node')
        
#         # Competition-optimized parameters
#         self.declare_parameters(
#             namespace='',
#             parameters=[
#                 ('serial_port', '/dev/ttyUSB0'),
#                 ('baud_rate', 115200),
#                 ('encoder_ticks_per_rev', 136),
#                 ('wheel_radius', 0.0325),
#                 ('wheel_separation', 0.22),
#                 ('velocity_window_size', 5),
#                 ('cmd_vel_timeout', 0.5)
#             ])
        
#         # Initialize parameters
#         self.serial_port = self.get_parameter('serial_port').value
#         self.baud_rate = self.get_parameter('baud_rate').value
#         self.ticks_per_rev = self.get_parameter('encoder_ticks_per_rev').value
#         self.wheel_radius = self.get_parameter('wheel_radius').value
#         self.wheel_separation = self.get_parameter('wheel_separation').value
        
#         # Competition tuning - covariance matrices
#         self.odom_pose_covariance = [
#             0.01, 0.0, 0.0, 0.0, 0.0, 0.0,
#             0.0, 0.01, 0.0, 0.0, 0.0, 0.0,
#             0.0, 0.0, 0.01, 0.0, 0.0, 0.0,
#             0.0, 0.0, 0.0, 0.03, 0.0, 0.0,
#             0.0, 0.0, 0.0, 0.0, 0.03, 0.0,
#             0.0, 0.0, 0.0, 0.0, 0.0, 0.03
#         ]
        
#         self.odom_twist_covariance = [
#             0.01, 0.0, 0.0, 0.0, 0.0, 0.0,
#             0.0, 0.01, 0.0, 0.0, 0.0, 0.0,
#             0.0, 0.0, 0.01, 0.0, 0.0, 0.0,
#             0.0, 0.0, 0.0, 0.03, 0.0, 0.0,
#             0.0, 0.0, 0.0, 0.0, 0.03, 0.0,
#             0.0, 0.0, 0.0, 0.0, 0.0, 0.03
#         ]
        
#         # Velocity filters
#         self.linear_filter = VelocityFilter(self.get_parameter('velocity_window_size').value)
#         self.angular_filter = VelocityFilter(self.get_parameter('velocity_window_size').value)
        
#         # Serial connection with enhanced reliability
#         self.serial = self._init_serial()
#         self.serial_lock = Lock()
        
#         # ROS2 interfaces
#         self.cmd_vel_sub = self.create_subscription(
#             Twist, '/cmd_vel', self.cmd_vel_callback, 10)
        
#         self.odom_pub = self.create_publisher(Odometry, '/odom', 10)
#         self.joint_pub = self.create_publisher(JointState, '/joint_states', 10)
#         self.tf_broadcaster = TransformBroadcaster(self)
        
#         # Odometry state with thread-safe access
#         self.odom_lock = Lock()
#         self.x = 0.0
#         self.y = 0.0
#         self.th = 0.0
#         self.last_time = self.get_clock().now()
        
#         # Safety monitoring
#         self.last_cmd_vel_time = self.get_clock().now()
#         self.cmd_vel_timeout = self.get_parameter('cmd_vel_timeout').value
#         self.safety_timer = self.create_timer(0.1, self.check_safety)
        
#         # Main control loop (50Hz)
#         self.control_timer = self.create_timer(0.02, self.update_odometry)
        
#         self.get_logger().info("Arduino bridge node initialized")

#     def _init_serial(self):
#         """Robust serial initialization with retries"""
#         max_retries = 5
#         for attempt in range(max_retries):
#             try:
#                 ser = serial.Serial(
#                     port=self.serial_port,
#                     baudrate=self.baud_rate,
#                     timeout=0.02,  # Short timeout for non-blocking reads
#                     write_timeout=0.1,
#                     parity=serial.PARITY_NONE,
#                     stopbits=serial.STOPBITS_ONE,
#                     bytesize=serial.EIGHTBITS
#                 )
#                 self.get_logger().info(f"Serial connected on {self.serial_port}")
#                 return ser
#             except serial.SerialException as e:
#                 if attempt == max_retries - 1:
#                     self.get_logger().fatal(f"Failed to connect to Arduino: {e}")
#                     raise
#                 self.get_logger().warning(f"Serial retry {attempt + 1}/{max_retries}")
#                 self.get_clock().sleep_for(rclpy.time.Duration(seconds=1))

#     def cmd_vel_callback(self, msg):
#         """Handle velocity commands with competition optimizations"""
#         self.last_cmd_vel_time = self.get_clock().now()
        
#         # Convert Twist to wheel velocities (rad/s)
#         left_speed = (msg.linear.x - (msg.angular.z * self.wheel_separation / 2)) / self.wheel_radius
#         right_speed = (msg.linear.x + (msg.angular.z * self.wheel_separation / 2)) / self.wheel_radius
        
#         # Scale to Arduino's expected range (-1.0 to 1.0)
#         left_speed = max(min(left_speed, 1.0), -1.0)
#         right_speed = max(min(right_speed, 1.0), -1.0)
        
#         # Send command with checksum
#         command = f"V{left_speed:.3f},{right_speed:.3f}\n"
#         with self.serial_lock:
#             try:
#                 self.serial.write(command.encode('ascii'))
#                 self.serial.flush()
#             except serial.SerialException as e:
#                 self.get_logger().error(f"Command write failed: {e}")
#                 self._reconnect_serial()

#     def update_odometry(self):
#         """Main odometry update loop at 50Hz"""
#         # Request and read encoder data
#         encoder_data = self._get_encoder_data()
#         if encoder_data is None:
#             return
            
#         left_ticks, right_ticks = encoder_data
        
#         # Calculate wheel displacements (meters)
#         left_dist = (2 * math.pi * self.wheel_radius) * (left_ticks / self.ticks_per_rev)
#         right_dist = (2 * math.pi * self.wheel_radius) * (right_ticks / self.ticks_per_rev)
        
#         # Update odometry (thread-safe)
#         with self.odom_lock:
#             current_time = self.get_clock().now()
#             dt = (current_time - self.last_time).nanoseconds / 1e9
#             self.last_time = current_time
            
#             # Compute displacements
#             linear = (left_dist + right_dist) / 2
#             angular = (right_dist - left_dist) / self.wheel_separation
            
#             # Update pose
#             self.x += linear * math.cos(self.th)
#             self.y += linear * math.sin(self.th)
#             self.th = math.atan2(math.sin(self.th + angular), math.cos(self.th + angular))  # Normalized
            
#             # Filter velocities
#             filtered_linear = self.linear_filter.filter(linear / dt if dt > 0 else 0.0)
#             filtered_angular = self.angular_filter.filter(angular / dt if dt > 0 else 0.0)
            
#             # Publish data
#             self._publish_odometry(filtered_linear, filtered_angular)
#             self._publish_joint_states(left_ticks, right_ticks)

#     def _get_encoder_data(self):
#         """Robust encoder data retrieval with error handling"""
#         with self.serial_lock:
#             try:
#                 # Request data
#                 self.serial.write(b"REQ\n")
                
#                 # Read response with timeout
#                 line = self.serial.readline().decode('ascii', errors='ignore').strip()
#                 if not line.startswith('E') or ',' not in line:
#                     return None
                    
#                 # Parse with validation
#                 parts = line[1:].split(',')
#                 if len(parts) != 2:
#                     return None
                    
#                 return int(parts[0]), int(parts[1])
                
#             except (serial.SerialException, UnicodeDecodeError, ValueError) as e:
#                 self.get_logger().warn(f"Encoder read error: {e}")
#                 self._reconnect_serial()
#                 return None

#     def _publish_odometry(self, linear_vel, angular_vel):
#         """Publish competition-grade odometry with proper covariance"""
#         odom_msg = Odometry()
#         odom_msg.header.stamp = self.get_clock().now().to_msg()
#         odom_msg.header.frame_id = 'odom'
#         odom_msg.child_frame_id = 'base_link'
        
#         # Pose with covariance
#         with self.odom_lock:
#             odom_msg.pose.pose.position.x = self.x
#             odom_msg.pose.pose.position.y = self.y
#             odom_msg.pose.pose.orientation.z = math.sin(self.th / 2)
#             odom_msg.pose.pose.orientation.w = math.cos(self.th / 2)
#             odom_msg.pose.covariance = self.odom_pose_covariance
            
#             # Twist with covariance
#             odom_msg.twist.twist.linear.x = linear_vel
#             odom_msg.twist.twist.angular.z = angular_vel
#             odom_msg.twist.covariance = self.odom_twist_covariance
            
#         self.odom_pub.publish(odom_msg)
        
#         # TF publication with proper timestamping
#         transform = TransformStamped()
#         transform.header.stamp = odom_msg.header.stamp
#         transform.header.frame_id = 'odom'
#         transform.child_frame_id = 'base_link'
#         transform.transform.translation.x = odom_msg.pose.pose.position.x
#         transform.transform.translation.y = odom_msg.pose.pose.position.y
#         transform.transform.rotation = odom_msg.pose.pose.orientation
#         self.tf_broadcaster.sendTransform(transform)

#     def _publish_joint_states(self, left_ticks, right_ticks):
#         """Publish wheel positions for visualization"""
#         joint_msg = JointState()
#         joint_msg.header.stamp = self.get_clock().now().to_msg()
#         joint_msg.name = ['left_wheel_joint', 'right_wheel_joint']
#         joint_msg.position = [
#             (left_ticks / self.ticks_per_rev) * 2 * math.pi,
#             (right_ticks / self.ticks_per_rev) * 2 * math.pi
#         ]
#         self.joint_pub.publish(joint_msg)

#     def check_safety(self):
#         """Stop robot if command timeout occurs"""
#         if (self.get_clock().now() - self.last_cmd_vel_time).nanoseconds > \
#            self.cmd_vel_timeout * 1e9:
#             with self.serial_lock:
#                 try:
#                     self.serial.write(b"V0.0,0.0\n")
#                 except serial.SerialException:
#                     pass

#     def _reconnect_serial(self):
#         """Handle serial reconnection"""
#         self.get_logger().warn("Attempting serial reconnection...")
#         with self.serial_lock:
#             try:
#                 self.serial.close()
#                 self.serial = self._init_serial()
#             except Exception as e:
#                 self.get_logger().error(f"Reconnection failed: {e}")

# def main():
#     rclpy.init()
#     node = ArduinoBridge()
#     try:
#         rclpy.spin(node)
#     except KeyboardInterrupt:
#         pass
#     finally:
#         node.destroy_node()
#         rclpy.shutdown()

# if __name__ == '__main__':
#     main()

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
        self.serial.flushInput()
        self.serial.readline() 
        self.get_logger().info(f"Connected to Arduino on {self.serial_port}")
        
        # Robot parameters (adjust for your hardware)
        self.WHEEL_RADIUS = 0.0325  # meters
        self.WHEEL_SEPARATION = 0.22  # meters
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

    # def read_serial(self):
    #     if self.serial.in_waiting:
    #         line = self.serial.readline().decode('utf-8').strip()
            
    #         # Parse encoder data (format: "E<left_ticks>,<right_ticks>\n")
    #         if line.startswith('E'):
    #             try:
    #                 left_ticks, right_ticks = map(int, line[1:].split(','))
    #                 self.process_encoder_data(left_ticks, right_ticks)
    #             except ValueError:
    #                 self.get_logger().warn("Malformed encoder data")

    # def read_serial(self):
    #     try:
    #         if self.serial.in_waiting:
    #             line = self.serial.readline().decode('utf-8').strip()
    #             if line.startswith('E'):
    #                 try:
    #                     left, right = map(int, line[1:].split(','))
    #                     self.process_encoder_data(left, right)
    #                 except ValueError:
    #                     self.get_logger().warn(f"Malformed encoder data: {line}")
    #     except serial.SerialException as e:
    #         self.get_logger().error(f"Serial error: {e}")
    #         # Attempt to reconnect
    #         self.serial.close()
    #         self.serial.open()

    # def read_serial(self):
    #     try:
    #         if self.serial.in_waiting:
    #             line = self.serial.readline().decode('utf-8', errors='ignore').strip()

    #             # Check format and validate
    #             if line.startswith('E') and ',' in line:
    #                 try:
    #                     payload = line[1:]
    #                     left_str, right_str = payload.split(',')
    #                     left = int(left_str.strip())
    #                     right = int(right_str.strip())
    #                     self.process_encoder_data(left, right)
    #                 except ValueError:
    #                     self.get_logger().warn(f"Malformed encoder data (value error): {line}")
    #             else:
    #                 self.get_logger().warn(f"Malformed encoder data: {line}")
    #     except serial.SerialException as e:
    #         self.get_logger().error(f"Serial error: {e}")
    #         self.serial.close()
    #         self.serial.open()

    def read_serial(self):
        try:
            self.serial.write(b"REQ\n")  # 🆕 Ask Arduino for encoder data

            if self.serial.in_waiting:
                line = self.serial.readline().decode('utf-8', errors='ignore').strip()

                # Check format and validate
                if line.startswith('E') and ',' in line:
                    try:
                        payload = line[1:]
                        left_str, right_str = payload.split(',')
                        left = int(left_str.strip())
                        right = int(right_str.strip())
                        self.process_encoder_data(left, right)
                    except ValueError:
                        self.get_logger().warn(f"Malformed encoder data (value error): {line}")
                else:
                    self.get_logger().warn(f"Malformed encoder data: {line}")
        except serial.SerialException as e:
            self.get_logger().error(f"Serial error: {e}")
            self.serial.close()
            self.serial.open()

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

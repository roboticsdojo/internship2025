#!/usr/bin/env python3
import time
import serial
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class CmdVelToSerial(Node):
    def __init__(self):
        super().__init__('cmdvel_to_serial')
        self.declare_parameter('port', '/dev/ttyACM0')
        self.declare_parameter('baud', 115200)
        self.declare_parameter('linear_deadband', 0.05)
        self.declare_parameter('angular_deadband', 0.05)
        self.declare_parameter('watchdog_timeout', 0.5)

        port = self.get_parameter('port').get_parameter_value().string_value
        baud = self.get_parameter('baud').get_parameter_value().integer_value
        self.dead_lin = self.get_parameter('linear_deadband').get_parameter_value().double_value
        self.dead_ang = self.get_parameter('angular_deadband').get_parameter_value().double_value
        self.timeout = self.get_parameter('watchdog_timeout').get_parameter_value().double_value

        try:
            self.ser = serial.Serial(port, baudrate=baud, timeout=0)
            time.sleep(2.0)  # wait for Arduino auto-reset
            self.get_logger().info(f'Opened serial {port} @ {baud}')
        except Exception as e:
            self.get_logger().fatal(f'Could not open serial port {port}: {e}')
            raise

        self.last_cmd_time = self.get_clock().now()
        self.last_sent = None

        self.sub = self.create_subscription(Twist, '/cmd_vel', self.on_cmd, 10)
        self.timer = self.create_timer(0.05, self.watchdog)  # 20 Hz

    def on_cmd(self, msg: Twist):
        vx = msg.linear.x
        wz = msg.angular.z

        # deadbands
        if abs(vx) < self.dead_lin: vx = 0.0
        if abs(wz) < self.dead_ang: wz = 0.0

        # choose a single char for your sketch
        if vx == 0.0 and wz == 0.0:
            ch = 'x'
        elif abs(wz) > abs(vx):
            ch = 'a' if wz > 0 else 'd'
        else:
            ch = 'w' if vx > 0 else 's'

        self.send_once(ch)
        self.last_cmd_time = self.get_clock().now()

    def watchdog(self):
        # auto-stop if no cmd recently
        dt = (self.get_clock().now() - self.last_cmd_time).nanoseconds / 1e9
        if dt > self.timeout:
            self.send_once('x')

    def send_once(self, ch: str):
        if self.last_sent != ch:
            try:
                self.ser.write(ch.encode('ascii'))  # no newline; your sketch reads single chars
                self.last_sent = ch
            except Exception as e:
                self.get_logger().error(f'Serial write failed: {e}')

def main():
    rclpy.init()
    node = CmdVelToSerial()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

# Arduino Bridge Node for TAZIMO (ROS 2 humble)
This is a Python-based ROS 2 node that enables communication between a differential drive robot (TAZIMO) and a raspberry Pi via a serial connection to Nano. It allows the robot to receive velocity commands `(/cmd_vel)` and publish odometry `(/odom)` and joint state data `(/joint_states)`.

### Features
1. Sends velocity commands from ROS 2 to the Arduino

2. Receives encoder feedback from the Arduino

3. Publishes odometry data for localization

4. Publishes joint states for visualization (e.g., in RViz)

### How the Code Works
The node subscribes to `/cmd_vel` (of type `geometry_msgs/msg/Twist`) and sends the corresponding left and right wheel speeds to the Arduino in the format:
```
V<left_speed>,<right_speed>\n
```
It reads encoder feedback from the Arduino in the format:
```
E<left_ticks>,<right_ticks>\n
```
Encoder ticks are converted into wheel displacements, and then used to compute:

 - Robot’s pose (x, y, θ)

 - Linear and angular velocities

The node publishes:

Odometry data to `/odom` (type: `nav_msgs/msg/Odometry`)

Joint states to `/joint_states` (type: `sensor_msgs/msg/JointState`)

## How to Run the Node
### Prerequisites
  1. ROS 2 installed (e.g., Foxy, Humble, etc.)

  2. Arduino connected to your Pi via USB
  3. The corresponding Arduino firmware(e.g motor_control.ino) flashed (expected to handle velocity commands and send encoder ticks)
  4. Add execution permissions to the Python script:
```
chmod +x arduino_bridge_node.py
```
Tip! Update Serial Port (if needed)
  Make sure the serial port in the code matches your connected Arduino port.
  Edit this line in arduino_bridge_node.py if necessary:

```
self.serial_port = '/dev/ttyUSB0'
```
### Run the Node
In a sourced ROS 2 workspace:
```
ros2 run arduino_bridge arduino_bridge_node
```


**Make sure your Arduino is connected and the port is not blocked by another process.**

## Expected Outcome
The robot should respond to `/cmd_vel` commands by moving accordingly.
```
ros2 topic pub /cmd_vel geometry_msgs/Twist '{linear: {x: 0.2}, angular: {z: 0.0}}'
```
You can vary the speed of the wheels by changig the the x value in linear and z value in angular.

Alternatively, you can use teleop_twist_keyboard. In a new terminal:
```
sudo apt install ros-humble-teleop-twist-keyboard
ros2 pkg list | grep teleop_twist_keyboard
ros2 run teleop_twist_keyboard teleop_twist_keyboard

```
Odometry (`/odom`) and joint states (`/joint_states`) should be published at ~50Hz.

You can visualize these in RViz (especially if you’re using a URDF model).

Serial logs will show Arduino connection status and warn if malformed data is received.


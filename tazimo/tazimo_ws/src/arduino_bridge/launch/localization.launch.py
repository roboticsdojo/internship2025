from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    # Get path to EKF config
    pkg_dir = get_package_share_directory('arduino_bridge')
    ekf_config = os.path.join(pkg_dir, 'config', 'ekf.yaml')

    return LaunchDescription([
        # Arduino Bridge Node
        Node(
            package='arduino_bridge',
            executable='arduino_bridge_node',
            name='arduino_bridge_node',
            parameters=[{
                'serial_port': '/dev/ttyUSB0',  # Explicitly set Arduino port
                'baudrate': 9600
            }]
        ),

        # EKF Node
        Node(
            package='robot_localization',
            executable='ekf_node',
            name='ekf_filter_node',
            output='screen',
            parameters=[ekf_config],
            remappings=[
                ('/odometry/filtered', '/odom/filtered'),
            ]
        ),

        Node(
            package='sllidar_ros2',
            executable='sllidar_node',
            name='sllidar_node',
            output='screen',
            parameters=[{
                'serial_port': '/dev/ttyUSB1',
                'serial_baudrate': 115200
            }]
        )
    ])
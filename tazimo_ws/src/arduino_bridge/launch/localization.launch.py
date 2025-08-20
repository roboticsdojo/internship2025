from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    # Paths
    pkg_dir = get_package_share_directory('arduino_bridge')
    ekf_config = os.path.join(pkg_dir, 'config', 'ekf.yaml')

    # slam_pkg_dir = get_package_share_directory('robot_slam')  # your slam_toolbox package
    # slam_params_file = os.path.join(slam_pkg_dir, 'config', 'slam_toolbox_params.yaml')

    return LaunchDescription([
        # Arduino Bridge Node
        Node(
            package='arduino_bridge',
            executable='arduino_bridge_node',
            name='arduino_bridge_node',
            parameters=[{
                'serial_port': '/dev/ttyUSB0',
                'baudrate': 9600
            }]
        ),

        # EKF Node
        # Node(
        #     package='robot_localization',
        #     executable='ekf_node',
        #     name='ekf_filter_node',
        #     output='screen',
        #     parameters=[ekf_config],
        #     remappings=[
        #         ('/odometry/filtered', '/odom'),  # Important: slam_toolbox expects /odom
        #     ]
        # ),

        # Lidar Node
        # Node(
        #     package='sllidar_ros2',
        #     executable='sllidar_node',
        #     name='sllidar_node',
        #     output='screen',
        #     parameters=[{
        #         'serial_port': '/dev/ttyUSB0',
        #         'serial_baudrate': 115200
        #     }]
        # ),

        # # SLAM Toolbox Node
        # Node(
        #     package='slam_toolbox',
        #     executable='sync_slam_toolbox_node',
        #     name='slam_toolbox',
        #     output='screen',
        #     parameters=[
        #         slam_params_file,
        #         {'use_sim_time': False}  # real robot!
        #     ]
        # )
    ])


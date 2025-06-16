import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/michfiona2002/dojo_robotics_2025/src/my_robot_package/install/my_robot_package'

import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/caleb253/internship2025/caleb_ros2_ws/src/install/robotic_dojo'

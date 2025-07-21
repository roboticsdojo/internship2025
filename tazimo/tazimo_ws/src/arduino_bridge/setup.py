from setuptools import find_packages, setup

package_name = 'arduino_bridge'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='robotics',
    maintainer_email='olumoruth3@gmail.com',
    description='ROS2 Arduino Bridge Package for Robot Control',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
    'console_scripts': [
        'arduino_bridge_node = arduino_bridge.arduino_bridge_node:main',
    ],
  },
)

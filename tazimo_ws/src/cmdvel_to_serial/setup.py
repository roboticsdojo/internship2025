from setuptools import find_packages, setup

package_name = 'cmdvel_to_serial'

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
    maintainer='tazimo',
    maintainer_email='tazimo@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        	'cmdvel_to_serial = cmdvel_to_serial.cmdvel_to_serial_node:main',
       ],
    },
)

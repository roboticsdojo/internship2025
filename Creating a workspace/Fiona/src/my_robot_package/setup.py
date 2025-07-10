from setuptools import find_packages, setup

package_name = 'my_robot_package'

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
    maintainer='michfiona2002',
    maintainer_email='michfiona2002@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [ 'my_first_node = my_robot_package.my_first_node:main',
                            'listener = my_robot_package.listener:main'
        ],
    },
)

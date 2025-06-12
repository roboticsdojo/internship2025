# Setting Up a ROS2 Workspace
A **ROS2** workspace is a structured environment where you can **develop, build and run ROS2 packages**
It provides a clean and modular way to organize your robotics software, keeping source code, build artifacts, and install files separate.

## Use Cases
 - Writing and testing custom ROS2 nodes
 - Simulating robots in Gazebo or RViz
 - Integrating with hardware (sensors, actuators)
 -Building robotics middleware and tools

## Step-by-Step Setup
### 1. Install ROS2
 - Ensure you have ROS2 installed in your computer.
 - Head over to the official docs: [ROS2 Installation Guide](https://docs.ros.org)
 - Choose the correct version for your OS (e.g **Ubuntu 22.04  -> ROS2 Humble**) then follow the instructions to:

  ```bash
    # Add the ROS2 repository
    sudo apt update && sudo apt install curl gnupg lsb-release
    sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key | sudo apt-key add -
    sudo sh -c 'echo "deb http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" > /etc/apt/sources.list.d/ros2-latest.list'

    # Install ROS2 and dependencies
    sudo apt update
    sudo apt install ros-humble-desktop

    # Source ROS2 environment
    source /opt/ros/humble/setup.bash
   
### 2. Create your Workspace Directory

 ```bash
    mkdir -p ~/ros2_ws/src
    cd ~/ros2_ws
```
 - `mkdir -p ~/ros2_ws/src`: Creates the workspace folder (`ros2_ws`) with a subdirectory `src` where your ROS2 packages will live.

- `cd ~/ros2_ws`: Navigates to the root of your workspace.

### 3. Create or Add Packages
 ```bash
    cd ~/ros2_ws/src
    ros2 pkg create my_package --build-type ament_python --dependencies rclpy
```
    - To see and edit your package, open it in vs code
```bash
code .
```
- Navigate back to the parent derictory `cd ..`
 - To Build the package, run `colcon build`

 - Source the Setup Script
 ```bash
    source install/setup.bash
 ```
### 4. Create a ROS2 Node using Python
**1. Create a Python file inside the package:**
```bash
        cd ~/ros2_ws/src/my_package/my_package
        touch my_first_node.py
```
**2. To make your file executable**
```bash
        chmod +x my_first_node.py
```

**3. Edit my_first_node.py*** 
 - Open the file in VS code using `code .`
 Navigate to my_first_node.py inside my_package directory
 You can add the following code or use your own code:
  ```python
    #!/usr/bin/env python3

    import rclpy
    from rclpy.node import Node

    class MyNode(Node): 

        def __init__(self):  
            super().__init__('first_node')  
            self.get_logger().info("Hello from ROS2")

    def main(args=None):
        rclpy.init(args=args)
        node = MyNode()
        rclpy.spin(node)  # Keeps the node alive
        rclpy.shutdown()

    if __name__ == '__main__':  
        main()
 ```

 **4. Install the node**
  - Navigate to setup.py on your VS code
  - Edit setup.py to include your node
  ```python
    from setuptools import find_packages, setup

    package_name = 'my_package'

    setup(
        name=package_name,
        version='1.0.0',
        packages=find_packages(exclude=['test']),
        data_files=[
            ('share/ament_index/resource_index/packages',
                ['resource/' + package_name]),
            ('share/' + package_name, ['package.xml']),
        ],
        install_requires=['setuptools'],
        zip_safe=True,
        maintainer='olumo',
        maintainer_email='olumoruth3@gmail.com',
        description='A simple ROS 2 package that prints "Hello from ROS2"',
        license='MIT',
        tests_require=['pytest'],
        entry_points={
            'console_scripts': [
                "test_node = my_package.my_first_node:main"
            ],
        },
    )
```
We've added the line : 
  ```python
    "test_node = my_package.my_first_node:main" 
 ```

**5. Build and Source**
- Go back to your workspace root
```bash
    cd ~/ros2_ws
    colcon build
    source install/setup.bash
```
**6. Run the Node**
```bash
    ros2 run my_package test_node
```
You should see:
```csharp
[INFO] [1749548856.703966696] [first_node]: Hello from ROS2
```

### Creating The Node Using C++
**1. Create a c++ Package**
- From you ROS2 workspace src folder:
```bash
cd ~/ros2_ws/src
ros2 pkg create --build-type ament_cmake my_cpp_package --dependencies rclcpp
```
- This creates a C++ ROS2 package named my_cpp_package

**2. Create a C++ file in my_cpp_package/src/ called my_cpp_node.cpp**
```bash
    cd src/
    touch my_cpp_node.cpp
```
**3. Add a Simple code for the node**
```cpp
    #include "rclcpp/rclcpp.hpp"

    class MyNode : public rclcpp::Node {
    public:
        MyNode() : Node("my_cpp_node") {
            RCLCPP_INFO(this->get_logger(), "Hello from C++ node!");
        }
    };

    int main(int argc, char **argv) {
        rclcpp::init(argc, argv);
        rclcpp::spin(std::make_shared<MyNode>());
        rclcpp::shutdown();
        return 0;
    }
```
**4. Modify CMakeLists.txt**
- Open my_cpp_package/CmakeLists.txt
- Add the executables and install it :
```cmake
    add_executable(my_cpp_node src/my_cpp_node.cpp)
    ament_target_dependencies(my_cpp_node rclcpp)
    install(TARGETS
        my_cpp_node
        DESTINATION lib/${PROJECT_NAME})
```
**5. Build the Package**
- From the workspace root:
```bash
    cd ~/ros2_ws
    colcon build
```
 - Then source
 ```bash
    source install/setup.bash
```
**6. Run the Node**
```bash
    ros2 run my_cpp_package my_cpp_node
```
Results:
```csharp
[INFO] [my_cpp_node]: Hello from C++ node!
```
# Creating a Publisher and a Subscriber Node in ROS2(Python)
We'll do:
   A publisher node that publishes messages on a topic.

    A subscriber node that listens to that topic and prints the received messages
**Prerequisites**
    Ensure you have:
    - A valid ROS2 workspace set up (eg `ros2_ws`) and a package created with python support e.g, `my_package`
        - Follow the steps before this to create a workspace and a package, if you haven't done so.

**Creating the talker Node (`talker.py`)**
Navigate to the your package directory and create a talker.py file:
```bash
    cd ros2_ws/src/my_package/my_package
    touch talker.py
```
Open VSCode in this file and add your python code to the talker.py file:
```bash 
  code .
```
An example Python Code for the publisher:
```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'chatter', 10)
        self.timer = self.create_timer(0.5, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = f'Hello ROS 2: {self.i}'
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}"')
        self.i += 1

def main(args=None):
    rclpy.init(args=args)
    node = MinimalPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
```
**Creating the Subscriber Node (`listener.py`)**
Navigate to the your package directory and create a listener.py file
```bash
    cd ros2_ws/src/my_package/my_package
    touch listener.py
```
Open VSCode in this file and add your python code to the listener.py file:
```bash 
  code .
```
An example Python Code for the subscriber:
```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalSubscriber(Node):
    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            String,
            'chatter',
            self.listener_callback,
            10)

    def listener_callback(self, msg):
        self.get_logger().info(f'I heard: "{msg.data}"')

def main(args=None):
    rclpy.init(args=args)
    node = MinimalSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
```
**Updating setup.py**
- Make Sure your setup.py includes the correct entry points:
```python
entry_points={
    'console_scripts': [
        'talker = my_package.talker:main',
        'listener = my_package.listener:main',
    ],
},
```
**Make the python files Executable**
 - Run this to ensure ROS2 can run the scripts:
 ```bash
 chmod +x my_package/my_package/*.py
```
**Build and Source the Workspace**
From your ROS2 workspace root:
```bash
colcon build --packages-select my_package
source install/setup.bash
```
**Running the nodes**
- In two separate terminals:
 
 Terminal 1(Talker):
 ```bash
 source install/setup.bash
ros2 run my_package talker
```
Terminal 2(Listener):
```bash
source install/setup.bash
ros2 run my_package listener
```
**Common Error You may Run Into**
If you run:
```bash
ros2 run my_package talker
```
and get:
```pgsql
No executable found
```
Follow thes steps:
    **Checklist to Fix:**
    (i).  Are talker.py and listener.py inside my_package/my_package/?

    (ii). Do both have a main() function?

    (iii). Are they listed in setup.py under console_scripts?

    (iv). Have you run colcon build and source install/setup.bash?

    (v). Have you cleaned and rebuilt if needed?

    To clean and rebuild, run:
```bash
    rm -rf build/ install/ log/
    colcon build
    source install/setup.bash
```
    (vi) Check Available Executables
    Run:
```bash
    ros2 pkg executables my_package
```
    - If you don't see talker or listener, it means either:
      (a). File structure is wrong
      (b). Setup.py is incorrect
      (c). You forgot to build or source.




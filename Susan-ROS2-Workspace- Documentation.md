
# ROS2 Workspace Setup and Usage Guide

## Introduction

A ROS2 workspace is a structured environment where you can develop, build, and test your ROS2 projects. Think of it as your personal lab where all your ROS2 code and packages live.

Setting up a ROS2 workspace is one of the first and most important steps when starting with ROS2. It allows you to organize your code, manage dependencies, and compile everything using a single tool. In this guide, we'll walk through how to install ROS2 Humble, create your first workspace, build it, and start using core ROS2 tools like nodes, topics, and actions — all in a way that's friendly to beginners.

## Structure of a ROS2 Workspace

A standard ROS2 workspace consists of the following folders:

- `src/`: This is where you place the source code for your packages. It is the only directory you need to create manually.
- `build/`: Created after running `colcon build`. It contains intermediate files during the build process.
- `install/`: Also created by `colcon build`. It holds the built files and environment setup scripts.
- `log/`: Stores logs from the build and test processes.

## Prerequisites

To follow this guide, ensure you are using:

- Ubuntu 22.04 (recommended for ROS2 Humble)
- A user account with sudo privileges
- Some familiarity with using the terminal

If you haven't installed ROS2 Humble or are unfamiliar with the installation process, please follow the official ROS2 installation guide before continuing: [ROS2 Humble Installation Guide](https://robotics-dojo.atlassian.net/wiki/spaces/rdj/pages/39452687/ROS+2+HUMBLE+INSTALLATION?atlOrigin=eyJpIjoiMTQ3YzIxNzkzMTNlNGYwOWFjMGNjNmU4YTM5MjIxYmEiLCJwIjoiYyJ9)

## Environment Setup

The environment setup in ROS2 is important because it tells your terminal where to find the ROS2 tools, packages, and configuration files. Without it, commands like `ros2 run`, `ros2 topic`, or even your own packages won't work because the system doesn't know where ROS2 is installed or how to access your workspace.

Setting up the environment ensures:

- ROS2 paths and variables are loaded properly
- Your workspace builds and runs with the correct configuration
- You can use ROS2 tools and features without errors
- Your terminal can locate packages from both the system and your custom workspace

In short, environment setup connects your terminal to ROS2 so everything functions smoothly.

### Temporary (for the current terminal session):
```bash
source /opt/ros/humble/setup.bash
```

### Permanently (automatically sourced in every new terminal):
```bash
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

## Create and Build a ROS2 Workspace

Create the workspace directory and the src folder inside it:
```bash
mkdir -p ~/dojo_robotics_2025/src
cd ~/dojo_robotics_2025
```

Build the workspace using colcon:
```bash
colcon build
```

After a successful build, new directories named `build/`, `install/`, and `log/` will be created.

## Source the Workspace

After building, you need to source the local setup file to use packages in your workspace:
```bash
source install/setup.bash
```

Add it to your `.bashrc` file to source it automatically each time:
```bash
echo "source ~/dojo_robotics_2025/install/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

## Verify the Setup

To check if the workspace and ROS2 are correctly configured, run:
```bash
ros2 pkg list
```

You should see a list of available packages.

## Troubleshooting Tips

- If `ros2` commands are not recognized, make sure you have sourced the setup file:
  ```bash
  source /opt/ros/humble/setup.bash
  ```

- If you get `command not found` for `colcon`, install it:
  ```bash
  sudo apt install python3-colcon-common-extensions
  ```

- If `colcon build` fails, check the output logs in the `log/` directory, and make sure all dependencies are installed using:
  ```bash
  rosdep install --from-paths src --ignore-src -r -y
  ```

- If packages are not found when running, ensure the workspace is sourced:
  ```bash
  source install/setup.bash
  ```

- Re-run `colcon build` if you add new packages or make major changes to the workspace:
  ```bash
  colcon build --packages-select <your_package_name>
  ```

## Package Creation

A package is an organizational unit for your ROS 2 code. If you want to be able to install your code or share it with others, then you'll need it organized in a package. With packages, you can release your ROS 2 work and allow others to build and use it easily.

Package creation in ROS 2 uses `ament` as its build system and `colcon` as its build tool. You can create a package using either CMake or Python, which are officially supported, though other build types do exist.

### CMake Package Structure
```
my_package/
     CMakeLists.txt
     include/my_package/
     package.xml
     src/
```

### Python Package Structure
```
my_package/
      package.xml
      resource/my_package
      setup.cfg
      setup.py
      my_package/
```

### Create Package

1. Navigate the source folder
```bash
cd ~/dojo_robotics_2025/src
```

2. Create the package
```bash
ros2 pkg create --build-type ament_python my_robot_package --dependencies rclpy std_msgs
```

This creates a Python-based ROS 2 package named `my_robot_package` with dependencies on `rclpy` (Python ROS client library) and `std_msgs`.

After running that command, you'll get:
```
my_robot_package/
├── package.xml
├── setup.cfg
├── setup.py
├── resource/
│   └── my_robot_package
└── my_robot_package/
    └── __init__.py
```

Now you can go ahead and add your Python scripts (`talker.py`, `listener.py`, etc.) inside the `my_robot_package/` folder.

3. Build the Package
```bash
colcon build
```

To use your new package and executable, first open a new terminal and source your main ROS 2 installation, then source the environment:
```bash
source install/setup.bash
```

Now that your workspace has been added to your path, you will be able to use your new package's executables.

## Creating Nodes

### Python Node Guide

**Step 1:** Access the Workspace
```bash
cd ~/dojo_robotics_2025
```

**Step 2:** Access the Package
```bash
cd src/my_robot_package
```

**Step 3:** Create a Python File
```bash
cd my_robot_package
touch my_first_node.py
chmod +x my_first_node.py
```

**Step 4:** Open in VS Code
```bash
cd ~/dojo_robotics_2025
code .
```

**Step 5:** Sample Python Code
```python
#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

class MyFirstNode(Node):
    def __init__(self):
        super().__init__('first_node')  # Initialize the node with a name
        self.create_timer(1.0, self.time_callback)  # Timer calls time_callback every second

    def time_callback(self):
        self.get_logger().info('Timer callback executed!')

def main(args=None):
    rclpy.init(args=args)  # Initialize the ROS 2 Python client library
    node = MyFirstNode()  # Instantiate your node class
    rclpy.spin(node)  # Keep the node alive
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

**Step 6:** Source Your ROS2 Setup
```bash
source /opt/ros/humble/setup.bash
source install/setup.bash
```

**Step 7:** Run Your Node
```bash
python3 src/my_robot_package/my_robot_package/my_first_node.py
```

### C++ Node Guide

**Step 1:** Create C++ File
```bash
cd ~/dojo_robotics_2025/src/my_robot_package/src
touch my_first_node.cpp
```

**Step 2:** Sample C++ Code
```cpp
#include "rclcpp/rclcpp.hpp"

class MyFirstNode : public rclcpp::Node
{
public:
    MyFirstNode() : Node("first_node")
    {
        timer_ = this->create_wall_timer(
            std::chrono::seconds(1),
            std::bind(&MyFirstNode::timer_callback, this));
    }

private:
    void timer_callback()
    {
        RCLCPP_INFO(this->get_logger(), "Timer callback executed!");
    }

    rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char * argv[])
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<MyFirstNode>());
    rclcpp::shutdown();
    return 0;
}
```

**Step 3:** Update CMakeLists.txt
```cmake
find_package(rclcpp REQUIRED)

add_executable(my_first_node src/my_first_node.cpp)
ament_target_dependencies(my_first_node rclcpp)

install(TARGETS
  my_first_node
  DESTINATION lib/${PROJECT_NAME}
```

**Step 4:** Build and Run
```bash
cd ~/dojo_robotics_2025
colcon build
source install/setup.bash
ros2 run my_robot_package my_first_node
```

## Quick Summary

**Workspace Setup:**
```bash
mkdir -p ~/dojo_robotics_2025/src && cd ~/dojo_robotics_2025 && colcon build && source install/setup.bash
```

**Package Creation:**
```bash
ros2 pkg create my_robot_package --build-type ament_python  # for Python
ros2 pkg create my_robot_package --build-type ament_cmake   # for C++
```

**Python Node Working:**
Create `.py` in `src/`, write ROS 2 code, add to `setup.py`, build, then run using `ros2 run`.

**C++ Node Working:**
Create `.cpp` in `src/`, edit `CMakeLists.txt`, build with `colcon`, then run using `ros2 run`.
```

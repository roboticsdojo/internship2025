# ROS2 Workspace Setup
Setting up a ROS 2 workspace means creating a structured environment where you can build, organize, and manage your own ROS 2 packages.

*In brief: A ROS 2 workspace is a directory with a specific structure that allows you to develop and build ROS 2 nodes (programs), libraries, and other components using tools like colcon.*

The following steps are followed to setup the ROS2 Workspace:

### 1. Create workspace directory

![alt text](image.png)

The image above shows the command used to create the workspace directory. Once the directory is created we are able to navigate it.
**mkdir -p** creates the workspace folder (ros2_ws) and a src/ subdirectory.
**The src/ folder** is where ROS 2 looks for packages to build.
**cd** navigates into the workspace so you can build or manage packages.

### 2.Create a new package

![alt text](image-1.png)

**ros2 pkg** create initializes a new ROS 2 package.
**--build-type ament_cmake** tells ROS 2 you’ll use CMake (for C++).
**my_cpp_pkg** the name of your new package.

### 3.Build the workspace

![alt text](image-2.png)

**colcon** scans the src/ folder for ROS 2 packages.
For each package:
It configures it using CMake (or setup.py for Python).
Compiles source files
Creates symlinks or copies build artifacts into install/

### 4.Source the workspace

![alt text](image-3.png)

It loads the packages you just built into your current shell session.
It updates your shell environment to include:
New package paths
New executables and libraries

*If this step is skipped, ros2 run and other tools won’t know about your custom packages.*

ROS 2 separates your system ROS packages (/opt/ros/humble) from your own. You have to manually source your workspace's environment each time you open a terminal unless you automate it using the command below:

![alt text](image-4.png)



## Write and Build a Node
ROS nodes are small programs that:
Publish/subscribe to topics
Call/offer services
Control robots or sensors

### 1. Using C++
**Create a file as shown below:**

![alt text](image-5.png)

**Paste a minimal ROS 2 C++ node and save:**
**Modify CMakeLists.txt to Build the Node as shown below:**

![alt text](image-6.png)

**Add this block after find_package(rclcpp REQUIRED):**

![alt text](image-7.png)

Then save and close.

**Rebuild the workspace as shown below:**

![alt text](image-8.png)

The workspace is successfully rebuilt as shown below:

![alt text](image-9.png)

**Source it:**

![alt text](image-10.png)

**Then run your node:**

![alt text](image-11.png)

Output is as shown below:
![alt text](image-13.png)


### 2. Using Python
**Create a Python package**
Navigate to your workspace src directory:

![alt text](image-14.png)

Create a Python package (we'll call it my_py_pkg):

![alt text](image-15.png)

**Write your Python Node**
Create a Python Script file:

![alt text](image-16.png)

Paste this simple node:

![alt text](image-17.png)

**Update setup.py**
Open:

![alt text](image-19.png)

Update it as follows:

![alt text](image-18.png)

The line below means ROS will run the main() function in hello_node.py.

![alt text](image-20.png)

**Make the node executable**
Give it execute permission:

![alt text](image-21.png)

**Build the workspace**
Go back to the root of your workspace and build:

![alt text](image-22.png)

Source it:

![alt text](image-23.png)

**Run your Python Node**

![alt text](image-24.png)

The output is as shown:

![alt text](image-25.png)


## Building a Publisher and Subscriber

### 1. Using Python
**Publisher node:** Publishes messages to a topic called /chatter.
**Subscriber node:** Listens to /chatter and logs what it receives.

**Create the Publisher Node**
Create a file: talker.py as shown below:

![alt text](image-27.png)

Paste this in the file:

![alt text](image-26.png)

**Create the Subscriber Node**
Create a file: listener.py as shown below:

![alt text](image-29.png)

Paste this in the file:

![alt text](image-28.png)

**Update setup.py to Register the New Scripts**
Open:

![alt text](image-31.png)

Update entry_points like this:

![alt text](image-30.png)

**Rebuild the Package**

![alt text](image-32.png)

**Run the Publisher and Subscriber**
In Terminal one:

![alt text](image-33.png)

The Output is as shown below:

![alt text](image-34.png)


In Terminal two:

![alt text](image-35.png)

The Output is as shown below:

![alt text](image-36.png)


### 2. Using C++
We’ll create two C++ nodes:
Publisher node (talker.cpp) — publishes messages to /chatter
Subscriber node (listener.cpp) — receives those messages

**Create talker.cpp**

![alt text](image-39.png)

Paste this code:

![alt text](image-37.png)

![alt text](image-38.png)


**Create listener.cpp**

![alt text](image-41.png)

Paste this code:

![alt text](image-40.png)


**Update CMakeLists.txt**
Open:

![alt text](image-44.png)

Add below find_package(ament_cmake REQUIRED):

![alt text](image-42.png)

Add at the bottom:

![alt text](image-43.png)


**Rebuild**

![alt text](image-45.png)

It is successfully rebuilt as shown below:

![alt text](image-46.png)


**Run Your C++ Nodes**
In Terminal 1 (Publisher):

![alt text](image-47.png)

In Terminal 2 (Subscriber):

![alt text](image-48.png)
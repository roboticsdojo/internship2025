# GENERAL TUTORIAL
## PACKAGES
ROS2 packages are built using a tool called COLCON. Colcon os installed through the command below:
`sudo apt install python3-colcon-common-extensions`

Packages are built within workspaces. A workspace is essentially a folder that contains a package and its constituent components. A workspace contains a source folder named 'src' where the package is created. The commands used for this is:
```bash
mkdir ws_name #name of choice
cd ws_name
mkdir src
```

The command `colcon build` is then run in the workspace folder to pre-build the package. 3 new folders appear which are `build` `install` and `log` which manipulate the code within the `src` directory.
The workspace may be sourced manually on every instance of opening the terminal through the command `soucrce install/setup.bash`. The command may be echoed to `bashrc.` to source it on every instance of running a terminal.

Packages are built through the following commands:
```bash
cd src
ros2 pkg create package_name --build-type ament_python #name of choice for package. ament_python is used to create the package using python, and ament_cmake for C++
```

Visual Studio Code is then opened to navigate within the created package by running `code .` in the src folder.
Three files are created in the package.These are:
- `package.xml`
- `setup.cfg`
- `setup.py`

Three folders are also created which are:
- `package_name`
- `resource`
- `test`

If `ament_cmake` were used instead, the created files would be:
- `package.xml`
- `CMakeLists.txt`

and the folders:
- `include`
- `src`

`colcon build` is run again to build the package.

## NODES
A node is a file in a ROS package that can be executed. Nodes are created in the package (CPP) folder which is of the same name as the package (for python), and are files of the language type chosen when creating the package. (`node_name.py` or `node_name.cpp`)
The desired code may then be written.

# PROJECT - CPP PUBLISHER AND PYTHON SUBSRIBER
This project consisits of a cpp publisher that publishes random numbers between 1 and 12, and a python subscriber that reacts every time the published number is 7.
_Creating the workspace_

![alt text](<Screenshot 2025-06-10 125209.png>)

_Building and sourcing package_

![alt text](<Screenshot 2025-06-10 125755.png>) 

_creating cpp publisher_

![alt text](<Screenshot 2025-06-10 130537.png>)

_creating python subscriber_

![alt text](<Screenshot 2025-06-10 130608.png>)

_vs code_

![alt text](<Screenshot 2025-06-10 131008.png>)

_Publisher code_

![alt text](<Screenshot 2025-06-10 131725.png>)

_Subscriber code_

![alt text](<Screenshot 2025-06-10 131753.png>)

_project demo_

![alt text](<Screenshot 2025-06-10 154222.png>)
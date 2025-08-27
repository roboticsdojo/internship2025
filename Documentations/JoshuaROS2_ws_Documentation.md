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
This project consisits of a cpp publisher that publishes random numbers between 1 and 10, and a python subscriber that reacts every time the published number is 7.
_Creating the workspace_

<img width="459" height="94" alt="Screenshot 2025-06-10 125209" src="https://github.com/user-attachments/assets/4cddb0db-1ec2-45fe-9418-98ddf3e906db" />

_Building and sourcing package_

<img width="625" height="137" alt="Screenshot 2025-06-10 125755" src="https://github.com/user-attachments/assets/09188c12-1830-4db9-b4fd-eab182666b41" />

_creating cpp publisher_

<img width="1238" height="664" alt="Screenshot 2025-06-10 130537" src="https://github.com/user-attachments/assets/f79808d1-08d8-42f8-8636-a5d09f2aaa5d" />

_creating python subscriber_

<img width="1213" height="842" alt="Screenshot 2025-06-10 130608" src="https://github.com/user-attachments/assets/2db5f813-a020-4480-8a95-1c27bcd304b5" />

_vs code_

<img width="421" height="449" alt="Screenshot 2025-06-10 131008" src="https://github.com/user-attachments/assets/1698a762-561e-49f8-adba-a7201f3ed598" />

_Publisher code_

<img width="963" height="792" alt="Screenshot 2025-06-10 131725" src="https://github.com/user-attachments/assets/6d7bb0a3-2971-4257-80cd-7db2c7737eda" />

_Subscriber code_

<img width="868" height="728" alt="Screenshot 2025-06-10 131753" src="https://github.com/user-attachments/assets/78398b2f-3fe8-4fcd-8f1c-67c8fbd56e2b" />

_project demo_

<img width="1233" height="552" alt="Screenshot 2025-06-10 154222" src="https://github.com/user-attachments/assets/c3685f1b-5b46-4f89-b726-d135c96ed612" />

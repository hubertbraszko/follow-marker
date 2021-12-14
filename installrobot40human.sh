#!/bin/bash
read -p "Do you want to install robot40human_ws and additional libraries? [y/n]" -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
sudo apt-get install ros-kinetic-gazebo-ros-pkgs ros-kinetic-gazebo-ros-control
sudo apt-get install ros-melodic-gazebo-ros-pkgs ros-melodic-gazebo-ros-control
sudo apt-key adv --keyserver hkp://keys.gnupg.net:80 --recv-key C8B3A55A6F3EFCDE
sudo add-apt-repository "deb http://realsense-hw-public.s3.amazonaws.com/Debian/apt-repo xenial main" -
sudo rm -f /etc/apt/sources.list.d/realsense-public.list
sudo apt-get update
sudo apt-get install librealsense2-dev
sudo apt-get install librealsense2-dbg
git clone https://bitbucket.org/robot40proj/robot40human_ws
cd ~/robot40human_ws/
catkin_make
git clone https://github.com/shadow-robot/optoforce.git ~/robot40human_ws/src/optoforce
git clone https://github.com/ros-industrial/universal_robot.git ~/robot40human_ws/src/universal_robot
sudo apt-get install ros-melodic-dynamixel-workbench
sudo apt-get install ros-melodic-dynamixel-workbench-msgs
sudo apt-get update
git clone https://github.com/ROBOTIS-GIT/dynamixel-workbench.git ~/robot40human_ws/src/dynamixel-workbench
git clone https://github.com/ROBOTIS-GIT/dynamixel-workbench-msgs.git ~/robot40human_ws/src/dynamixel-workbench-msgs
git clone https://github.com/ros-drivers/urg_node.git ~/robot40human_ws/src/urg_node
git clone https://github.com/ros-drivers/urg_c.git ~/robot40human_ws/src/urg_c
git clone https://github.com/ros-perception/laser_proc.git ~/robot40human_ws/src/laser_proc
sudo apt-get install ros-melodic-dynamixel-sdk
sudo apt-get install ros-melodic-qt-build
sudo chmod a+rw /dev/ttyUSB0
cd ~/robot40human_ws/src/
git clone https://github.com/OpenKinect/libfreenect2.git
cd libfreenect2
sudo apt-get install ros-kinetic-dynamixel-workbench
sudo apt-get install ros-kinetic-dynamixel-workbench-msgs
sudo apt-get install build-essential cmake pkg-config
sudo apt-get install libusb-1.0-0-dev
sudo apt-get install libturbojpeg libjpeg-turbo8-dev 
sudo apt-get install libturbojpeg0-dev
sudo apt-get install libglfw3-dev
sudo apt-get install beignet-dev
sudo apt-get install libva-dev libjpeg-dev
sudo apt-get install libopenni2-dev
sudo apt install xdotool
mkdir build && cd build
cmake .. -DCMAKE_INSTALL_PREFIX=$HOME/freenect2
make
make install
cd ..
cmake -Dfreenect2_DIR=$HOME/freenect2/lib/cmake/freenect2
cd ~/robot40human_ws/src/
git clone https://github.com/code-iai/iai_kinect2.git
cd iai_kinect2
rosdep install -r --from-paths .
cd ~/robot40human_ws/
mkdir ~/robot40human_ws/devel/include/
cp -a ~/robot40human_ws/bin/includes/. ~/robot40human_ws/devel/include/
catkin_make
sudo chmod a+rw /dev/ttyUSB0
sudo cp ~/robot40human_ws/src/libfreenect2/platform/linux/udev/90-kinect2.rules /etc/udev/rules.d/
fi

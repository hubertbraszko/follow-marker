#! /bin/bash
export LC_NUMERIC="en_US.UTF-8"
cd /home/robot40/robot40human_ws/
sleep 5
source devel/setup.bash
export ROS_MASTER_URI=http://robot40:11311
export ROS_IP=192.168.1.58
export ROS_HOSTNAME=robot40
# roslaunch controller_robot40 start_robot.launch 
roslaunch controller_robot40 start_robot_ur5_limits.launch
export ROS_MASTER_URI=http://robot40:11311
export ROS_IP=192.168.1.58
export ROS_HOSTNAME=robot40


#!/bin/bash
export LC_NUMERIC="en_US.UTF-8"
stty -F /dev/ttyUSB0 115200
cd /home/robot40base/robot40human_ws/
source /home/robot40base/robot40human_ws/devel/setup.bash
export ROS_IP=192.168.1.61
export ROS_MASTER_URI=http://robot40:11311
echo "lrm" | sudo nmcli device wifi rescan
echo "Scanning wifi network..."
sleep 5
echo "lrm" | sudo nmcli device wifi connect SLAMWARE-701DD3
docker run -d --rm --name slamtech_docker --network host -it ros:robot40 &
sleep 2
docker exec slamtech_docker bash -c "source /ros_entrypoint.sh" &
sleep 3
roslaunch labmate labmate.launch

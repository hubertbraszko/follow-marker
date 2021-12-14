#!/usr/bin/env python
import rospy
from fiducial_msgs.msg import FiducialArray
import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
from math import pi
from std_msgs.msg import String
from moveit_commander.conversions import pose_to_list
from geometry_msgs.msg import Twist, Vector3


# moveit_commander.roscpp_initialize(sys.argv)
# robot = moveit_commander.RobotCommander()
# scene = moveit_commander.PlanningSceneInterface()
# group_name = "right_arm"
# group = moveit_commander.MoveGroupCommander(group_name)
# display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path',
#                                                moveit_msgs.msg.DisplayTrajectory,
#                                                queue_size=20)


rospy.init_node('aruco_goto', anonymous=True)
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
rate = rospy.Rate(10) # 10hz


def goto(aruco_cords):
    linear = Vector3(0,0,0)
    angular = Vector3(0,0,0.0)
    r_border = 373
    l_border = 313
    #żeby szukanie działało trzeba zastosować srednia z ostatnich 10 probek
    if aruco_cords[0]==0 and aruco_cords[1]==0: #czyli kiedy nie wykrywa znacznika
        #linear = Vector3(0,0,0)
        angular = Vector3(0,0,0.05)
        print('szukaj')

    # if aruco_cords[0]==0:
    #     linear = Vector3(0,0,0)
    #     angular = Vector3(0,0,0.0)

    if aruco_cords[0]<l_border:
        #linear = Vector3(0,0,0)
        angular = Vector3(0,0,0.05)
        print("w prawo")

    elif aruco_cords[0]>r_border:
        #linear = Vector3(0,0,0)
        angular = Vector3(0,0,-0.05)
        print("w lewo")
    else:# l_border>aruco_cords[0]>r_border:
        print('go')
        linear = Vector3(0.2,0,0)
    
    hello = Twist(linear, angular)
    pub.publish(hello)
    return 0


def convert_data(data):
    #ten kod bedzie do poprawy xdxd
    data = str(data)
    axes = ['x0','y0','x1']
    pos = []
    try:
        for a in range(2):
            index1 = data.find(axes[a])
            index2 = data.find(axes[a+1])
            tmp_position = data[index1+4:index2-1]
            tmp_position = tmp_position[:tmp_position.find('.')+5]
            pos.append(float(tmp_position))
        return pos #lista 2 floatów z pozycją
    except:
        return [0,0]

  

def callback(data):
    aruco_cords = convert_data(data)
    #print(aruco_cords)
    goto(aruco_cords)
    #rospy.signal_shutdown("end") 
    
    
def listener():
    rospy.Subscriber("/fiducial_vertices", FiducialArray, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()





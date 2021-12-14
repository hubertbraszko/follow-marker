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

moveit_commander.roscpp_initialize(sys.argv)
robot = moveit_commander.RobotCommander()
scene = moveit_commander.PlanningSceneInterface()
group_name = "right_arm"
group = moveit_commander.MoveGroupCommander(group_name)
display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path',
                                               moveit_msgs.msg.DisplayTrajectory,
                                               queue_size=20)

def starting_point():
    joint_goal = group.get_current_joint_values()
    start_joint_state = [3.0141982735007637, -2.0429579797429156, -1.7148698841374959, 0.6378837608602952, 1.6235141893962481, 0.7490375776349065]

    for a in range(len(joint_goal)):
        joint_goal[a]=start_joint_state[a]

    group.go(joint_goal, wait=True)

    group.stop()

def move(aruco_cord):
    wpose = group.get_current_pose().pose
    if aruco_cord[0]!=0:
        print(aruco_cord)
        if aruco_cord[1]< 160:
            print("góra")
            wpose.position.z = wpose.position.z + 0.01
            update_arm(wpose)
        elif aruco_cord[1]>185: 
            print("dol")
            wpose.position.z = wpose.position.z - 0.01
            update_arm(wpose)
        elif aruco_cord[0]<345:
            print("lewo")
            wpose.position.y = wpose.position.y + 0.01
            update_arm(wpose)
        elif aruco_cord[0]>375:
            print("prawo")
            wpose.position.y = wpose.position.y - 0.01
            update_arm(wpose)

    # group.set_pose_target(wpose)
    # plan = group.go(wait=False)
    # group.stop()

def update_arm(wpose):
    group.set_pose_target(wpose)
    plan = group.go(wait=False)
    group.stop()

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
    if aruco_cords[0]!=0: 
        print(aruco_cords)
        move(aruco_cords)
    #rospy.signal_shutdown("end") 
    
    
def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("/fiducial_vertices", FiducialArray, callback)
    rospy.spin()

if __name__ == '__main__':
    starting_point()
    listener()







# print(wpose)

# pose_goal = geometry_msgs.msg.Pose()
# joint_goal = group.get_current_joint_values()

# # joint_goal[5] = 0#pi/3
# # group.go(joint_goal, wait=False)

# pose_goal.position.x = 0.26
# pose_goal.position.y = -0
# pose_goal.position.z = 1
# pose_goal.orientation.w=0
# group.set_pose_target(pose_goal)
# plan = group.go(wait=True)
# group.stop()
# # joint_goal[5] = -2*pi/3
# # group.go(joint_goal, wait=True)

# group.clear_pose_targets()
# print("Obecna pozycja: ")
# print(wpose)


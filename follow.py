#!/usr/bin/env python
import rospy
from fiducial_msgs.msg import FiducialArray
from fiducial_msgs.msg import FiducialTransformArray
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

moveit_commander.roscpp_initialize(sys.argv)
robot = moveit_commander.RobotCommander()
scene = moveit_commander.PlanningSceneInterface()
group_name = "right_arm"
group = moveit_commander.MoveGroupCommander(group_name)
display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path',
                                               moveit_msgs.msg.DisplayTrajectory,
                                               queue_size=20)
flagStart = True

aruco_area = 0.0

pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)



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
    elif aruco_area < 6000:# l_border>aruco_cords[0]>r_border:
        print('go')
        linear = Vector3(0.2,0,0)
    else:
        linear = Vector3(0,0,0)

    hello = Twist(linear, angular)
    pub.publish(hello)
    return 0

def move(aruco_cord):
    wpose = group.get_current_pose().pose
    if aruco_cord[0]!=0:
        print(aruco_cord)
        if aruco_cord[1]< 160:
            print("góra")
            wpose.position.z = wpose.position.z + 0.01
        elif aruco_cord[1]>185: 
            print("dol")
            wpose.position.z = wpose.position.z - 0.01

        if aruco_cord[0]<345:
            print("lewo")
            wpose.position.y = wpose.position.y + 0.01
        elif aruco_cord[0]>375:
            print("prawo")
            wpose.position.y = wpose.position.y - 0.01

        print("globalnie:")
        print(aruco_area)
        if aruco_area < 6000.0:
            wpose.position.x = wpose.position.x + 0.01
            print("do przodu")

   # print(wpose)
    rospy.sleep(0.1)
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

        

def getAreaOfAruco(data: FiducialTransformArray):
    try:
        stringData = str(data.transforms)
        stringData = stringData.splitlines()
        for line in stringData:
            if("fiducial_area" in line):
                areaLine = line
                break
            
        #print(areaLine)
        area = float(areaLine[15:len(areaLine)-1])
        print("lokalnie")
        print(area)
        global aruco_area
        aruco_area = area
    except:
        aruco_area = 6500
        
        


def callback(data):
    
    aruco_cords = convert_data(data)
   
    print(aruco_cords)
    if aruco_area < 6500 or aruco_cords[0] == 0:
        goto(aruco_cords)
    else:
        move(aruco_cords)
    #rospy.signal_shutdown("end") 
    
    
def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("/fiducial_vertices", FiducialArray, callback)
    rospy.Subscriber("/fiducial_transforms", FiducialTransformArray, getAreaOfAruco)
    rospy.spin()

if __name__ == '__main__':

    listener()


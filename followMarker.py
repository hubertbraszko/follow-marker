#!/usr/bin/env python
from aruco_follow import update_arm
from moveit_commander import robot
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
from geometry_msgs.msg import Twist, Vector3, Transform, Quaternion




class Aruco_marker:
    def __init__(self) -> None:
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.area = 0.0
        self.transform = Transform()
        

    def getPosition(self):
        return [self.x, self.y]

    def isSeen(self) -> bool:
        if self.x == 0.0 and self.y == 0.0:
            return False
        return True
    
    def isInRange(self) -> bool:
        return self.area > 6000


class Following_node:
    def __init__(self) -> None:
        rospy.init_node('follow_marker')
        moveit_commander.roscpp_initialize(sys.argv)
        self.robot = moveit_commander.RobotCommander()
        self.scene = moveit_commander.PlanningSceneInterface()
        self.group_name = "right_arm"
        self.group = moveit_commander.MoveGroupCommander(self.group_name)
        self.display_trajectory_pub = rospy.Publisher('/move_group/display_planned_path',
                                               moveit_msgs.msg.DisplayTrajectory,
                                               queue_size=20)
        
        self.base_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        self.linear = Vector3(0,0,0)
        self.angular = Vector3(0,0,0)
        self.right_border = 373
        self.left_border = 313
        self.aruco = Aruco_marker()
        self.pose = self.group.get_current_pose().pose
        
        rospy.Subscriber("/fiducial_vertices", FiducialArray, self.update_aruco_pos)
        rospy.Subscriber("/fiducial_transforms", FiducialTransformArray, self.get_arucos_rotation)
        
        
    def get_to_start_point(self) -> None:
        joint_goal = self.group.get_current_joint_values()
        start_joint_state = [3.3, -2.0, -1.7, 0.6, 1.6, 0.7]

        for a in range(len(joint_goal)):
            joint_goal[a]=start_joint_state[a]

        self.group.go(joint_goal, wait=True)

        self.group.stop()


    def update_aruco_pos(self, data) -> None:
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

            self.aruco.x = pos[0]
            self.aruco.y = pos[1]
            #return pos #lista 2 floatów z pozycją
        except:
            self.aruco.x = 0.0
            self.aruco.y = 0.0
           
    def get_arucos_translation(self, data: FiducialTransformArray) -> Vector3:
        #print(data.transforms)
        translation: Vector3 = Vector3(0,0,0)
        try:
            stringData = str(data.transforms)
            stringData = stringData.splitlines()
            #print(stringData[3])
            #print(stringData[4])
            xData:String = stringData[3]
            yData:String = stringData[4]
            zData:String = stringData[5]
            #print(xData.strip()[3:])
            translation.x = float(xData.strip()[3:])
            translation.y = float(yData.strip()[3:])
            translation.z = float(zData.strip()[3:])
            #print(translation)
        except Exception as e:
            print("error calculating translation: " + e)
        return translation
    
    def get_arucos_rotation(self,data: FiducialTransformArray) -> Quaternion:
        rotation: Quaternion = Quaternion(0,0,0,0)
        try:
            stringData = str(data.transforms)
            stringData = stringData.splitlines()
            #print(stringData[3])
            #print(stringData[4])
            xData:String = stringData[7]
            yData:String = stringData[8]
            zData:String = stringData[9]
            wData:String = stringData[10]
            rotation.x = float(xData.strip()[3:])
            rotation.y = float(yData.strip()[3:])
            rotation.z = float(zData.strip()[3:])
            rotation.w = float(wData.strip()[3:])
            print(rotation)
        except Exception as e:
            print("error calculating rotation: " + e)
        return rotation   



    def get_aruco_area(self, data: FiducialTransformArray) -> float:
        area: float = 0
        try:
            stringData = str(data.transforms)
            stringData = stringData.splitlines()
            for line in stringData:
                if("fiducial_area" in line):
                    areaLine = line
                    break    
            area = float(areaLine[15:len(areaLine)-1])
            return area
        except Exception as e:
            return 0.0
            print("error calculating area: " + e)
          

    def update_aruco_data(self, data: FiducialTransformArray) -> None:
        self.aruco.area = self.get_aruco_area(data)
        self.aruco.transform.translation = self.get_arucos_translation(data)
        self.aruco.transform.rotation = self.get_arucos_rotation(data)

    def update_arm(self) -> None:
        self.group.set_pose_target(self.pose)
        self.plan = self.group.go(wait=False)
        self.group.stop()

    def move_arm(self) -> None:
        #wpose = group.get_current_pose().pose
        rospy.sleep(0.1)
        if self.aruco.isSeen():

            print("Current Aruco Postion: ")
            print(self.aruco.getPosition())
            print("\n")
            self.pose = self.group.get_current_pose().pose
            if self.aruco.y< 160:
                print("GOING UP \n")
                self.pose.position.z += 0.01
                self.update_arm()

            elif self.aruco.y>185: 
                print("GOING DOWN \n")
                self.pose.position.z -= 0.01
                self.update_arm()

            if self.aruco.x<345:
                print("GOING LEFT \n")
                self.pose.position.y += 0.01
                self.update_arm()
                
            elif self.aruco.x>375:
                print("GOING RIGHT \n")
                self.pose.position.y -= 0.01
                self.update_arm()

            # print("globalnie:")
            # print(self.aruco.area)
            # print("\n")

            # if self.aruco.area < 6000.0:
            #     if(self.pose.position.x < 0.49):
            #         self.pose.position.x += 0.01
            #         print("GOING FORWARD \n")
            #     print("Current x pose pos: ")
            #     print(self.pose.position.x)
            #     print("GOING FORWARD \n")





    def update_base(self) -> None:
        msg = Twist(self.linear, self.angular)
        self.base_publisher.publish(msg)

    def turn_around(self) -> None:

        self.angular.z = -0.05

        self.update_base()
   


    def stop_moving(self) -> None:
        self.linear.x = 0
        self.angular.z = 0

        self.update_base()

    def go_forward(self) -> None:
        
        self.linear.x = 0.2

        self.update_base()

    def find_aruco(self) -> None:

        if not self.aruco.isSeen():
            self.turn_around()
        else:
            self.stop_moving()

    


if __name__ == '__main__':

    node = Following_node()

    while not rospy.is_shutdown():
        if node.aruco.isSeen():
            pass
        #node.move_arm()
        # node.get_to_start_point()
        # rospy.Rate(10)
        # if not node.aruco.isSeen():
        #     node.find_aruco()
        # elif not node.aruco.isInRange():
        # #   node.move_arm()
        #     print("going forward")
        #     node.go_forward()
        # else:
        #     node.stop_moving()
       #node.stop_moving()

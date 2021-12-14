#!/usr/bin/env python

import rospy
import numpy as np
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped

def move_to_pose(pose2):
    path = Path()


    pose = PoseStamped()
    pose.pose.orientation.w = 2.0
    pose.pose.orientation.x = 0.0
    pose.pose.orientation.y = 0.0
    pose.pose.orientation.z = 0.0
    pose.pose.position.x = 0.0
    pose.pose.position.y = 0.0
    pose.pose.position.z = 0.0
    path.poses.append(pose)
    path.poses.append(pose2)
    
    rospy.sleep(0.5)
    pub.publish(path)
    rospy.sleep(0.5)



if __name__ == '__main__':

    rospy.init_node('move_to_pose2')
    rospy.Subscriber('/controller_ur/move_to_pose', PoseStamped, move_to_pose)
    pub = rospy.Publisher('/trajectory_planned', Path, queue_size=1)


    rospy.spin()
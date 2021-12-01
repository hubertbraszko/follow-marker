#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import sys
import cv2
from cv_bridge import CvBridge
from sensor_msgs.msg import Image

def process_image(msg):
    bridge = CvBridge()
    img = bridge.imgmsg_to_cv2(msg, "bgr8")
    cv2.imshow("image",img)
    cv2.waitKey(50)

if __name__ == '__main__':
    while not rospy.is_shutdown():
        rospy.init_node('kinect_subscriber')
        rospy.loginfo('image_sub node started')
        rospy.Subscriber("/base_kinect/color/image_raw", Image, process_image)

        rospy.spin()

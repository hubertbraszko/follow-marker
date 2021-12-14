#!/usr/bin/env python
# license removed for brevity
from genpy import message
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist, Vector3

def talker():
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    rospy.init_node('talker', anonymous=True) #to do usuniecie w momencie mergu z subskryberem wizji
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        linear = Vector3(0,0,0)
        angular = Vector3(0,0,0)
        hello = Twist(linear, angular)
        rospy.loginfo(hello)
        pub.publish(hello)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
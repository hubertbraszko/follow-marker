#!/usr/bin/env python
import rospy
from geometry_msgs.msg import PoseWithCovarianceStamped 

      
    

def convert_data(data):
    #ten kod bedzie do poprawy xdxd
    data = str(data)
    data = data.split('\n')
    poses = []
    for a in data:
            if a.find("x:")!= -1 or a.find("y:")!= -1 or a.find("z:")!= -1 or a.find("w:")!= -1:
                tmp = a[a.find(": ")+2:]
                tmp = tmp[:tmp.find('.')+4]
                poses.append(float(tmp))
    return poses
    
def callback(data):
    print(convert_data(data))
    rospy.signal_shutdown("end") 
    
     
def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("/fiducial_pose", PoseWithCovarianceStamped, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()

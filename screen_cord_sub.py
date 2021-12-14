#!/usr/bin/env python
import rospy
from fiducial_msgs.msg import FiducialArray
from std_msgs.msg import String




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
    print(convert_data(data))
    #rospy.signal_shutdown("end") #żeby nie mnożyć nodów
    
    
def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber("/fiducial_vertices", FiducialArray, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()

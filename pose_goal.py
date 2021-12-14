import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
from math import pi
from std_msgs.msg import String
from moveit_commander.conversions import pose_to_list

def starting_point():
    joint_goal = group.get_current_joint_values()
    start_joint_state = [2.652393622875633, -1.2463236081522506, -2.5898667688541863, 0.7183400230211117, 1.9863549048701117, 0.7581805663393064]

    for a in range(len(joint_goal)):
        joint_goal[a]=start_joint_state[a]

    group.go(joint_goal, wait=True)

    group.stop()

def move():
    wpose = group.get_current_pose().pose
    wpose.position.x = wpose.position.x + 0.1
    #wpose.position.y = wpose.position.y - 0.01
    # wpose.orientation.y = wpose.orientation.y + 0.15

    group.set_pose_target(wpose)
    plan = group.go(wait=True)
    group.stop()

moveit_commander.roscpp_initialize(sys.argv)
rospy.init_node('move_group_python_interface_tutorial',
                anonymous=True)

robot = moveit_commander.RobotCommander()
scene = moveit_commander.PlanningSceneInterface()
group_name = "right_arm"
group = moveit_commander.MoveGroupCommander(group_name)
display_trajectory_publisher = rospy.Publisher('/move_group/display_planned_path',
                                               moveit_msgs.msg.DisplayTrajectory,
                                               queue_size=20)


joint_goal = group.get_current_joint_values()
print(joint_goal)

#print(wpose)

#starting_point()
#move()

# wpose = group.get_current_pose().pose
#  pose.position.x = wpose.position.x  0.35
#wpose.position.y = wpose.position.y - 0.1
# wpose.orientation.y = wpose.orientation.y + 0.15

# group.set_pose_target(wpose)
# plan = group.go(wait=True)
# group.stop()
# joint_goal[5] = -2*pi/3
# group.go(joint_goal, wait=True)

group.clear_pose_targets()


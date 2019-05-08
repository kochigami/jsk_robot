#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''
node to wait until Pepper takes wakeup pose
If Pepper hasn't take wakeup pose yet, all jsk_pepper_startup.launch fails.
'''

import rospy
from std_srvs.srv import Trigger
from subprocess import *

def is_robot_wakeup():
    rospy.wait_for_service('/pepper_robot/pose/is_robot_wakeup')
    is_robot_wakeup_proxy = rospy.ServiceProxy('/pepper_robot/pose/is_robot_wakeup', Trigger)
    res = is_robot_wakeup_proxy()
    return res.success

def main():
    print is_robot_wakeup()
    # if is_robot_wakeup() is False, jsk_pepper_startup.launch will be killed
    # '/pepper_robot/pose/pose_controller' is required in jsk_pepper_startup.launch
    if not is_robot_wakeup():
        call(['rosnode', 'kill', '/pepper_robot/pose/pose_controller'])

if __name__=="__main__":
    rospy.init_node("is_robot_wakeup")
    main()
    

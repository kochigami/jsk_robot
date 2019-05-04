#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''
test
'''

import rospy
from std_msgs.msg import String

def test():
    default_ip = rospy.get_param("~ip", "127.0.0.1")
    pub = rospy.Publisher('chatter', String, queue_size=10)
    r = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        rospy.loginfo(default_ip)
        pub.publish(str(default_ip))
        r.sleep()
    
if __name__=="__main__":
    rospy.init_node("test")
    test()
    rospy.spin()

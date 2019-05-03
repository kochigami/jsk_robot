#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''
test
'''

import rospy

def test():
    print "test"
    
if __name__=="__main__":
    rospy.init_node("test")
    nao_ip = rospy.get_param('~nao_ip', "777")
    print nao_ip
    test()
    rospy.spin()

#! /usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from subprocess import *
from speech_recognition_msgs.srv import (
    SpeechRecognition,
    SpeechRecognitionRequest)

def start_speech_recognition_service(req):
    rospy.wait_for_service('speech_recognition')
    speech_recognition_proxy = rospy.ServiceProxy('speech_recognition', SpeechRecognition)
    res = speech_recognition_proxy(req)
    return res

def detect_calling():
    req = SpeechRecognitionRequest()
    robot_name = rospy.get_param("~robot_name", None)
    req.vocabulary.words.append("pepper")
    if robot_name:
        req.vocabulary.words.append(robot_name)
    req.duration = 10
    req.threshold = 0.3
    res = start_speech_recognition_service(req)
    if res.result.transcript is not None:
        return res.result.transcript
    else:
        return None
    
def start_speech_recognition():
    # TODO: if some signal detected
    if True:
        ans = detect_calling()
        print ans # []
        if ans and len(ans) > 0:
            print ans 
            print "someone is calling"
            # TODO: add more speech recognition
        
if __name__ == "__main__":
    rospy.init_node("start_speech_recognition")
    start_speech_recognition()
    #rospy.spin()
    exit(0)

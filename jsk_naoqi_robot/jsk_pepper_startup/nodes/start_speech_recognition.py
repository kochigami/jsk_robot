#! /usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from subprocess import *
from speech_recognition_msgs.srv import (
    SpeechRecognition,
    SpeechRecognitionRequest)
from std_msgs.msg import Bool

class StartSpeechRecognition():
    def __init__(self):
        # sub
        self.sub = rospy.Subscriber("speech_detection", Bool, self.detect_calling)
        
    def detect_calling(self, msg):
        #self.speech_detected = msg.data
        if msg.data:
            req = SpeechRecognitionRequest()
            req.vocabulary.words.append("おはよう")
            req.vocabulary.words.append("おやすみ")
            req.vocabulary.words.append("紹介して")
            req.vocabulary.words.append("ハンコ押して")
            req.vocabulary.words.append("配って")
            req.vocabulary.words.append("代わって")
            req.vocabulary.words.append("移動して")
            req.duration = 10 # change to 5?
            req.threshold = 0.3
            res = start_speech_recognition_service(req)
            if res.result.transcript is not None:
                return res.result.transcript
            else:
                return None
        
    def start_speech_recognition_service(self, req):
        rospy.wait_for_service('speech_recognition')
        speech_recognition_proxy = rospy.ServiceProxy('speech_recognition', SpeechRecognition)
        res = speech_recognition_proxy(req)
        return res
        
if __name__ == "__main__":
    rospy.init_node("start_speech_recognition")
    rospy.spin()
    exit(0)

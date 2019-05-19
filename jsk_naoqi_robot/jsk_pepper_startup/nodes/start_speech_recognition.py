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
        self.sub = rospy.Subscriber("/speech_recognition_start_signal", Bool, self.detect_calling)

    def detect_calling(self, msg):
        if msg.data:
            req = SpeechRecognitionRequest()
            req.vocabulary.words.append("おはよう")
            req.vocabulary.words.append("おやすみ")
            req.vocabulary.words.append("紹介して")
            req.vocabulary.words.append("ハンコ押して")
            req.vocabulary.words.append("配って")
            req.vocabulary.words.append("代わって")
            req.vocabulary.words.append("移動して")
            req.duration = 5
            req.threshold = 0.3
            res = self.start_speech_recognition_service(req)
            if res.result.transcript is not None and len(res.result.transcript) > 0:
                if res.result.transcript[0] == "おはよう":
                    self.good_morning()
                elif res.result.transcript[0] == "おやすみ":
                    self.good_night()
                elif res.result.transcript[0] == "紹介して":
                    # TODO: select language
                    self.miraikan_introduction()
            else:
                return None

    def start_speech_recognition_service(self, req):
        rospy.wait_for_service('speech_recognition')
        speech_recognition_proxy = rospy.ServiceProxy('speech_recognition', SpeechRecognition)
        res = speech_recognition_proxy(req)
        return res

    def get_package_path(self):
        rospack = rospkg.RosPack()
        path_to_pkg = rospack.get_path('miraikan_live')
        return path_to_pkg
        
    def good_morning(self):
        file_path = path_to_pkg + '/scripts/actions/' + 'good_morning.sh'
        call(['bash', file_path])
        return True

    def good_night(self):
        file_path = path_to_pkg + '/scripts/actions/' + 'good_night.sh'
        call(['bash', file_path])
        return True
        
    def miraikan_introduction(self):
        file_path = path_to_pkg + '/scripts/actions/' + 'miraikan_introduction.sh'
        call(['bash', file_path])
        return True
        
if __name__ == "__main__":
    rospy.init_node("start_speech_recognition")
    start_speech_recognition = StartSpeechRecognition()
    rospy.spin()
    exit(0)

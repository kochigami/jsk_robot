#! /usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from jsk_topic_tools import ConnectionBasedTransport
from speech_recognition_msgs.srv import (
    SpeechRecognition,
    SpeechRecognitionRequest)
from std_msgs.msg import (
    Bool,
    String)

class StartSpeechRecognition(ConnectionBasedTransport):
    def __init__(self):
        super(StartSpeechRecognition, self).__init__()

    def subscribe(self):
        self.sub = rospy.Subscriber("/speech_recognition_start_signal", Bool, self.detect_calling)
        # pub
        self.pub = rospy.Publisher("/speech", String, queue_size=1)

    def unsubscribe(self):
        self.sub.unregister()

    def detect_calling(self, msg):
        if msg.data:
            self.unsubscribe()
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
            '''
            [ERROR] [1558169595.278265]: bad callback: <bound method StartSpeechRecognition.detect_calling of <__main__.StartSpeechRecognition instance at 0x7fb514f3b5f0>>
            Traceback (most recent call last):
            File "/opt/ros/kinetic/lib/python2.7/dist-packages/rospy/topics.py", line 750, in _invoke_callback
    cb(msg)
            File "/home/kanae/catkin_ws/src/jsk_robot/jsk_naoqi_robot/jsk_pepper_startup/nodes/start_speech_recognition.py", line 41, in detect_calling
            if res.result.transcript[0] == 'ohayo':
            IndexError: list index out of range => len(res.result.transcript) > 0:
            '''
            if res.result.transcript is not None and len(res.result.transcript) > 0:
                if res.result.transcript[0] == "おはよう":
                    msg = String()
                    msg.data = "\\vct=120\\おはよう\\pau=1000\\オッケー，グーグル，未来館の電気をつけて"
                    self.pub.publish(msg)
                if res.result.transcript[0] == "おやすみ":
                    msg = String()
                    msg.data = "\\vct=120\\おやすみ\\pau=1000\\オッケー，グーグル，未来館の電気を消して"
                    self.pub.publish(msg)
            else:
                return None
            self.subscribe()

    def start_speech_recognition_service(self, req):
        rospy.wait_for_service('speech_recognition')
        speech_recognition_proxy = rospy.ServiceProxy('speech_recognition', SpeechRecognition)
        res = speech_recognition_proxy(req)
        return res
        
if __name__ == "__main__":
    rospy.init_node("start_speech_recognition")
    start_speech_recognition = StartSpeechRecognition()
    rospy.spin()
    exit(0)

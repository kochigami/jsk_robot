#! /usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from speech_recognition_msgs.srv import (
    SpeechRecognition,
    SpeechRecognitionRequest)
from std_msgs.msg import (
    Bool,
    String)

class StartSpeechRecognition():
    def __init__(self):
        # sub
        self.sub = rospy.Subscriber("/speech_recognition_start_signal", Bool, self.detect_calling)
        # pub
        self.pub = rospy.Publisher("/speech", String, queue_size=1)
        # param
        self.room = rospy.get_param("~room", "未来館")

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
                    msg = String()
                    msg.data = "\\vct=120\\おはようッ\\pau=2000\\オッケー\\pau=500\\グーグル\\pau=500\\" + self.room + "の電気をつけて"
                    self.pub.publish(msg)
                elif res.result.transcript[0] == "おやすみ":
                    msg = String()
                    msg.data = "\\vct=120\\おやすみッ\\pau=2000\\オッケー\\pau=500\\グーグル\\pau=500\\" + self.room +"の電気を消して"
                    self.pub.publish(msg)
                elif res.result.transcript[0] == "紹介して":
                    # select language
                    # tablet.launch
                    # speech.launch
                    # main.l
                    pass
            else:
                return None

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

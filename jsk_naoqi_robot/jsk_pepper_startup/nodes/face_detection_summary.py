#! /usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from jsk_topic_tools import ConnectionBasedTransport
from opencv_apps.msg import FaceArrayStamped
from std_msgs.msg import Bool

class FaceDetectionSummary(ConnectionBasedTransport):
    def __init__(self):
        self.pub = rospy.Publisher("/speech_recognition_start_signal", Bool, queue_size=1)

        self.size = rospy.get_param("~size", 70)
        self.count_limit = rospy.get_param("~count_limit", 10)
        self.time_limit = rospy.get_param("~time_limit", 7)

        self.time = rospy.Time.now()
        self.count = 0

    def subscribe(self):
        self.sub = rospy.Subscriber("/face_detection/faces", FaceArrayStamped, self.detect_calling)

    def unsubscribe(self):
        self.sub.unregister()

    def detect_calling(self, msg):
        if len(msg.faces) > 0:
            faces = msg.faces
            face = faces[0]
            if face.face.width > self.size and face.face.height > self.size:
                if self.count == 0:
                    self.time = rospy.Time.now()
                    self.count += 1
                else:
                    now = rospy.Time.now()
                    if self.count < self.count_limit and (rospy.Time.now() - self.time).secs < self.time_limit:
                        self.count += 1
                    elif (self.count > self.count_limit or self.count == self.count_limit) and (rospy.Time.now() - self.time).secs < self.time_limit:
                        msg = Bool()
                        msg.data = True
                        self.pub.publish(msg)
                        self.count = 0
                    else:
                        self.count = 0
                        
if __name__ == "__main__":
    rospy.init_node("face_detection_summary")
    face_detection_summary = FaceDetectionSummary()
    rospy.spin()
    exit(0)

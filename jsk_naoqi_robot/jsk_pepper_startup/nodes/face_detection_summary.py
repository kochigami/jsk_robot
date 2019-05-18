#! /usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from opencv_apps.msg import FaceArrayStamped
from std_msgs.msg import Bool

class FaceDetectionSummary():
    def __init__(self):
        # sub
        self.sub = rospy.Subscriber("/face_detection/faces", FaceArrayStamped, self.detect_calling)
        # pub
        self.pub = rospy.Publisher("/speech_recognition_start_signal", Bool, queue_size=1)

        self.time = rospy.Time.now()
        self.count = 0

    def detect_calling(self, msg):
        if len(msg.faces) > 0:
            faces = msg.faces
            face = faces[0]
            if face.face.width > 70 and face.face.height > 70:
                if self.count == 0:
                    self.time = rospy.Time.now()
                    self.count += 1
                else:
                    now = rospy.Time.now()
                    if self.count < 10 and (rospy.Time.now() - self.time).secs < 7:
                        self.count += 1
                    elif (self.count > 10 or self.count == 10) and (rospy.Time.now() - self.time).secs < 7:
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

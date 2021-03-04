#!/usr/bin/env python

import rospy
# import json
import tf
import tf_conversions
import yaml
import json
import math
import tf2_ros
import geometry_msgs.msg
import numpy
import rospkg
from std_msgs.msg import String,Float32,Float32MultiArray,MultiArrayLayout,MultiArrayDimension
from apriltag_ros.msg import AprilTagDetectionArray

rospy.init_node('AprilListener', anonymous = True)
listen = tf.TransformListener()

filename = "latest_output_file.yaml"
filepath = rospkg.RosPack().get_path('hk_ros_2021') + '/exported_detection_logs/'
#detections = []
taglist= [None] * 10

def Aprildetections(msg):

    rate = rospy.Rate(10.0)
    alltags = ["tag_9","tag_8","tag_7","tag_6","tag_5","tag_4","tag_3","tag_2", "tag_1", "tag_0"]

        #with open(filepath + filename, 'w') as outfile:
    while not rospy.is_shutdown():

        for tagID in alltags:
            coordinates = tagTransform(tagID)
            IDnum = int(remove_prefix(tagID, "tag_"))
            #print(IDnum)

            if coordinates is not None:

                strang = "XY_pos: " + str(coordinates) + ", obj_type: A"

                taglist[IDnum] = strang

                print(taglist)

        rate.sleep()
        #rospy.spin()

def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text

def tagTransform(tagId):
    try:
        #listen.waitForTransform('/static_frame', tagId, rospy.Time(), rospy.Duration(1))
        (coords,rotation) = listen.lookupTransform('/static_frame', tagId, rospy.Time(0))

    except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
        return None

    (x, y, z) = coords

    return (x, y)

#         detections.append({"obj_type": "A", "XY_pos" : x['coords'], "name" : x['name']})

if __name__ == '__main__':

    rospy.Subscriber('/tag_detections', AprilTagDetectionArray, Aprildetections)


    rospy.spin()

    with open(filepath + filename, 'w') as outfile:
        yaml.dump(taglist, outfile, explicit_start=True)

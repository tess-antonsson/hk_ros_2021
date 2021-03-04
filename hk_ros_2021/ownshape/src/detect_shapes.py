#! /usr/bin/env python
import rospy
from pyimagesearch.shapedetector import ShapeDetector
import argparse
import imutils
import cv2
import geometry_msgs.msg
from std_msgs.msg import String, Float32,Float32MultiArray,MultiArrayLayout,MultiArrayDimension
from sensor_msgs.msg import Image, CameraInfo
from cv_bridge import CvBridge
import numpy as np
import turtlesim.msg

def callback(image):
	# construct the argument parse and parse the arguments
	#ap = argparse.ArgumentParser()
	#ap.add_argument("-i", "--image", required=True,
					#help="path to the input image")
	#args = vars(ap.parse_args())
	# load the image and resize it to a smaller factor so that
	# the shapes can be approximated better
	#image = cv2.imread("image")
	pub = rospy.Publisher('/shape_coordinates', turtlesim.msg.Pose, queue_size=10)
	pub1 = rospy.Publisher('/shape_names', String, queue_size=10)
	bridge=CvBridge()
	image = bridge.imgmsg_to_cv2(image, desired_encoding='passthrough')
	hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
	lower_green = np.array([25, 35,23])
	upper_green= np.array([160, 130, 160])
	mask = cv2.inRange(hsv, lower_green, upper_green)
        mask=cv2.bitwise_not(mask)
	result = cv2.bitwise_and(image, image, mask=mask)
	image=result
	resized = imutils.resize(image, width=300)
	ratio = image.shape[0] / float(resized.shape[0])
	# convert the resized image to grayscale, blur it slightly,
	# and threshold it
	gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

	blurred = cv2.GaussianBlur(gray, (5, 5), 0)
	thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY_INV)[1]
	#cv2.imshow("Image",thresh)
	# find contours in the thresholded image and initialize the
	# shape detector
	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
							cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	sd = ShapeDetector()
	i = 0

	# loop over the contours
	for c in cnts:
		# compute the center of the contour, then detect the name of the
		# shape using only the contour
		i = i + 1
		M = cv2.moments(c)
		cX = int((M["m10"] / (M["m00"]+1e-7)) * ratio)
		cY = int((M["m01"] / (M["m00"]+1e-7)) * ratio)
		shape = sd.detect(c)
		if shape == "triangle" or shape == "pentagon" or shape== "square":
			print("shape=%s" % (shape))
			# multiply the contour (x, y)-coordinates by the resize ratio,
			# then draw the contours and the name of the shape on the image
			c = c.astype("float")
			c *= ratio
			c = c.astype("int")
			cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
			cv2.putText(image, shape, (cX, cY), cv2.FONT_HERSHEY_SIMPLEX,
						0.5, (255, 255, 255), 2)
			coor=turtlesim.msg.Pose()
			coor.x=cX
			coor.y=cY
			pub.publish(coor)
			pub1.publish(shape)


	cv2.imshow("Image", image)
	cv2.waitKey(10)



		# show the output image




def detect_shapes():
	rospy.init_node('detect_shapes', anonymous=True)
	rospy.Subscriber("/raspicam_node/image", Image, callback)






if __name__ == '__main__':
    detect_shapes()
    rospy.spin()


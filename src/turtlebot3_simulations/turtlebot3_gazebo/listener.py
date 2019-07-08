#!/usr/bin/env python
import rospy
import math
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from tf.transformations import euler_from_quaternion, quaternion_from_euler
from numpy.random import choice

tb3_0_x = 0
tb3_0_y = 0
tb3_1_x = 0
tb3_1_y = 0


def turtlebot3_odom(message, args):
	global tb3_0_x
	global tb3_0_y
	global tb3_1_x
	global tb3_1_y
	if (args == 0):
	    #get_caller_id(): Get fully resolved name of local node
		if (choice([0,1], 1, [1.0, 0.0]) == 0):
			tb3_0_x = message.pose.pose.position.x
			tb3_0_y = message.pose.pose.position.y
		rospy.loginfo("TB3_0 Pose x: %.2f", tb3_0_x)
		rospy.loginfo("TB3_0 Pose y: %.2f", tb3_0_y)
	elif (args == 1):
		tb3_1_x = message.pose.pose.position.x
		tb3_1_y = message.pose.pose.position.y
		#get_caller_id(): Get fully resolved name of local node
		rospy.loginfo("TB3_1 Pose x: %.2f", tb3_1_x)
		rospy.loginfo("TB3_1 Pose y: %.2f", tb3_1_y)
		# diff vector
		x = tb3_0_x - tb3_1_x
		y = tb3_0_y - tb3_1_y
		targetAngle = math.atan2(y, x)
		rospy.loginfo("TB3_vx : %.2f", x)
		rospy.loginfo("TB3_vy : %.2f", y)
		rospy.loginfo("TB3_targetAngle : %.2f", targetAngle)

		tb3_1_yaw = round(get_rotation(message), 2)
		rospy.loginfo("TB3_orientation : %f", tb3_1_yaw)

		distance = math.sqrt(math.pow(tb3_0_y - tb3_1_y, 2) + math.pow(tb3_0_x - tb3_1_x, 2))
		rospy.loginfo("TB3_distance : %.2f", distance)

		if (targetAngle < (tb3_1_yaw - 0.1) or targetAngle > (tb3_1_yaw + 0.1)):

			if (distance > 0.5):
				if (rotation_side (targetAngle, tb3_1_yaw) == 1):
					twist = Twist()
					twist.linear.x = 0.0; twist.linear.y = 0.0; twist.linear.z = 0.0
					twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = -0.8
					pub.publish(twist)
				else: 
					twist = Twist()
					twist.linear.x = 0.0; twist.linear.y = 0.0; twist.linear.z = 0.0
					twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = 0.8
					pub.publish(twist)
			else:
				twist = Twist()
				twist.linear.x = 0.22; twist.linear.y = 0.0; twist.linear.z = 0.0
				twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = 0.0
				pub.publish(twist)

		else:
			twist = Twist()
			twist.linear.x = 0.22; twist.linear.y = 0.0; twist.linear.z = 0.0
			twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = 0.0
			pub.publish(twist)


def get_rotation (msg):
    global roll, pitch, yaw
    orientation_q = msg.pose.pose.orientation
    orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
    (roll, pitch, yaw) = euler_from_quaternion (orientation_list)
    return yaw


def rotation_side (target, given):
	
	tx = math.cos(target)
	ty = math.sin(target)

	gx = math.cos(given)
	gy = math.sin(given)

	crossProd = (tx * gy) - (ty * gx)

	if (crossProd > 0):
		return 1
	return 0


def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # node are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('poseListenerTB', anonymous=True)

    rospy.Subscriber("/tb3_0/odom", Odometry, turtlebot3_odom, 0)
    rospy.Subscriber("/tb3_1/odom", Odometry, turtlebot3_odom, 1)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
	pub = rospy.Publisher('/tb3_1/cmd_vel', Twist, queue_size=10)
	listener()


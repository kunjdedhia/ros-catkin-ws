#!/usr/bin/env python
import rospy
import math
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from tf.transformations import euler_from_quaternion, quaternion_from_euler

tb3_0_scan_0 = 0.0
tb3_0_scan_45 = 0.0
tb3_0_scan_315 = 0.0
tb3_0_angle = 0.0
tb3_1_angle = 0.0

def turtlebot3_scan(message, args):
	global tb3_0_scan_0
	global tb3_0_scan_45
	global tb3_0_scan_315
	global tb3_0_angle
	global tb3_1_angle

	if (args == 0):
		tb3_0_scan_0 = message.ranges[0]
		tb3_0_scan_45 = message.ranges[45]
		tb3_0_scan_315 = message.ranges[315]
		
		rospy.loginfo("TB3_0 Scan 0: %.2f", tb3_0_scan_0)
		rospy.loginfo("TB3_0 Scan 45: %.2f", tb3_0_scan_45)
		rospy.loginfo("TB3_0 Scan 315: %.2f", tb3_0_scan_315)
		
	elif (args == 1):
		tb3_0_angle = round(get_rotation(message), 2)
		rospy.loginfo("TB3_0 Angle: %.2f", tb3_0_angle)

	elif (args == 2):
		tb3_1_angle = round(get_rotation(message), 2)
		rospy.loginfo("TB3_1 Angle: %.2f", tb3_1_angle)

		if (tb3_0_scan_0 > 0.7 and tb3_0_scan_45 > 0.5 and tb3_0_scan_315 > 0.5):
			twist = Twist()
			twist.linear.x = 0.22; twist.linear.y = 0.0; twist.linear.z = 0.0
			twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = 0.0
			pub.publish(twist)				
		else:
			if (tb3_0_scan_45 < 0.5):
				twist = Twist()
				twist.linear.x = 0.0; twist.linear.y = 0.0; twist.linear.z = 0.0
				twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = -0.8
				pub.publish(twist)
			else:
				twist = Twist()
				twist.linear.x = 0.0; twist.linear.y = 0.0; twist.linear.z = 0.0
				twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = 0.8
				pub.publish(twist)


def rotation_side (target, given):
	
	tx = math.cos(target)
	ty = math.sin(target)

	gx = math.cos(given)
	gy = math.sin(given)

	crossProd = (tx * gy) - (ty * gx)

	if (crossProd > 0):
		return 1
	return 0


def get_rotation (msg):
    global roll, pitch, yaw
    orientation_q = msg.pose.pose.orientation
    orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
    (roll, pitch, yaw) = euler_from_quaternion (orientation_list)
    return yaw


def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # node are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
	rospy.init_node('evaderTB', anonymous=True)
	rospy.Subscriber("/tb3_0/scan", LaserScan, turtlebot3_scan, 0)
	rospy.Subscriber('/tb3_0/odom', Odometry, turtlebot3_scan, 1)
	rospy.Subscriber('/tb3_1/odom', Odometry, turtlebot3_scan, 2)

	rospy.spin()


if __name__ == '__main__':
	pub = rospy.Publisher('/tb3_0/cmd_vel', Twist, queue_size=10)
	listener()


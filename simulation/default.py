#! /usr/bin/env morseexec

""" Basic MORSE simulation scene for <simulation> environment

Feel free to edit this template as you like!
"""

from morse.builder import *

# Add a robot with a position sensor and a motion controller
robot = ATRV()
robot.properties(frequency = 50.0)

robot.translate(17.0, -13.0, 0.0)
robot.rotate(0.0, 0.0, 2.5)


pose = Pose()
pose.add_interface('socket')
pose.properties(frequency = 50.0)
robot.append(pose)

odom = Odometry()
odom.level("differential")
odom.add_interface('socket')
odom.properties(frequency = 50.0)
robot.append(odom)

int_odom = Odometry()
int_odom.add_interface('socket')
int_odom.properties(frequency = 50.0)
robot.append(int_odom)

goal = Waypoint()
goal.add_interface('socket')
goal.properties(ObstacleAvoidance = False)
robot.append(goal)

motion = MotionVW()
motion.add_interface('socket')
robot.append(motion)

# Append a laser scanner
# Sick LMS500, range: 30m, field: 180deg, 90 sample points
laser = Sick()
laser.add_stream('socket')
laser.properties(resolution = 2.0)
laser.properties(scan_window = 180.0)
laser.properties(frequency = 50.0)
robot.append(laser)

# Make it possible to control the robot with the keyboard
keyboard = Keyboard()
robot.append(keyboard)
keyboard.properties(ControlType = 'Position')

# Configure the robot on the 'socket' interface
robot.add_default_interface('socket')

# Environment
env = Environment('/home/julian/PycharmProjects/RobotNavigationWithNengo/simulation/environments/boxes_custom.blend')
env.set_camera_location([30.0,-25.0,30.0])

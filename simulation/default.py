#! /usr/bin/env morseexec

""" Basic MORSE simulation scene for <simulation> environment

Feel free to edit this template as you like!
"""

from morse.builder import *

# Add a robot with a position sensor and a motion controller
robot = ATRV()

pose = Pose()
pose.add_interface('socket')
pose.properties(frequency = 5.0)
robot.append(pose)

odom = Odometry()
odom.level("differential")
odom.add_interface('socket')
odom.properties(frequency = 5.0)
robot.append(odom)

int_odom = Odometry()
int_odom.add_interface('socket')
int_odom.properties(frequency = 5.0)
robot.append(int_odom)

motion = Waypoint()
motion.add_interface('socket')
robot.append(motion)

# Append a laser scanner
# Sick LMS500, range: 30m, field: 180deg, 180 sample points
laser = Sick()
laser.add_stream('socket')
laser.properties(resolution = 3.0)
laser.properties(frequency = 5.0)
robot.append(laser)

# Make it possible to control the robot with the keyboard
#keyboard = Keyboard()
#robot.append(keyboard)
#keyboard.properties(ControlType = 'Position')

# Configure the robot on the 'socket' interface
robot.add_default_interface('socket')

# Environment
env = Environment('/home/julian/PycharmProjects/RobotNavigationWithNengo/simulation/environments/land_empty.blend')

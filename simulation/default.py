__author__ = "Julian Petruck"

#! /usr/bin/env morseexec

""" Basic MORSE simulation scene for <simulation> environment

Feel free to edit this template as you like!
"""

from morse.builder import *

# Adds a robot and sets its starting position
robot = ATRV()
robot.properties(GroundRobot = True)
robot.translate(29.0, 0.0, 0.0)
robot.rotate(0.0, 0.0, 3.1)

# Adds a pose sensor to the robot
pose = Pose()
pose.add_interface('socket')
pose.properties(frequency = 50.0)
robot.append(pose)

# Adds a odometry sensor to the robot
odom = Odometry()
odom.add_interface('socket')
odom.properties(frequency = 50.0)
robot.append(odom)

# Adds a laser scanner to the robot
# Sick LMS500, range: 30m, field: 180deg, 90 sample points
laser = Sick()
laser.add_stream('socket')
laser.translate(x=.5)
laser.properties(resolution = 2.0)
laser.properties(scan_window = 180.0)
laser.properties(frequency = 50.0)
robot.append(laser)

# Adds a velocity actuator to the robot which allows to apply a pair of velocities (v,w) to him
motion = MotionVW()
motion.add_interface('socket')
robot.append(motion)

# Makes it possible to control the robot with the keyboard
keyboard = Keyboard()
robot.append(keyboard)
keyboard.properties(ControlType = 'Position')

# Configure the robot on the 'socket' interface
robot.add_default_interface('socket')

# Sets the environment and the camera position
env = Environment('/home/julian/PycharmProjects/RobotNavigationWithNengo/simulation/environments/corridor.blend')
env.set_camera_location([0.0,0.0,45.0])
env.set_camera_rotation([0.0, 0.0, 0.0])
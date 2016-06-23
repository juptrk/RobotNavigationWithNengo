#! /usr/bin/env morseexec

""" Basic MORSE simulation scene for <simulation> environment

Feel free to edit this template as you like!
"""

from morse.builder import *

# Append ATRV robot to the scene
robot = ATRV()
robot.translate(8,-8.0,0)
robot.rotate(0.0,0.0,2.25)


# Append motion
motion = MotionVW()
motion.add_interface('socket')
robot.append(motion)

# Append pose
pose = Pose()
pose.translate(z = 0.75)
pose.add_stream('socket')
robot.append(pose)

# Append a laser scanner
# Sick LMS500, range: 30m, field: 180deg, 180 sample points
laser = Sick()
laser.add_stream('socket')
laser.properties(resolution = 3.0)
robot.append(laser)

videocamera = VideoCamera()
robot.add_stream('socket')
robot.append(videocamera)

# Make it possible to control the robot with the keyboard
keyboard = Keyboard()
robot.append(keyboard)
keyboard.properties(ControlType = 'Position')

# Configure the robot on the 'socket' interface
robot.add_default_interface('socket')

env = Environment('/home/julian/PycharmProjects/RobotNavigationWithNengo/simulation/environments/boxes_custom.blend')


#! /usr/bin/env morseexec

""" Basic MORSE simulation scene for <simulation> environment

Feel free to edit this template as you like!
"""

from morse.builder import *

# Add a robot with a position sensor and a motion controller
r2d2 = ATRV()

pose = Pose()
pose.add_interface('socket')
r2d2.append(pose)

motion = Waypoint()
motion.add_interface('socket')
r2d2.append(motion)


# Environment
env = Environment('land-1/trees')

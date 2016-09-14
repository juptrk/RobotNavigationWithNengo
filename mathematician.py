__author__ = "Julian Petruck"

import math
import numpy as np
import nengo.utils.numpy as npext

"""
Maximum speed, acceleration and decceleration values for the translational and angular velocity
"""


max_vel = [1.0, 1.0] # form: (v in m/s, w in deg/s [90])
max_acc = [0.3, 0.4] # form: (v_acc in m/s^2, w_acc in deg/s^2 [---])
max_dec = [0.4, 0.5]   # form: (v_dec in m/s^2, w_dec in deg/s^2 [---])


"""
Value for the p controller.
The value is found by trying and must be positive or at least zero.
"""

v_proportional = 1.2
proportional = 1.2
integral = 0.9
weighting = .5
v_factor = .95
w_factor = .05


"""
Calculates the future position for the given angle, position, translational and angular velocity after an also given
timestep.

The formulas used below are taken from the 1997 paper introducing the dynamic window approach with one modification.
While in the paper there is a minus-sign in front of the future y formula, I have one in front of the future x formula
(Both only takes place for the w \= 0 case). This is because the paper seems to use different coordinate axes.
"""


def calculate_future_pos(act_pos, vel, t):

    future_x = act_pos[0] + calculate_future_x(act_pos[2], vel, t)

    future_y = act_pos[1] + calculate_future_y(act_pos[2], vel, t)

    return [future_x, future_y]


"""
Calculates the future x position change for the given angle, translational and angular velocity after an also given
timestep.
"""


def calculate_future_x(theta, vel, t):

    if vel[1] == 0:
        f = vel[0] * np.cos(theta) * t

    else:
        f = -(vel[0] / vel[1]) * (np.sin(theta) - np.sin(theta + (vel[1] * t)))

    return f


"""
Calculates the future y position change for the given angle, translational and angular velocity after an also given
timestep.
"""


def calculate_future_y(theta, vel, t):

    if vel[1] == 0:
        f = vel[0] * np.sin(theta) * t

    else:
        f = (vel[0] / vel[1]) * (np.cos(theta) - np.cos(theta + (vel[1] * t)))

    return f



def calculate_hypot(x, y):

    return math.sqrt((x**2) + (y**2))


"""
Method gets a number of neurons, a number of dimensions and a content.
It then creates a a uniform distribution on an n-dimensional unit hypersphere as it is also done in nengo.dists for
UniformHypersphere.
In addition to UniformHypersphere, this methods lets you shift the distributions mean via the mean-input and it lets
you set the variance via the variance-input.
This was necessary to create neurons reacting to either positiv or negativ input
"""


def create_encoders(neurons, dimensions, mean, variance):

    encoders = variance * np.random.randn(neurons, dimensions) + mean
    encoders /= npext.norm(encoders, axis=1, keepdims=True)

    return encoders

"""
Transformates a point from a parent frame into a child frame with the given informations
"""

def transformate_point(new_frame, point_in_old_frame):

    x_old = point_in_old_frame[0]
    y_old = point_in_old_frame[1]
    x_trans = new_frame[0]
    y_trans = new_frame[1]

    theta_cos = math.cos(new_frame[2])
    theta_sin = math.sin(new_frame[2])

    x_new = (theta_cos * x_old) + (theta_sin * y_old) - (theta_cos * x_trans) - (theta_sin * y_trans)
    y_new = (-theta_sin * x_old) + (theta_cos * y_old) + (theta_sin * x_trans) - (theta_cos * y_trans)
    theta_new = math.atan2(y_new, x_new)

    return [x_new, y_new, theta_new]


"""
Implements a p controller to compare the given velocities with a ideal and give back their weights.
The goal needs to be given from the robots perspective.
"""
def pi_control(goal_robot, velocities, dists, integral_sum, smallest, angle):

    # the potential velocities are calculated by the pi controller
    v_pot = math.hypot(goal_robot[0], goal_robot[1]) * proportional
    if v_pot > max_vel[0]:
        v_pot = max_vel[0] * proportional
    w_pot = goal_robot[2] * proportional + integral_sum * integral

    # the dist_weight is calculated and applied to the potential velocity
    dist_weight = scale(smallest, 0.0, 1.0) * weighting
    if (angle < 0 and w_pot < 0) or (angle > 0 and w_pot > 0):
        w_pot *= -dist_weight

    if (angle < 0 and w_pot > 0) or (angle > 0 and w_pot < 0):
        w_pot *= dist_weight

    vel_pot = [v_pot, w_pot]

    best_weight = 0.0
    best_vel = vel_pot

    # goes through th  velocities and calculates the weights for them
    for vel in velocities:

        v_distance = math.fabs(vel_pot[0] - vel[0])
        w_distance = math.fabs(vel_pot[1] - vel[1])

        e = v_factor * scale(v_distance, 0, max_vel[0])
        e2 = w_factor * (scale(w_distance, 0, math.fabs(vel_pot[1])))
        e3 = 1 - scale(dists[i], 0.0, 10.0)

        # if the calculated weight is bigger then the best one before, this weight is used as best weight.
        if (e+e2+e3) > best_weight:
            best_weight = (e+e2+e3)
            best_vel = vel

    # returns the best velocity
    return best_vel


"""
Scales a given distance with a linear interpolation, where the given min and max values are used.
If the distance is the same or smaller than the min value, it is weighted with one.
If the distance is the same or greater than the max value, it is weighted with zero.
"""


def scale(distance, min, max):

    if distance <= min:
        return 1

    elif distance >= max:
        return 0

    else:
        return 1 - ((distance - min) / (max - min))

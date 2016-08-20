import math

import numpy as np
import nengo.utils.numpy as npext


"""
Maximum speed, acceleration and decceleration values for the translational and angular velocity
"""


max_vel = [1.0, 1.57] # form: (v in m/s, w in deg/s [90])
max_acc = [0.3, 0.4] # form: (v_acc in m/s^2, w_acc in deg/s^2 [---])
max_dec = [0.4, 0.5]   # form: (v_dec in m/s^2, w_dec in deg/s^2 [---])


"""
Value for the p controller.
The value is found by trying and must be positive or at least zero.
"""


p = 1.0


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
Calculates the possible translational and angular velocities within the dynamic window and returns them
as a list of (v, w) pairs.
"""


def dynamic_window(act_vel, t):
    velocities = []

    if act_vel[1] < 0:
        lower_w = act_vel[1] - (max_acc[1] * t)
        upper_w = act_vel[1] + (max_dec[1] * t)
    else:
        lower_w = act_vel[1] - (max_dec[1] * t)
        upper_w = act_vel[1] + (max_acc[1] * t)

    if lower_w < (-max_vel[1]):
        lower_w = -max_vel[1]

    if upper_w > max_vel[1]:
        upper_w = max_vel[1]

    angle_step = 0.1

    while lower_w <= upper_w:

        lower_v = act_vel[0] - (max_dec[0] * t)
        upper_v = act_vel[0] + (max_acc[0] * t)

        if lower_v < 0:
            lower_v = 0

        if upper_v > max_vel[0]:
            upper_v = max_vel[0]

        v_step = 0.1

        while lower_v <= upper_v:

            velocities.append([lower_v, lower_w])

            lower_v += v_step

        lower_w += angle_step

    return velocities


"""
Calculates the admissible velocities from a given dynmaic window of velocities.
Therefore I use the formula given in the 1997 paper introducing the dynamic window approach (same as above).
"""


def admissible_velocities(act_pos, data, velocities, t):

    admis_velocities = []

    if len(data) <= 0:
        return admis_velocities

    for i in range(0, len(velocities)):

        vel = velocities[i]

        fut_pos = calculate_future_pos(act_pos, vel, t)

        dif_point = transformate_point(act_pos, fut_pos)

        point_angle = math.degrees(dif_point[2])

        point_angle = int((point_angle + 90.0) / 2.0)

        if point_angle > 87:
            lower = 85
            upper = 91

        elif point_angle < 3:
            lower = 0
            upper = 6

        else:
            lower = point_angle - 3
            upper = point_angle + 4

        path_dist = 100

        angle = (lower * 2.0) - 90.0

        for j in range(lower, upper):
            if data[j] < path_dist:
                path_dist = data[j]
                angle = (j * 2.0) - 90.0

        print("Distance on path before is %s" % path_dist)
        path_dist /= 2.0
        print("What we substract from is %s" % path_dist)
        print("What we substract is %s" % (calculate_hypot(dif_point[0], dif_point[1])))
        path_dist -= calculate_hypot(dif_point[0], dif_point[1])
        if path_dist < 0:
            path_dist = 0

        compare_vel = [23, 42]

        if path_dist > 0:
            compare_vel = [math.sqrt(path_dist * max_dec[0]), math.sqrt(path_dist * max_dec[1])]

            if angle < 0:
                compare_vel[1] = -compare_vel[1]

                if vel[0] <= compare_vel[0] and vel[1] >= compare_vel[1]:
                    admis_velocities.append(vel)

            else:
                if vel[0] <= compare_vel[0] and vel[1] <= compare_vel[1]:
                    admis_velocities.append(vel)

        print("The velocity %s is compared to the velocity %r" % (vel, compare_vel))
        print("Distance on path after is %s \n" % path_dist)

    return admis_velocities


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


def p_control(act_pos, goal_robot, velocities, t):

    distance = calculate_hypot(goal_robot[0], goal_robot[1])

    v_pot = distance * 0.1 * p
    w_pot = goal_robot[2] * p

    if v_pot > max_vel[0]:
        v_pot = max_vel[0]
    if w_pot > max_vel[1]:
        w_pot = max_vel[1]
    elif w_pot < -max_vel[1]:
        w_pot = -max_vel[1]

    vel_pot = [v_pot, w_pot]

    best_weight = 0.0
    smallest_distance = max_vel[0] + max_vel[1]
    best_vel = vel_pot

    v_factor = 0.95
    w_factor = 0.05
    max_distance = (v_factor * max_vel[0]) + (w_factor * max_vel[1])

    for i in range(0, len(velocities)):

        vel = velocities[i]

        fut_distance = (v_factor * math.fabs(vel_pot[0] - vel[0])) + (w_factor * math.fabs(vel_pot[1] - vel[1]))

        e = scale(fut_distance, 0, max_distance)

        if e > best_weight:
            best_weight = e
            smallest_distance = fut_distance
            best_vel = vel

        elif best_weight <= 0.0 and fut_distance < smallest_distance:
            smallest_distance = fut_distance
            best_vel = vel

    print("Potential vel: %s \n" % vel_pot)

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
        # form: y = y0 + (y1 - y0) * ((x - x0) / (x1 - x0))
        # with: y0 = 0, y1 = 1
        return 1 - ((distance - min) / (max - min))

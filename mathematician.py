import math

import numpy as np
import nengo.utils.numpy as npext


def calculate_future_pos(act_x, act_y, theta, v, w, timestep):

    future_x = self.calculate_future_x(act_x, theta, v, w, timestep)

    future_y = self.calculate_future_y(act_y, theta, v, w, timestep)



def calculate_future_x(act_x, theta, v, w, t):

    f = 0.0

    if w == 0:
        f = v * np.cos(theta) * t

    else:
        f = (v / w) * (np.sin(theta) - np.sin(theta + (w * t)))

    return act_x + f



def calculate_future_y(act_y, theta, v, w, t):

    f = 0.0

    if w == 0:
        f = v * np.sin(theta) * t

    else:
        f = -(v / w) * (np.cos(theta) - np.cos(theta + (w * t)))

    return act_y + f



def calculate_trans_vel(x, y):

    return math.sqrt((x**2) + (y**2))


"""
Method gets a number of neurons, a number of dimensions and a content.
It then creates a a uniform distribution on an n-dimensional unit hypersphere as it is also done in nengo.dists for
UniformHypersphere.
In addition to UniformHypersphere, this methods lets you shift the distributions mean via the mean-input.
Thi was necessary to create neurons reacting to either positiv or negativ input
"""
def create_encoders(neurons, dimensions, mean):

    encoders = 0.25 * np.random.randn(neurons, dimensions) + mean
    encoders /= npext.norm(encoders, axis=1, keepdims=True)

    return encoders
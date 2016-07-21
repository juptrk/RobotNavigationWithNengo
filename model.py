import nengo
import random

from nengo.dists import Uniform

import mathematician


class Model:

    robot_sim = 0
    robot_pose = 0
    robot_odom = 0
    robot_laser = 0

    x_temp = 30.0
    y_temp = 25.0

    # x_temp = 0.0
    # y_temp = 0.0

    counter = 0
    rad_value = rad_change = 0
    model = 0
    sim = 0
    z_rotation = trans_velocity = 0
    min_distance = max_distance = 0.0
    scan_distances = 0

    left = right = mover = speed = distance = 0

    left_neuron = right_neuron = left_neuron_changes = right_neuron_changes = mover_neuron = 0

    speed_neuron = distance_neuron = 0

    left_con = right_con = left_changes = right_changes = mover_con = 0

    rot_speed_con = trans_speed_con = max_distance_con = min_distance_con = 0

    left_probe = right_probe = mover_probe = speed_probe = distance_probe = 0

    left_neuron_probe = right_neuron_probe = left_neuron_changes_probe = right_neuron_changes_probe = mover_neuron_probe = 0

    speed_neuron_probe = distance_neuron_probe = 0

    left_con_probe = right_con_probe = left_changes_probe = right_changes_probe = mover_con_probe = 0

    rot_speed_con_probe = trans_speed_con_probe = max_distance_con_probe = min_distance_con_probe = 0

    left_raw_probe = right_raw_probe = 0



    def __init__(self):

        self.x_temp = 30.0
        self.y_temp = 25.0

        # self.x_temp = 0.0
        # self.y_temp = 0.0

        self.z_rotation = 0
        self.trans_velocity = 0

        self.model = nengo.Network(label = 'Morse - Nengo')

        with self.model:
            # Neurons
            self.left_neuron = nengo.Ensemble(100, dimensions = 1,
                                              encoders=mathematician.create_encoders(100, 1, 1))

            self.right_neuron = nengo.Ensemble(100, dimensions=1,
                                              encoders=mathematician.create_encoders(100, 1, -1))

            self.left_neuron_changes = nengo.Ensemble(100, dimensions=1,
                                              encoders=mathematician.create_encoders(100, 1, 1))

            self.right_neuron_changes = nengo.Ensemble(100, dimensions=1,
                                              encoders=mathematician.create_encoders(100, 1, -1))

            self.mover_neuron = nengo.Ensemble(100, dimensions=1)

            self.speed_neuron = nengo.Ensemble(100, dimensions=2)

            self.distance_neuron = nengo.Ensemble(100, dimensions=2)


            # Input Nodes
            self.low = nengo.Node(output = 1.0)
            self.high = nengo.Node(output = 10.0)
            self.mover = nengo.Node(output = 0.01)
            self.speed = nengo.Node(output = 1.0)
            self.distance = nengo.Node(output = 0.1)

            # Connections
            self.left_con = nengo.Connection(self.low, self.left_neuron, function = self.output_whole)
            self.right_con = nengo.Connection(self.low, self.right_neuron, function = self.output_whole)

            self.left_changes = nengo.Connection(self.high, self.left_neuron_changes, function = self.output_change)
            self.right_changes = nengo.Connection(self.high, self.right_neuron_changes, function = self.output_change)

            self.mover_con = nengo.Connection(self.mover, self.mover_neuron, function = self.move)

            self.trans_speed_con = nengo.Connection(self.speed, self.speed_neuron[0], function = self.translation_speed)
            self.rot_speed_con = nengo.Connection(self.speed, self.speed_neuron[1], function = self.rotation_speed)

            self.max_distance_con = nengo.Connection(self.distance, self.distance_neuron[0], function = self.maximum_distance)
            self.min_distance_con = nengo.Connection(self.distance, self.distance_neuron[1], function=self.minimum_distance)


            # Probes
            ## Input Node Probes
            self.left_probe = nengo.Probe(self.low)
            self.right_probe = nengo.Probe(self.high)
            self.mover_probe = nengo.Probe(self.mover)
            self.speed_probe = nengo.Probe(self.speed)
            self.distance_probe = nengo.Probe(self.distance)

            ## Neuron Probes
            self.left_neuron_probe = nengo.Probe(self.left_neuron, synapse=0.01)
            self.right_neuron_probe = nengo.Probe(self.right_neuron, synapse=0.01)

            self.left_neuron_changes_probe = nengo.Probe(self.left_neuron_changes, synapse=0.01)
            self.right_neuron_changes_probe = nengo.Probe(self.right_neuron_changes, synapse=0.01)

            self.mover_neuron_probe = nengo.Probe(self.mover_neuron, synapse=0.01)

            self.speed_neuron_probe = nengo.Probe(self.speed_neuron, synapse=0.01)

            self.distance_neuron_probe = nengo.Probe(self.distance_neuron, synapse=0.01)

            ## Connection Probes
            self.left_con_probe = nengo.Probe(self.left_con)
            self.right_con_probe = nengo.Probe(self.right_con)

            self.left_changes_probe = nengo.Probe(self.left_changes)
            self.right_changes_probe = nengo.Probe(self.right_changes)

            self.mover_con_probe = nengo.Probe(self.mover_con)

            self.trans_speed_con_probe = nengo.Probe(self.trans_speed_con)
            self.rot_speed_con_probe = nengo.Probe(self.rot_speed_con)

            self.max_distance_con_probe = nengo.Probe(self.max_distance_con)
            self.min_distance_con_probe = nengo.Probe(self.min_distance_con)

            ## Raw Probes
            self.left_raw_probe = nengo.Probe(self.left_neuron.neurons)
            self.right_raw_probe = nengo.Probe(self.right_neuron.neurons)


        self.sim = nengo.Simulator(self.model)


    def output_whole(self, x):
        number = self.get_rad_value() / 3.14159

        number = number * x[0]

        print("Yaaaaaw: %s \n" % number)


        return number

    def output_change(self, x):
        number = self.get_rad_change()

        number = number * x[0]

        print("Change: %s \n" % number)

        return number


    def move(self, x):
        self.counter = self.counter + 1

        if self.counter % 500 == 0:
            self.x_temp = random.uniform(float(self.robot_pose.get('x')), float(self.robot_sim.x))
            self.y_temp = random.uniform(float(self.robot_pose.get('y')), float(self.robot_sim.y))

        return self.x_temp * x[0]


    def rotation_speed(self, x):

        return self.z_rotation * x[0]

    def translation_speed(self, x):

        return self.trans_velocity * x[0]

    def minimum_distance(self, x):

        return self.min_distance * x[0]

    def maximum_distance(self, x):

        return self.max_distance * x[0]



    def run_steps(self, steps):
        self.sim.run_steps(steps, progress_bar=False)

    def set_rad_value(self, value):
        self.rad_value = self.rad_value + value
        self.rad_change = value

    def get_rad_value(self):
        return self.rad_value

    def get_rad_change(self):
        return self.rad_change

    def set_robot_sim(self, robot):
        self.robot_sim = robot

    def set_pose(self, pose):
        self.robot_pose = pose

    def set_odom(self, odom):
        self.robot_odom = odom

        self.z_rotation = self.robot_odom.get('wz')

        self.trans_velocity = mathematician.calculate_trans_vel(self.robot_odom.get('vx'), self.robot_odom.get('vy'))

    def set_laser(self, laser):
        act_min = 30.0
        act_max = 0.0
        self.scan_distances = laser.get('range_list')

        for i in range(0, len(self.scan_distances)):
            act_distance = self.scan_distances[i]

            if act_distance < act_min:
                act_min = act_distance

            if act_distance > act_max:
                act_max = act_distance

        self.min_distance = act_min
        self.max_distance = act_max



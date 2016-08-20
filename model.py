import nengo
import math
import mathematician


class Model:

    """
    Class variables are created and initialized
    """

    """
    Position variables
    """

    goal_world = [-10.0, 8.0, 0.0] # form: (x, y, theta)
    goal_odom = [100.0, 100.0, 0.0] # form: (x, y, theta)
    act_pos = [0.0, 0.0, 0.0] # form: (x, y, theta)

    """
    Velocity variables
    """

    vel = [1.0, 0.0] # form: (v, w)
    act_vel = [0.0, 0.0] # form: (v, w)

    """
    Robot specific variables
    """

    robot_sim = 0
    robot_pose = 0
    robot_odom = 0
    rad_value = rad_change = 0
    z_rotation = trans_velocity = 0.0
    min_distance = max_distance = 0.0
    t = 1.0

    "Laser specific variables"

    scan_distances = []
    laser_points = []

    scan_window = 180.0
    laser_res = 2.0

    """
    Model specific variables
    """

    model = 0
    sim = 0

    "Neuron variables"

    mover_neuron = 0

    "Input Node variables"

    medium = 0

    "Connection Variables"

    mover_con = 0

    "Probe variables"

    mover_neuron_probe = 0

    """
    Obstacle Avoidance specific variables.
    Maximum speed, acceleration and decceleration values for the translational and angular velocity
    """

    max_vel = [1.0, 1.57]  # form: (v in m/s, w in deg/s [90])
    max_acc = [0.3, 0.4]  # form: (v_acc in m/s^2, w_acc in deg/s^2 [---])
    max_dec = [0.4, 0.5]  # form: (v_dec in m/s^2, w_dec in deg/s^2 [---])

    ####################################################################################################################
    # left_neuron = right_neuron = left_changes_neuron = right_changes_neuron = 0
    #
    # trans_speed_neuron = rot_speed_neuron = max_distance_neuron = min_distance_neuron = 0
    #
    # x_act_neuron = x_fut_neuron = y_act_neuron = y_fut_neuron = 0
    ####################################################################################################################
    # very_low = low = high = 0
    ####################################################################################################################
    # left_con = right_con = left_changes = right_changes = 0
    #
    # rot_speed_con = trans_speed_con = max_distance_con = min_distance_con = 0
    #
    # x_act_con = x_fut_con = y_act_con = y_fut_con = 0
    ####################################################################################################################
    # left_neuron_probe = right_neuron_probe = left_neuron_changes_probe = right_neuron_changes_probe = 0
    #
    # trans_speed_neuron_probe = rot_speed_neuron_probe = max_distance_neuron_probe = min_distance_neuron_probe = 0
    #
    # x_act_neuron_probe = x_fut_neuron_probe = y_act_neuron_probe = y_fut_neuron_probe = 0
    #
    # left_con_probe = right_con_probe = left_changes_probe = right_changes_probe = mover_con_probe = 0
    #
    # rot_speed_con_probe = trans_speed_con_probe = max_distance_con_probe = min_distance_con_probe = 0
    #
    # x_act_con_probe = x_fut_con_probe = y_act_con_probe = y_fut_con_probe = 0
    ####################################################################################################################


    """
    Method initializes a model which uses the dynamic window approach with alternative heuristics to navigate a robot
    """

    def __init__(self):

        # self.model = nengo.Network(label = 'Morse - Nengo')

        # with self.model:

            "Neurons are created"

            # self.mover_neuron = nengo.Ensemble(100, dimensions=1)

            "Input Nodes are created"

            # self.medium = nengo.Node(output = 1.0)

            "Connections are established"

            # self.mover_con = nengo.Connection(self.medium, self.mover_neuron, function = self.move)

            "Probes"

            # Neuron Probes

            # self.mover_neuron_probe = nengo.Probe(self.mover_neuron, synapse=0.01)

            # Connection Probes

            # self.mover_con_probe = nengo.Probe(self.mover_con)

            ############################################################################################################
            # self.left_neuron = nengo.Ensemble(100, dimensions = 1,
            #                                   encoders=mathematician.create_encoders(100, 1, 1, 0.25))
            #
            # self.right_neuron = nengo.Ensemble(100, dimensions=1,
            #                                   encoders=mathematician.create_encoders(100, 1, -1, 0.25))
            #
            # self.left_changes_neuron = nengo.Ensemble(100, dimensions=1,
            #                                   encoders=mathematician.create_encoders(100, 1, 1, 0.1))
            #
            # self.right_changes_neuron = nengo.Ensemble(100, dimensions=1,
            #                                   encoders=mathematician.create_encoders(100, 1, -1, 0.1))
            #
            # self.rot_speed_neuron = nengo.Ensemble(100, dimensions=1)
            # self.trans_speed_neuron = nengo.Ensemble(100, dimensions=1)
            #
            # self.max_distance_neuron = nengo.Ensemble(100, dimensions=1)
            # self.min_distance_neuron = nengo.Ensemble(100, dimensions=1)
            #
            # self.x_act_neuron = nengo.Ensemble(100, dimensions=1)
            # self.x_fut_neuron = nengo.Ensemble(100, dimensions=1)
            #
            # self.y_act_neuron = nengo.Ensemble(100, dimensions=1)
            # self.y_fut_neuron = nengo.Ensemble(100, dimensions=1)
            ############################################################################################################
            # self.left_con = nengo.Connection(self.medium, self.left_neuron, function = self.output_whole)
            # self.right_con = nengo.Connection(self.medium, self.right_neuron, function = self.output_whole)
            #
            # self.left_changes = nengo.Connection(self.high, self.left_changes_neuron, function = self.output_change)
            # self.right_changes = nengo.Connection(self.high, self.right_changes_neuron, function = self.output_change)
            #
            # self.trans_speed_con = nengo.Connection(self.medium, self.trans_speed_neuron, function = self.translation_speed)
            # self.rot_speed_con = nengo.Connection(self.medium, self.rot_speed_neuron, function = self.rotation_speed)
            #
            # self.max_distance_con = nengo.Connection(self.low, self.max_distance_neuron, function=self.maximum_distance)
            # self.min_distance_con = nengo.Connection(self.low, self.min_distance_neuron, function=self.minimum_distance)
            #
            # self.x_act_con = nengo.Connection(self.low, self.x_act_neuron, function=self.act_x)
            # self.x_fut_con = nengo.Connection(self.low, self.x_fut_neuron, function=self.future_x)
            #
            # self.y_act_con = nengo.Connection(self.low, self.y_act_neuron, function=self.act_y)
            # self.y_fut_con = nengo.Connection(self.low, self.y_fut_neuron, function=self.future_y)
            ############################################################################################################
            #self.very_low = nengo.Node(output=0.01)
            #self.low = nengo.Node(output=0.1)
            #self.high = nengo.Node(output=10.0)
            ############################################################################################################
            # self.left_neuron_probe = nengo.Probe(self.left_neuron, synapse=0.01)
            # self.right_neuron_probe = nengo.Probe(self.right_neuron, synapse=0.01)
            #
            # self.left_changes_neuron_probe = nengo.Probe(self.left_changes_neuron, synapse=0.01)
            # self.right_changes_neuron_probe = nengo.Probe(self.right_changes_neuron, synapse=0.01)
            #
            #
            # self.trans_speed_neuron_probe = nengo.Probe(self.trans_speed_neuron, synapse=0.01)
            # self.rot_speed_neuron_probe = nengo.Probe(self.rot_speed_neuron, synapse=0.01)
            #
            # self.max_distance_neuron_probe = nengo.Probe(self.max_distance_neuron, synapse=0.01)
            # self.min_distance_neuron_probe = nengo.Probe(self.min_distance_neuron, synapse=0.01)
            #
            # self.x_act_neuron_probe = nengo.Probe(self.x_act_neuron, synapse=0.01)
            # self.x_fut_neuron_probe = nengo.Probe(self.x_fut_neuron, synapse=0.01)
            #
            # self.y_act_neuron_probe = nengo.Probe(self.y_act_neuron, synapse=0.01)
            # self.y_fut_neuron_probe = nengo.Probe(self.y_fut_neuron, synapse=0.01)
            ############################################################################################################
            # self.left_con_probe = nengo.Probe(self.left_con)
            # self.right_con_probe = nengo.Probe(self.right_con)
            #
            # self.left_changes_probe = nengo.Probe(self.left_changes)
            # self.right_changes_probe = nengo.Probe(self.right_changes)
            #
            #
            # self.trans_speed_con_probe = nengo.Probe(self.trans_speed_con)
            # self.rot_speed_con_probe = nengo.Probe(self.rot_speed_con)
            #
            # self.max_distance_con_probe = nengo.Probe(self.max_distance_con)
            # self.min_distance_con_probe = nengo.Probe(self.min_distance_con)
            #
            # self.x_act_con_probe = nengo.Probe(self.x_act_con)
            # self.x_fut_con_probe = nengo.Probe(self.x_fut_con)
            #
            # self.y_act_con_probe = nengo.Probe(self.y_act_con)
            # self.y_fut_con_probe = nengo.Probe(self.y_fut_con)
            ############################################################################################################

        # self.sim = nengo.Simulator(self.model, dt=0.05)

    """
    normalizes the whole rotation with pi, multiplies it with the input an returns it
    """

    def output_whole(self, x):
        number = self.get_rad_value() / 3.14159

        #print("Yaaaaaw: %s \n" % number)

        return number * x[0]

    """
    multiplies the last angular change with the input and returns it
    """

    def output_change(self, x):
        number = self.get_rad_change()

        #print("Change: %s \n" % number)

        return number * x[0]

    """
    Executes the dynamic window approach to calculate a new velocity command which is than multiplied with the input
    and returned
    """

    def move(self, x):

        best_vel = self.dynamic_window_approach(self.act_vel,
                                                self.act_pos,
                                                self.scan_distances,
                                                self.t)

        self.vel = best_vel

        #return best_vel[0] * x[0]

    """
    multiplies the actual translational velocity with the input and returns it
    """

    def translation_speed(self, x):

        return self.act_vel[0] * x[0]

    """
    multiplies the actual angular velocity with the input and returns it
    """

    def rotation_speed(self, x):

        return self.act_vel[1] * x[0]

    """
    multiplies the actual minimum distance to an object with the input and returns it
    """

    def minimum_distance(self, x):

        return self.min_distance * x[0]

    """
    multiplies the actual maximum distance to an object with the input and returns it
    """

    def maximum_distance(self, x):

        return self.max_distance * x[0]

    """
    multiplies the actual x position with the input and returns it
    """

    def act_x(self, x):

        return self.act_pos[0] * x[0]

    """
    multiplies the actual y position with the input and returns it
    """

    def act_y(self, x):

        return self.act_pos[1] * x[0]

    """
    calculates the future x position after a certain timestep when keeping the actual velocity, multiplies it with
    the input and returns ist
    """

    def future_x(self, x):

        fut_x = self.act_pos[0] + mathematician.calculate_future_x(self.act_pos[2],
                                             self.act_vel,
                                             self.t)

        return fut_x * x[0]

    """
    calculates the future y position after a certain timestep when keeping the actual velocity, multiplies it with
    the input and returns ist
    """

    def future_y(self, x):

        fut_y = self.act_pos[1] + mathematician.calculate_future_y(self.act_pos[2],
                                             self.act_vel,
                                             self.t)

        return fut_y * x[0]

    """
    Gets a number of steps for which the simulation should be run and calls its implemented run_steps method with
    this number
    """

    def run_steps(self, steps):
        self.sim.run_steps(steps, progress_bar=False)

    """
    Lets the simulation do one step by calling its implemented step method
    """

    def step(self):
       self.sim.step()

    """
    Returns the class variable rad_value
    """

    def get_rad_value(self):
        return self.rad_value

    """
    Returns the class variable rad_change
    """

    def get_rad_change(self):
        return self.rad_change

    """
    Adds the given value to the last known rotation value.
    The given value should be the real angular change the robot has made.
    """

    def set_rad_value(self, value):
        self.rad_value = self.rad_value + value
        self.rad_change = value

    """
    Sets the class variable robot_sim to the given value.
    The given variable robot should be a pymorse simulation object.
    """

    def set_robot_sim(self, robot):
        self.robot_sim = robot

    """
    Sets the class variable robot_pose to the given value.
    The given variable pose should be an object returned by a Morse pose sensor.
    """

    def set_pose(self, pose):
        self.robot_pose = pose

    """
    Sets the class variable robot_odom to the given value.
    It also sets the class variables act_pos and act_vel to values from the given odom object.
    The given variable odom should be an object returned by a Morse integral odom sensor.
    """

    def set_odom(self, odom):
        self.robot_odom = odom

        self.act_pos[0] = self.robot_odom.get('x')
        self.act_pos[1] = self.robot_odom.get('y')
        self.act_pos[2] = self.robot_odom.get('yaw')

        self.act_vel[0] = mathematician.calculate_hypot(self.robot_odom.get('vx'), self.robot_odom.get('vy'))
        self.act_vel[1] = self.robot_odom.get('wz')
        # self.act_vel[0] = 1.0
        # self.act_vel[1] = 0.0

    """
    Sets the class variables scan_distances, laser_points, scan_window and laser_res to given values or to values from
    the given laser object.
    It also sets the class variables min_distance and max_distance by calculating the mininum and maximum from the
    list scan_distances.
    The given variable laser should be an object returned by a Morse laser sensor (Sick).
    The given variables scan_window and resolution should correspond to the real properties from the Morse laser sensor.
    """

    def set_laser(self, laser, scan_window, resolution):
        act_min = 30.0
        act_max = 0.0

        self.scan_distances = laser.get('range_list')
        self.laser_points = laser.get('point_list')
        self.scan_window = scan_window
        self.laser_res = resolution

        for i in range(0, len(self.scan_distances)):
            act_distance = self.scan_distances[i]

            if act_distance < act_min:
                act_min = act_distance

            if act_distance > act_max:
                act_max = act_distance

        self.min_distance = act_min
        self.max_distance = act_max

    """
    Sets the two class variables goal_world and goal_odom to the given values.
    The given variable goal_world should represent the robots goal in the world frame, the variable goal_odom should
    represent the same goal in the robots odom frame.
    """

    def set_goal(self, goal_world, goal_odom):

        self.goal_world = goal_world
        self.goal_odom = goal_odom

    """









    """

    def dynamic_window_approach(self, act_vel, act_pos, scan_data, t):

        counter_ad = 0
        counter_dyn = 0

        goal_robot = mathematician.transformate_point(self.act_pos, self.goal_odom)

        print("WHO AM I? I AM YOU: %s \n" % self.act_vel)

        velocities = []

        if len(scan_data) <= 0:
            return velocities

        if act_vel[1] < 0:
            lower_w = act_vel[1] - (self.max_acc[1] * t)
            upper_w = act_vel[1] + (self.max_dec[1] * t)
        else:
            lower_w = act_vel[1] - (self.max_dec[1] * t)
            upper_w = act_vel[1] + (self.max_acc[1] * t)

        if lower_w < (-self.max_vel[1]):
            lower_w = -self.max_vel[1]

        if upper_w > self.max_vel[1]:
            upper_w = self.max_vel[1]

        angle_step = 0.1

        while lower_w <= upper_w:

            lower_v = act_vel[0] - (self.max_dec[0] * t)
            upper_v = act_vel[0] + (self.max_acc[0] * t)

            if lower_v < 0:
                lower_v = 0

            if upper_v > self.max_vel[0]:
                upper_v = self.max_vel[0]

            v_step = 0.1

            while lower_v <= upper_v:

                counter_dyn += 1

                vel = [lower_v, lower_w]
                path_dist = 30

                fut_pos = mathematician.calculate_future_pos(act_pos, vel, t)
                dif_point = mathematician.transformate_point(act_pos, fut_pos)

                angle = math.degrees(dif_point[2])
                point_angle = int((angle + 90.0) / 2.0)

                if point_angle > 88:
                    lower = 86
                    upper = 91

                elif point_angle < 2:
                    lower = 0
                    upper = 5

                else:
                    lower = point_angle - 2
                    upper = point_angle + 3

                for j in range(lower, upper):
                    if scan_data[j] < path_dist:
                        path_dist = scan_data[j]
                        angle = (j * 2.0) - 90.0

                print("The angle is %s " % angle)
                print("Distance on path before is %s" % path_dist)
                path_dist /= 2.0
                print("What we subtract from is %s" % path_dist)
                print("What we subtract is %s" % (mathematician.calculate_hypot(dif_point[0], dif_point[1])))
                path_dist -= mathematician.calculate_hypot(dif_point[0], dif_point[1])

                if path_dist < 0:
                    path_dist = 0

                compare_vel = [23, 42]

                if path_dist > 0:
                    compare_vel = [math.sqrt(path_dist * self.max_dec[0]), math.sqrt(path_dist * self.max_dec[1])]

                    if angle < 0:
                        compare_vel[1] = -compare_vel[1]

                        if vel[0] <= compare_vel[0] and vel[1] >= compare_vel[1]:
                            counter_ad += 1
                            velocities.append(vel)

                    else:tu
                        if vel[0] <= compare_vel[0] and vel[1] <= compare_vel[1]:
                            counter_ad += 1
                            velocities.append(vel)

                print("The velocity %s is compared to the velocity %r" % (vel, compare_vel))
                print("Distance on path after is %s \n" % path_dist)

                lower_v += v_step

            lower_w += angle_step

        best_vel = mathematician.p_control(self.act_pos, goal_robot, velocities, t)

        print("WHO AM I? I AM YOU: %s \n" % self.act_vel)
        print("Dynamic Window : %s \n" % velocities)
        print("We have %s dynamic velocities, %r remain after safety check. \n" % (counter_dyn, counter_ad))
        print("%s velocities are unsafe. \n" % (counter_dyn - counter_ad))
        print("Best Velocity: %s \n" % best_vel)
        print("Laser: %s \n" % self.scan_distances)

        return best_vel

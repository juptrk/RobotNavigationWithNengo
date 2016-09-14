import nengo
import math
import mathematician


class Model:

    """
    Method initializes a neural model which uses the dynamic window approach with alternative heuristics to navigate a robot
    """

    def __init__(self):

        """
        Position variables
        """
        self.__goal_world = [-28.0, 0.0, 0.0]  # form: (x, y, theta)
        self.__goal_odom = [-28.0, 0.0, 0.0]  # form: (x, y, theta)
        self.__act_pos = [0.0, 0.0, 0.0]  # form: (x, y, theta)

        """
        Velocity variables
        """
        self.vel = [1.0, 0.0]  # form: (v, w)
        self.__act_vel = [0.0, 0.0]  # form: (v, w)

        """
        Robot specific variables
        """
        self.__robot_sim = 0
        self.__t = .9

        "Laser specific variables"
        self.__scan_distances = []

        for i in range(0, 91):
            self.__scan_distances.append(30.0)

        self.__scan_window = 180.0
        self.__laser_res = 2.0
        self.__distance_radius = 30.0

        """
        Obstacle Avoidance specific variables.
        Maximum speed and decceleration values for the translational and angular velocity
        Moreover the dynamic window is created with the specified translational and rotational velocities
        """
        self.__max_vel = [1.0, 1.0]  # form: (v in m/s, w in deg/s [90])
        self.__max_dec = [0.4, 0.5]  # form: (v_dec in m/s^2, w_dec in deg/s^2 [---])

        self.__translational_velocities = [0.0, 0.25, 0.5, 0.75, 1.0]
        self.__rotational_velocities = [-1.0,-0.8,-0.6,-0.4,-0.2,
                                        0.0,0.2,0.4,0.6,0.8,1.0]
        self.__dynamic_window = []

        for i in self.__translational_velocities:
            for j in self.__rotational_velocities:
                self.__dynamic_window.append([i, j])

        """
        Value for the p controller.
        The values are found by trying and must be positive or at least zero.
        """
        self.__v_proportional = 1.0
        self.__proportional = 1.0
        self.__integral = 0.12
        self.__weighting = 1.5
        self.__v_factor = .55
        self.__w_factor = .45

        # Creates the Network
        self.__model = nengo.Network(label = 'Morse - Nengo')

        # Calculates the number of scans
        self.__scans = int(self.__scan_window/self.__laser_res) + 1

        """
        Calculates the value for the length of a list, that contains the (v,w) pairs from the the dynamic window
        not as lists of two, but in a row, e.g. [v1,w1,v2,w2,v3,w3,v4,w4,...]
        """
        self.__velocities_combination = len(self.__dynamic_window) * 2

        with self.__model:

            "Input Nodes are created"

            self.__position = nengo.Node(output=1.0)
            self.__velocity = nengo.Node(output=1.0)
            self.__odometry_goal = nengo.Node(output=1.0)
            self.__distances = nengo.Node(output=1.0)
            self.__window = nengo.Node(output=1.0)

            """
            Neurons are created.

            Most of them are Neurons of type Direct.
            Every neuron has as much dimensions as its input list will have values. The number of neurons is 100 for
            every dimension if there are less then 10, for more dimensions there are 10 neurons for every dimension.
            the radius gives the range to which the neuron react without saturating.

            For the LIFRate neuron the time constant after which the activation will be 0 again is set to tau_rc = .05.
            How long the activation is held at zero after a spike is set by tau_ref = .002.
            """

            self.__position_neuron = nengo.Ensemble(300,
                                                  dimensions=3,
                                                  radius=60.0,
                                                  neuron_type=nengo.Direct())
            self.__velocity_neuron = nengo.Ensemble(200,
                                                  dimensions=2,
                                                  radius=3.0,
                                                  neuron_type=nengo.Direct())
            self.__goal_neuron = nengo.Ensemble(300,
                                              dimensions=3,
                                              radius=60.0,
                                              neuron_type=nengo.Direct())
            self.__distances_neuron = nengo.Ensemble(self.__scans*10,
                                                   dimensions=self.__scans,
                                                   radius=self.__distance_radius,
                                                   neuron_type=nengo.Direct())
            self.__position_goal_neuron = nengo.Ensemble(600,
                                                       dimensions=6,
                                                       radius=60.0,
                                                       neuron_type=nengo.Direct())
            self.__dynamic_window_neuron = nengo.Ensemble(self.__velocities_combination*10,
                                                        dimensions=self.__velocities_combination,
                                                        radius=3.0,
                                                        neuron_type=nengo.Direct())

            self.__position_window_distances_neuron = nengo.Ensemble(30+((self.__velocities_combination+self.__scans)*10),
                                                                   dimensions=3+self.__velocities_combination+self.__scans,
                                                                   radius=60.0,
                                                                   neuron_type=nengo.Direct())

            self.__robot_goal_neuron = nengo.Ensemble(300,
                                                             dimensions=3,
                                                             radius=60.0,
                                                             neuron_type=nengo.Direct())

            self.__admissible_velocities_neuron = nengo.Ensemble(self.__velocities_combination*15,
                                                               dimensions=int(self.__velocities_combination*1.5),
                                                               radius=60.0,
                                                               neuron_type=nengo.Direct())

            self.__robot_goal_admissible_neuron = nengo.Ensemble(40 + self.__velocities_combination*15,
                                                                   dimensions=4 + int(self.__velocities_combination*1.5),
                                                                   radius=60.0,
                                                                   neuron_type=nengo.Direct())

            self.__integrator = nengo.Ensemble(100, dimensions=1, radius=4.0, neuron_type=nengo.LIFRate(tau_rc=0.05, tau_ref=0.002))

            self.__controlling_neuron = nengo.Ensemble(200,
                                                     dimensions=2,
                                                     radius=3.0,
                                                     neuron_type=nengo.Direct())

            """
            Connections are established.

            All Connections use a .05 synapse Lowpass filter for filtering the input.
            They use different functions which are implemented later in the class.
            """

            self.__position_connection = nengo.Connection(self.__position,
                                                        self.__position_neuron,
                                                        function=self.get_position,
                                                        synapse=0.05)
            self.__velocity_connection = nengo.Connection(self.__velocity,
                                                        self.__velocity_neuron,
                                                        function=self.get_velocity,
                                                        synapse=0.05)
            self.__goal_connection = nengo.Connection(self.__odometry_goal,
                                                    self.__goal_neuron,
                                                    function=self.get_goal,
                                                        synapse=0.05)
            self.__distances_connection = nengo.Connection(self.__distances,
                                                         self.__distances_neuron,
                                                         function=self.get_distances,
                                                        synapse=0.05)
            self.__dynamic_window_connection = nengo.Connection(self.__window,
                                                              self.__dynamic_window_neuron,
                                                              function=self.get_dynamic_window,
                                                        synapse=0.05)

            self.__position_goal_connection = nengo.Connection(self.__position_neuron,
                                                             self.__position_goal_neuron,
                                                             function=self.combine_position_goal,
                                                        synapse=0.05)
            self.__goal_position_connection = nengo.Connection(self.__goal_neuron,
                                                             self.__position_goal_neuron,
                                                             function=self.combine_goal_position,
                                                        synapse=0.05)

            self.__position_window_distances_connection = nengo.Connection(self.__position_neuron,
                                                                         self.__position_window_distances_neuron,
                                                                         function=self.combine_position_window_distances,
                                                        synapse=0.05)
            self.__window_position_distances_connection = nengo.Connection(self.__dynamic_window_neuron,
                                                               self.__position_window_distances_neuron,
                                                               function=self.combine_window_position_distances,
                                                        synapse=0.05)
            self.__distances_position_window_connection = nengo.Connection(self.__distances_neuron,
                                                                         self.__position_window_distances_neuron,
                                                                         function=self.combine_distances_position_window,
                                                        synapse=0.05)

            self.__robot_goal_connection = nengo.Connection(self.__position_goal_neuron,
                                                                   self.__robot_goal_neuron,
                                                                   function=self.get_robot_goal,
                                                        synapse=0.05)

            self.__admissible_velocities_connection = nengo.Connection(self.__position_window_distances_neuron,
                                                                     self.__admissible_velocities_neuron,
                                                                     function=self.get_admissible_velocities,
                                                        synapse=0.05)

            self.__robot_goal_admissible_connection = nengo.Connection(self.__robot_goal_neuron,
                                                                         self.__robot_goal_admissible_neuron,
                                                                         function=self.combine_robot_goal_admissible,
                                                        synapse=0.05)
            self.__admissible_robot_goal_connection = nengo.Connection(self.__admissible_velocities_neuron,
                                                                         self.__robot_goal_admissible_neuron,
                                                                         function=self.combine_admissible_robot_goal,
                                                        synapse=0.05)

            self.__integrator_connection = nengo.Connection(self.__robot_goal_neuron,
                                                          self.__integrator,
                                                          transform=[[0.05]],
                                                          function=self.get_goal_angle,
                                                        synapse=0.05)
            self.__integrator_self_connection = nengo.Connection(self.__integrator,
                                                               self.__integrator,
                                                               transform=[[1]],
                                                        synapse=0.05)

            self.__integrator_send_connection = nengo.Connection(self.__integrator,
                                                               self.__robot_goal_admissible_neuron,
                                                               function=self.combine_integrator,
                                                        synapse=0.05)

            self.__controlling_connection = nengo.Connection(self.__robot_goal_admissible_neuron,
                                                           self.__controlling_neuron,
                                                           function=self.control_values,
                                                        synapse=0.05)



            """
            Probes.

            Shows how to use probes to take data from the model and plot it.
            The following probes are used to track data for the default plot of the integrator.
            This data is ploted in the default configuration of the gui.

            To print the plot to a pdf file, use the following code:

            from matplotlib import pyplot as plt
            from matplotlib.backends.backend_pdf import PdfPages
            pp = PdfPages('example.pdf')
            plt.plot(self.sim.trange(), self.sim.data[self.integrator_probe], label='Integrator')
            plt.plot(self.sim.trange(), self.sim.data[self.integrator_connection_probe], label='Con')
            plt.plot(self.sim.trange(), self.sim.data[self.integrator_self_connection_probe], label='Self Con')
            plt.plot(self.sim.trange(), self.sim.data[self.robot_goal_neuron_probe][:, 2], label='Real')
            plt.savefig(pp, format='pdf')
            pp.close()
            """
            self.robot_goal_neuron_probe = nengo.Probe(self.__robot_goal_neuron, synapse = 0.01)
            self.integrator_probe = nengo.Probe(self.__integrator, synapse = 0.01)
            self.integrator_connection_probe = nengo.Probe(self.__integrator_connection, synapse=0.01)
            self.integrator_self_connection_probe = nengo.Probe(self.__integrator_self_connection, synapse=0.01)

        # Creates the simulation from our model with a 50 ms timestep
        self.sim = nengo.Simulator(self.__model, dt=0.05)

    """
    returns the actual position
    """
    def get_position(self, x):

        return self.__act_pos

    """
    returns the odometry goal
    """
    def get_goal(self, x):

        return self.__goal_odom

    """
    returns the actual scan distances
    """
    def get_distances(self, x):

        return self.__scan_distances

    """
    returns the dynamic window velocities.
    format is no longer [[v1,w1],[v2,w2],...] but [v1,w1,v2,w2,v3,w3,v4,w4,...]
    """
    def get_dynamic_window(self, x):

        temp = []

        for vel in self.__dynamic_window:

            temp.append(vel[0])
            temp.append(vel[1])

        return temp

    """
    Returns the angle to the robot goal when given the whole robot goal
    """
    def get_goal_angle(self,x):

        return x[2]

    """
    adds three zeros behind the actual position and returns it
    """
    def combine_position_goal(self, x):

        return [x[0], x[1], x[2], 0.0, 0.0, 0.0]

    """
    adds three zeros before the odometry goal and returns it
    """
    def combine_goal_position(self, x):

        return [0.0, 0.0, 0.0, x[0], x[1], x[2]]

    """
    adds as many zeros behind the actual position as there are velocities returned by get_dynamic_window(...) and returns it
    """
    def combine_position_window(self, x):

        temp = [x[0], x[1], x[2]]

        for i in range(0, self.__velocities_combination):

            temp.append(0.0)

        return temp

    """
    adds three zeros before the actual dynamic window and returns it
    """
    def combine_window_position(self, x):

        temp = [0.0, 0.0, 0.0]

        for i in range(0, self.__velocities_combination):

            temp.append(x[i])

        return temp

    """
    adds as many zeros behind the position window list as there are scan distances and dynamic velocities combined and returns it
    """
    def combine_position_window_distances(self, x):

        temp = [x[0], x[1], x[2]]

        for i in range(0, self.__velocities_combination+self.__scans):

            temp.append(0.0)

        return temp

    """
    adds three zeros before and as many zeros as there are scan distances behind the dynamic window list and returns it
    """
    def combine_window_position_distances(self, x):

        temp = [0.0, 0.0, 0.0]

        for i in range(0, self.__velocities_combination):

            temp.append(x[i])

        for j in range(0, self.__scans):

            temp.append(0.0)

        return temp

    """
    adds as many zeros before the distance list as there are elements in the dynamic window list plus 3 and returns it
    """

    def combine_distances_position_window(self, x):

        temp = []

        for i in range(0, 3+self.__velocities_combination):

            temp.append(0.0)

        for j in range(0, self.__scans):

            temp.append(x[j])

        return temp

    """
    adds as many zeros behind the robot goal as there are elements in the admissible velocities and used
    distances list plus 1 for the integrator value and returns it
    """
    def combine_robot_goal_admissible(self, x):

        temp = [x[0], x[1], x[2], 0.0]

        for i in range(0, int(self.__velocities_combination*1.5)):

            temp.append(0.0)

        return temp

    """
    adds 4 zeros before the admissible velocities and used distances list and returns it
    """

    def combine_admissible_robot_goal(self, x):

        temp = [0.0, 0.0, 0.0, 0.0]

        for i in range(0, len(x)):

            temp.append(x[i])

        return temp


    """
    Combines three zeros before and as many zeros as there are values in the admissible velocities and used distances list
    behind the integrator value and returns it.
    """

    def combine_integrator(self,x):

        temp = [0.0, 0.0, 0.0, x[0]]

        for i in range(0, int(self.__velocities_combination*1.5)):

            temp.append(0.0)

        return temp

    """
    calculates the goal in the robot frame and returns it
    """

    def get_robot_goal(self, x):

        x_old = x[3]
        y_old = x[4]
        x_trans = x[0]
        y_trans = x[1]

        theta_cos = math.cos(x[2])
        theta_sin = math.sin(x[2])

        x_new = (theta_cos * x_old) + (theta_sin * y_old) - (theta_cos * x_trans) - (theta_sin * y_trans)
        y_new = (-theta_sin * x_old) + (theta_cos * y_old) + (theta_sin * x_trans) - (theta_cos * y_trans)
        theta_new = math.atan2(y_new, x_new)

        return [x_new, y_new, theta_new]

    """
    Calculates the admissible velocities and returns it
    """

    def get_admissible_velocities(self, x):

        # Position, velocities and measured distances are read out of the input
        act_pos = [x[0], x[1], x[2]]

        velocities = []
        new_velocities = []

        for i in range(0, int((self.__velocities_combination / 2))):

            velocities.append([x[3+(i*2)], x[3+(i*2)+1]])

        dists = []
        used_dists = []
        smallest = 30

        for j in range(0, self.__scans):

            dists.append(x[3+self.__velocities_combination+j])

            if dists[j] < smallest:
                smallest = dists[j]

        # these boundaries will later be added to and subtracted from the measured angle of a future position
        bound_minus = 3
        bound_plus = 4

        # if a wall is closer than 2.5 meters, the boundaries will be greater
        if smallest < 2.5:
            if smallest <= 0.19:
                bound_minus = 40
            else:
                bound_minus = int(7.5/smallest)

            bound_plus = bound_minus + 1

        # goes through all given velocities
        for velocity in velocities:

            path_dist = 30

            # calculates the future position with the current pair of velocities and transforms it into the robot frame
            fut_pos = mathematician.calculate_future_pos(act_pos, velocity, self.__t)
            dif_point = mathematician.transformate_point(act_pos, fut_pos)

            # turns the radian angle to a degree angle and adds 90 degrees, to have a positiv range of possible angles
            angle = math.degrees(dif_point[2])
            point_angle = angle + 90.0

            # if the calculated angle is zero, the velocity will be ignored, otherwise the angle will be divided by zero
            # to match the 91 used matchpoints of the laser scanner.
            if point_angle != 0:
                point_angle = int(point_angle/2.0)
            else:
                used_dists.append(-1)
                new_velocities.append(2.0)
                new_velocities.append(2.0)
                continue

            # calculates the lower and upper boundaries for the distance search range
            lower = point_angle - bound_minus
            upper = point_angle + bound_plus

            if upper > 90:
                lower = 90 - (bound_minus * 2)
                upper = 90

            elif lower < 0:
                lower = 0
                upper = 0 + (bound_minus * 2)

            # Searches for the smallest distance in the current range and sets path_dist to this value
            for k in range(lower, upper):
                if dists[k] < path_dist:
                    path_dist = dists[k]
                    angle = (k * 2.0) - 90.0

            # calculates the distance between the future position and the measured object
            path_dist -= mathematician.calculate_hypot(dif_point[0], dif_point[1])

            # if the distance is not zero, it will be compared, otherwise it will be thrown out of the list
            if path_dist > 0:

                # calculates a velocity to compare from the measured distance and the robots maximum deccelerations
                compare_vel = [math.sqrt(path_dist * self.__max_dec[0]), math.sqrt(path_dist * self.__max_dec[1])]

                # if the angle where the distance was measured, is smaller than zero, it will be compared to the negative
                # rotation velocity of the compare velocity, otherwise it will be compared to the normal rotation velocity
                if angle < 0:
                    compare_vel[1] = -compare_vel[1]

                    # If both tested velocities are smaller than the compare velocities it is added to our list, otherwise
                    # default values will be inserted
                    if velocity[0] <= compare_vel[0] and velocity[1] >= compare_vel[1]:
                        used_dists.append(path_dist)
                        new_velocities.append(velocity[0])
                        new_velocities.append(velocity[1])

                    else:
                        used_dists.append(-1)
                        new_velocities.append(2.0)
                        new_velocities.append(2.0)

                else:
                    # If both tested velocities are smaller than the compare velocities it is added to our list, otherwise
                    # default values will be inserted
                    if velocity[0] <= compare_vel[0] and velocity[1] <= compare_vel[1]:
                        used_dists.append(path_dist)
                        new_velocities.append(velocity[0])
                        new_velocities.append(velocity[1])

                    else:
                        used_dists.append(-1)
                        new_velocities.append(2.0)
                        new_velocities.append(2.0)

            else:
                used_dists.append(-1)
                new_velocities.append(2.0)
                new_velocities.append(2.0)

        # velocities andd the corresponding measured distances are returned
        velocities_distances = new_velocities + used_dists

        return velocities_distances

    """
    pi controls the velocities and returns the best velocity.
    Moreover it will apply the velocity to the robot.
    """

    def control_values(self, x):

        # reads out robot goal, integrator value, velocities and used distances from the input
        velocities = []
        dists = []
        smallest = 30
        angle = 0
        goal_robot = [x[0], x[1], x[2]]
        integrate_sum = x[3]

        for i in range(0, int((self.__velocities_combination / 2))):

            if x[4+(i*2)] != 2.0 and x[4+(i*2)+1] != 2.0:

                velocities.append([x[4 + (i * 2)], x[4 + (i * 2) + 1]])

            if x[4+self.__velocities_combination+i] != -1:

                dists.append(x[4+self.__velocities_combination+i])

                # smallest distance is measured
                if dists[len(dists)-1] < smallest:
                    smallest = dists[len(dists)-1]
                    angle = i - 45

        # the potential velocities are calculated by the pi controller
        v_pot = math.hypot(goal_robot[0], goal_robot[1])
        if v_pot > self.__max_vel[0]:
            v_pot = self.__max_vel[0] * self.__v_proportional
        else:
            v_pot *= self.__v_proportional

        w_pot = goal_robot[2] * self.__proportional + integrate_sum * self.__integral

        # the dist_weight is calculated and applied to the potential velocity
        dist_weight = self.scale(smallest, 0.0, 1.0) * self.__weighting
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

            e = self.__v_factor * self.scale(v_distance, 0, self.__max_vel[0])
            e2 = self.__w_factor * (self.scale(w_distance, 0, math.fabs(vel_pot[1])))
            e3 = 1 - self.scale(dists[i], 0.0, 10.0)

            # if the calculated weight is bigger then the best one before, this weight is used as best weight.
            if (e + e2 + e3) > best_weight:
                best_weight = (e + e2 + e3)
                best_vel = vel

        # sets the class attribute vel to the new best_vel
        self.vel = best_vel

        # applies the velocity to the robot and returns it
        if self.__robot_sim != 0:
            self.__robot_sim.motion_publisher(self.__robot_sim.simu, best_vel)

        return best_vel

    """
    Scales a given distance with a linear interpolation, where the given min and max values are used.
    If the distance is the same or smaller than the min value, it is weighted with one.
    If the distance is the same or greater than the max value, it is weighted with zero.
    """

    def scale(self, distance, min, max):

        if distance <= min:
            return 1

        elif distance >= max:
            return 0

        else:
            # form: y = y0 + (y1 - y0) * ((x - x0) / (x1 - x0))
            # with: y0 = 0, y1 = 1
            return 1 - ((distance - min) / (max - min))


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
        if self.sim != 0:
            self.sim.step()

    """
    Sets the class variable robot_sim to the given value.
    The given variable robot should be a pymorse simulation object.
    """

    def set_robot_sim(self, robot):
        self.__robot_sim = robot


    """
    Sets the class variable robot_odom to the given value.
    It also sets the class variables act_pos and act_vel to values from the given odom object.
    The given variable odom should be an object returned by a Morse integral odom sensor.
    """

    def set_odom(self, odom):

        self.__act_pos[0] = odom.get('x')
        self.__act_pos[1] = odom.get('y')
        self.__act_pos[2] = odom.get('yaw')

        self.__act_vel[0] = math.hypot(odom.get('vx'), odom.get('vy'))
        self.__act_vel[1] = odom.get('wz')

    """
    Sets the class variables scan_distances, laser_points, scan_window and laser_res to given values or to values from
    the given laser object.
    The given variable laser should be an object returned by a Morse laser sensor (Sick).
    The given variables scan_window and resolution should correspond to the real properties from the Morse laser sensor.
    """

    def set_laser(self, laser, scan_window, resolution):

        self.__scan_distances = laser.get('range_list')
        self.__scan_points = laser.get('points_list')
        self.__scan_window = scan_window
        self.__laser_res = resolution

    """
    Sets the two class variables goal_world and goal_odom to the given values.
    The given variable goal_world should represent the robots goal in the world frame, the variable goal_odom should
    represent the same goal in the robots odom frame.
    """

    def set_goal(self, goal_world, goal_odom):

        self.__goal_world = goal_world
        self.__goal_odom = goal_odom

__author__ = "Julian Petruck"

import math
import mathematician

class DWA:

    """
    Method initializes a class instance
    """

    def __init__(self):
        """
        Class variables are created and initialized
        """
        """
        Maximum speed, acceleration and decceleration values for the translational and angular velocity
        """
        self.max_vel = [1.0, 1.0]  # form: (v in m/s, w in deg/s [90])
        self.max_acc = [0.3, 0.4]  # form: (v_acc in m/s^2, w_acc in deg/s^2 [---])
        self.max_dec = [0.4, 0.5]  # form: (v_dec in m/s^2, w_dec in deg/s^2 [---])

        """
        Value for the p controller.
        The value is found by trying and must be positive or at least zero.
        """
        self.v_proportional = 1.2
        self.proportional = 1.2
        self.integral = 0.9
        self.weighting = .5
        self.v_factor = .95
        self.w_factor = .05

        """
        Position variables
        """
        self.goal_world = [-28.0, 0.0, 0.0]  # form: (x, y, theta)
        self.goal_odom = [-28.0, 0.0, 0.0]  # form: (x, y, theta)
        self.act_pos = [0.0, 0.0, 0.0]  # form: (x, y, theta)

        """
        Velocity variables
        """
        self.vel = [1.0, 0.0]  # form: (v, w)
        self.act_vel = [0.0, 0.0]  # form: (v, w)

        """
        Robot specific variables
        """
        self.robot_sim = 0
        self.robot_odom = 0
        t = .9

        """
        Laser specific variables
        """
        self.scan_distances = []
        self.scan_window = 180.0
        self.laser_res = 2.0

        """
        Obstacle Avoidance specific variables.
        Maximum speed and decceleration values for the translational and angular velocity.
        Moreover the dynamic window is created.
        """
        self.max_vel = [1.0, 1.4]  # form: (v in m/s, w in deg/s [90])
        self.max_dec = [0.4, 0.5]  # form: (v_dec in m/s^2, w_dec in deg/s^2 [---])

        self.translational_velocities = [0.0, 0.25, 0.5, 0.75, 1.0]
        self.rotational_velocities = [-1.4, -1.2, -1.0, -0.8, -0.6, -0.4, -0.2,
                                 0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4]
        self.dynamic_window = []
        self.velocities_combination = 0

        for i in self.translational_velocities:
            for j in self.rotational_velocities:
                self.dynamic_window.append([i, j])

                self.integrator_sum = 0

    """
    Calculates the best velocity for the next timestep by calling the dynamic_window_approach(...) method
    """
    def move(self):

        best_vel = self.dynamic_window_approach(self.goal_odom,
                                                self.act_pos,
                                                self.scan_distances,
                                                self.t)

        # Applies the calculated velocity to the robot
        if self.robot_sim != 0:
            self.robot_sim.motion_publisher(self.robot_sim.simu, best_vel)

        self.vel = best_vel

    """
    Sets the class variable robot_sim to the given value.
    The given variable robot should be a pymorse simulation object.
    """

    def set_robot_sim(self, robot):
        self.robot_sim = robot

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

    """
    Sets the class variables scan_distances, scan_window and laser_res to given values or to values from
    the given laser object.
    The given variable laser should be an object returned by a Morse laser sensor (Sick).
    The given variables scan_window and resolution should correspond to the real properties from the Morse laser sensor.
    """

    def set_laser(self, laser, scan_window, resolution):

        self.scan_distances = laser.get('range_list')
        self.scan_window = scan_window
        self.laser_res = resolution


    """
    Sets the two class variables goal_world and goal_odom to the given values.
    The given variable goal_world should represent the robots goal in the world frame, the variable goal_odom should
    represent the same goal in the robots odom frame.
    """

    def set_goal(self, goal_world, goal_odom):

        self.goal_world = goal_world
        self.goal_odom = goal_odom

    """
    Applies the Dynamic Window Approach to the data.
    """

    def dynamic_window_approach(self, goal_odom, act_pos, scan_data, t):

        # transforms the goal in the robot frame
        goal_robot = mathematician.transformate_point(act_pos, goal_odom)

        velocities = []
        dists = []

        if len(scan_data) <= 0:
            return velocities

        smallest = 30
        angle = 0

        # gets the smallest measured distance
        for i in range(0, len(scan_data)):
            if scan_data[i] < smallest:
                smallest = scan_data[i]
                angle = i - 45

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

        # goes through the whole dynamic window
        for vel in self.dynamic_window:
            path_dist = 30

            # calculates the future position with the current pair of velocities and transforms it into the robot frame
            fut_pos = mathematician.calculate_future_pos(act_pos, vel, t)
            dif_point = mathematician.transformate_point(act_pos, fut_pos)

            # turns the radian angle to a degree angle and adds 90 degrees, to have a positiv range of possible angles
            angle = math.degrees(dif_point[2])
            point_angle = angle + 90.0

            # if the calculated angle is zero, the velocity will be ignored, otherwise the angle will be divided by zero
            # to match the 91 used matchpoints of the laser scanner.
            if point_angle != 0:
                point_angle = int(point_angle/2.0)
            else:
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
            for j in range(lower, upper):
                if scan_data[j] < path_dist:
                    path_dist = scan_data[j]
                    angle = (j * 2.0) - 90.0

            # calculates the distance between the future position and the measured object
            path_dist -= mathematician.calculate_hypot(dif_point[0], dif_point[1])

            # if the distance is not zero, it will be compared, otherwise it will be thrown out of the list
            if path_dist > 0:
                # calculates a velocity to compare from the measured distance and the robots maximum deccelerations
                compare_vel = [math.sqrt(path_dist * self.max_dec[0]), math.sqrt(path_dist * self.max_dec[1])]

                # if the angle where the distance was measured, is smaller than zero, it will be compared to the negative
                # rotation velocity of the compare velocity, otherwise it will be compared to the normal rotation velocity
                if angle < 0:
                    compare_vel[1] = -compare_vel[1]

                    # If both tested velocities are smaller than the compare velocities it is added to our list, otherwise
                    # default values will be inserted
                    if vel[0] <= compare_vel[0] and vel[1] >= compare_vel[1]:
                        dists.append(path_dist)
                        velocities.append(vel)

                else:
                    # If both tested velocities are smaller than the compare velocities it is added to our list, otherwise
                    # default values will be inserted
                    if vel[0] <= compare_vel[0] and vel[1] <= compare_vel[1]:
                        dists.append(path_dist)
                        velocities.append(vel)

        # integrator value is summed up
        self.integrator_sum += 0.05 * goal_robot[2]

        # the pi controller is applied and returns the best velocity which is then returned
        best_vel = mathematician.pi_control(goal_robot, velocities, dists, self.integrator_sum, smallest, angle)

        return best_vel


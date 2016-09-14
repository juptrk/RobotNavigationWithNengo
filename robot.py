__author__ = "Julian Petruck"

import pymorse
import time
import mathematician

class Robot:

    """
    Method initializing the Morse simulation with the corresponding subscribers and starting the main loop, which
    lets the robot walk till it reaches the goal.
    """

    def __init__(self, nengo):

        """
        Class variables are created and initialized
        """

        """
        Goal variables
        """

        self.goal_world = [-28.0, 0.0, 0.0]  # form: (x, y, theta)
        self.goal_odom = [100.0, 100.0, 0.0]  # form: (x, y, theta)

        """
        Simulation specific variables
        """

        self.simu = 0
        self.nengo_sim = 0

        "Data set booleans - one time"

        self.goal_set = False

        "Data set booleans - several times"

        self.odom_set = laser_set = False

        """
        Robot specific variables
        """

        self.odom = self.rad_value = 0
        self.position = [0.0, 0.0, 0.0]

        "Laser specific variables"

        self.laser = 0
        self.scan_window = 180.0
        self.resolution = 2.0

        """
        Time specific variables
        """

        self.zaehler = 0
        self.firststamp = 0
        self.secondstamp = 0
        self.firstset = False

        self.start_time = time.time()
        self.model = nengo
        self.model.set_robot_sim(self)

        with pymorse.Morse() as self.simu:

            # subscribes to updates from the Pose sensor by passing a callback
            self.simu.robot.pose.subscribe(self.update_pose)
            self.simu.robot.odom.subscribe(self.update_odom)
            self.simu.robot.laser.subscribe(self.update_laser)

            # sends a destination
            self.motion_publisher(self.simu, self.model.vel)


            # Leave a couple of millisec to the simulator to start the action
            self.simu.sleep(0.1)

            # waits until we reach the target
            while True:

                # checks whether the robot is in the goal area - if so the robot is stopped and the simulation finished
                x_dist = self.goal_odom[0] - self.position[0]
                y_dist = self.goal_odom[1] - self.position[1]

                if -2.5 <= x_dist <= 2.5 and -2.5 <= y_dist <= 2.5:
                    self.model.vel = [0.0, 0.0]
                    self.motion_publisher(self.simu, self.model.vel)
                    break

                # sends the data if all informations are set
                if self.odom_set and self.laser_set:

                    self.model.set_odom(self.odom)
                    self.model.set_laser(self.laser, self.scan_window, self.resolution)

                    self.odom_set = self.laser_set = False

                    # makes one step with the model or the Dynamic Window Approach
                    self.model.step()
                    #self.model.move()
                    self.zaehler += .05

            act_time = time.time() - self.start_time


            print("Here we are! \n")

            print("Nengo s: %s \n" % self.zaehler)
            print("Python s: %s \n" % act_time)
            print("Morse s: %s \n" % (self.secondstamp - self.firststamp))

    """
    Method called by the pose subscriber to calculate the odometry goal with the pose position.
    This will only be done once at the beginning of the simulation.
    """

    def update_pose(self, pose):

        if not self.goal_set:
            pos_world = [pose.get('x'), pose.get('y'), pose.get('yaw')]
            self.goal_odom = mathematician.transformate_point(pos_world, self.goal_world)
            self.model.set_goal(self.goal_world, self.goal_odom)
            self.goal_set = True


    """
    Method called by the odom subscriber to set the class variable odom to the latest data from the
    Morse odom sensor.
    This is only done once in a time step to have corresponding data when sending it to the Nengo model.
    """

    def update_odom(self, odom):

        if not self.odom_set:
            self.odom = odom
            self.position[0] = odom.get('x')
            self.position[1] = odom.get('y')
            self.position[2] = odom.get('yaw')
            self.odom_set = True

        if self.firstset:
            self.secondstamp = odom.get('timestamp')
        else:
            self.firststamp = odom.get('timestamp')
            self.firstset = True

    """
    Method called by the laser subscriber to set the class variable laser to the latest data from the Morse laser sensor.
    This is only done once in a time step to have corresponding data when sending it to the Nengo model.
    """

    def update_laser(self, laser):

        if not self.laser_set:
            self.laser = laser
            self.laser_set = True


    """
    Method applies the given velocity to the robot via a publisher
    """

    def motion_publisher(self, simulation, vel):
        simulation.robot.motion.publish({'v': vel[0],
                                         'w': vel[1]})


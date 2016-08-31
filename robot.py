import pymorse
import time
import mathematician
import math


class Robot:

    """
    Class variables are created and initialized
    """

    """
    Goal variables
    """

    goal_world = [-15.0, 12.0, 0.0] # form: (x, y, theta)
    goal_odom = [100.0, 100.0, 0.0] # form: (x, y, theta)

    """
    Simulation specific variables
    """

    simu = 0
    nengo_sim = 0

    "Data set booleans - one time"

    goal_set = False

    "Data set booleans - several times"

    pose_set = odom_set = laser_set = rad_set = False

    """
    Robot specific variables
    """

    pose = odom = rad_value = 0
    position = [0.0, 0.0, 0.0]

    "Laser specific variables"

    laser = 0
    scan_window = 180.0
    resolution = 2.0

    """
    Time specific variables
    """

    zaehler = 0
    start_time = time.time()
    firststamp = 0
    secondstamp = 0
    firstset = False

    """
    Method initializing the Morse simulation with the corresponding subscribers and starting the main loop, which
    lets the robot walk till it reaches the goal.
    """

    def __init__(self, nengo):
        self.nengo_sim = nengo
        self.nengo_sim.set_robot_sim(self)
        with pymorse.Morse() as self.simu:

            # subscribes to updates from the Pose sensor by passing a callback
            self.simu.robot.pose.subscribe(self.update_pose)
            self.simu.robot.odom.subscribe(self.update_rad_value)
            self.simu.robot.int_odom.subscribe(self.update_odom)
            self.simu.robot.laser.subscribe(self.update_laser)

            # sends a destination
            #self.goal_publisher(self.simu)
            self.motion_publisher(self.simu)


            # Leave a couple of millisec to the simulator to start the action
            self.simu.sleep(0.1)

            # waits until we reach the target
            while True:
                # if self.simu.robot.goal.get_status() == "Arrived":
                #     self.nengo_sim.vel = [0.0, 0.0]
                #     self.motion_publisher(self.simu)
                #     break

                x_dist = math.fabs(self.goal_odom[0] - self.position[0])
                y_dist = math.fabs(self.goal_odom[1] - self.position[1])

                if x_dist <= 3.0 and y_dist <= 3.0:
                    self.nengo_sim.vel = [0.0, 0.0]
                    self.motion_publisher(self.simu)
                    break

                if self.pose_set and self.odom_set and self.laser_set and self.rad_set:

                    if not self.goal_set:

                        pos_world = [self.pose.get('x'), self.pose.get('y'), self.pose.get('yaw')]
                        self.goal_odom = mathematician.transformate_point(pos_world, self.goal_world)
                        self.nengo_sim.set_goal(self.goal_world, self.goal_odom)
                        self.goal_set = True

                    self.nengo_sim.set_pose(self.pose)
                    self.nengo_sim.set_rad_value(self.rad_value)
                    self.nengo_sim.set_odom(self.odom)
                    self.nengo_sim.set_laser(self.laser, self.scan_window, self.resolution)

                    self.pose_set = self.odom_set = self.laser_set = self.rad_set = False

                    self.nengo_sim.step()
                    #self.nengo_sim.move(.5)
                    self.zaehler += .005

                    self.motion_publisher(self.simu)

            act_time = time.time() - self.start_time

            print("Here we are! \n")

            print("Python ms: %s \n" % self.zaehler)

            print("Python s: %s \n" % act_time)

    """
    Method called by the pose subscriber to set the class variable pose to the latest data from the Morse pose sensor.
    This is only done once in a time step to have corresponding data when sending it to the Nengo model.
    """

    def update_pose(self, pose):

        if not self.pose_set:
            self.pose = pose
            self.pose_set = True

            #self.update_data()

    """
    Method called by the odom subscriber to set the class variable rad_value to the latest data from the
    Morse odom sensor.
    moreover the timestep is set to calculate the whole Morse working time.
    This is only done once in a time step to have corresponding data when sending it to the Nengo model.
    """

    def update_rad_value(self, odom):

        if not self.rad_set:
            self.rad_value = odom.get('dyaw')
            self.rad_set = True

           # self.update_data()

        if self.firstset:
            self.secondstamp = odom.get('timestamp')
        else:
            self.firststamp = odom.get('timestamp')
            self.firstset = True

    """
    Method called by the int_odom subscriber to set the class variable odom to the latest data from the
    Morse int_odom sensor.
    This is only done once in a time step to have corresponding data when sending it to the Nengo model.
    """

    def update_odom(self, int_odom):

        if not self.odom_set:
            self.odom = int_odom
            self.position[0] = int_odom.get('x')
            self.position[1] = int_odom.get('y')
            self.position[2] = int_odom.get('yaw')
            self.odom_set = True

            #self.update_data()

    """
    Method called by the laser subscriber to set the class variable laser to the latest data from the Morse laser sensor.
    This is only done once in a time step to have corresponding data when sending it to the Nengo model.
    """

    def update_laser(self, laser):

        if not self.laser_set:
            self.laser = laser
            self.laser_set = True

            #self.update_data()

    """
    Method publishes the goal which is set at the beginning to the robot to let him walk there.
    This method should only be called once to set the goal and let the dynamic window approach work properly afterwards.
    """

    def goal_publisher(self, simulation):
        simulation.robot.goal.publish({'x': self.goal_world[0], 'y': self.goal_world[1], 'z': 0.0,
                                   'tolerance': 0.5,
                                   'speed': 1.0})

    """
    Method publishes the last velocity the dynamic window approach calculated to avoid obstacles.
    """

    def motion_publisher(self, simulation):
        simulation.robot.motion.publish({'v': self.nengo_sim.vel[0],
                                         'w': self.nengo_sim.vel[1]})
        # simulation.robot.motion.publish({'v': 0,
        #                                  'w': 0})






        # def update_data(self):
        #
        #     if self.pose_set and self.odom_set and self.laser_set and self.rad_set:
        #
        #         if not self.goal_set:
        #             pos_world = [self.pose.get('x'), self.pose.get('y'), self.pose.get('yaw')]
        #             self.goal_odom = mathematician.transformate_point(pos_world, self.goal_world)
        #             self.nengo_sim.set_goal(self.goal_world, self.goal_odom)
        #             self.goal_set = True
        #
        #         self.nengo_sim.set_pose(self.pose)
        #         self.nengo_sim.set_rad_value(self.rad_value)
        #         self.nengo_sim.set_odom(self.odom)
        #         self.nengo_sim.set_laser(self.laser, 180.0, 2.0)
        #
        #         self.pose_set = self.odom_set = self.laser_set = self.rad_set = False
        #
        #         self.nengo_sim.step()
        #         self.zaehler += .05
        #
        #         self.motion_publisher(self.simu)
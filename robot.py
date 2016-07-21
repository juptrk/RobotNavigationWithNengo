import pymorse
import time


class Robot:
    x = 30.0
    y = 25.0

    # x = 0.0
    # y = 0.0

    direction = 0
    zaehler = 0
    start_time = time.time()
    firststamp = 0
    secondstamp = 0
    firstset = False
    nengo_sim = 0

    def __init__(self, nengo):
        self.nengo_sim = nengo
        self.nengo_sim.set_robot_sim(self)
        with pymorse.Morse() as simu:

            # subscribes to updates from the Pose sensor by passing a callback
            simu.robot.pose.subscribe(self.print_pos)
            simu.robot.odom.subscribe(self.print_odom)
            simu.robot.int_odom.subscribe(self.print_int_odom)
            simu.robot.laser.subscribe(self.print_laser)

            # sends a destination
            self.motion_publisher(simu)

            # Leave a couple of millisec to the simulator to start the action
            simu.sleep(0.1)

            # waits until we reach the target
            while True:
                if simu.robot.motion.get_status() == "Arrived":
                        break

                self.nengo_sim.run_steps(500)
                self.zaehler = self.zaehler + 500
                self.motion_publisher(simu)


            print("Here we are! \n")

            print("Python ms: %s \n" % self.zaehler)

            act_time = time.time() - self.start_time

            print("Python s: %s \n" % act_time)


    def print_pos(self, pose):

        self.nengo_sim.set_pose(pose)

    def print_odom(self, odom):

        self.nengo_sim.set_rad_value(odom.get('dyaw'))

        print("Yaaaaaw: %s \n" % self.nengo_sim.get_rad_value())

        if self.firstset:
            self.secondstamp = odom.get('timestamp')
        else:
            self.firststamp = odom.get('timestamp')
            self.firstset = True

    def print_int_odom(self, int_odom):

        self.nengo_sim.set_odom(int_odom)

    def print_laser(self, laser):
        self.nengo_sim.set_laser(laser)

    def motion_publisher(self, simulation):
        simulation.robot.motion.publish({'x': self.nengo_sim.x_temp, 'y': self.nengo_sim.y_temp, 'z': 0.0,
                                   'tolerance': 0.5,
                                   'speed': 1.0})

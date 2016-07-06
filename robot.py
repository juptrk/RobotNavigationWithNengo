import pymorse
import time


class Robot:
    x = 15.0
    y = 10.0
    direction = 0

    zähler = 0
    start_time = time.time()
    firststamp = 0
    secondstamp = 0
    firstset = False
    nengo_sim = 0

    def __init__(self, nengo):
        self.nengo_sim = nengo
        with pymorse.Morse() as simu:

            # subscribes to updates from the Pose sensor by passing a callback
            #simu.robot.pose.subscribe(self.print_pos)
            simu.robot.odom.subscribe(self.print_odom)

            #simu.robot.laser.subscribe(self.print_laser)

            # sends a destination
            self.motion_publisher(simu)

            # Leave a couple of millisec to the simulator to start the action
            simu.sleep(0.1)

            # waits until we reach the target
            while True:
                if simu.robot.motion.get_status() == "Arrived":
                    self.direction = self.direction + 1

                    if self.direction == 1:
                        self.x = 0.0
                        self.motion_publisher(simu)

                    elif self.direction == 2:
                        self.y = 20.0
                        self.motion_publisher(simu)

                    elif self.direction == 3:
                        self.x = 15.0
                        self.motion_publisher(simu)

                    elif self.direction == 4:
                        self.x = 0.0
                        self.motion_publisher(simu)

                    elif self.direction == 5:
                        self.y = 10.0
                        self.motion_publisher(simu)

                    elif self.direction > 5:
                        break

                self.nengo_sim.run_steps(500)
                self.zähler = self.zähler + 500


            print("Here we are! \n")

            print("Python ms: %s \n" % self.zähler)

            act_time = time.time() - self.start_time

            print("Python s: %s \n" % act_time)


    def print_pos(self, pose):

        self.nengo_sim.set_rad_value(pose.get('yaw'))

        print("Yaaaaaw: %s \n" % self.nengo_sim.get_rad_value())

        if self.firstset:
            self.secondstamp = pose.get('timestamp')
        else:
            self.firststamp = pose.get('timestamp')
            self.firstset = True

    def print_odom(self, odom):

        self.nengo_sim.set_rad_value(odom.get('dyaw'))

        print("Yaaaaaw: %s \n" % self.nengo_sim.get_rad_value())

        if self.firstset:
            self.secondstamp = odom.get('timestamp')
        else:
            self.firststamp = odom.get('timestamp')
            self.firstset = True


    def print_laser(self, laser):
        print("Laser: %s \n" % laser)

    def motion_publisher(self, simulation):
        simulation.robot.motion.publish({'x': self.x, 'y': self.y, 'z': 0.0,
                                   'tolerance': 0.5,
                                   'speed': 1.0})

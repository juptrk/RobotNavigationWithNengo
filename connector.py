import pymorse
import nengo
from nengo.dists import Uniform
import matplotlib.pyplot as plt
import time
import random
from matplotlib.backends.backend_pdf import PdfPages
from nengo.utils.matplotlib import rasterplot


rad_value = 0

class Nengo:
    model = 0
    sim = 0
    neuron = 0
    my_node = 0
    input_probe = 0
    raw_probe = 0
    neurons_probe = 0

    def __init__(self):
        self.model = nengo.Network()

        with self.model:
            self.neuron = nengo.Ensemble(n_neurons=10,
                                         dimensions=1,
                                         intercepts=Uniform(-.5, -.5),
                                         max_rates=Uniform(100, 100),
                                         encoders=[[1],[1],[1],[1],[1],[1],[1],[1],[1],[1]])

            self.my_node = nengo.Node(output=rad_value)

            nengo.Connection(self.my_node, self.neuron)

            self.input_probe = nengo.Probe(self.my_node)

            self.raw_probe = nengo.Probe(self.neuron.neurons)

            self.neurons_probe = nengo.Probe(self.neuron, synapse=0.01)

        self.sim = nengo.Simulator(self.model)


    def print_stuff(self):
        pp = PdfPages('multipage.pdf')

        # Plot the decoded output of the ensemble
        plt.plot(self.sim.trange(), self.sim.data[self.input_probe])
        plt.plot(self.sim.trange(), self.sim.data[self.neurons_probe])
        plt.xlim(0, 10)

        plt.savefig(pp, format='pdf')

        plt.figure(figsize=(10, 8))
        plt.subplot(221)
        rasterplot(self.sim.trange(), self.sim.data[self.raw_probe])
        plt.ylabel("Neuron")
        plt.xlim(0, 10)

        plt.savefig(pp, format='pdf')

        pp.close()


class Morse:
    x = 15.0
    y = 10.0
    go_on = True
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
            simu.robot.pose.subscribe(self.print_pos)

            simu.robot.laser.subscribe(self.print_laser)

            # sends a destination
            self.motion_publisher(simu)

            # Leave a couple of millisec to the simulator to start the action
            simu.sleep(0.1)

            # waits until we reach the target
            while self.go_on == True:
                if simu.robot.motion.get_status() == "Arrived":
                    self.direction = self.direction + 1

                    if self.direction == 1:
                        self.x = 25.0
                        self.motion_publisher(simu)

                    elif self.direction == 2:
                        self.y = -10.0
                        self.motion_publisher(simu)

                    elif self.direction == 3:
                        self.x = 10.0
                        self.motion_publisher(simu)

                    elif self.direction > 3:
                        self.go_on = False

                for counter in range(0, 5000):
                    self.nengo_sim.sim.step()
                    self.zähler = self.zähler + 1

                simu.sleep(0.5)

            print("Here we are! \n")

            print("Python ms: %s \n" % self.zähler)

            act_time = time.time() - self.start_time

            print("Python s: %s \n" % act_time)


    def print_pos(self, pose):
        rad_value = pose.get('yaw')

        #if rad_value > 0:
         #   rad_value = 1
        #else:
        #    rad_value = 0

        number = random.random()

        if number < 0.5:
            rad_value = 0
        else:
            rad_value = 1

        self.nengo_sim.my_node.output = rad_value

        print("Yaaaaaw: %s \n" % rad_value)

        if self.firstset:
            self.secondstamp = pose.get('timestamp')
        else:
            self.firststamp = pose.get('timestamp')
            self.firstset = True


    def print_laser(self, laser):
        print("Laser: %s \n" % laser)

    def motion_publisher(self, simulation):
        simulation.robot.motion.publish({'x': self.x, 'y': self.y, 'z': 0.0,
                                   'tolerance': 0.5,
                                   'speed': 1.0})






nengo_sim = Nengo()
morse_sim = Morse(nengo_sim)


print("Morse s: %s \n" % (morse_sim.secondstamp - morse_sim.firststamp))

nengo_sim.print_stuff()


#print(sim.data[neurons_probe][-10:])




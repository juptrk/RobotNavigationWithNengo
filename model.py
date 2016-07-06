import nengo
from nengo.dists import Uniform

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from nengo.utils.matplotlib import rasterplot



class Model:

    rad_value = 0
    model = 0
    sim = 0
    left_neuron = 0
    right_neuron = 0
    left = 0
    right = 0
    left_probe = 0
    right_probe = 0
    neurons_probe = 0
    left_connection = 0
    right_connection = 0
    left_connector_probe = 0
    right_connector_probe = 0
    left_raw_probe = 0
    right_raw_probe = 0

    def __init__(self):
        self.rad_value = 0

        self.model = nengo.Network(label = 'Morse - Nengo')

        with self.model:
            self.left_neuron = nengo.Ensemble(1, dimensions = 1,
                                         intercepts = Uniform(-.5, -.5),
                                         max_rates = Uniform(100, 100),
                                         encoders = [[1]])

            self.right_neuron = nengo.Ensemble(1, dimensions=1,
                                              intercepts=Uniform(-.5, -.5),
                                              max_rates=Uniform(100, 100),
                                              encoders=[[-1]])

            self.left = nengo.Node(output = 1.0)
            self.right = nengo.Node(output = 1.0)

            self.left_connection = nengo.Connection(self.left, self.left_neuron, function = self.output_left)
            self.right_connection = nengo.Connection(self.right, self.right_neuron, function = self.output_left)

            self.left_probe = nengo.Probe(self.left)
            self.right_probe = nengo.Probe(self.right)

            self.left_neuron_probe = nengo.Probe(self.left_neuron, synapse=0.01)
            self.right_neuron_probe = nengo.Probe(self.right_neuron, synapse=0.01)

            self.left_connector_probe = nengo.Probe(self.left_connection)
            self.right_connector_probe = nengo.Probe(self.right_connection)

            self.left_raw_probe = nengo.Probe(self.left_neuron.neurons)
            self.right_raw_probe = nengo.Probe(self.right_neuron.neurons)


        self.sim = nengo.Simulator(self.model)


    def output_left(self, x):
        number = self.get_rad_value() / 3.14159

        number = number * x[0]

        print("Yaaaaaw left: %s \n" % number)

        return number


    def output_right(self,x):
        number = self.get_rad_value() / 3.14159

        number = number * x[0]

        print("Yaaaaaw right: %s \n" % number)

        return number


    def print_stuff(self, limit):
        pp = PdfPages('LeftNeuron.pdf')

        # Plot the decoded output of the ensemble
        plt.figure(figsize=(10, 8))
        plt.plot(self.sim.trange(), self.sim.data[self.left_neuron_probe], label = 'Left Neuron')
        plt.plot(self.sim.trange(), self.sim.data[self.left_connector_probe], label = 'Left')
        plt.legend()
        plt.xlim(0, limit)
        plt.ylim(-1.1, 3)

        plt.savefig(pp, format='pdf')

        pp.close()

        pp = PdfPages('RightNeuron.pdf')

        plt.figure(figsize=(10, 8))
        plt.plot(self.sim.trange(), self.sim.data[self.right_neuron_probe], label='Right Neuron')
        plt.plot(self.sim.trange(), self.sim.data[self.right_connector_probe], label = 'Right')
        plt.legend()
        plt.xlim(0, limit)
        plt.ylim(-1.1,3)

        plt.savefig(pp, format='pdf')

        pp.close()

        pp = PdfPages('LeftRaw.pdf')

        plt.figure(figsize=(10, 8))
        plt.subplot(221)
        rasterplot(self.sim.trange(), self.sim.data[self.left_raw_probe])
        plt.ylabel("Left_Neuron")
        plt.xlim(0, limit)

        plt.savefig(pp, format='pdf')

        pp.close()

        pp = PdfPages('RightRaw.pdf')

        plt.figure(figsize=(10, 8))
        plt.subplot(221)
        rasterplot(self.sim.trange(), self.sim.data[self.right_raw_probe])
        plt.ylabel("Right_Neuron")
        plt.xlim(0, limit)

        plt.savefig(pp, format='pdf')

        pp.close()


    def run_steps(self, steps):
        self.sim.run_steps(steps, progress_bar=False)

    def set_rad_value(self, value):
        self.rad_value = self.rad_value + value

    def get_rad_value(self):
        return self.rad_value

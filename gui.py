import tkinter as tk

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_pdf import PdfPages
from nengo.utils.matplotlib import rasterplot
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure


class Gui():
    def __init__(self, master, nengo, limit):
        self.f = Figure(figsize=(11, 10), dpi=80)
        self.ax0 = self.f.add_axes((0.05, .05, .4, .4), axisbg=(.75, .75, .75), frameon=True)
        self.ax1 = self.f.add_axes((0.05, .55, .4, .4), axisbg=(.75, .75, .75), frameon=True)

        self.ax0.set_xlabel('Time (s)')
        self.ax0.set_ylabel('Reaction')
        self.ax0.plot(nengo.sim.trange(), nengo.sim.data[nengo.left_neuron_probe], label = 'Left Neuron')
        self.ax0.plot(nengo.sim.trange(), nengo.sim.data[nengo.left_connector_probe], label = 'Left')
        self.ax0.legend()

        self.ax1.set_xlabel('Time (s)')
        self.ax1.set_ylabel('Reaction')
        self.ax1.plot(nengo.sim.trange(), nengo.sim.data[nengo.right_neuron_probe], label = 'Right Neuron')
        self.ax1.plot(nengo.sim.trange(), nengo.sim.data[nengo.right_connector_probe], label = 'Right')
        self.ax1.legend()

        self.frame = tk.Frame(master)
        self.frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        self.canvas = FigureCanvasTkAgg(self.f, master=self.frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5, expand=1)
        self.canvas.show()

        self.toolbar = NavigationToolbar2TkAgg(self.canvas, self.frame)
        self.toolbar.pack()
        self.toolbar.update()
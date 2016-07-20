import tkinter as tk

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from nengo.utils.matplotlib import rasterplot


class Gui():
    def __init__(self, master, nengo, limit):
        self.f = Figure(figsize=(16, 10), dpi=80)
        self.ax0 = self.f.add_axes((.05, .55, .275, .4), axisbg=(.75, .75, .75), frameon=True)
        self.ax1 = self.f.add_axes((.375, .55, .275, .4), axisbg=(.75, .75, .75), frameon=True)
        self.ax2 = self.f.add_axes((.05, .05, .275, .4), axisbg=(.75, .75, .75), frameon=True)
        self.ax3 = self.f.add_axes((.375, .05, .275, .4), axisbg=(.75, .75, .75), frameon=True)
        self.ax4 = self.f.add_axes((.7, .55, .275, .4),  axisbg=(.75, .75, .75), frameon=True)
        self.ax5 = self.f.add_axes((.7, .05, .275, .4),  axisbg=(.75, .75, .75), frameon=True)


        self.ax0.set_xlabel('Time (s)')
        self.ax0.set_ylabel('Reaction')
        self.ax0.set_ylim(-2,2)
        self.ax0.plot(nengo.sim.trange(), nengo.sim.data[nengo.left_neuron_probe], label = 'Left Neurons')
        self.ax0.plot(nengo.sim.trange(), nengo.sim.data[nengo.left_con_probe], label = 'Input')
        self.ax0.legend()

        self.ax1.set_xlabel('Time (s)')
        self.ax1.set_ylabel('Reaction')
        self.ax1.set_ylim(-2,2)
        self.ax1.plot(nengo.sim.trange(), nengo.sim.data[nengo.right_neuron_probe], label = 'Right Neurons')
        self.ax1.plot(nengo.sim.trange(), nengo.sim.data[nengo.right_con_probe], label = 'Input')
        self.ax1.legend()

        self.ax2.set_xlabel('Time (s)')
        self.ax2.set_ylabel('Reaction')
        self.ax2.set_ylim(-2,2)
        self.ax2.plot(nengo.sim.trange(), nengo.sim.data[nengo.left_neuron_changes_probe], label = 'Left Neurons')
        self.ax2.plot(nengo.sim.trange(), nengo.sim.data[nengo.left_changes_probe], label = 'Input Change')
        self.ax2.legend()

        self.ax3.set_xlabel('Time (s)')
        self.ax3.set_ylabel('Reaction')
        self.ax3.set_ylim(-2,2)
        self.ax3.plot(nengo.sim.trange(), nengo.sim.data[nengo.right_neuron_changes_probe], label = 'Right Neurons')
        self.ax3.plot(nengo.sim.trange(), nengo.sim.data[nengo.right_changes_probe], label = 'Input Change')
        self.ax3.legend()

        self.ax4.set_xlabel('Time (s)')
        self.ax4.set_ylabel('Reaction')
        self.ax4.set_ylim(0, 5)
        self.ax4.plot(nengo.sim.trange(), nengo.sim.data[nengo.mover_neuron_probe], label = 'Mover Neurons')
        self.ax4.plot(nengo.sim.trange(), nengo.sim.data[nengo.mover_con_probe], label = 'Moves')
        self.ax4.legend()

        self.ax5.set_xlabel('Time (s)')
        self.ax5.set_ylabel('Reaction')
        self.ax5.set_ylim(-2,2)
        self.ax5.plot(nengo.sim.trange(), nengo.sim.data[nengo.speed_neuron_probe], label = 'Speed Neurons')
        self.ax5.plot(nengo.sim.trange(), nengo.sim.data[nengo.trans_speed_con_probe], label = 'Trans')
        self.ax5.plot(nengo.sim.trange(), nengo.sim.data[nengo.rot_speed_con_probe], label = 'Rot')
        self.ax5.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05), ncol=3, fancybox=True, shadow=True)

        self.frame = tk.Frame(master)
        self.frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        self.canvas = FigureCanvasTkAgg(self.f, master=self.frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5, expand=1)
        self.canvas.show()

        self.toolbar = NavigationToolbar2TkAgg(self.canvas, self.frame)
        self.toolbar.pack()
        self.toolbar.update()
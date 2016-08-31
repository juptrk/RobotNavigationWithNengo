import tkinter as tk

from tkinter import Tk, Frame, Canvas, Scrollbar
from tkinter.constants import NSEW, HORIZONTAL, EW, NS, ALL

from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D


class Gui():

    f = 0

    def __init__(self, master, nengo):
        master.rowconfigure(0, weight=1)
        master.columnconfigure(0, weight=1)

        self.frame = tk.Frame(master)
        self.frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        self.frame.grid(sticky=NSEW)
        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)

        self.scroll_canvas = Canvas(self.frame)
        self.scroll_canvas.grid(row=0, column=0, sticky=NSEW)

        xScrollbar = Scrollbar(self.frame, orient=HORIZONTAL)
        yScrollbar = Scrollbar(self.frame)

        xScrollbar.grid(row=1, column=0, sticky=EW)
        yScrollbar.grid(row=0, column=1, sticky=NS)

        self.scroll_canvas.config(xscrollcommand=xScrollbar.set)
        xScrollbar.config(command=self.scroll_canvas.xview)
        self.scroll_canvas.config(yscrollcommand=yScrollbar.set)
        yScrollbar.config(command=self.scroll_canvas.yview)

        self.create_plot(nengo)

        self.figure_canvas = FigureCanvasTkAgg(self.f, master=self.scroll_canvas)
        self.canvas = self.figure_canvas.get_tk_widget()
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5, expand=1)

        self.scroll_canvas.create_window(0, 0, window=self.canvas)
        self.scroll_canvas.config(scrollregion=self.scroll_canvas.bbox(ALL))
        self.figure_canvas.show()

        self.toolbar = NavigationToolbar2TkAgg(self.figure_canvas, self.scroll_canvas)
        self.toolbar.pack()
        self.toolbar.update()


    def create_plot(self, nengo):
        self.f = Figure(figsize=(20, 9), dpi=80)

        self.ax0 = self.f.add_axes((.025, .55, .21, .4), axisbg=(.75, .75, .75), frameon=True)
        self.ax1 = self.f.add_axes((.275, .55, .21, .4), axisbg=(.75, .75, .75), frameon=True)
        self.ax2 = self.f.add_axes((.275, .05, .21, .4), axisbg=(.75, .75, .75), frameon=True)
        self.ax3 = self.f.add_axes((.525, .55, .21, .4), axisbg=(.75, .75, .75), frameon=True)
        self.ax3 = self.f.add_axes((.525, .05, .21, .4), axisbg=(.75, .75, .75), frameon=True)



        self.ax0.set_xlabel('Time (s)')
        self.ax0.set_ylabel('Reaction')
        self.ax0.plot(nengo.sim.trange(), nengo.sim.data[nengo.mover_neuron_probe], label = 'Mover Neurons')
        self.ax0.plot(nengo.sim.trange(), nengo.sim.data[nengo.mover_con_probe], label = 'Moves')
        #self.ax0.legend()

        self.ax1.plot(nengo.sim.data[nengo.position_neuron_probe][:, 0],
                nengo.sim.data[nengo.position_neuron_probe][:, 1])
        #self.ax1.legend()

        self.ax2.set_xlabel('Time (s)')
        self.ax2.set_ylabel('Reaction')
        self.ax2.plot(nengo.sim.trange(), nengo.sim.data[nengo.position_neuron_probe], label='Position Dimensions')
        self.ax2.plot(nengo.sim.trange(), nengo.sim.data[nengo.position_connection_probe], label='Input')
        #self.ax2.legend()

        self.ax3.plot(nengo.sim.data[nengo.velocity_neuron_probe][:, 0],
                nengo.sim.data[nengo.velocity_neuron_probe][:, 1])
        #self.ax1.legend()

        self.ax4.set_xlabel('Time (s)')
        self.ax4.set_ylabel('Reaction')
        self.ax4.plot(nengo.sim.trange(), nengo.sim.data[nengo.velocity_neuron_probe], label='Velocity Dimensions')
        self.ax4.plot(nengo.sim.trange(), nengo.sim.data[nengo.velocity_connection_probe], label='Input')
        # self.ax2.legend()

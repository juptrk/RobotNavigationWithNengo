__author__ = "Julian Petruck"

import tkinter as tk

import matplotlib
matplotlib.use("TkAgg")

from tkinter import Canvas, Scrollbar
from tkinter.constants import NSEW, HORIZONTAL, EW, NS, ALL
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure

class GUI():

    """
    Method gets a Tk instance (master) and a model instance implemented with nengo.
    It then creates a GUI with the polts that where specified in create_plot(...).
    """

    def __init__(self, master, model):
        self.f = 0

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

        self.create_plot(model)

        self.figure_canvas = FigureCanvasTkAgg(self.f, master=self.scroll_canvas)
        self.canvas = self.figure_canvas.get_tk_widget()
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, padx=5, pady=5, expand=1)

        self.scroll_canvas.create_window(0, 0, window=self.canvas)
        self.scroll_canvas.config(scrollregion=self.scroll_canvas.bbox(ALL))
        self.figure_canvas.show()

        self.toolbar = NavigationToolbar2TkAgg(self.figure_canvas, self.scroll_canvas)
        self.toolbar.pack()
        self.toolbar.update()

        """
        Adds the specified plots to the figure displayed in the GUI. It gets a model instance implemented with nengo
        """
    def create_plot(self, model):

        self.f = Figure(figsize=(16, 9), dpi=80)

        """
        Example plot which plots the integrators back connection, its input, its real value and the real robot goal angle
        """
        self.ax00 = self.f.add_axes((.2, .2, .6, .6), axisbg=(.75, .75, .75), frameon=True)
        self.ax00.plot(model.sim.trange(), model.sim.data[model.integrator_probe], label = 'Integrator')
        self.ax00.plot(model.sim.trange(), model.sim.data[model.integrator_connection_probe], label = 'Con')
        self.ax00.plot(model.sim.trange(), model.sim.data[model.integrator_self_connection_probe], label = 'Self Con')
        self.ax00.plot(model.sim.trange(), model.sim.data[model.robot_goal_neuron_probe][:, 2], label = 'Real')
        self.ax00.legend()



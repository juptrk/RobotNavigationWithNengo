import tkinter as tk

from tkinter import Tk, Frame, Canvas, Scrollbar
from tkinter.constants import NSEW, HORIZONTAL, EW, NS, ALL

from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure


class Gui():

    f = 0

    def __init__(self, master, nengo, limit):
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

        #self.ax0 = self.f.add_axes((.025, .55, .21, .4), axisbg=(.75, .75, .75), frameon=True)

        #self.ax0.set_xlabel('Time (s)')
        #self.ax0.set_ylabel('Reaction')
        #self.ax0.set_ylim(-2, 2)
        #self.ax0.plot(nengo.sim.trange(), nengo.sim.data[nengo.mover_neuron_probe], label = 'Mover Neurons')
        #self.ax0.plot(nengo.sim.trange(), nengo.sim.data[nengo.mover_con_probe], label = 'Moves')
        #self.ax0.legend()


        # self.ax0 = self.f.add_axes((.025, .55, .21, .4), axisbg=(.75, .75, .75), frameon=True)
        # self.ax1 = self.f.add_axes((.275, .55, .21, .4), axisbg=(.75, .75, .75), frameon=True)
        # self.ax2 = self.f.add_axes((.025, .05, .21, .4), axisbg=(.75, .75, .75), frameon=True)
        # self.ax3 = self.f.add_axes((.275, .05, .21, .4), axisbg=(.75, .75, .75), frameon=True)
        # self.ax4 = self.f.add_axes((.525, .55, .21, .4), axisbg=(.75, .75, .75), frameon=True)
        # self.ax5 = self.f.add_axes((.527, .05, .21, .4), axisbg=(.75, .75, .75), frameon=True)
        # self.ax6 = self.f.add_axes((.775, .55, .21, .4), axisbg=(.75, .75, .75), frameon=True)
        # self.ax7 = self.f.add_axes((.775, .05, .21, .4), axisbg=(.75, .75, .75), frameon=True)
        #
        # self.ax0.set_xlabel('Time (s)')
        # self.ax0.set_ylabel('Reaction')
        # self.ax0.set_ylim(-2, 2)
        # self.ax0.plot(nengo.sim.trange(), nengo.sim.data[nengo.left_neuron_probe], label='Left Neurons')
        # self.ax0.plot(nengo.sim.trange(), nengo.sim.data[nengo.left_con_probe], label='Input')
        # self.ax0.legend()
        #
        # self.ax1.set_xlabel('Time (s)')
        # self.ax1.set_ylabel('Reaction')
        # self.ax1.set_ylim(-2, 2)
        # self.ax1.plot(nengo.sim.trange(), nengo.sim.data[nengo.right_neuron_probe], label='Right Neurons')
        # self.ax1.plot(nengo.sim.trange(), nengo.sim.data[nengo.right_con_probe], label='Input')
        # self.ax1.legend()
        #
        # self.ax2.set_xlabel('Time (s)')
        # self.ax2.set_ylabel('Reaction')
        # self.ax2.set_ylim(-2, 2)
        # self.ax2.plot(nengo.sim.trange(), nengo.sim.data[nengo.left_changes_neuron_probe], label='Left Neurons')
        # self.ax2.plot(nengo.sim.trange(), nengo.sim.data[nengo.left_changes_probe], label='Input Change')
        # self.ax2.legend()
        #
        # self.ax3.set_xlabel('Time (s)')
        # self.ax3.set_ylabel('Reaction')
        # self.ax3.set_ylim(-2, 2)
        # self.ax3.plot(nengo.sim.trange(), nengo.sim.data[nengo.right_changes_neuron_probe], label='Right Neurons')
        # self.ax3.plot(nengo.sim.trange(), nengo.sim.data[nengo.right_changes_probe], label='Input Change')
        # self.ax3.legend()
        #
        # self.ax4.set_xlabel('Time (s)')
        # self.ax4.set_ylabel('Reaction')
        # self.ax4.set_ylim(0, 5)
        # self.ax4.plot(nengo.sim.trange(), nengo.sim.data[nengo.mover_neuron_probe], label = 'Mover Neurons')
        # self.ax4.plot(nengo.sim.trange(), nengo.sim.data[nengo.mover_con_probe], label = 'Moves')
        # self.ax4.legend()
        #
        # self.ax4.set_xlabel('Time (s)')
        # self.ax4.set_ylabel('Reaction')
        # self.ax4.set_ylim(0, 4.5)
        # self.ax4.plot(nengo.sim.trange(), nengo.sim.data[nengo.max_distance_neuron_probe], label='max Neurons')
        # self.ax4.plot(nengo.sim.trange(), nengo.sim.data[nengo.min_distance_neuron_probe], label='min Neurons')
        # self.ax4.plot(nengo.sim.trange(), nengo.sim.data[nengo.max_distance_con_probe], label='Max')
        # self.ax4.plot(nengo.sim.trange(), nengo.sim.data[nengo.min_distance_con_probe], label='Min')
        # self.ax4.legend(loc='upper center', bbox_to_anchor=(0.45, 1.05), ncol=3, fancybox=True, shadow=True)
        #
        # self.ax5.set_xlabel('Time (s)')
        # self.ax5.set_ylabel('Reaction')
        # self.ax5.set_ylim(-2, 2)
        # self.ax5.plot(nengo.sim.trange(), nengo.sim.data[nengo.trans_speed_neuron_probe], label='trans Neurons')
        # self.ax5.plot(nengo.sim.trange(), nengo.sim.data[nengo.rot_speed_neuron_probe], label='rot Neurons')
        # self.ax5.plot(nengo.sim.trange(), nengo.sim.data[nengo.trans_speed_con_probe], label='Trans')
        # self.ax5.plot(nengo.sim.trange(), nengo.sim.data[nengo.rot_speed_con_probe], label='Rot')
        # self.ax5.legend(loc='upper center', bbox_to_anchor=(0.45, 1.05), ncol=3, fancybox=True, shadow=True)
        #
        # self.ax6.set_xlabel('Time (s)')
        # self.ax6.set_ylabel('Reaction')
        # self.ax6.set_ylim(0, 4.5)
        # self.ax6.plot(nengo.sim.trange(), nengo.sim.data[nengo.x_act_neuron_probe], label='act Neurons')
        # self.ax6.plot(nengo.sim.trange(), nengo.sim.data[nengo.x_fut_neuron_probe], label='fut Neurons')
        # self.ax6.plot(nengo.sim.trange(), nengo.sim.data[nengo.x_act_con_probe], label='act x')
        # self.ax6.plot(nengo.sim.trange(), nengo.sim.data[nengo.x_fut_con_probe], label='fut x')
        # self.ax6.legend(loc='upper center', bbox_to_anchor=(0.45, 1.05), ncol=3, fancybox=True, shadow=True)
        #
        # self.ax7.set_xlabel('Time (s)')
        # self.ax7.set_ylabel('Reaction')
        # self.ax7.set_ylim(0, 4.5)
        # self.ax7.plot(nengo.sim.trange(), nengo.sim.data[nengo.y_act_neuron_probe], label='act Neurons')
        # self.ax7.plot(nengo.sim.trange(), nengo.sim.data[nengo.y_fut_neuron_probe], label='fut Neurons')
        # self.ax7.plot(nengo.sim.trange(), nengo.sim.data[nengo.y_act_con_probe], label='act x')
        # self.ax7.plot(nengo.sim.trange(), nengo.sim.data[nengo.y_fut_con_probe], label='fut x')
        # self.ax7.legend(loc='upper center', bbox_to_anchor=(0.45, 1.05), ncol=3, fancybox=True, shadow=True)

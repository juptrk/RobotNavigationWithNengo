__author__ = "Julian Petruck"

import model
import robot
import dwa
import gui
import tkinter as tk

"""
Initializes a model instance
"""
model = model.Model()

"""
Initilizes an instance of the DWA class (Dynamic Window Approach)
"""
#model = dwa.DWA()

"""
Initializes an instance of the robot - the model created above is given.
This does also start the simulation.
"""
robot = robot.Robot(model)

"""
Opens up a GUI which shows some graphs for the simulated model.
Which data is shown must be specified in the GUI class.
"""
# if __name__ == '__main__':
#     root = tk.Tk()
#     app = gui.GUI(root, nengo_sim)
#     root.title("MatplotLib with Tkinter")
#     root.update()
#     root.deiconify()
#     root.mainloop()





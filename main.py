import tkinter as tk
import dwa

import model
import gui
import robot

nengo_sim = model.Model()
morse_sim = robot.Robot(nengo_sim)


print("Morse s: %s \n" % (morse_sim.secondstamp - morse_sim.firststamp))

#nengo_sim.print_stuff(limit)

if __name__ == '__main__':
    root = tk.Tk()
    app = gui.Gui(root, nengo_sim)
    root.title("MatplotLib with Tkinter")
    root.update()
    root.deiconify()
    root.mainloop()


#print(sim.data[neurons_probe][-10:])




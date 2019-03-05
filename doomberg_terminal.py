#The main code to run

from Tkinter import *
import terminal

root = Tk()
root.minsize(500,100)
myThing = terminal.stockClass(root)

root.mainloop()
from tkinter import *
from tkinter.ttk import *

from time import strftime

def time():
    string = strftime('%H:%M:%S %p')
    Label.config(text=string)
    Label.after(1000,time)

root= Tk()
root.title("clock")
Label = Label(root , font=("ds-digital", 80 ), background = "black" , foreground ="red")
Label.pack(anchor='center')
time()
mainloop()
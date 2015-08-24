try:
    # for Python2
    import Tkinter as tk
except ImportError:
    # for Python3
    import tkinter as tk
from projectBot import genDefaultOptions as gdo
from projectBot import create_project as cp
from projectBot import getTemplateList as gtl
import logging

class pbgui():

    logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')

    def __init__(self, win):
        self.main = win
        self.frame = tk.Frame(self.main).grid(row=0, column=0)

        self.o = gdo()

        templates = gtl() #get template options

        self.nameVar = tk.StringVar()
        self.templateVar = tk.StringVar(self.frame)
        self.templateVar.set(templates[0]) #default value

        l0 = tk.Label(self.frame, text="Name: ").grid(row=0, column=0)
        e0 = tk.Entry(self.frame, textvariable=self.nameVar).grid(row=0, column=1)
        l1 = tk.Label(self.frame, text="Template: ").grid(row=1, column=0)

        o0 = tk.OptionMenu(self.frame, self.templateVar, *templates).grid(row=1, column=1)
        
        b0 = tk.Button(self.frame, text="Generate", command=self.generate).grid(row=2, column = 2)

    def generate(self):
        n = self.nameVar.get()
        self.o['name'] = n
        logging.debug('NameVar : ' + n)
        self.nameVar.set("")

        t = self.templateVar.get()
        self.o['template_name'] = t
        logging.debug('TemplateVar : ' + t)

        cp(self.o)
        #self.main.destroy() #close the window
        #do more stuff               

win = tk.Tk()
win.title("Project-Bot")
gui = pbgui(win)
win.mainloop()

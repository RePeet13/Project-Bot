from tkinter import *
from projectBot import genDefaultOptions as gdo
from projectBot import create_project as cp
from projectBot import getTemplateList as gtl

class pbgui():

    def __init__(self, win):
        self.main = win
        self.frame = Frame(self.main).grid(row=0, column=0)

        self.o = gdo()
        # TODO this is a stopgap
        self.o['scm']='_stop_'

        templates = gtl() #get template options

        self.nameVar = StringVar()
        self.templateVar = StringVar(self.frame)
        self.templateVar.set(templates[0]) #default value

        l0 = Label(self.frame, text="Name: ").grid(row=0, column=0)
        e0 = Entry(self.frame, textvariable=self.nameVar).grid(row=0, column=1)
        l1 = Label(self.frame, text="Template: ").grid(row=1, column=0)

        o0 = OptionMenu(self.frame, self.templateVar, *templates).grid(row=1, column=1)
        
        b0 = Button(self.frame, text="Generate", command=self.generate()).grid(row=2, column = 2)

    def generate(self):
        self.o['name'] = self.nameVar.get()
        #self.nameVar.set("")
        self.o['template_name'] = self.templateVar.get()
        #self.templateVar().set("")
        cp(self.o)
        #self.main.destroy() #close the window
        #do more stuff               

win = Tk()
win.title("Project-Bot")
gui = pbgui(win)
win.mainloop()

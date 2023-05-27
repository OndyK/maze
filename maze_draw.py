import Translator
from tkinter import *

class Maze:
    def __init__(self):  
        self.canvas = None
        self.window = None  
        self.create_window()

    def create_window(self):
        self.window = Tk()
        self.window.geometry("800x450")
        self.window.title("Maze")
        self.canvas = Canvas(self.window, width = 800, height = 450)
        self.canvas.pack()
        start_program_button = Button(self.window, text = "Start_program", bg = "red")
        start_program_button.place(x = 550, y = 300, width = 230, height = 100)
        x = Label(self.window, text = "x position")
        y = Label(self.window, text = "y position")
        x.place(x = 540, y = 200, width = 80, height = 20)
        y.place(x = 540, y = 240, width = 80, height = 20)
        self.input_x = Entry(self.window)
        self.input_y = Entry(self.window)
        self.input_x.place(x = 640, y = 200, width = 40, height = 20)
        self.input_y.place(x = 640, y = 240, width = 40, height = 20)
        button = Button(self.window, text = "Enter", command = self.create_robot)
        button.place(x = 720, y = 220, width = 40, height = 20)
        lvl_button = Button(self.window, text = "Select Level", command = self.select_lvl)
        lvl_button.place(x = 560, y = 50, width = 210, height = 100)
        self.window.mainloop()
            
    def create_robot(self):
        if self.input_x.get()!= "" and self.input_y.get() != "":
            x = int(self.input_x.get())
            y = int(self.input_y.get())+1
            self.canvas.create_oval(20*x, 20*y, 20*x+20, 20*y+20)
    def select_lvl(self):
        self.Lvl_1 = Button(self.window, text = "Level 1", command = self.draw_level_1)
        self.Lvl_1.place(x = 225,y = 30, width = 100, height = 50)
        self.Lvl_2 = Button(self.window, text = "Level 2", command = self.draw_level_2)
        self.Lvl_2.place(x = 225, y = 110, width = 100, height = 50)
        self.Lvl_3 = Button(self.window, text = "Level 3", command = self.draw_level_3)
        self.Lvl_3.place(x = 225, y = 190, width = 100, height = 50)
        self.window.mainloop()
        
    def draw_level_1(self):
        pass

    def draw_level_2(self):
        pass

    def draw_level_3(self):
        pass

Maze()
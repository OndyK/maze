from Translator import *
from tkinter import *
from tkinter import filedialog
from path_finder import *

class Maze:
    def __init__(self):  
        self.canvas = None
        self.window = None 
        self.width = 450
        self.height = 450
        self.robot = None
        self.memory = []
        self.way = []
        self.end = None
        self.queue = []
        self.root = None
        self.previous = None
        self.warning_txt = None
        self.error_txt = None
        self.walked = []
        self.lvl = None
        self.bcanvas_width = 150
        self.bcanvas_height = 150
        self.create_window()

    def create_window(self):
        #create window interface
        self.window = Tk()
        self.window.geometry("800x450")
        self.window.title("Maze")
        self.canvas = Canvas(self.window, width = self.width, height = self.height)
        self.canvas.pack(side = LEFT)
        self.start_program_button = Button(self.window, text = "Start program", bg = "red", command = self.go_robot)
        self.start_program_button.place(x = 550, y = 300, width = 230, height = 100)
        x = Label(self.window, text = "x position")
        y = Label(self.window, text = "y position")
        place_robot_txt = Label(self.window, text = "Place robot:", fg = "red")
        place_robot_txt.place(x = 545, y = 160, width = 80, height = 40)
        x.place(x = 540, y = 200, width = 80, height = 20)
        y.place(x = 540, y = 240, width = 80, height = 20)
        self.input_x = Entry(self.window)
        self.input_y = Entry(self.window)
        self.input_x.place(x = 640, y = 200, width = 40, height = 20)
        self.input_y.place(x = 640, y = 240, width = 40, height = 20)
        self.enter_button = Button(self.window, text = "Enter", command = self.create_robot)
        self.enter_button.place(x = 720, y = 220, width = 40, height = 20)
        self.lvl_button = Button(self.window, text = "Select Level", command = self.select_lvl)
        self.lvl_button.place(x = 560, y = 50, width = 210, height = 100)
        self.exit = Button(self.window, text = "Exit", command = self.window.destroy)
        self.exit.place(x = 625, y = 420, width = 70, height = 20)
        self.window.mainloop()
            
    def create_robot(self):
        if self.error_txt != None:
            self.error_txt.destroy()
        #checks if you can place robot and create it
        if self.warning_txt != None:
            self.warning_txt.destroy()
        if self.robot != None:
             self.canvas.delete(self.robot)
        try:
            int(self.input_x.get())
            int(self.input_y.get())
            if int(self.input_x.get()) != 0:
                x = int(self.input_x.get())-1
            else:
                x = int(self.input_x.get())
            if int(self.input_y.get()) != 0:
                y = int(self.input_y.get())-1
            else:
                y = int(self.input_y.get())
            if int(self.input_x.get()) >= 0 and int(self.input_y.get()) >= 0:
                self.robot = self.canvas.create_oval(x*(self.width/self.width_lvl), y*(self.height/self.height_lvl),x*(self.width/self.width_lvl)+(self.width/self.width_lvl), y*(self.height/self.height_lvl)+(self.height/self.height_lvl), fill = "blue")
            else:
                 self.error("Input numbers greater than zero")
        except ValueError:
            self.error("Please input numbers whole numbers")    
             
    def select_lvl(self):
        if self.error_txt != None:
            self.error_txt.destroy()
        try:
            self.destroy_texts()
        except AttributeError:
            pass
        #create lvl buttons
        self.canvas.delete("all")
        self.lvl = None
        self.Lvl_1 = Button(self.window, text = "Level 1", command = self.preview_level_1)
        self.Lvl_1.place(x = 225,y = 30, width = 100, height = 50)
        self.Lvl_2 = Button(self.window, text = "Level 2", command = self.preview_level_2)
        self.Lvl_2.place(x = 225, y = 110, width = 100, height = 50)
        self.Lvl_3 = Button(self.window, text = "Level 3", command = self.preview_level_3)
        self.Lvl_3.place(x = 225, y = 190, width = 100, height = 50)
        self.own_lvl = Button(self.window, text = "Own level", command = self.own_level_preview)
        self.own_lvl.place(x = 225, y = 270, width = 100, height = 50)
        self.window.mainloop()
    
    def own_level_preview(self):
        self.disable_edit()
        self.Lvl_1.destroy()
        self.Lvl_2.destroy()
        self.Lvl_3.destroy()
        self.own_lvl.destroy()
        level_path = filedialog.askopenfilename(title = "Open a text file",filetypes =(("text   files","*.txt"), ("all   files","*.*")))
        self.lvl = Translator().return_maze(level_path)
        self.bcanvas = Canvas(self.window, height = 160, width = 160)
        self.bcanvas.place(x = 280, y = 150)
        width_list = []
        for i in self.lvl[0]:
            if i == "0" or i == "1" or i == "2":
                width_list.append(i)
        exits = []
        for y in range(len(self.lvl)):
            x = 0
            for x in range(len(self.lvl[y])):
                if self.lvl[y][x] == "2":
                    exits.append(1)
        self.height_lvl = len(self.lvl)
        self.width_lvl = len(width_list)
        self.preview_txt = Label(self.window, text = "MAZE 1", font = "Helvetica 25 bold", fg = "blue")
        self.preview_txt.place(x = 175, y = 10, width = 200, height = 100)
        self.info = Label(self.window, text = "This is level 1 Maze\n parameters:\n width: {fwidth}\n height: {fheight}\n number of exits: {fexits}".format(fwidth = self.width_lvl, fheight = self.height_lvl, fexits = len(exits)), font = "Helvetica 16")
        self.info.place(x = 10, y = 100, width = 200, height = 200)
        self.select_button = Button(self.window, text = "Select", command = self.draw_level) 
        self.select_button.place(x = 70, y = 310, width = 80, height = 40)
        for y in range(len(self.lvl)):
            x = 0
            for x in range(len(self.lvl[y])):
                if self.lvl[y][x] == "0":
                    self.bcanvas.create_rectangle(x*(self.bcanvas_width/self.width_lvl)+10, y*(self.bcanvas_height/self.height_lvl)+10,x*(self.bcanvas_width/self.width_lvl)+10 + (self.bcanvas_width/self.width_lvl),  y*(self.bcanvas_height/self.height_lvl)+10 + (self.bcanvas_height/self.height_lvl))
                elif self.lvl[y][x] == "1":
                     self.bcanvas.create_rectangle(x*(self.bcanvas_width/self.width_lvl)+10, y*(self.bcanvas_height/self.height_lvl)+10,x*(self.bcanvas_width/self.width_lvl)+10 + (self.bcanvas_width/self.width_lvl),  y*(self.bcanvas_height/self.height_lvl)+10 + (self.bcanvas_height/self.height_lvl), fill = "black")
                elif self.lvl[y][x] == "2":
                     self.bcanvas.create_rectangle(x*(self.bcanvas_width/self.width_lvl)+10, y*(self.bcanvas_height/self.height_lvl)+10,x*(self.bcanvas_width/self.width_lvl)+10 + (self.bcanvas_width/self.width_lvl),  y*(self.bcanvas_height/self.height_lvl)+10 + (self.bcanvas_height/self.height_lvl), fill = "red")
    
    def draw_level(self):
        self.enable_edit()
        self.destroy_texts()
        for y in range(len(self.lvl)):
            x = 0
            for x in range(len(self.lvl[y])):
                if self.lvl[y][x] == "0":
                    self.canvas.create_rectangle(x*(self.width/self.width_lvl), y*(self.height/self.height_lvl),x*(self.width/self.width_lvl) + (self.width/self.width_lvl),  y*(self.height/self.height_lvl) + (self.height/self.height_lvl))
                elif self.lvl[y][x] == "1":
                     self.canvas.create_rectangle(x*(self.width/self.width_lvl), y*(self.height/self.height_lvl),x*(self.width/self.width_lvl) + (self.width/self.width_lvl),  y*(self.height/self.height_lvl) + (self.height/self.height_lvl), fill = "black")
                elif self.lvl[y][x] == "2":
                     self.canvas.create_rectangle(x*(self.width/self.width_lvl), y*(self.height/self.height_lvl),x*(self.width/self.width_lvl) + (self.width/self.width_lvl),  y*(self.height/self.height_lvl) + (self.height/self.height_lvl), fill = "red")
    
    def preview_level_1(self):
        self.disable_edit()
        self.Lvl_1.destroy()
        self.Lvl_2.destroy()
        self.Lvl_3.destroy()
        self.own_lvl.destroy()
        self.bcanvas = Canvas(self.window, height = 160, width = 160)
        self.bcanvas.place(x = 280, y = 150)
        self.lvl = Translator().return_maze(r"LVL_1.txt")
        self.preview_txt = Label(self.window, text = "MAZE 1", font = "Helvetica 25 bold", fg = "blue")
        self.preview_txt.place(x = 175, y = 10, width = 200, height = 100)
        self.info = Label(self.window, text = "This is level 1 Maze\n parameters:\n width: 4\n height: 4\n number of exits: 1", font = "Helvetica 16")
        self.info.place(x = 10, y = 100, width = 200, height = 200)
        self.select_button = Button(self.window, text = "Select", command = self.draw_level) 
        self.select_button.place(x = 70, y = 310, width = 80, height = 40)
        width_list = []
        for i in self.lvl[0]:
            if i == "0" or i == "1" or i == "2":
                width_list.append(i)
        self.height_lvl = len(self.lvl)
        self.width_lvl = len(width_list)
        for y in range(len(self.lvl)):
            x = 0
            for x in range(len(self.lvl[y])):
                if self.lvl[y][x] == "0":
                    self.bcanvas.create_rectangle(x*(self.bcanvas_width/self.width_lvl)+10, y*(self.bcanvas_height/self.height_lvl)+10,x*(self.bcanvas_width/self.width_lvl)+10 + (self.bcanvas_width/self.width_lvl),  y*(self.bcanvas_height/self.height_lvl)+10 + (self.bcanvas_height/self.height_lvl))
                elif self.lvl[y][x] == "1":
                     self.bcanvas.create_rectangle(x*(self.bcanvas_width/self.width_lvl)+10, y*(self.bcanvas_height/self.height_lvl)+10,x*(self.bcanvas_width/self.width_lvl)+10 + (self.bcanvas_width/self.width_lvl),  y*(self.bcanvas_height/self.height_lvl)+10 + (self.bcanvas_height/self.height_lvl), fill = "black")
                elif self.lvl[y][x] == "2":
                     self.bcanvas.create_rectangle(x*(self.bcanvas_width/self.width_lvl)+10, y*(self.bcanvas_height/self.height_lvl)+10,x*(self.bcanvas_width/self.width_lvl)+10 + (self.bcanvas_width/self.width_lvl),  y*(self.bcanvas_height/self.height_lvl)+10 + (self.bcanvas_height/self.height_lvl), fill = "red")

    def preview_level_2(self):
        self.Lvl_1.destroy()
        self.Lvl_2.destroy()
        self.Lvl_3.destroy()
        self.own_lvl.destroy()
        self.disable_edit()
        self.bcanvas = Canvas(self.window, height = 160, width = 160)
        self.bcanvas.place(x = 280, y = 150)
        self.lvl = Translator().return_maze(r"LVL_2.txt")
        self.preview_txt = Label(self.window, text = "MAZE 2", font = "Helvetica 25 bold", fg = "blue")
        self.preview_txt.place(x = 175, y = 10, width = 200, height = 100)
        self.info = Label(self.window, text = "This is level 2 Maze\n parameters:\n width: 6\n height: 6\n number of exits: 1", font = "Helvetica 16")
        self.info.place(x = 10, y = 100, width = 200, height = 200)
        self.select_button = Button(self.window, text = "Select", command = self.draw_level) 
        self.select_button.place(x = 70, y = 310, width = 80, height = 40)
        width_list = []
        for i in self.lvl[0]:
            if i == "0" or i == "1" or i == "2":
                width_list.append(i)
        self.height_lvl = len(self.lvl)
        self.width_lvl = len(width_list)
        for y in range(len(self.lvl)):
            x = 0
            for x in range(len(self.lvl[y])):
                if self.lvl[y][x] == "0":
                    self.bcanvas.create_rectangle(x*(self.bcanvas_width/self.width_lvl)+10, y*(self.bcanvas_height/self.height_lvl)+10,x*(self.bcanvas_width/self.width_lvl)+10 + (self.bcanvas_width/self.width_lvl),  y*(self.bcanvas_height/self.height_lvl)+10 + (self.bcanvas_height/self.height_lvl))
                elif self.lvl[y][x] == "1":
                     self.bcanvas.create_rectangle(x*(self.bcanvas_width/self.width_lvl)+10, y*(self.bcanvas_height/self.height_lvl)+10,x*(self.bcanvas_width/self.width_lvl)+10 + (self.bcanvas_width/self.width_lvl),  y*(self.bcanvas_height/self.height_lvl)+10 + (self.bcanvas_height/self.height_lvl), fill = "black")
                elif self.lvl[y][x] == "2":
                     self.bcanvas.create_rectangle(x*(self.bcanvas_width/self.width_lvl)+10, y*(self.bcanvas_height/self.height_lvl)+10,x*(self.bcanvas_width/self.width_lvl)+10 + (self.bcanvas_width/self.width_lvl),  y*(self.bcanvas_height/self.height_lvl)+10 + (self.bcanvas_height/self.height_lvl), fill = "red")
    
    def preview_level_3(self):
        self.Lvl_1.destroy()
        self.Lvl_2.destroy()
        self.Lvl_3.destroy()
        self.own_lvl.destroy()
        self.disable_edit()
        self.bcanvas = Canvas(self.window, height = 160, width = 160)
        self.bcanvas.place(x = 280, y = 150)
        self.lvl = Translator().return_maze(r"LVL_3.txt")
        self.preview_txt = Label(self.window, text = "MAZE 3", font = "Helvetica 25 bold", fg = "blue")
        self.preview_txt.place(x = 175, y = 10, width = 200, height = 100)
        self.info = Label(self.window, text = "This is level 3 Maze\n parameters:\n width: 10\n height: 10\n number of exits: 1", font = "Helvetica 16")
        self.info.place(x = 10, y = 100, width = 200, height = 200)
        self.select_button = Button(self.window, text = "Select", command = self.draw_level) 
        self.select_button.place(x = 70, y = 310, width = 80, height = 40)
        width_list = []
        for i in self.lvl[0]:
            if i == "0" or i == "1" or i == "2":
                width_list.append(i)
        self.height_lvl = len(self.lvl)
        self.width_lvl = len(width_list)
        for y in range(len(self.lvl)):
            x = 0
            for x in range(len(self.lvl[y])):
                if self.lvl[y][x] == "0":
                    self.bcanvas.create_rectangle(x*(self.bcanvas_width/self.width_lvl)+10, y*(self.bcanvas_height/self.height_lvl)+10,x*(self.bcanvas_width/self.width_lvl)+10 + (self.bcanvas_width/self.width_lvl),  y*(self.bcanvas_height/self.height_lvl)+10 + (self.bcanvas_height/self.height_lvl))
                elif self.lvl[y][x] == "1":
                     self.bcanvas.create_rectangle(x*(self.bcanvas_width/self.width_lvl)+10, y*(self.bcanvas_height/self.height_lvl)+10,x*(self.bcanvas_width/self.width_lvl)+10 + (self.bcanvas_width/self.width_lvl),  y*(self.bcanvas_height/self.height_lvl)+10 + (self.bcanvas_height/self.height_lvl), fill = "black")
                elif self.lvl[y][x] == "2":
                     self.bcanvas.create_rectangle(x*(self.bcanvas_width/self.width_lvl)+10, y*(self.bcanvas_height/self.height_lvl)+10,x*(self.bcanvas_width/self.width_lvl)+10 + (self.bcanvas_width/self.width_lvl),  y*(self.bcanvas_height/self.height_lvl)+10 + (self.bcanvas_height/self.height_lvl), fill = "red")
                
    def find_end(self):
        self.root = Node([int(self.input_x.get())-1,int(self.input_y.get())-1])
        memory_obj = Memory(self.lvl)
        queue = memory_obj.queue
        memory_list = memory_obj.memory
        queue.append(self.root)
        memory_list.append(self.root)
        while memory_obj.way == []:
            memory_obj.find_way(queue.pop())
        self.way = memory_obj.way
        return self.way

            
    def walk(self):
            try:
                x = (self.place[0]-self.previous[0])*(self.width/self.width_lvl)
                y = (self.place[1]-self.previous[1])*(self.height/self.height_lvl)
                self.canvas.move(self.robot, x, y)
                self.previous = self.place
                self.place = self.way.pop()
                x = None
                y = None
                self.window.after(600, self.walk)
            except IndexError:
                x = (self.place[0]-self.previous[0])*40
                y = (self.place[1]-self.previous[1])*40
                self.canvas.move(self.robot, x, y)
                self.window.update()
                self.game_over()
                
    def go_robot(self):
        self.error_txt = None
        #disable buttons -> need to do
        self.play_again_but = None
        self.exit_button = None
        #checks if it is walkable -> need to do
        if self.lvl != None:
            if self.input_x.get() != "" and self.input_y.get() != "":
                    if self.lvl[int(self.input_y.get())-1][int(self.input_x.get())-1] != "2":
                        if self.lvl[int(self.input_y.get())-1][int(self.input_x.get())-1] != "1":
                                try:
                                    self.disable_edit()
                                    self.way = self.find_end()
                                    self.previous = self.way.pop()
                                    self.place = self.way.pop()
                                    self.walk()
                                except IndexError:
                                    self.enable_edit()
                                    self.error("Robot can't reach end")
                        else:
                            self.error("Do not place robot on wall")
                    else:
                        self.error("Don't place robot on end")
            else:
                self.error("Put both coordinates")
            
        else:
            self.error("select level")  
    
    
    def error(self, text):
        if self.error_txt != None:
            self.error_txt.destroy()
        self.error_txt = Label(self.window, text = text)
        self.error_txt.place(x = 560, y = 400, width = 200, height = 20)
        self.start_program_button["state"] = NORMAL
        self.exit["state"] = NORMAL
        self.lvl_button["state"] = NORMAL
        self.enter_button["state"] = NORMAL

    def game_over(self):
        self.window.after(500, self.canvas.delete("all"))
        self.window.update()
        self.congrats = Label(self.window, text = "CONGRATULATIONS", fg = "green", font = "Helvetica 25 bold")
        self.congrats.place(x = 80, y = 150, width = 400, height = 100)
        self.play_again_but = Button(self.window, text = "Play again", command = self.play_again)
        self.play_again_but.place(x = 225, y = 260, width = 100, height = 40)
        self.exit_button = Button(self.window, text = "Quit game", command= self.window.destroy)
        self.exit_button.place(x = 235, y = 310, width = 80, height = 40)

    def play_again(self):
        self.lvl = None
        self.way = []
        self.memory = []
        self.queue = []
        self.congrats.destroy()
        self.play_again_but.destroy()
        self.exit_button.destroy()
        self.start_program_button["state"] = NORMAL
        self.enter_button["state"] = NORMAL
        self.lvl_button["state"] = NORMAL
        self.exit["state"] = NORMAL
        self.input_x["state"] = NORMAL
        self.input_y["state"] = NORMAL
        self.input_x.delete(0, last = None)
        self.input_y.delete(0, last = None)
    
    def destroy_texts(self):
        self.canvas.delete("all")
        self.bcanvas.destroy()
        self.preview_txt.destroy()
        self.info.destroy()
        self.select_button.destroy()
    
    def disable_edit(self):
        self.input_x["state"] = DISABLED
        self.input_y["state"] = DISABLED
        self.start_program_button["state"] = DISABLED
        self.enter_button["state"] = DISABLED
    
    def enable_edit(self):
        self.input_x["state"] = NORMAL
        self.input_y["state"] = NORMAL
        self.start_program_button["state"] = NORMAL
        self.enter_button["state"] = NORMAL

Maze()
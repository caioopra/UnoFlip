from tkinter import *
from Window import Window

class TelaMenu():

    def __init__(self,window,next_state) -> None:
        self.window = window
        self.next_state = next_state
        
    
        
    def setCanvas(self):
        self.canvas = Canvas(
            self.window,
            bg = "#ffffff",
            height = 720,
            width = 1280,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge")
        self.canvas.place(relx=0.5, rely=0.5, anchor=CENTER)


    def createDesign(self):
        self.background_img = PhotoImage(file = f"menu_images/background.png")
        background = self.canvas.create_image(
            0, 0,
            image=self.background_img,anchor="nw")

        self.img0 = PhotoImage(file = f"menu_images/img0.png")
        button_start = self.canvas.create_image(270, 360, image=self.img0)
        self.canvas.tag_bind(button_start, "<Button-1>", self.next_state)
        
    
    def start(self):  
        self.setCanvas()    
        self.createDesign()
        self.window.resizable(False, False)
        self.window.mainloop()
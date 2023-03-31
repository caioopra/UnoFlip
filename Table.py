from tkinter import *
from PIL import Image, ImageTk

class Table():

    def __init__(self,window) -> None:
        self.window = window
        self.dict_of_cards ={}
           
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
        self.background_img = PhotoImage(file = f"table_images/background.png")
        background = self.canvas.create_image(
            0, 0,
            image=self.background_img,anchor="nw")
    
    def selectCard(self,card):
        button_card = self.canvas.create_image(640, 360, image=self.dict_of_cards[card])
        self.canvas.tag_bind(button_card, "<Button-1>", lambda x:print('OI'))

    def add_card(self,card,x,y):
        image=Image.open(f'UNO_cards_small_dark/{card}.png')
        img=image.resize((100, 150))
        self.dict_of_cards[card] = ImageTk.PhotoImage(img)
        button_card = self.canvas.create_image(x, y, image=self.dict_of_cards[card])
        self.canvas.tag_bind(button_card, "<Button-1>", lambda x:self.selectCard(card))
    
    def start(self):      
        self.setCanvas()
        self.createDesign()
        self.add_card(card='1_6',x=340,y=570)
        self.add_card(card='2_6',x=460,y=570)
        self.add_card(card='3_6',x=580,y=570)
        self.add_card(card='2_4',x=700,y=570)
        self.add_card(card='4_6',x=820,y=570)
        self.add_card(card='1_8',x=940,y=570)
        self.window.resizable(False, False)
        self.window.mainloop()
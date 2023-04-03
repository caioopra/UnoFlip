from tkinter import *
from PIL import Image, ImageTk

class Table():

    def __init__(self,window) -> None:
        self.window = window
        self.dict_of_cards ={}
        self.list_of_cards_in_hand = []
           
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

        self.img0 = PhotoImage(file = f"table_images/ButtonUno.png")
        button_start = self.canvas.create_image(640, 80, image=self.img0)
        self.canvas.tag_bind(button_start, "<Button-1>", lambda x: print('Gritou uno'))
        
        card ='0_0'
        image=Image.open(f'UNO_cards_small_light/{card}.png')
        img=image.resize((100, 150))
        self.dict_of_cards[card] = ImageTk.PhotoImage(img)
        button_card = self.canvas.create_image(500, 300, image=self.dict_of_cards[card])
        self.list_of_cards_in_hand.append((button_card,card))
        self.canvas.tag_bind(button_card, "<Button-1>", lambda x:print('comprou carta'))
    
    def selectCard(self,card):
        button_card = self.canvas.create_image(640, 300, image=self.dict_of_cards[card])
        self.canvas.tag_bind(button_card, "<Button-1>", lambda x:print('OI'))
        
        for k,i in enumerate(self.list_of_cards_in_hand):
            if i[1] ==card:
                self.canvas.delete(self.list_of_cards_in_hand[k][0])
                del self.list_of_cards_in_hand[k]



    def addCard(self,card,x,y):
        image=Image.open(f'UNO_cards_small_dark/{card}.png')
        img=image.resize((100, 150))
        self.dict_of_cards[card] = ImageTk.PhotoImage(img)
        button_card = self.canvas.create_image(x, y, image=self.dict_of_cards[card])
        self.list_of_cards_in_hand.append((button_card,card))
        self.canvas.tag_bind(button_card, "<Button-1>", lambda x:self.selectCard(card))
        
    def addRemoteCard(self,card,x,y,angle):
        image=Image.open(f'UNO_cards_small_light/{card}.png')
        img=image.resize((80, 130))
        self.dict_of_cards[f'dark{card}{angle}'] = ImageTk.PhotoImage(img.rotate(angle, expand=True))
        self.canvas.create_image(x, y, image=self.dict_of_cards[f'dark{card}{angle}'])




    def start(self):      
        self.setCanvas()
        self.createDesign()
        



        self.addCard(card='1_6',x=340,y=570)
        self.addCard(card='2_6',x=460,y=570)
        self.addCard(card='3_6',x=580,y=570)
        self.addCard(card='2_4',x=700,y=570)
        self.addCard(card='4_6',x=820,y=570)
        self.addCard(card='1_8',x=940,y=570)

        self.addRemoteCard(card='1_6',x=140,y=150,angle = 90)
        self.addRemoteCard(card='2_6',x=140,y=255,angle = 90)
        self.addRemoteCard(card='3_6',x=140,y=360,angle = 90)
        self.addRemoteCard(card='2_4',x=140,y=465,angle = 90)
        self.addRemoteCard(card='4_6',x=140,y=570,angle = 90)

        self.addRemoteCard(card='1_6',x=1140,y=150,angle = 270)
        self.addRemoteCard(card='2_6',x=1140,y=255,angle = 270)
        self.addRemoteCard(card='3_6',x=1140,y=360,angle = 270)
        self.addRemoteCard(card='2_4',x=1140,y=465,angle = 270)
        self.addRemoteCard(card='4_6',x=1140,y=570,angle = 270)

        self.window.resizable(False, False)
        self.window.mainloop()
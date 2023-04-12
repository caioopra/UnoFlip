from tkinter import *
from Window import Window
from PIL import Image, ImageTk
from tkinter import messagebox
from tkinter import simpledialog
from dog.dog_interface import DogPlayerInterface
from dog.dog_actor import DogActor
from random import randint
from Baralho import Baralho

class ActorInterface(DogPlayerInterface):

    def __init__(self,window) -> None:
        self.window = window
        self.dict_of_cards = {}
        self.list_of_cards_in_hand_local = []
        self.list_of_cards_in_hand_remote_right = []
        self.list_of_cards_in_hand_remote_left = []
        self.slots_local = []
        self.slots_remote_right = []
        self.slots_remote_left = []
        self.list_of_cards_in_cheap = []
        self.inicio_mao = 0
        self.loadCardImages()
        self.startMenu()
        

    def setMenuCanvas(self):
        self.canvas = Canvas(
            self.window,bg = "#ffffff",height = 720,width = 1280,bd = 0,highlightthickness = 0,relief = "ridge")
        self.canvas.place(relx=0.5, rely=0.5, anchor=CENTER)


    def createMenuDesign(self):
        self.background_img = PhotoImage(file = f"menu_images/background.png")
        background = self.canvas.create_image(0, 0,image=self.background_img,anchor="nw")
        self.img0 = PhotoImage(file = f"menu_images/img0.png")
        button_start = self.canvas.create_image(270, 360, image=self.img0)
        self.canvas.tag_bind(button_start, "<Button-1>", lambda x: self.start_match())


    def startMenu(self):
        self.setMenuCanvas() 
        self.createMenuDesign()
        self.window.resizable(False, False)
        player_name = simpledialog.askstring(title='player indentification', prompt= 'Qual seu nome?')
        self.dog_server_interface = DogActor()
        message = self.dog_server_interface.initialize(player_name,self)
        messagebox.showinfo(message=message)
        self.window.mainloop()

    def setTableCanvas(self):
        self.canvas = Canvas(self.window,bg = "#ffffff",height = 720,width = 1280,bd = 0,highlightthickness = 0,relief = "ridge")
        self.canvas.place(relx=0.5, rely=0.5, anchor=CENTER)


    def createTableDesign(self):
        self.background_img = PhotoImage(file = f"table_images/background.png")
        background = self.canvas.create_image(0, 0, image=self.background_img,anchor="nw")

        self.img0 = PhotoImage(file = f"table_images/ButtonUno.png")
        button_start = self.canvas.create_image(640, 80, image=self.img0)
        self.canvas.tag_bind(button_start, "<Button-1>", lambda x: print('Gritou uno'))


        self.img1 = PhotoImage(file = f"table_images/Button(2).png")
        button_passar_vez = self.canvas.create_image(800, 300, image=self.img1)
        self.canvas.tag_bind(button_passar_vez, "<Button-1>", lambda x: print('Passou vez'))
        

        self.img2 = PhotoImage(file = f"table_images/seta_esquerda.png")
        button_passar_vez = self.canvas.create_image(340, 670, image=self.img2)
        self.canvas.tag_bind(button_passar_vez, "<Button-1>", lambda x: self.mover_mao(0))


        self.img3 = PhotoImage(file = f"table_images/seta_direita.png")
        button_passar_vez = self.canvas.create_image(940, 670, image=self.img3)
        self.canvas.tag_bind(button_passar_vez, "<Button-1>", lambda x:self.mover_mao(1))


        button_card = self.canvas.create_image(500, 300, image=self.dict_of_cards['light_0'])
        self.canvas.tag_bind(button_card, "<Button-1>", lambda x: self.comprar())
    
    def loadCardImages(self):
        for i in range(64):
            image=Image.open(f'UNO_cards_light/light_{i}.png')
            img=image.resize((100, 150))
            self.dict_of_cards[f"light_{i}"] = ImageTk.PhotoImage(img)

            image=Image.open(f'UNO_cards_light/light_{i}.png')
            img=image.resize((80, 130))
            self.dict_of_cards[f"light_{i}_90"] = ImageTk.PhotoImage(img.rotate(90, expand=True))

            image=Image.open(f'UNO_cards_light/light_{i}.png')
            img=image.resize((80, 130))
            self.dict_of_cards[f"light_{i}_270"] = ImageTk.PhotoImage(img.rotate(270, expand=True))

            image=Image.open(f'UNO_cards_dark/dark_{i}.png')
            img=image.resize((100, 150))
            self.dict_of_cards[f"dark_{i}"] = ImageTk.PhotoImage(img)

            image=Image.open(f'UNO_cards_dark/dark_{i}.png')
            img=image.resize((80, 130))
            self.dict_of_cards[f"dark_{i}_90"] = ImageTk.PhotoImage(img.rotate(90, expand=True))

            image=Image.open(f'UNO_cards_dark/dark_{i}.png')
            img=image.resize((80, 130))
            self.dict_of_cards[f"dark_{i}_270"] = ImageTk.PhotoImage(img.rotate(270, expand=True))


    def selectCard(self,card):
        try:
            self.canvas.delete(self.button_cheap)
        except:
            pass

        self.button_cheap = self.canvas.create_image(640, 300, image=self.dict_of_cards[card[1]])

        self.delete_local()       

        for k, j in enumerate(self.list_of_cards_in_hand_local):
            if card[1] == j:

                del self.list_of_cards_in_hand_local[k]
                break
    
        self.addCard()

    def mover_mao(self,direcao):
        for k,i in enumerate(self.slots_local):
            self.canvas.delete(self.slots_local[k][0])
        
        if direcao ==1:
            if self.inicio_mao+6<len(self.list_of_cards_in_hand_local):
                self.inicio_mao +=1

        if direcao ==0:
            if self.inicio_mao > 0:
                self.inicio_mao -=1

        
        self.addCard()

    def addCard(self):
        self.slots_local = []

        func0 = lambda x:self.selectCard(self.slots_local[0])
        func1 = lambda x:self.selectCard(self.slots_local[1])
        func2 = lambda x:self.selectCard(self.slots_local[2])
        func3 = lambda x:self.selectCard(self.slots_local[3])
        func4 = lambda x:self.selectCard(self.slots_local[4])
        func5 = lambda x:self.selectCard(self.slots_local[5])
        funcs = [func0,func1,func2,func3,func4,func5]
        

        for i in range(6):
            if (i+self.inicio_mao) < len(self.list_of_cards_in_hand_local):
                self.slots_local.append(self.list_of_cards_in_hand_local[i+self.inicio_mao])
            if i < len(self.slots_local):
                button_card = self.canvas.create_image(340+i*120, 570, image=self.dict_of_cards[self.slots_local[i]])
                self.slots_local[i] = (button_card,self.slots_local[i])
                self.canvas.tag_bind(button_card, "<Button-1>", funcs[i])
            

        
    def addRemoteCard(self,card,x,y):
        self.canvas.create_image(x, y, image=self.dict_of_cards[card])

    def start_match(self):        
        start_status = self.dog_server_interface.start_match(1)
        message = start_status.get_message()
        messagebox.showinfo(message=message)
        if message == 'Partida iniciada':
            self.start_table()

    def delete_local(self):
        for k,i in enumerate(self.slots_local):
            self.canvas.delete(self.slots_local[k][0])

    def comprar(self):
        self.delete_local()
        a = randint(1,63)
        self.list_of_cards_in_hand_local.insert(0,f'dark_{a}')
        self.addCard()

    def start_table(self):
        self.setTableCanvas()
        self.createTableDesign()
        
        self.list_of_cards_in_hand_local.append('dark_34')
        self.list_of_cards_in_hand_local.append('dark_17')
        self.list_of_cards_in_hand_local.append('dark_63')
        self.list_of_cards_in_hand_local.append('dark_47')
        self.list_of_cards_in_hand_local.append('dark_30')
        self.list_of_cards_in_hand_local.append('dark_4')
        self.list_of_cards_in_hand_local.append('dark_47')
        self.list_of_cards_in_hand_local.append('dark_21')
        self.list_of_cards_in_hand_local.append('dark_57')
        self.list_of_cards_in_hand_local.append('dark_63')
        self.list_of_cards_in_hand_local.append('dark_41')
        self.list_of_cards_in_hand_local.append('dark_39')
        self.list_of_cards_in_hand_local.append('dark_4')
        self.list_of_cards_in_hand_local.append('dark_12')
        self.addCard()

        self.addRemoteCard(card='light_16_90',x=140,y=150)
        self.addRemoteCard(card='light_26_90',x=140,y=255)
        self.addRemoteCard(card='light_36_90',x=140,y=360)
        self.addRemoteCard(card='light_24_90',x=140,y=465)
        self.addRemoteCard(card='light_46_90',x=140,y=570)

        self.addRemoteCard(card='light_16_270',x=1140,y=150)
        self.addRemoteCard(card='light_26_270',x=1140,y=255)
        self.addRemoteCard(card='light_36_270',x=1140,y=360)
        self.addRemoteCard(card='light_24_270',x=1140,y=465)
        self.addRemoteCard(card='light_46_270',x=1140,y=570)


window = Window()
tela = ActorInterface(window.window)

from tkinter import *
from Window import Window
from PIL import Image, ImageTk
from tkinter import messagebox
from tkinter import simpledialog
from dog.dog_interface import DogPlayerInterface
from dog.dog_actor import DogActor
from random import randint
from Baralho import Baralho
from Jogo import Jogo
from Jogador import Jogador


class ActorInterface(DogPlayerInterface):

    def __init__(self,window: Window) -> None:
        self.window = window.get_window()
        self.dict_of_cards = {}
        self.list_of_cards_in_hand_local = []
        self.list_of_cards_in_hand_remote_right = []
        self.list_of_cards_in_hand_remote_left = []
        self.slots_local = []
        self.slots_remote_right = []
        self.slots_remote_left = []
        self.list_of_cards_in_cheap = []
        self.inicio_mao = 0
        self.jogo = Jogo()
        self.loadCardImages()
        self.startMenu()
        
    def receive_move(self, a_move: dict) -> None:
        pass

    def receive_start(self, start_status:str) -> None:
        pass

    def receive_withdrawal_notification(self) -> None:
        pass

    def start_match(self) -> None:        
        start_status = self.dog_server_interface.start_match(1)
        message = start_status.get_message()
        messagebox.showinfo(message=message)

        if message == 'Partida iniciada':

            jogadores = start_status.get_players()
            id_jogador_local = start_status.get_local_id()
            self.jogo.set_local_id(id_jogador_local)
            self.jogo.criar_jogadores(jogadores)
            dict_inicial = self.jogo.transform_play_to_dict('init')
            self.dog_server_interface.send_move(dict_inicial)
            self.start_table()

    def setMenuCanvas(self) -> None:
        self.canvas = Canvas(
            self.window,bg = "#ffffff",height = 720,width = 1280,bd = 0,highlightthickness = 0,relief = "ridge")
        self.canvas.place(relx=0.5, rely=0.5, anchor=CENTER)


    def createMenuDesign(self) -> None:
        self.background_img = PhotoImage(file = f"menu_images/background.png")
        background = self.canvas.create_image(0, 0,image=self.background_img,anchor="nw")
        self.img0 = PhotoImage(file = f"menu_images/img0.png")
        button_start = self.canvas.create_image(270, 360, image=self.img0)
        self.canvas.tag_bind(button_start, "<Button-1>", lambda x: self.start_match())


    def startMenu(self) -> None:
        self.setMenuCanvas() 
        self.createMenuDesign()
        self.window.resizable(False, False)
        player_name = simpledialog.askstring(title='player indentification', prompt= 'Qual seu nome?')
        self.dog_server_interface = DogActor()
        message = self.dog_server_interface.initialize(player_name,self)
        messagebox.showinfo(message=message)
        self.window.mainloop()

    def setTableCanvas(self) -> None:
        self.canvas = Canvas(self.window,bg = "#ffffff",height = 720,width = 1280,bd = 0,highlightthickness = 0,relief = "ridge")
        self.canvas.place(relx=0.5, rely=0.5, anchor=CENTER)


    def createTableDesign(self) -> None:
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
    
    def loadCardImages(self) -> None:
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


    def selectCard(self,card) -> None:
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

    def mover_mao(self,direcao: int) -> None:
        self.delete_local()
        
        if direcao ==1:
            if self.inicio_mao+6<len(self.list_of_cards_in_hand_local):
                self.inicio_mao +=1

        if direcao ==0:
            if self.inicio_mao > 0:
                self.inicio_mao -=1

        
        self.addCard()

    def addCard(self) -> None:
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
            

        
    def addRemoteCardRight(self) -> None:
        self.slots_remote_right = []

        for i in range(5):
            if i < len(self.list_of_cards_in_hand_remote_right):
                self.slots_remote_right.append(self.list_of_cards_in_hand_remote_right[i])

            if i <len(self.slots_remote_right):
                identificator = self.canvas.create_image(1140, 150+(105*i), image=self.dict_of_cards[self.slots_remote_right[i]])
                self.slots_remote_right[i] = (identificator,self.slots_remote_right[i])

    def addRemoteCardLeft(self) -> None:
        self.slots_remote_left = []

        for i in range(5):
            if i < len(self.list_of_cards_in_hand_remote_left):
                self.slots_remote_left.append(self.list_of_cards_in_hand_remote_left[i])

            if i <len(self.slots_remote_left):
                identificator = self.canvas.create_image(140, 150+(105*i), image=self.dict_of_cards[self.slots_remote_left[i]])
                self.slots_remote_left[i] = (identificator,self.slots_remote_left[i])

    def delete_local(self) -> None:
        for k,i in enumerate(self.slots_local):
            self.canvas.delete(self.slots_local[k][0])

    def comprar(self) -> None:
        self.delete_local()
        a = randint(1,63)
        self.list_of_cards_in_hand_local.insert(0,f'dark_{a}')
        self.addCard()

    def start_table(self) -> None:
        self.setTableCanvas()
        self.createTableDesign()

        self.addCard()

        self.list_of_cards_in_hand_remote_right.append('light_16_90')
        self.list_of_cards_in_hand_remote_right.append('light_16_90')
        self.list_of_cards_in_hand_remote_right.append('light_16_90')
        self.addRemoteCardRight()
        

        self.list_of_cards_in_hand_remote_left.append('light_19_270')
        self.list_of_cards_in_hand_remote_left.append('light_19_270')
        self.list_of_cards_in_hand_remote_left.append('light_19_270')
        self.addRemoteCardLeft()



window = Window()
tela = ActorInterface(window)

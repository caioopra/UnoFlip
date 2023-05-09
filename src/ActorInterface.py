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
import json

class ActorInterface(DogPlayerInterface):

    def __init__(self,window: Window) -> None:
        self.window = window.get_window()
        self.dict_of_cards = {}
        self.hand_local = 0
        self.hand_remote_left = 0
        self.hand_remote_right = 0
        self.slots_local = []
        self.slots_remote_right = []
        self.slots_remote_left = []
        self.list_of_cards_in_cheap = []
        self.inicio_mao = 0
        self.jogo = Jogo()
        self.loadCardImages()
        self.startMenu()
        
    def receive_move(self, a_move: dict) -> None:
        if a_move['tipo'] == 'init':
            self.jogo.transform_dict_to_object(a_move)
            jogadores = self.jogo.get_jogadores()
            for k,jogador in enumerate(jogadores):
                if jogador.id ==self.jogo.local_id:
                    self.hand_local=k
                    self.hand_remote_right= (k+1)%3
                    self.hand_remote_left= k-1
            self.jogo.jogador_atual = self.jogo.jogadores[0]
            self.jogo.proximo_jogador =self.jogo.jogadores[1]
            self.start_table()
        elif a_move['tipo'] == 'comprar':
            self.jogo.comprarCarta()
            self.atualizarInterface()
        elif a_move['tipo'] == 'jogar':
            index = a_move['index']
            self.jogo.jogarCarta(index)
            self.atualizarInterface()
        
        elif a_move['tipo'] == 'passar':
            self.jogo.passarVez()
            print('PASSOU')

        print()
        for jogadores in self.jogo.jogadores:
            print(jogadores.id)

    def receive_start(self, start_status) -> None:
        self.jogo.set_local_id(start_status.get_local_id())

    def receive_withdrawal_notification(self) -> None:
        pass

    def start_match(self) -> None:        
        start_status = self.dog_server_interface.start_match(3)
        message = start_status.get_message()
        messagebox.showinfo(message=message)

        if message == 'Partida iniciada':
            jogadores = start_status.get_players()
            print(jogadores)
            id_jogador_local = start_status.get_local_id()
            self.jogo.set_local_id(id_jogador_local)
            self.jogo.criar_jogadores(jogadores)
            dict_inicial = self.jogo.transform_play_to_dict('init')
            self.dog_server_interface.send_move(dict_inicial)
            jogadores = self.jogo.get_jogadores()
            for k,jogador in enumerate(jogadores):
                if jogador.id ==self.jogo.local_id:
                    self.hand_local=k
                    self.hand_remote_right= (k+1)%3
                    self.hand_remote_left= k-1
            self.jogo.jogador_atual = self.jogo.jogadores[0]
            self.jogo.proximo_jogador =self.jogo.jogadores[1]
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
        self.canvas.tag_bind(button_passar_vez, "<Button-1>", lambda x: self.passarVez())
        

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






    def comprar(self) -> None:
        print(self.jogo.local_id)
        if self.jogo.local_id == self.jogo.jogador_atual.id:
            self.jogo.comprarCarta()
            self.dog_server_interface.send_move(self.jogo.dict_jogada)
            self.atualizarInterface()
        else:
            print('nao e sua vez')




    def mover_mao(self,direcao: int) -> None:
        self.delete_local()
        
        if direcao ==1:
            if self.inicio_mao+6<len(self.jogo.jogadores[self.hand_local].get_mao()):
                self.inicio_mao +=1

        if direcao ==0:
            if self.inicio_mao > 0:
                self.inicio_mao -=1
       
        self.atualizarInterface()

    def passarVez(self):
        print('atual',self.jogo.jogador_atual.id)
        if self.jogo.local_id == self.jogo.jogador_atual.id: 
            
            self.jogo.passarVez()

            self.dog_server_interface.send_move(self.jogo.dict_jogada)
        else:
            print('nao e sua vez')

    def jogarCarta(self,index) -> None:
        if self.jogo.local_id == self.jogo.jogador_atual.id:           
   
            self.jogo.jogarCarta(self.inicio_mao+index)
            
            self.dog_server_interface.send_move(self.jogo.dict_jogada)


            self.atualizarInterface()

        else:
            print('nao e sua vez')

    def addCard(self) -> None:
        self.slots_local = []

        
        func0 = lambda x:self.jogarCarta(0)
        func1 = lambda x:self.jogarCarta(1)
        func2 = lambda x:self.jogarCarta(2)
        func3 = lambda x:self.jogarCarta(3)
        func4 = lambda x:self.jogarCarta(4)
        func5 = lambda x:self.jogarCarta(5)
        funcs = [func0,func1,func2,func3,func4,func5]
        

        for i in range(6):
            if (i+self.inicio_mao) < len(self.jogo.jogadores[self.hand_local].get_mao()):
                self.slots_local.append(self.jogo.jogadores[self.hand_local].get_mao()[i+self.inicio_mao])
            if i < len(self.slots_local):
                button_card = self.canvas.create_image(340+i*120, 570, image=self.dict_of_cards[self.slots_local[i].get_face_atual().get_id()])
                self.slots_local[i] = (button_card,self.slots_local[i])
                self.canvas.tag_bind(button_card, "<Button-1>", funcs[i])
            
    def addRemoteCardRight(self) -> None:
        self.slots_remote_right = []

        for i in range(5):
            if i < len(self.jogo.jogadores[self.hand_remote_right].get_mao()):
                self.slots_remote_right.append(self.jogo.jogadores[self.hand_remote_right].get_mao()[i])

            if i <len(self.slots_remote_right):
                identificator = self.canvas.create_image(1140, 150+(105*i), image=self.dict_of_cards[f'{self.slots_remote_right[i].get_verso().get_id()}_270'])
                self.slots_remote_right[i] = (identificator,self.slots_remote_right[i])

    def addRemoteCardLeft(self) -> None:
        self.slots_remote_left = []

        for i in range(5):
            if i < len(self.jogo.jogadores[self.hand_remote_left].get_mao()):
                self.slots_remote_left.append(self.jogo.jogadores[self.hand_remote_left].get_mao()[i])

            if i <len(self.slots_remote_left):
                identificator = self.canvas.create_image(140, 150+(105*i), image=self.dict_of_cards[f'{self.slots_remote_left[i].get_verso().get_id()}_90'])
                self.slots_remote_left[i] = (identificator,self.slots_remote_left[i])



    def addCheap(self):
        try:
                self.canvas.delete(self.button_cheap)
        except:
                pass

        carta = self.jogo.mesa.getUltimaCarta()

        self.button_cheap = self.canvas.create_image(640, 300, image=self.dict_of_cards[carta.get_face_atual().get_id()])


    def delete_local(self) -> None:
        for k,i in enumerate(self.slots_local):
            self.canvas.delete(self.slots_local[k][0])





    def start_table(self) -> None:

        self.setTableCanvas()
        self.createTableDesign()

        self.atualizarInterface()



    def atualizarInterface(self):
        self.delete_local()

        self.addCheap()

        self.addCard()

        self.addRemoteCardRight()
        
        self.addRemoteCardLeft()


window = Window()
tela = ActorInterface(window)

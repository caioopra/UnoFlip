from tkinter import *
from Window import Window
from PIL import Image, ImageTk
from tkinter import messagebox
from tkinter import simpledialog
from dog.dog_interface import DogPlayerInterface
from dog.dog_actor import DogActor
from FaceCoringa import FaceCoringa
from Jogo import Jogo

from time import sleep

# teste
class ActorInterface(DogPlayerInterface):

    def __init__(self,window: Window) -> None:
        self.window = window.get_window()
        self.dict_of_cards = {}
        self.slots_local = []
        self.slots_remote_right = []
        self.slots_remote_left = []
        self.inicio_mao = 0
        self.jogo = Jogo()
        self.loadCardImages()
        self.startMenu()

    def receive_move(self, a_move: dict) -> None:
        if a_move['tipo'] == 'init':
            print("comecou")
            self.jogo.transform_dict_to_object(a_move)
            jogadores = self.jogo.getJogadores()
            for k,jogador in enumerate(jogadores):
                if jogador.getId() ==self.jogo.getLocalId():
                    self.jogo.setLocalPosition(k)
                    self.jogo.setRightPosition((k+1)%3) 
                    self.jogo.setLeftPosition(k-1)
            self.jogo.setJogadorAtual(self.jogo.getJogadores()[0])
            self.jogo.setProximoJogador(self.jogo.getJogadores()[1])
            self.start_table()
        elif a_move['tipo'] == 'comprar':
            self.jogo.comprarCarta()
            self.atualizarInterface()
            
        elif a_move['tipo'] == 'jogar':
            index = a_move['index']
            self.jogo.jogarCarta(index)
            self.atualizarInterface()
            if not self.jogo.getJogadorAtual().getMao():
                sleep(0.2)
                self.mostrarEndGame()
        
        elif a_move['tipo'] == 'passar':
            self.jogo.passarVez()
        
        elif a_move['tipo'] == 'muda_cor':
            self.mudaCor(a_move['cor'])

            carta = self.jogo.getMesa().getUltimaCarta()
            if carta.frente.simbolo == 'compra_ate_vir':
                self.jogo.getProximoJogador().receberCartas(1, self.jogo.getMesa().baralho)
                carta_comprada = self.jogo.getProximoJogador().getMao()[0]

                if not isinstance(carta_comprada.frente, FaceCoringa):
                    while carta_comprada.frente.cor != a_move['cor']:
                        if not isinstance(carta_comprada.frente, FaceCoringa):
                            self.jogo.getProximoJogador().receberCartas(1, self.jogo.getMesa().baralho)
                            carta_comprada = self.jogo.getProximoJogador().getMao()[0]

            self.atualizarInterface()
        elif a_move['tipo'] == 'uno':
            self.jogo.getJogadorAtual().gritarUno()
            self.jogo.verificar_UNO()
            self.atualizarInterface()

    def receive_start(self, start_status) -> None:
        self.jogo.setLocalId(start_status.get_local_id())

    def receive_withdrawal_notification(self) -> None:
        pass

    def start_match(self) -> None:        
        start_status = self.dog_server_interface.start_match(3)
        message = start_status.get_message()
        messagebox.showinfo(message=message)

        if message == 'Partida iniciada':
            jogadores = start_status.get_players()
            id_jogador_local = start_status.get_local_id()
            
            dict_inicial = self.jogo.comecarPartida(jogadores, id_jogador_local)
            self.dog_server_interface.send_move(dict_inicial)

            self.jogo.configurarJogadores()

            self.start_table()
            

    def setCanvas(self) -> None:
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
        self.setCanvas() 
        self.createMenuDesign()
        self.window.resizable(False, False)
        # player_name = simpledialog.askstring(title='player indentification', prompt= 'Qual seu nome?')
        player_name = 'joao'
        self.dog_server_interface = DogActor()
        message = self.dog_server_interface.initialize(player_name,self)
        messagebox.showinfo(message=message)
        self.window.mainloop()


    def createTableDesign(self) -> None:
        self.background_img = PhotoImage(file = f"table_images/background.png")
        background = self.canvas.create_image(0, 0, image=self.background_img,anchor="nw")

        self.img0 = PhotoImage(file = f"table_images/ButtonUno.png")
        button_start = self.canvas.create_image(640, 80, image=self.img0)
        self.canvas.tag_bind(button_start, "<Button-1>", lambda x: self.gritarUno())


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


    def gritarUno(self):
        self.jogo.getJogadorAtual().gritarUno()
        self.jogo.verificar_UNO()
        self.atualizarInterface()
        self.dog_server_interface.send_move(self.jogo.getDictJogada())


    def comprar(self) -> None:
        if (self.jogo.getLocalId() == self.jogo.getJogadorAtual().getId() and 
            not (self.jogo.getJogadorAtual().getComprouCarta() or self.jogo.getJogadorAtual().getJogouCarta())
        ):
            self.jogo.comprarCarta()
            self.dog_server_interface.send_move(self.jogo.getDictJogada())
            self.atualizarInterface()
        else:
            print('nao e sua vez')

            

    def mover_mao(self,direcao: int) -> None:
        self.delete_local()
        
        if direcao ==1:
            if self.inicio_mao+6<len(self.jogo.getJogadores()[self.jogo.getLocalPosition()].getMao()):
                self.inicio_mao +=1

        if direcao ==0:
            if self.inicio_mao > 0:
                self.inicio_mao -=1
       
        self.atualizarInterface()

    def passarVez(self):
        if self.jogo.getLocalId() == self.jogo.getJogadorAtual().getId(): 
            
            self.jogo.passarVez()

            self.dog_server_interface.send_move(self.jogo.getDictJogada())
        else:
            print('nao e sua vez')

    def jogarCarta(self,index) -> None:
        if self.jogo.getLocalId() == self.jogo.getJogadorAtual().getId():           
   
            valida = self.jogo.jogarCarta(self.inicio_mao+index)
            if valida:
                self.dog_server_interface.send_move(self.jogo.getDictJogada())
                self.atualizarInterface()
                if self.jogo.getMesa().getUltimaCarta().frente.tipo == 'coringa':
                    self.escolherCor()
            
            if not self.jogo.getJogadorAtual().getMao():
                sleep(0.2)
                self.mostrarEndGame()
        else:
            print('nao e sua vez')

    def addCard(self) -> None:
        self.slots_local = []

        
        func0 = lambda x: self.jogarCarta(0)
        func1 = lambda x: self.jogarCarta(1)
        func2 = lambda x: self.jogarCarta(2)
        func3 = lambda x: self.jogarCarta(3)
        func4 = lambda x: self.jogarCarta(4)
        func5 = lambda x: self.jogarCarta(5)
        funcs = [func0,func1,func2,func3,func4,func5]
        

        for i in range(6):
            if (i+self.inicio_mao) < len(self.jogo.getJogadores()[self.jogo.getLocalPosition()].getMao()):
                self.slots_local.append(self.jogo.getJogadores()[self.jogo.getLocalPosition()].getMao()[i+self.inicio_mao])
            if i < len(self.slots_local):
                button_card = self.canvas.create_image(340+i*120, 570, image=self.dict_of_cards[self.slots_local[i].get_frente().getId()])
                self.slots_local[i] = (button_card,self.slots_local[i])
                self.canvas.tag_bind(button_card, "<Button-1>", funcs[i])
            
    def addRemoteCardRight(self) -> None:
        self.slots_remote_right = []

        for i in range(5):
            if i < len(self.jogo.getJogadores()[self.jogo.getRightPosition()].getMao()):
                self.slots_remote_right.append(self.jogo.getJogadores()[self.jogo.getRightPosition()].getMao()[i])

            if i <len(self.slots_remote_right):
                identificator = self.canvas.create_image(1140, 150+(105*i), image=self.dict_of_cards[f'{self.slots_remote_right[i].get_verso().getId()}_270'])
                self.slots_remote_right[i] = (identificator,self.slots_remote_right[i])



    def addRemoteCardLeft(self) -> None:
        self.slots_remote_left = []

        for i in range(5):
            if i < len(self.jogo.getJogadores()[self.jogo.getLeftPosition()].getMao()):
                self.slots_remote_left.append(self.jogo.getJogadores()[self.jogo.getLeftPosition()].getMao()[i])

            if i <len(self.slots_remote_left):
                identificator = self.canvas.create_image(140, 150+(105*i), image=self.dict_of_cards[f'{self.slots_remote_left[i].get_verso().getId()}_90'])
                self.slots_remote_left[i] = (identificator,self.slots_remote_left[i])



    def addCheap(self):
        try:
            self.canvas.delete(self.button_cheap)
        except:
            pass

        carta = self.jogo.getMesa().getUltimaCarta()

        self.button_cheap = self.canvas.create_image(640, 300, image=self.dict_of_cards[carta.get_frente().getId()])


    def delete_local(self) -> None:
        for k, _ in enumerate(self.slots_local):
            self.canvas.delete(self.slots_local[k][0])

    

    def mostrarEndGame(self):
        indice_jogador = self.jogo.getLocalPosition()
        self.setCanvas()
        if len(self.jogo.getJogadores()[indice_jogador].getMao()):
            imagem = 'perdeu'
        else:
            imagem = 'venceu'
        self.background_img = PhotoImage(file = f"menu_images/{imagem}.png")
        background = self.canvas.create_image(0, 0,image=self.background_img,anchor="nw")
    

    def escolherCor(self):
        carta = self.jogo.getMesa().getUltimaCarta()
        cor = carta.frente.id[0]
        
        if cor == "l":
            retangulo = 'Rectangle_light'
            quadrado1 = 'vermelho'
            quadrado2 = 'azul'
            quadrado3 = 'amarelo'
            quadrado4 = 'verde'
        else:
            retangulo = 'Rectangle_dark'
            quadrado1 = 'ciano'
            quadrado2 = 'laranja'
            quadrado3 = 'rosa'
            quadrado4 = 'roxo'        
            

        self.rectangle = PhotoImage(file = f"table_images/{retangulo}.png")
        self.rectangle_id = self.canvas.create_image(640, 360, image=self.rectangle)
    
        
        self.vermelho = PhotoImage(file = f"table_images/{quadrado1}.png")
        self.button1_id = self.canvas.create_image(745, 255, image=self.vermelho)
        self.canvas.tag_bind(self.button1_id, "<Button-1>", lambda x:  self.mudaCor(quadrado1))


        self.azul = PhotoImage(file = f"table_images/{quadrado2}.png")
        self.button2_id = self.canvas.create_image(535, 255, image=self.azul)
        self.canvas.tag_bind(self.button2_id, "<Button-1>", lambda x: self.mudaCor(quadrado2))


        self.amarelo = PhotoImage(file = f"table_images/{quadrado3}.png")
        self.button3_id = self.canvas.create_image(745, 465, image=self.amarelo)
        self.canvas.tag_bind(self.button3_id, "<Button-1>", lambda x: self.mudaCor(quadrado3))


        self.verde = PhotoImage(file = f"table_images/{quadrado4}.png")
        self.button4_id = self.canvas.create_image(535, 465, image=self.verde)
        self.canvas.tag_bind(self.button4_id, "<Button-1>", lambda x: self.mudaCor(quadrado4))
        
        # jogo.mudarCor
        
        # atualiza interface e faz envio da jogada, destruindo a tela criada

    def mudaCor(self, cor: str):
        carta = self.jogogetMesa().getUltimaCarta()
        carta.frente.cor = cor
 
        cores_mais_dois = {
            'amarelo': 'light_7',
            'vermelho': 'light_8',
            'azul': 'light_9',
            'verde': 'light_10'
        }
        cores_compra_ate_vir= {
            'laranja': 'dark_7',
            'rosa': 'dark_8',
            'roxo': 'dark_9',
            'ciano': 'dark_10'
        }

        cores_coringa = {
            'amarelo': 'light_2',
            'vermelho': 'light_3',
            'azul': 'light_4',
            'verde': 'light_5',
            'laranja': 'dark_2',
            'rosa': 'dark_3',
            'roxo': 'dark_4',
            'ciano': 'dark_5'
        }

        if carta.frente.simbolo == 'mais_dois':
            carta.frente.id = cores_mais_dois[cor]
            self.jogo.getMesa().setUltimaCarta(carta)
        elif carta.frente.simbolo == 'compra_ate_vir':
            carta.frente.id = cores_compra_ate_vir[cor]
            self.jogo.getMesa().setUltimaCarta(carta)
        elif carta.frente.simbolo == 'coringa':
            carta.frente.id = cores_coringa[cor]
            self.jogo.getMesa().setUltimaCarta(carta)
        ################
        # ficar no Actor
        self.atualizarInterface()

        if self.jogo.getJogadorAtual().getId() == self.jogo.getJogadores()[self.jogo.getLocalPosition()].getId():
            sleep(0.2)

            a = self.rectangle_id
            for i in range(a,a+5):
                self.canvas.delete(i)

            dict_a = {
                'match_status': 'progress',
                'tipo': 'muda_cor',
                'cor': cor
            }

            self.dog_server_interface.send_move(dict_a)


    def start_table(self) -> None:
        self.setCanvas()
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

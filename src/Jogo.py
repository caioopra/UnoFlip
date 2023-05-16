from Baralho import Baralho
from Carta import Carta
from FaceNumerica import FaceNumerica
from FaceColoridaComPoder import FaceColoridaComPoder
from FaceCoringa import FaceCoringa
from Jogador import Jogador
from mesa import Mesa
import json
from types import SimpleNamespace

class Jogo:

    def __init__(self) -> None:
        self.jogadores = [0,0,0]
        self.local_id = ''
        self.status = 0
        self.jogador_atual = None
        self.proximo_jogador = None
        self.jogou_carta = False
        self.comprou_carta = False
        self.gritou_uno = False
        self.dict_jogada = {}
        self.mesa = Mesa(Baralho())


    def get_jogadores(self) -> list:
        return self.jogadores

    def get_status(self) -> int:
        return self.status
    
    def get_baralho(self) -> Baralho:
        return self.baralho
        
    def get_jogador_atual(self) -> int:
        return self.jogador_atual

    def set_local_id(self, local_id):
        self.local_id = local_id

    def set_ordem(self, direcao:int) -> None:
        self.direcao = direcao
    
    def set_jogador_atual(self,jogador:int) -> None:
        self.jogador_atual = jogador

    def criar_jogadores(self,jogadores):
        for i, jogador in enumerate(jogadores):
            mao = self.dar_cartas_iniciais()
            self.jogadores[i]=Jogador(id = jogador[1], nome =jogador[0],ordem=jogador[2], mao = mao)
        

    def dar_cartas_iniciais(self) -> list:
        mao = []
        for _ in range(8):
            carta = self.mesa.baralho.cartas.pop()
            mao.append(carta)
        return mao

    def darCarta(self,jogador,quantidade):
        for _ in range(quantidade):
            carta = self.mesa.baralho.comprar_carta()
            jogador.adicionarCartaMao(carta)
            jogador.gritou_uno = False


    def jogarCarta(self,index):

        if not self.comprou_carta and not self.jogou_carta:

            self.tentarColocarCartaNaMesa(index)
                    

        else:
            print('voce ja atuou nesse turno')
            

    def tentarColocarCartaNaMesa(self,index):
        valida =self.verificarValida(index)

        if valida:
            self.dict_jogada = {}
            self.dict_jogada['tipo'] = 'jogar'
            self.dict_jogada['index'] = index
            self.dict_jogada['match_status'] = 'progress'
            self.mesa.setUltimaCarta(self.jogador_atual.mao[index])
            del self.jogador_atual.mao[index]
            self.aplicarEfeito(index)
            self.jogou_carta = True



        else:
            print('nao pode jogar essa carta')



    def verificarValida(self,index):

        carta = self.jogador_atual.mao[index]

        if isinstance(carta.face_atual,FaceCoringa):

            return True

        elif self.mesa.ultima_carta.face_atual.cor == carta.face_atual.cor:

            return True

        elif self.mesa.ultima_carta.face_atual.get_simbolo() == carta.face_atual.get_simbolo():

            return True 
        
        else:
            return False


    def aplicarEfeito(self,index):
        print()
        print(len(self.jogador_atual.mao))
        print(index)
        print()

        carta = self.jogador_atual.mao[index]
        
        if (isinstance(carta.frente, FaceNumerica) or isinstance(carta.frente, FaceColoridaComPoder)):
            efeito = carta.frente.simbolo
            if efeito == 'mais_um':
                self.darCarta(self.proximo_jogador,1)
            elif efeito == 'pular_vez':
                for k,jogador in enumerate(self.jogadores):
                    if jogador.id ==self.proximo_jogador.id:
                        index = (k+1)%3
                        self.proximo_jogador = self.jogadores[index]
                        break


    def comprarCarta(self):
        
        if not (self.comprou_carta or self.jogou_carta):
            self.darCarta(self.jogador_atual,1)

            self.comprou_carta = True

            self.dict_jogada['tipo'] = 'comprar'
            self.dict_jogada['match_status'] = 'progress'

            # carta = self.jogador_atual.mao[0]

            # self.tentarColocarCartaNaMesa(carta)

        else:
            print('ja atuou')


    def passarVez(self):
        self.dict_jogada = {}
        self.jogador_atual = self.proximo_jogador
        for k,jogador in enumerate(self.jogadores):
            if jogador.id ==self.proximo_jogador.id:
                index = (k+1)%3
                self.proximo_jogador = self.jogadores[index]
                break
                
        self.dict_jogada['tipo'] = 'passar'
        self.dict_jogada['match_status'] = 'next'

        self.jogou_carta = False
        self.comprou_carta = False

    def transform_play_to_dict(self, tipo_jogada) -> dict:
        
        jogada ={}

        if tipo_jogada == 'init':
            jogada['tipo'] = 'init'
            jogada['match_status'] = 'progress'
            jogada['baralho'] = self.mesa.baralho.to_json()
            jogada['jogador_1'] = self.jogadores[0].to_json()
            jogada['jogador_2'] = self.jogadores[1].to_json()      
            jogada['jogador_3'] = self.jogadores[2].to_json()      
            jogada['jogador_atual'] = self.get_jogador_atual()
            jogada['mesa'] = self.mesa.ultima_carta.to_json()
            
        return jogada
        
    def transform_dict_to_object(self,dict_json: dict):
        baralho = dict_json['baralho']['cartas']
        
        baralho_list =[]

        for carta in baralho:
            frente = carta['frente']
            verso = carta['verso']
            if frente['tipo'] == 'numerica':
                frente = FaceNumerica(frente['id'],frente['cor'],frente['simbolo'],frente['tipo'])
            elif frente['tipo'] == 'colorida_poder':
                frente = FaceColoridaComPoder(frente['id'],frente['cor'],frente['simbolo'],frente['tipo'])
            if verso['tipo'] == 'numerica':
                verso = FaceNumerica(verso['id'],verso['cor'],verso['simbolo'],verso['tipo'])
            elif verso['tipo'] == 'colorida_poder':
                verso = FaceColoridaComPoder(verso['id'],verso['cor'],verso['simbolo'],verso['tipo'])
            baralho_list.append(Carta(frente,verso))

        self.mesa.baralho.cartas = baralho_list
        
        carta_mesa = dict_json['mesa']

        frente = carta_mesa['frente']
        verso = carta_mesa['verso']
        if frente['tipo'] == 'numerica':
            frente = FaceNumerica(frente['id'],frente['cor'],frente['simbolo'],frente['tipo'])
        elif frente['tipo'] == 'colorida_poder':
            frente = FaceColoridaComPoder(frente['id'],frente['cor'],frente['simbolo'],frente['tipo'])
        if verso['tipo'] == 'numerica':
            verso = FaceNumerica(verso['id'],verso['cor'],verso['simbolo'],verso['tipo'])
        elif verso['tipo'] == 'colorida_poder':
            verso = FaceColoridaComPoder(verso['id'],verso['cor'],verso['simbolo'],verso['tipo'])
        
        carta_mesa = Carta(frente,verso)        
        
        self.mesa.ultima_carta = carta_mesa

        jogador_1 =dict_json['jogador_1']
        id_jogador = jogador_1['id']
        nome = jogador_1['nome']
        mao = jogador_1['mao']
        ordem = jogador_1['ordem']
        mao_list =[]

        for carta in mao:
            frente = carta['frente']
            verso = carta['verso']
            if frente['tipo'] == 'numerica':
                frente = FaceNumerica(frente['id'],frente['cor'],frente['simbolo'],frente['tipo'])
            elif frente['tipo'] == 'colorida_poder':
                frente = FaceColoridaComPoder(frente['id'],frente['cor'],frente['simbolo'],frente['tipo'])
            if verso['tipo'] == 'numerica':
                verso = FaceNumerica(verso['id'],verso['cor'],verso['simbolo'],verso['tipo'])
            elif verso['tipo'] == 'colorida_poder':
                verso = FaceColoridaComPoder(verso['id'],verso['cor'],verso['simbolo'],verso['tipo'])
            mao_list.append(Carta(frente,verso))

        self.jogadores[0] = Jogador(id_jogador,nome,ordem,mao_list)

        jogador_2 =dict_json['jogador_2']
        id_jogador = jogador_2['id']
        nome = jogador_2['nome']
        ordem = jogador_2['ordem']
        mao = jogador_2['mao']
        mao_list =[]

        for carta in mao:
            frente = carta['frente']
            verso = carta['verso']
            if frente['tipo'] == 'numerica':
                frente = FaceNumerica(frente['id'],frente['cor'],frente['simbolo'],frente['tipo'])
            elif frente['tipo'] == 'colorida_poder':
                frente = FaceColoridaComPoder(frente['id'],frente['cor'],frente['simbolo'],frente['tipo'])
            if verso['tipo'] == 'numerica':
                verso = FaceNumerica(verso['id'],verso['cor'],verso['simbolo'],verso['tipo'])
            elif verso['tipo'] == 'colorida_poder':
                verso = FaceColoridaComPoder(verso['id'],verso['cor'],verso['simbolo'],verso['tipo'])
            mao_list.append(Carta(frente,verso))

        self.jogadores[1] = Jogador(id_jogador,nome,ordem,mao_list)


        jogador_3 =dict_json['jogador_3']
        id_jogador = jogador_3['id']
        nome = jogador_3['nome']
        ordem = jogador_3['ordem']
        mao = jogador_3['mao']

        mao_list =[]

        for carta in mao:
            frente = carta['frente']
            verso = carta['verso']
            if frente['tipo'] == 'numerica':
                frente = FaceNumerica(frente['id'],frente['cor'],frente['simbolo'],frente['tipo'])
            elif frente['tipo'] == 'colorida_poder':
                frente = FaceColoridaComPoder(frente['id'],frente['cor'],frente['simbolo'],frente['tipo'])
            if verso['tipo'] == 'numerica':
                verso = FaceNumerica(verso['id'],verso['cor'],verso['simbolo'],verso['tipo'])
            elif verso['tipo'] == 'colorida_poder':
                verso = FaceColoridaComPoder(verso['id'],verso['cor'],verso['simbolo'],verso['tipo'])
            mao_list.append(Carta(frente,verso))

        self.jogadores[2] = Jogador(id_jogador,nome,ordem,mao_list)

        self.jogador_atual = dict_json['jogador_atual']
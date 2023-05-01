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
        self.grtou_uno = False
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


    def jogarCarta(self,carta,index):
        if not self.comprou_carta and not self.jogou_carta:
            valida =self.verificarValida(carta[1])
            if valida:
                self.tentarColocarCartaNaMesa(carta[1],index)
                     

        else:
            print('voce ja atuou nesse turno')
            

    def tentarColocarCartaNaMesa(self,carta,index):

        for k, j in enumerate(self.jogadores[index].mao):
            if carta is j:
                self.mesa.setUltimaCarta(j)
                del self.jogadores[index].mao[k]
                self.jogou_carta = True
                break





    def verificarValida(self,carta):

        if isinstance(carta.face_atual,FaceCoringa):

            return True

        elif self.mesa.ultima_carta.face_atual.cor == carta.face_atual.cor:

            return True

        elif self.mesa.ultima_carta.face_atual.get_simbolo() == carta.face_atual.get_simbolo():

 
            return True 
        
        else:
            return False


    def aplicarEfeito(self):
        pass
            


    def comprarCarta(self):
        pass







    def transform_play_to_dict(self, tipo_jogada) -> dict:
        
        jogada ={}

        if tipo_jogada == 'init':
            jogada['tipo'] = 'init'
            jogada['match_status'] = 'next'
            jogada['baralho'] = self.mesa.baralho.to_json()
            jogada['jogador_1'] = self.jogadores[0].to_json()
            jogada['jogador_2'] = self.jogadores[1].to_json()      
            jogada['jogador_3'] = self.jogadores[2].to_json()      
            jogada['jogador_atual'] = self.get_jogador_atual()
            
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
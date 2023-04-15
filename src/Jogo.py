from Baralho import Baralho
from Jogador import Jogador
import json

class Jogo:

    def __init__(self) -> None:
        self.jogadores = []
        self.local_id = ''
        self.status = 0
        self.direcao = 0
        self.jogador_atual = 0
        self.baralho = Baralho()

    def get_jogadores(self) -> list:
        return self.jogadores

    def get_status(self) -> int:
        return self.status

    def get_direcao(self) -> int:
        return self.direcao
    
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
        for jogador in jogadores:
            mao = self.dar_cartas_iniciais()
            self.jogadores.append(Jogador(id = jogador[1], nome =jogador[0], mao = mao))

    def dar_cartas_iniciais(self) -> list:
        mao = []
        for _ in range(8):
            carta = self.baralho.cartas.pop(0)
            mao.append(carta)
        return mao

    def transform_play_to_dict(self, tipo_jogada) -> dict:
        jogada ={}

        if tipo_jogada == 'init':
            jogada['baralho'] = self.baralho.tojson()
            jogada['jogador_1'] = self.jogadores[0].to_json()
            jogada['jogador_2'] = self.jogadores[1].to_json()      
            jogada['jogador_3'] = self.jogadores[2].to_json()      
            jogada['jogador_atual'] = self.get_jogador_atual()
            jogada['direcao'] = self.get_direcao()
        

    
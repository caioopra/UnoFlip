from Baralho import Baralho
from Jogador import Jogador

class Jogo:

    def __init__(self) -> None:
        self.jogadores = []
        self.status = 0
        self.ordem = 0
        self.jogador_atual = None
        self.baralho = Baralho()

    def get_jogadores(self) -> list:
        return self.jogadores

    def get_status(self) -> int:
        return self.status

    def get_ordem(self) -> int:
        return self.ordem
    
    def get_baralho(self) -> Baralho:
        return self.baralho
        
    def get_jogador_atual(self) -> Jogador:
        return self.jogador_atual

    def set_ordem(self, ordem:int) -> None:
        self.ordem = ordem
    
    
    

    
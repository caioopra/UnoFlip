from Baralho import Baralho


class Jogo:

    def __init__(self,jogadores:list,local_id:str) -> None:
        self.jogadores = jogadores
        self.local_id = local_id
        self.status = 0
        self.ordem = 0
        self.jogador_atual = 0
        self.baralho = Baralho()

    def get_jogadores(self) -> list:
        return self.jogadores

    def get_status(self) -> int:
        return self.status

    def get_ordem(self) -> int:
        return self.ordem
    
    def get_baralho(self) -> Baralho:
        return self.baralho
        
    def get_jogador_atual(self) -> int:
        return self.jogador_atual

    def set_ordem(self, ordem:int) -> None:
        self.ordem = ordem
    
    def set_jogador_atual(self,jogador:int) -> None:
        self.jogador_atual = jogador

    def dar_cartas_iniciais(self) -> None:
        for jogador in self.jogadores:
            for _ in range(8):
                pass
                # carta = self.baralho.pop(0)

    

    
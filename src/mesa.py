


class Mesa:

    def __init__(self,baralho) -> None:
        self.baralho = baralho
        self.ultima_carta = self.baralho.cartas.pop()

    def getUltimaCarta(self):
        return self.ultima_carta
    
    def setUltimaCarta(self, carta):
        self.ultima_carta=carta
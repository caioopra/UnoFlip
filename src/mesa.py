from random import randint


class Mesa:

    def __init__(self,baralho) -> None:
        self.baralho = baralho
        self.ultima_carta = self.baralho.cartas.pop()
        # self.setCartaInicial()

    def getUltimaCarta(self):
        return self.ultima_carta
    
    def setUltimaCarta(self, carta):
        self.ultima_carta=carta
    
    def setCartaInicial(self):
        carta = self.baralho.cartas.pop()
        self.setUltimaCarta(carta)
        if carta.frente.tipo == 'coringa':
            self.baralho.cartas.insert(randint(0, len(self.baralho.cartas)-2), carta)
            self.setCartaInicial()
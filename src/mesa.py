from random import randint


class Mesa:

    def __init__(self,baralho) -> None:
        self.baralho = baralho
        self.setCartaInicial()

    def getUltimaCarta(self):
        return self.ultima_carta
    
    def setUltimaCarta(self, carta):
        self.ultima_carta=carta
    
    def setCartaInicial(self):
        carta = self.baralho.cartas.pop()
        self.setUltimaCarta(carta)
        while carta.frente.tipo == 'coringa':
            self.baralho.cartas.insert(randint(0, len(self.baralho.cartas)-1), carta)
            carta = self.baralho.cartas.pop()
            self.setUltimaCarta(carta)   
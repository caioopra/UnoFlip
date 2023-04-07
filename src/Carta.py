

class Carta():
    def __init__(self, frente, verso) -> None:
        self.frente = frente
        self.verso = verso
        self.face_atual = frente

    def get_frente(self):
        return self.frente

    def get_verso(self):
        return self.verso

    def get_face_atual(self):
        return self.face_atual

    def flip(self):
        self.face_atual = self.verso if self.face_atual == self.frente else self.frente


    
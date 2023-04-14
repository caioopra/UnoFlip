from Face import Face

class Carta():
    def __init__(self, frente: Face, verso: Face) -> None:
        self.frente = frente
        self.verso = verso
        self.face_atual = frente

    def get_frente(self) -> Face:
        return self.frente

    def get_verso(self) -> Face:
        return self.verso

    def get_face_atual(self) -> Face:
        return self.face_atual

    def flip(self) -> None:
        self.face_atual = self.verso if self.face_atual == self.frente else self.frente


    
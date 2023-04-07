from abc import ABC
from Face import Face

class FaceColorida(Face, ABC):

    def __init__(self,cor,modelo):
        super().__init__()
        self.cor = cor

    def get_cor(self):
        return self.get_cor


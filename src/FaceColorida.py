from abc import ABC
from Face import Face

class FaceColorida(Face, ABC):

    def __init__(self,id,cor):
        super().__init__(id)
        self.cor = cor


    def get_cor(self):
        return self.cor


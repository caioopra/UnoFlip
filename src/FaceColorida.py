from abc import ABC
from Face import Face

class FaceColorida(Face, ABC):

    def __init__(self,id:str,cor:str) -> None:
        super().__init__(id)
        self.cor = cor


    def get_cor(self) -> str:
        return self.cor


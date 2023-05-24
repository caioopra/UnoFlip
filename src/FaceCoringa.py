from Face import Face

class FaceCoringa(Face):
    def __init__(self,id:str,cor:str,simbolo:str,tipo:str) -> None:
        super().__init__(id)
        self.simbolo = simbolo
        self.cor = cor
        self.tipo = tipo

    def get_poder(self) -> str:
        return self.poder
from FaceColorida import FaceColorida

class FaceNumerica(FaceColorida):

    def __init__(self,id:str,cor:str,simbolo:int,tipo) -> None:
        super().__init__(id,cor)
        self.simbolo = simbolo
        self.tipo = tipo

    def get_simbolo(self) -> int:
        return self.simbolo
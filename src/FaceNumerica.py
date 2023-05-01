from FaceColorida import FaceColorida

class FaceNumerica(FaceColorida):

    def __init__(self,id:str,cor:str,numero:int,tipo) -> None:
        super().__init__(id,cor)
        self.numero = numero
        self.tipo = tipo

    def get_numero(self) -> int:
        return self.numero
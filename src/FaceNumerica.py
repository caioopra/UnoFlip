from FaceColorida import FaceColorida

class FaceNumerica(FaceColorida):

    def __init__(self,id:str,cor:str,numero:int) -> None:
        super().__init__(id,cor)
        self.numero = numero

    def get_numero(self) -> int:
        return self.numero
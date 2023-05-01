from FaceColorida import FaceColorida

class FaceColoridaComPoder(FaceColorida):

    def __init__(self,id:str,cor:str,simbolo:str,tipo) -> None:
        super().__init__(id,cor)
        self.simbolo = simbolo
        self.tipo = tipo

    def get_simbolo(self) -> str:
        return self.simbolo
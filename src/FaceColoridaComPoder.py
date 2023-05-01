from FaceColorida import FaceColorida

class FaceColoridaComPoder(FaceColorida):

    def __init__(self,id:str,cor:str,poder:str,tipo) -> None:
        super().__init__(id,cor)
        self.poder = poder
        self.tipo = tipo

    def get_poder(self) -> str:
        return self.poder
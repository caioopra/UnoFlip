from FaceColorida import FaceColorida

class FaceColoridaComPoder(FaceColorida):

    def __init__(self,id:str,cor:str,poder:str) -> None:
        super().__init__(id,cor)
        self.poder = poder

    def get_poder(self) -> str:
        return self.poder
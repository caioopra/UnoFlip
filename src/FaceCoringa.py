from Face import Face

class FaceCoringa(Face):
    def __init__(self,poder:str,tipo) -> None:
        super().__init__()
        self.poder = poder
        self.tipo = tipo

    def get_poder(self) -> str:
        return self.poder
from Face import Face

class FaceCoringa(Face):
    def __init__(self,poder:str) -> None:
        super().__init__()
        self.poder = poder

    def get_poder(self) -> str:
        return self.poder
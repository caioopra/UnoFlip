from FaceColorida import FaceColorida

class FaceNumerica(FaceColorida):

    def __init__(self,numero):
        super().__init__()
        self.numero = numero

    def get_poder(self):
        return self.numero
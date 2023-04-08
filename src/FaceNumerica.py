from FaceColorida import FaceColorida

class FaceNumerica(FaceColorida):

    def __init__(self,id,cor,numero):
        super().__init__(id,cor)
        self.numero = numero

    def get_numero(self):
        return self.numero
from FaceColorida import FaceColorida

class FaceColoridaComPoder(FaceColorida):

    def __init__(self,id,cor,poder):
        super().__init__(id,cor)
        self.poder = poder

    def get_poder(self):
        return self.poder
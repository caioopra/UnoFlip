from FaceColorida import FaceColorida

class FaceColoridaComPoder(FaceColorida):

    def __init__(self,poder):
        super().__init__()
        self.poder = poder

    def get_poder(self):
        return self.poder
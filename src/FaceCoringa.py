from Face import Face

class FaceCoringa(Face):
    def __init__(self,poder):
        super().__init__()
        self.poder = poder

    def get_poder(self):
        return self.poder
from abc import ABC

class Face(ABC):

    def __init__(self,id):
        self.id =id

    def get_id(self):
        return self.id
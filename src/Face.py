from abc import ABC

class Face(ABC):

    def __init__(self):
        self.id =''

    def get_id(self):
        return self.id
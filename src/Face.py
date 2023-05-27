from abc import ABC

class Face(ABC):

    def __init__(self,id:str) -> None: 
        self.id =id

    def getId(self) -> str:
        return self.id
import json

class Jogador():

    def __init__(self,id :str, nome:str ,mao:list) -> None:
        self.id =id
        self.nome = nome
        self.mao = mao

    def get_id(self) -> str:
        return self.id


    def get_nome(self) -> str:
        return self.nome


    def get_mao(self) -> list:
        return self.mao

    def to_json(self) -> dict:
        return json.dumps(self, default=lambda o:o.__dict__)
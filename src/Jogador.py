import json

class Jogador():

    def __init__(self,id :str, nome:str, ordem ,mao:list) -> None:
        self.id =id
        self.nome = nome
        self.ordem = ordem
        self.mao = mao
        self.gritou_uno = False

    def get_id(self) -> str:
        return self.id

    def get_nome(self) -> str:
        return self.nome

    def get_mao(self) -> list:
        return self.mao

    def adicionarCartaMao(self,carta):
        self.mao.insert(0,carta)

    def gritar_uno(self):
        self.gritou_uno = True

    def to_json(self) -> dict:
        a =  json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        json_acceptable_string = a.replace("'", "\"")
        json_ = json.loads(json_acceptable_string)
        return json_
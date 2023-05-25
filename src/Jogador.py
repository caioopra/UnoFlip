import json


class Jogador:
    def __init__(self, id: str, nome: str, ordem, mao: list) -> None:
        self.id = id
        self.nome = nome
        self.ordem = ordem
        self.mao = mao

        self.denunciavel = False
        self.jogou_carta = False
        self.comprou_carta = False

    def gritar_uno(self):
        self.denunciavel = False

    def comprarCarta(self, baralho):
        print("comprando carta no jogador")
        self.mao.insert(0, baralho.darCarta())
        self.comprou_carta = True
        self.denunciavel = False
    
    # para quando recebe punição
    def receberCartas(self, quantidade, baralho):  
        for _ in range(quantidade):
            self.mao.insert(0, baralho.darCarta())

        self.denunciavel = False
        
    def verificarDenunciavel(self):
        if len(self.mao) == 1: 
            self.denunciavel = True
            print("virou denunciavel")

    def to_json(self) -> dict:
        a = json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        json_acceptable_string = a.replace("'", "\"")
        json_ = json.loads(json_acceptable_string)
        return json_
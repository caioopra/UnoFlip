import json


class Jogador:
    def __init__(self, id: str, nome: str, mao: list) -> None:
        self.__id = id
        self.__nome = nome
        self.__mao = mao

        self.__denunciavel = False
        self.__jogou_carta = False
        self.__comprou_carta = False

    def get_id(self):
        return self.__id
    
    def set_id(self, id):
        self.__id = id
        
    def get_nome(self):
        return self.__nome
    
    def set_nome(self, nome):
        self.__nome = nome
        
    def get_mao(self):
        return self.__mao
    
    def set_mao(self, mao):
        self.__mao = mao
        
    def get_denunciavel(self):
        return self.__denunciavel
    
    def set_denunciavel(self, estado):
        self.__denunciavel = estado
    
    def get_jogou_carta(self):
        return self.__jogou_carta

    def set_jogou_carta(self, jogou):
        self.__jogou_carta = jogou
        
    def get_comprou_carta(self):
        return self.__comprou_carta
    
    def set_comprou_carta(self, comprou):
        self.__comprou_carta = comprou

    def gritar_uno(self):
        self.__denunciavel = False

    def comprarCarta(self, baralho):
        self.__mao.insert(0, baralho.darCarta())
        self.__comprou_carta = True
        self.__denunciavel = False
    
    # para quando recebe punição
    def receberCartas(self, quantidade, baralho):  
        for _ in range(quantidade):
            self.__mao.insert(0, baralho.darCarta())

        self.__denunciavel = False
        
    def verificarDenunciavel(self):
        if len(self.__mao) == 1: 
            self.__denunciavel = True
            print("virou denunciavel")

    def to_json(self) -> dict:
        a = json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        json_acceptable_string = a.replace("'", "\"")
        json_ = json.loads(json_acceptable_string)
        return json_
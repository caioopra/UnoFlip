class Face:
    def __init__(self, id: str, cor: str, simbolo: str, tipo: str) -> None:
        self.id = id
        self.cor = cor
        self.simbolo = simbolo
        self.tipo = tipo

    def getId(self) -> str:
        return self.id

    def getCor(self) -> str:
        return self.cor

    def getSimbolo(self) -> str:
        return self.simbolo

    def getTipo(self) -> str:
        return self.tipo

from Face import Face
import json

class Carta():
    def __init__(self, frente: Face, verso: Face) -> None:
        self.__frente = frente
        self.__verso = verso

    def getFrente(self) -> Face:
        return self.__frente

    def getVerso(self) -> Face:
        return self.__verso

    def flip(self) -> None:
        self.__frente, self.__verso = self.__verso, self.__frente

    def to_json(self) -> dict:
        a =  json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        json_acceptable_string = a.replace("'", "\"")
        json_ = json.loads(json_acceptable_string)
        return json_
    
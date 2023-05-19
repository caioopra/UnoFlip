from Face import Face
import json

class Carta():
    def __init__(self, frente: Face, verso: Face) -> None:
        self.frente = frente
        self.verso = verso


    def get_frente(self) -> Face:
        return self.frente

    def get_verso(self) -> Face:
        return self.verso

    def flip(self) -> None:
        self.frente, self.verso = self.verso, self.frente

    def to_json(self) -> dict:
        a =  json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        json_acceptable_string = a.replace("'", "\"")
        json_ = json.loads(json_acceptable_string)
        return json_
    
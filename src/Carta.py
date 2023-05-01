from Face import Face
import json

class Carta():
    def __init__(self, frente: Face, verso: Face) -> None:
        self.frente = frente
        self.verso = verso
        self.face_atual = frente

    def get_frente(self) -> Face:
        return self.frente

    def get_verso(self) -> Face:
        return self.verso

    def get_face_atual(self) -> Face:
        return self.face_atual

    def flip(self) -> None:
        self.face_atual = self.verso if self.face_atual == self.frente else self.frente

    def to_json(self) -> dict:
        a =  json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        json_acceptable_string = a.replace("'", "\"")
        json_ = json.loads(json_acceptable_string)
        return json_
    
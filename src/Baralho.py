from Carta import Carta
from Face import Face
from random import shuffle
import json
class Baralho():
    
    def __init__(self) -> None:
        self.__cartas = []
        self.criar_baralho()

    def getCartas(self):
        return self.__cartas

    def setCartas(self, cartas: list) -> None:
        self.__cartas = cartas

    def criar_baralho(self) -> None:
        cores = ['amarelo','vermelho', 'azul','verde']
        cores2 = ['laranja','rosa', 'roxo', 'ciano']
        
        aux = []
        aux2 = []

        pos = [12,25,38,51]

        for i in range(4):
            for j in range(1,10):
                face_numerica = Face(f'light_{pos[i]+j-1}',cores[i],str(j),'numerica')
                face_numerica_2 = Face(f'dark_{pos[i]+j-1}',cores2[i],str(j),'numerica')
                for _ in range(2):
                    aux.append(face_numerica)
                    aux2.append(face_numerica_2)

            face_girar = Face(f'light_{pos[i]+9}',cores[i],'girar','colorida_poder')
            face_girar2 = Face(f'dark_{pos[i]+9}',cores2[i],'girar','colorida_poder')
            for _ in range(2):
                aux.append(face_girar)
                aux2.append(face_girar2)

            face_compre_um = Face(f'light_{pos[i]+10}',cores[i],'mais_um','colorida_poder')
            face_compre_cinco = Face(f'dark_{pos[i]+10}',cores2[i],'mais_cinco','colorida_poder')
            for _ in range(2):
                aux.append(face_compre_um)
                aux2.append(face_compre_cinco)

            face_pular_vez = Face(f'light_{pos[i]+11}',cores[i],'pular_vez','colorida_poder')
            face_pular_todos = Face(f'dark_{pos[i]+11}',cores2[i],'pular_todos','colorida_poder')
            for _ in range(2):
                aux.append(face_pular_vez)
                aux2.append(face_pular_todos)
            
            face_inverter_ordem = Face(f'light_{pos[i]+12}',cores[i],'inverter_ordem','colorida_poder')
            face_inverter_ordem2 = Face(f'dark_{pos[i]+12}',cores2[i],'inverter_ordem','colorida_poder')
            for _ in range(2):
                aux.append(face_inverter_ordem)
                aux2.append(face_inverter_ordem2)

            face_coringa1 = Face(f'light_1',cores[i],'troca_cor','coringa')
            face_coringa2 = Face(f'dark_1',cores2[i],'troca_cor','coringa')
            for _ in range(2):
                aux.append(face_coringa1)
                aux2.append(face_coringa2)

            face_mais_dois = Face(f'light_6',cores[i],'mais_dois','coringa')
            face_compra_ate_vir = Face(f'dark_6',cores2[i],'compra_ate_vir','coringa')
            for _ in range(2):
                aux.append(face_mais_dois)
                aux2.append(face_compra_ate_vir)
            
        
            for _ in range(10):
                shuffle(aux)
                shuffle(aux2)

            for i in range(len(aux)):
                self.__cartas.append(Carta(aux[i],aux2[i]))

    def to_json(self) -> dict:
        a =  json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        json_acceptable_string = a.replace("'", "\"")
        json_ = json.loads(json_acceptable_string)
        return json_

    def darCarta(self):
        return self.__cartas.pop(0)

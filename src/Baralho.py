from Carta import Carta
from FaceNumerica import FaceNumerica
from FaceColoridaComPoder import FaceColoridaComPoder
from FaceCoringa import FaceCoringa
from random import shuffle
class Baralho():
    
    def __init__(self) -> None:
        self.cartas = []
        self.cartas_jogadas = []
        self.criar_baralho()



    def criar_baralho(self) -> None:
        cores = ['amarelo','vermelho', 'azul','verde']
        cores2 = ['laranja','rosa', 'roxo', 'ciano']
        
        aux = []
        aux2 = []

        pos = [12,25,38,51]

        for i in range(4):
            for j in range(1,10):
                face_numerica = FaceNumerica(f'light_{pos[i]+j-1}',cores[i],str(j))
                face_numerica_2 = FaceNumerica(f'dark_{pos[i]+j-1}',cores2[i],str(j))
                for _ in range(2):
                    aux.append(face_numerica)
                    aux2.append(face_numerica_2)

            face_girar = FaceColoridaComPoder(f'light_{pos[i]+9}',cores[i],'girar')
            face_girar2 = FaceColoridaComPoder(f'dark_{pos[i]+9}',cores[i],'girar')
            for _ in range(2):
                aux.append(face_girar)
                aux2.append(face_girar2)

            face_compre_um = FaceColoridaComPoder(f'light_{pos[i]+10}',cores[i],'mais_um')
            face_compre_cinco = FaceColoridaComPoder(f'dark_{pos[i]+10}',cores[i],'mais_cinco')
            for _ in range(2):
                aux.append(face_compre_um)
                aux2.append(face_compre_cinco)

            face_pular_vez = FaceColoridaComPoder(f'light_{pos[i]+11}',cores[i],'pular_vez')
            face_pular_todos = FaceColoridaComPoder(f'dark_{pos[i]+11}',cores[i],'pular_todos')
            for _ in range(2):
                aux.append(face_pular_vez)
                aux2.append(face_pular_todos)
            
            face_inverter_ordem = FaceColoridaComPoder(f'light_{pos[i]+12}',cores[i],'inverter_ordem')
            face_inverter_ordem2 = FaceColoridaComPoder(f'dark_{pos[i]+12}',cores[i],'inverter_ordem')
            for _ in range(2):
                aux.append(face_inverter_ordem)
                aux2.append(face_inverter_ordem2)

            # face_coringa1= FaceColoridaComPoder(f'light_{pos[i]+12}',cores[i],'inverter_ordem')
            # face_coring2 = FaceColoridaComPoder(f'dark_{pos[i]+12}',cores[i],'inverter_ordem')
            # for _ in range(2):
            #     aux.append(face_inverter_ordem)
            #     aux2.append(face_inverter_ordem2)
        
            shuffle(aux)
            shuffle(aux2)
            for i in range(len(aux)):
                self.cartas.append(Carta(aux[i],aux2[i]))


    def embaralhar(self) -> None:
        shuffle(self.cartas)


    def comprar_carta(self) -> None:
        carta = self.cartas.pop(0)
        self.cartas_jogadas.append(carta)
        return carta

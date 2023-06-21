from Baralho import Baralho
from Carta import Carta
from Face import Face
from Jogador import Jogador
from mesa import Mesa
from time import sleep


class Jogo:
    def __init__(self) -> None:
        self.__jogadores = [0, 0, 0]
        self.__local_id = ""
        self.__status = 0
        self.__jogador_atual = None
        self.__proximo_jogador = None
        self.__left_position = 0
        self.__local_position = 0
        self.__right_position = 0
        self.__dict_jogada = {}
        self.__mesa = Mesa(Baralho())
        self.__ordem = 1
        self.__fim_jogo = False
        self.__jogo_abandonado = False

    def getJogadores(self) -> list:
        return self.__jogadores

    def getStatus(self) -> int:
        return self.__status

    def getJogadorAtual(self) -> int:
        return self.__jogador_atual

    def getLocalId(self) -> str:
        return self.__local_id

    def setLocalId(self, local_id):
        self.__local_id = local_id

    def set_ordem(self, direcao: int) -> None:
        self.direcao = direcao

    def setJogadorAtual(self, jogador: int) -> None:
        self.__jogador_atual = jogador

    def getJogadorAtual(self) -> int:
        return self.__jogador_atual

    def getProximoJogador(self) -> int:
        return self.__proximo_jogador

    def setProximoJogador(self, proximo: int) -> int:
        self.__proximo_jogador = proximo

    def getLeftPosition(self) -> int:
        return self.__left_position

    def setLeftPosition(self, position: int) -> None:
        self.__left_position = position

    def getRightPosition(self) -> int:
        return self.__right_position

    def setRightPosition(self, position: int) -> None:
        self.__right_position = position

    def getLocalPosition(self) -> int:
        return self.__local_position

    def setLocalPosition(self, position: int) -> None:
        self.__local_position = position

    def getDictJogada(self) -> dict:
        return self.__dict_jogada

    def getMesa(self) -> Mesa:
        return self.__mesa
    
    def getFimJogo(self) -> bool:
        return self.__fim_jogo
    
    def setFimJogo(self, state: bool) -> None:
        self.__fim_jogo = state
        
    def getJogoAbandonado(self) -> bool:
        return self.__jogo_abandonado
    
    def setJogoAbandonado(self, state: bool) -> None:
        self.__jogo_abandonado = state

    def comecarPartida(self, jogadores: list, id_jogador_local: int):
        self.setLocalId(id_jogador_local)
        self.criar_jogadores(jogadores)

        return self.transform_play_to_dict("init")

    def criar_jogadores(self, jogadores):
        for i, jogador in enumerate(jogadores):
            mao = self.dar_cartas_iniciais()
            self.__jogadores[i] = Jogador(id=jogador[1], nome=jogador[0], mao=mao)

    def configurarJogadores(self):
        for k, jogador in enumerate(self.__jogadores):
            if jogador.getId() == self.__local_id:
                self.setLocalPosition(k)
                self.setRightPosition((k + 1) % 3)
                self.setLeftPosition(k - 1)

        self.setJogadorAtual(self.getJogadores()[0])
        self.setProximoJogador(self.getJogadores()[1])

    def dar_cartas_iniciais(self) -> list:
        mao = []
        for _ in range(7):
            carta = self.getMesa().getBaralho().getCartas().pop()
            mao.append(carta)
        return mao

    def darCarta(self, jogador, quantidade):
        baralho = self.getMesa().getBaralho()
        jogador.receberCartas(quantidade, baralho)

        if jogador.getDenunciavel():
            jogador.setDenunciavel(False)

    def jogarCarta(self, index):
        valida = False
        if (
            not self.getJogadorAtual().getComprouCarta()
            and not self.getJogadorAtual().getJogouCarta()
        ):
            valida = self.tentarColocarCartaNaMesa(index)
            self.getJogadorAtual().verificarDenunciavel()
        else:
            print("voce ja atuou nesse turno")

        return valida

    def tentarColocarCartaNaMesa(self, index):
        valida = self.verificarValida(index)

        if valida:
            self.getJogadorAtual().setJogouCarta(True)
            self.getMesa().setUltimaCarta(self.getJogadorAtual().getMao()[index])
            self.aplicarEfeito(index)
            del self.getJogadorAtual().getMao()[index]
            self.__dict_jogada = {}
            self.__dict_jogada["tipo"] = "jogar"
            self.__dict_jogada["index"] = index
            self.__dict_jogada["match_status"] = "progress"
        else:
            print("nao pode jogar essa carta")

        return valida

    def verificarValida(self, index):
        carta = self.getJogadorAtual().getMao()[index]

        if carta.getFrente().getTipo() == "coringa":
            return True

        elif self.getMesa().getUltimaCarta().getFrente().cor == carta.getFrente().cor:
            return True

        elif (
            self.getMesa().getUltimaCarta().getFrente().getSimbolo()
            == carta.getFrente().getSimbolo()
        ):
            return True

        else:
            return False

    def verificar_UNO(self):
        self.__dict_jogada = {}
        achou_denunciavel = False

        for jogador in self.__jogadores:
            if jogador.getDenunciavel():
                self.darCarta(jogador, 2)
                achou_denunciavel = True

        # verificacao para o jogador atual
        tamanho = len(self.getJogadorAtual().getMao())
        if not achou_denunciavel and tamanho > 1:
            self.darCarta(self.getJogadorAtual(), 2)

        self.__dict_jogada["tipo"] = "uno"
        self.__dict_jogada["match_status"] = "progress"

    def aplicarEfeito(self, index):
        carta = self.getJogadorAtual().getMao()[index]

        if (
            carta.getFrente().getTipo() == "coringa"
            or carta.getFrente().getTipo() == "colorida_poder"
        ):
            efeito = carta.getFrente().simbolo
            if efeito == "mais_um":
                self.darCarta(self.getProximoJogador(), 1)
            elif efeito == "inverter_ordem":
                self.__ordem = -self.__ordem
                for k, i in enumerate(self.__jogadores):
                    if i.getId() == self.__jogador_atual.getId():
                        self.__proximo_jogador = self.__jogadores[
                            (k + self.__ordem) % 3
                        ]
                        break

            elif efeito == "pular_vez":
                for k, jogador in enumerate(self.getJogadores()):
                    if jogador.getId() == self.getProximoJogador().getId():
                        index = (k + self.__ordem) % 3
                        self.setProximoJogador(self.getJogadores()[index])
                        break
            elif efeito == "girar":
                print("girando")
                for carta in self.getMesa().getBaralho().getCartas():
                    carta.flip()
                for jogador in self.__jogadores:
                    for carta in jogador.getMao():
                        carta.flip()
            elif efeito == "mais_cinco":
                self.darCarta(self.getProximoJogador(), 5)
            elif efeito == "pular_todos":
                for k, jogador in enumerate(self.__jogadores):
                    if jogador.getId() == self.getProximoJogador().getId():
                        index = (k + 2 * self.__ordem) % 3
                        self.setProximoJogador(self.getJogadores()[index])
                        break

            elif efeito == "compra_ate_vir":
                pass
            elif efeito == "mais_dois":
                self.darCarta(self.getProximoJogador(), 2)

    def verificarTurno(self) -> bool:
        return self.getLocalId() == self.getJogadorAtual().getId()

    def comprarCarta(self):
        if not (
            self.getJogadorAtual().getComprouCarta()
            or self.getJogadorAtual().getJogouCarta()
        ):
            self.getJogadorAtual().comprarCarta(self.getMesa().getBaralho())

            if self.getJogadorAtual().getDenunciavel():
                self.getJogadorAtual().setDenunciavel(False)

            self.__dict_jogada["tipo"] = "comprar"
            self.__dict_jogada["match_status"] = "progress"
        else:
            print("ja atuou")

    def passarVez(self):
        print(f"{self.getJogadorAtual().getId()} passando a vez para ", end="")
        self.__dict_jogada = {}

        self.getJogadorAtual().setJogouCarta(False)
        self.getJogadorAtual().setComprouCarta(False)
        self.setJogadorAtual(self.getProximoJogador())

        for k, jogador in enumerate(self.__jogadores):
            if jogador.getId() == self.getProximoJogador().getId():
                index = (k + self.__ordem) % 3
                self.setProximoJogador(self.__jogadores[index])
                # for jogador in self.__jogadores: print("jogador: ", jogador.getId())
                break

        print("proximo jogador: ", self.__jogador_atual.getId())
        self.__dict_jogada["tipo"] = "passar"
        self.__dict_jogada["match_status"] = "next"

    def compraAteVir(self, cor: str):
        self.getProximoJogador().receberCartas(1, self.getMesa().getBaralho())
        carta_comprada = self.getProximoJogador().getMao()[0]

        if not carta_comprada.getFrente().getTipo() == "coringa":
            while carta_comprada.getFrente().cor != cor:
                if not carta_comprada.getFrente().getTipo() == "coringa":
                    self.getProximoJogador().receberCartas(
                        1, self.getMesa().getBaralho()
                    )
                    carta_comprada = self.getProximoJogador().getMao()[0]

    def transform_play_to_dict(self, tipo_jogada) -> dict:
        jogada = {}

        if tipo_jogada == "init":
            jogada["tipo"] = "init"
            jogada["match_status"] = "progress"
            jogada["baralho"] = self.getMesa().getBaralho().to_json()
            jogada["jogador_1"] = self.__jogadores[0].to_json()
            jogada["jogador_2"] = self.__jogadores[1].to_json()
            jogada["jogador_3"] = self.__jogadores[2].to_json()
            jogada["jogador_atual"] = self.getJogadorAtual()
            jogada["mesa"] = self.getMesa().getUltimaCarta().to_json()

        return jogada

    def transform_dict_to_object(self, dict_json: dict):
        baralho = dict_json["baralho"]["_Baralho__cartas"]

        baralho_list = []

        for carta in baralho:
            frente = carta["_Carta__frente"]
            verso = carta["_Carta__verso"]
            
            frente = Face(frente["id"], frente["cor"], frente["simbolo"], frente["tipo"])
            verso = Face(verso["id"], verso["cor"], verso["simbolo"], verso["tipo"])
            
            baralho_list.append(Carta(frente, verso))

        self.getMesa().getBaralho().setCartas(baralho_list)

        carta_mesa = dict_json["mesa"]

        frente = carta_mesa["_Carta__frente"]
        verso = carta_mesa["_Carta__verso"]
        
        frente = Face(frente["id"], frente["cor"], frente["simbolo"], frente["tipo"])
        verso = Face(verso["id"], verso["cor"], verso["simbolo"], verso["tipo"])

        carta_mesa = Carta(frente, verso)

        self.getMesa().setUltimaCarta(carta_mesa)

        jogador_1 = dict_json["jogador_1"]
        id_jogador = jogador_1["_Jogador__id"]
        nome = jogador_1["_Jogador__nome"]
        mao = jogador_1["_Jogador__mao"]
        mao_list = []

        for carta in mao:
            frente = carta["_Carta__frente"]
            verso = carta["_Carta__verso"]
            
            frente = Face(frente["id"], frente["cor"], frente["simbolo"], frente["tipo"])
            verso = Face(verso["id"], verso["cor"], verso["simbolo"], verso["tipo"])

            mao_list.append(Carta(frente, verso))

        self.__jogadores[0] = Jogador(id_jogador, nome, mao_list)

        jogador_2 = dict_json["jogador_2"]
        id_jogador = jogador_2["_Jogador__id"]
        nome = jogador_2["_Jogador__nome"]
        mao = jogador_2["_Jogador__mao"]
        mao_list = []

        for carta in mao:
            frente = carta["_Carta__frente"]
            verso = carta["_Carta__verso"]
            
            frente = Face(frente["id"], frente["cor"], frente["simbolo"], frente["tipo"])
            verso = Face(verso["id"], verso["cor"], verso["simbolo"], verso["tipo"])
            
            mao_list.append(Carta(frente, verso))

        self.__jogadores[1] = Jogador(id_jogador, nome, mao_list)

        jogador_3 = dict_json["jogador_3"]
        id_jogador = jogador_3["_Jogador__id"]
        nome = jogador_3["_Jogador__nome"]
        mao = jogador_3["_Jogador__mao"]

        mao_list = []

        for carta in mao:
            frente = carta["_Carta__frente"]
            verso = carta["_Carta__verso"]
            
            frente = Face(frente["id"], frente["cor"], frente["simbolo"], frente["tipo"])
            verso = Face(verso["id"], verso["cor"], verso["simbolo"], verso["tipo"])
            
            mao_list.append(Carta(frente, verso))

        self.__jogadores[2] = Jogador(id_jogador, nome, mao_list)

        self.__jogador_atual = dict_json["jogador_atual"]

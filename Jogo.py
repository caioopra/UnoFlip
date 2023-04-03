from tkinter import *
from PIL import Image, ImageTk
from Window import Window
from TelaMenu import TelaMenu
from TelaMesa import TelaMesa


class Jogo():
    def __init__(self) -> None:
        self.window = Window()
        self.menu = TelaMenu(self.window.window, lambda x:self.table.start())
        self.table = TelaMesa(self.window.window)


    def start_game(self):
        self.menu.start()

                


if __name__ == '__main__':
        
    tela = Jogo()

    tela.start_game()
from tkinter import *
from PIL import Image, ImageTk
from Window import Window
from Menu import Menu
from Table import Table


class Game():
    def __init__(self) -> None:
        self.window = Window()
        self.menu = Menu(self.window.window, lambda x:self.table.start())
        self.table = Table(self.window.window)


    def start_game(self):
        self.menu.start()

                



tela = Game()

tela.start_game()
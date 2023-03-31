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

                
    def add_card(self,card,x,y):
        image=Image.open(f'UNO_cards_small_dark/{card}.png')
        img=image.resize((100, 150))
        self.dict_of_cards[card] = ImageTk.PhotoImage(img)
        button_card = self.table.canvas.create_image(x, y, image=self.dict_of_cards[card])
        self.canvas.tag_bind(button_card, "<Button-1>", lambda x:self.selectCard(card))


tela = Game()

tela.start_game()
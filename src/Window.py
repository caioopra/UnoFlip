from tkinter import *

class Window():

    def __init__(self) -> None:
        self.window = Tk()
        self.createWindow()

    def createWindow(self):
        self.window.geometry("1280x720")
        self.window.configure(bg = "#ffffff")
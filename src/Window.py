from tkinter import *

class Window():

    def __init__(self) -> None:
        self.window = Tk()
        self.createWindow()

    def createWindow(self) -> None:
        self.window.geometry("1280x720")
        self.window.configure(bg = "#ffffff")

    def get_window(self) -> Tk:
        return self.window
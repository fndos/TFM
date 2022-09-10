from tkinter import *
from common.constants import *


class ButtonWidget:
    def __init__(self, master, title, fn):
        button = Button(master, text=title, command=fn)
        button.pack(side=LEFT, pady=BUTTON_PADX, padx=BUTTON_PADY)
        self.button = button

from tkinter import *
from common.constants import *


class ButtonWidget:
    def __init__(self, master, label, fn):
        button = Button(master, text=label, command=fn)
        button.pack(side=LEFT, pady=BUTTON_PADX, padx=BUTTON_PADY)
        self.button = button

from tkinter import *
from common.constants import *


class LabelWidget:
    def __init__(self, master, title):
        frame = Frame(master,  borderwidth=DEFAULT_BORDERWIDTH)
        frame.pack(fill=BOTH, expand=True)
        label = Label(frame, text=title, anchor=W, width=LARGE_LABEL_WIDTH)
        label.pack(fill=BOTH, side=LEFT, padx=LARGE_LABEL_PADX)
        self.label = label

    def update(self, label):
        self.label.config(text=label)

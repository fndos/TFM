from tkinter import *
from common.constants import *


class InputWidget:
    def __init__(self, master, label):
        frame = Frame(master,  borderwidth=FRAME_BORDERWIDTH)
        frame.pack(fill=BOTH, expand=True)
        label = Label(frame, text=label, anchor=W, width=LABEL_WIDTH)
        label.pack(fill=BOTH, side=LEFT, padx=LABEL_PADX)
        entry = Entry(frame)
        entry.pack(side=LEFT)
        self.entry = entry

    def get_entry(self):
        return self.entry.get()

    def delete_entry(self):
        self.entry.delete(0, END)

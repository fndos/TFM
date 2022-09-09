from tkinter import *
from common.constants import *


class ContainerWidget:
    def __init__(self, master, label, children=False):
        labelframe = LabelFrame(
            master, text=label, borderwidth=DEFAULT_BORDERWIDTH)
        labelframe.pack(fill=BOTH, expand=True,
                        padx=CONTAINER_PADX, pady=CONTAINER_PADY)
        if (children):
            frame = Frame(labelframe,  borderwidth=FRAME_BORDERWIDTH)
            frame.pack(fill=BOTH, expand=True)
            self.frame = frame
        self.labelframe = labelframe

from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo
from common.constants import *


class TableWidget:
    def __init__(self, master, headers):
        frame = Frame(master,  borderwidth=DEFAULT_BORDERWIDTH)
        frame.pack(fill=BOTH, expand=True)

        tree = ttk.Treeview(frame, columns=headers, show='headings')
        [tree.heading(header, text=header) for header in headers]
        tree.bind('<<TreeviewSelect>>', self.item_selected)
        tree.pack(side=LEFT)

        scrollbar = ttk.Scrollbar(frame, orient=VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill='y')

        self.tree = tree
        self.scrollbar = scrollbar

    def create(self, data):
        self.destroy()
        [self.tree.insert('', END, values=value) for value in data]

    def destroy(self):
        self.tree.delete(*self.tree.get_children())

    def item_selected(self, event):
        for selected_item in self.tree.selection():
            item = self.tree.item(selected_item)
            record = [str(value) for value in item['values']]
            #showinfo(title='Information', message=','.join(record))

import tkinter as tk
from tkinter import ttk
from . import views as v
from . import models as m


class Application(tk.Tk):
    """Application root window"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.model = m.Model()

        self.title("ABQ Data Entry Application")
        self.columnconfigure(0, weight=1)

        ttk.Label(
            self,
            text="ABQ Data Entry Application",
            font=("TkDefaultFont", 16)
        ).grid(row=0)

        self.form = v.DataRecordForm(self, self.model)
        self.form.grid(row=1, padx=10, sticky=(tk.W + tk.E))

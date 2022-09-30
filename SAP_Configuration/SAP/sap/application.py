import tkinter as tk
from tkinter import ttk
from . import views as v
from .utils import verify_window
from . import models as m


class Application(tk.Tk):
    """Application root window"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        
        self.title("ConfigTool Application")
        self.columnconfigure(0, weight=1)

        ttk.Button(self, text="Configuration",
                   command=verify_window).grid(sticky=(tk.W + tk.E))

from tkinter import messagebox
from .views import SAPWindow

import sap


def verify_window():
    if sap.flag:
        SAPWindow()
    else:
        messagebox.showerror(
            title="Error!",
            message="You just have already opened the window!")

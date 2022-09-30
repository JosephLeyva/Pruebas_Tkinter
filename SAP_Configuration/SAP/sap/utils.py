from tkinter import messagebox
from .views import SAPWindow

from sap import flag


def verify_window():
    global flag
    print(flag)
    if flag:
        SAPWindow()
    else:
        messagebox.showerror(
            title="Error!",
            message="You just have already opened the window!")

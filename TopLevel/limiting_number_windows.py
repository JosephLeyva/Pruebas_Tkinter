'''
On these program we are going to try to limit the number of TopLevel() widgets that are created
'''

import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.geometry("300x200")
root.title("Pruebas con Ventanas TopLevel")

global counter
counter = 0


def on_closing(top):
    global counter
    counter -= 1
    top.destroy()


def open():
    global counter

    # Create counter logic
    if counter < 1:
        top = tk.Toplevel()
        top.geometry("400x200")
        top.title("New Window")

        my_label = tk.Label(top, text="New Window!", font=("Helvetica", 30))
        my_label.pack(padx=50, pady=50)

        top.protocol('WM_DELETE_WINDOW', lambda: on_closing(top))

        counter += 1
    else:
        messagebox.showerror(
            title="Error!",
            message="You just have already opened the window!")



entry = tk.Entry().pack()
my_button = tk.Button(root, text='Open Window', command=open)
my_button.pack(pady=50, padx=50)


root.mainloop()

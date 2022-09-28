import tkinter as tk


def New_Window():
    Window = tk.Toplevel()
    canvas = tk.Canvas(Window, height=HEIGHT, width=WIDTH)
    canvas.pack()


HEIGHT = 300
WIDTH = 500

root = tk.Tk()
root.title("Python Guides")
canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

button = tk.Button(root, text="Click ME", bg='White', fg='Black',
                   command=New_Window)

button.pack()
root.mainloop()

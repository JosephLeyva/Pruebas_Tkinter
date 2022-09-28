import tkinter as tk

root = tk.Tk()
root.title('Root window')


def open():
    top = tk.Toplevel()
    top.title("Second window")
    lbl = tk.Label(top, text="Hello World!").pack()
    btn2 = tk.Button(top,text='close window', command=top.destroy).pack()


btn = tk.Button(root, text="Open second window", command=open).pack()

root.mainloop()

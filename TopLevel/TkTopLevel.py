import tkinter as tk


class SettingsWindow:
    def __init__(self) -> None:
        self.win = tk.Toplevel()

        self.frame = tk.Frame(self.win)
        self.frame.pack(padx=5, pady=5)

        self.label = tk.Label(self.frame, text="This is the Settings Window")
        self.label.pack(padx=20, pady=5)

        var = tk.IntVar()

        self.radio1 = tk.Radiobutton(
            self.frame, text="Option 1", value=1, variable=var)
        self.radio1.pack(padx=10, pady=5)

        self.radio2 = tk.Radiobutton(
            self.frame, text="Option 2", value=2, variable=var)
        self.radio2.pack(padx=10, pady=5)


class MainWindow:
    def __init__(self, master) -> None:
        self.master = master

        self.frame = tk.Frame(self.master, width=200, height=200)
        self.frame.pack()

        self.button = tk.Button(
            self.frame, text="Settings Window", command=self.cl)
        self.button.place(x=50, y=50)

        self.button2 = tk.Button(
            self.frame, text="Min/Max Settings", command=self.c2)
        self.button2.place(x=50, y=100)

        self.flag = 0

    def cl(self):
        self.settings = SettingsWindow()
        self.flag = 1
        self.settings.win.mainloop()

    def c2(self):
        if self.flag == 1:  # If the window is active, withdraw it
            self.settings.win.withdraw()
            self.flag = 0
        else:
            self.settings.win.deiconify()


root = tk.Tk()
window = MainWindow(root)
root.mainloop()

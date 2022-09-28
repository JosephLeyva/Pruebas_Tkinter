from cgitb import text
import tkinter as tk


class Window:
    def __init__(self, master) -> None:
        self.frame = tk.Frame(master)
        self.settingsWindow = None

        button = tk.Button(self.frame, text="Open Settings", command=self.open)
        button.pack(padx=50, pady=50)

        button = tk.Button(
            self.frame, text="Update Settings", command=self.config)
        button.pack(padx=50, pady=50)

        self.label = tk.Label(self.frame, text="")
        self.label.pack(pady=10)

        self.frame.pack(padx=10, pady=10)

    def open(self):
        self.settingsWindow = SettingsWindow(self.update)

    def config(self):
        if self.settingsWindow != None:
            self.settingsWindow.input.set("Default Value")

    def update(self, input, option):
        print("Updated function belonging to Main Window was called")
        print(f"Entry Widget Value: {input.get()}")
        print(f"Radio Button Value: {option.get()}")

        self.label.configure(text=f"{input.get()} - {option.get()}")


class SettingsWindow:
    def __init__(self, update) -> None:
        top = tk.Toplevel()
        self.frame = tk.Frame()
        self.update = update

        self.input = tk.StringVar()
        entry = tk.Entry(top, textvariable=self.input)
        entry.pack(padx=50, pady=30)

        self.option = tk.IntVar()
        option1 = tk.Radiobutton(
            top, value=1, text="Option 1", variable=self.option)
        option1.pack(padx=10, pady=10)
        option2 = tk.Radiobutton(
            top, value=2, text="Option 2", variable=self.option)
        option2.pack(padx=10, pady=10)

        button = tk.Button(top, text="Apply Settings", command=self.submit)
        button.pack(pady=10)
        self.frame.pack(padx=10, pady=10)

    def submit(self):
        self.update(self.input, self.option)


root = tk.Tk()
window = Window(root)
root.mainloop()

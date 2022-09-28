import tkinter as tk
from tkinter import ttk


class Application:

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.agregar_menu()
        self.root.mainloop()

    def agregar_menu(self):
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)
        self.opciones = tk.Menu(self.menubar)
        self.opciones.add_command(
            label="Configurar ventana", command=self.configurar)
        self.menubar.add_cascade(label="Opciones", menu=self.opciones)

    def configurar(self):
        dialogo = DialogoTamaño(self.root)
        s = dialogo.mostrar()
        self.root.geometry(s[0]+"x"+s[1])


class DialogoTamaño:

    def __init__(self, root_window) -> None:
        self.dialogo = tk.Toplevel(root_window)
        self.label1 = ttk.Label(self.dialogo, text="Ingrese ancho")
        self.label1.grid(column=0, row=0, padx=5, pady=5)
        self.ancho = tk.StringVar()
        self.entry1 = ttk.Entry(self.dialogo, textvariable=self.ancho)
        self.entry1.grid(column=1, row=0, padx=5, pady=5)
        self.entry1.focus()

        self.label2 = ttk.Label(self.dialogo, text="Ingrese alto")
        self.label2.grid(column=0, row=1, padx=5, pady=5)
        self.alto = tk.StringVar()
        self.entry2 = ttk.Entry(self.dialogo, textvariable=self.alto)
        self.entry2.grid(column=1, row=1, padx=5, pady=5)

        self.boton = ttk.Button(
            self.dialogo, text="Confirmar", command=self.confirmar)
        self.boton.grid(column=1, row=2, padx=5, pady=5)

        self.dialogo.protocol("WM_DELETE_WINDOW", self.confirmar)
        self.dialogo.resizable(False, False)
        self.dialogo.grab_set()

    def mostrar(self):
        self.dialogo.wait_window()
        return (self.ancho.get(), self.alto.get())

    def confirmar(self):
        self.dialogo.destroy()


app = Application()

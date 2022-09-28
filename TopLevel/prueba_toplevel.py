'''
tk.TopLevel()
Ejemplo donde creamos nuevas ventanas usando el método TopLevel()
'''

import tkinter as tk


# para que no se ejecute al iniciar la aplicación, creemos una función que se active al presionar un boton
def envia_boton(i=[0]):
    # Creación de otra ventana
    ventana_nueva = tk.Toplevel()

    # ventana_nueva.grab_set()

    # Podemos crear tantas ventanas secundarias como queramos, y son modificables
    # al igual que hacemos con root
    ventana_nueva.title("Ventana Secundaria")
    ventana_nueva.geometry("300x200")

    # obtener el valor de entrada
    entry_value = entry.get()

    # Generar etiqueta
    label = tk.Label(
        ventana_nueva, text=f'El valor introducido en la ventana principal es: {entry_value}').grid(row=0)

    # cerrar ventana
    close_window = tk.Button(
        root, text="Cerrar la ventana", command=ventana_nueva.destroy).grid(row=2)


root = tk.Tk()
root.title("Ventana principal")
root.geometry("300x100")


entry = tk.Entry(root, width=20)
entry.grid(row=0)

# Al presionar el botón, ejecutará la función evia_boton y crear la nueva ventana
btn_enviar = tk.Button(root, text='Enviar', command=envia_boton).grid(row=1)

# botón para cerrar la ventana root
cerrar_root = tk.Button(root, text="Cerrar ventana principal",
                        command=root.destroy).grid(row=3)


root.mainloop()

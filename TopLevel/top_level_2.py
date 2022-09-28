import tkinter as tk


root = tk.Tk()
root.title("Ventana Principal")
label1 = tk.Label(
    root, text="Ventana Princial, cerra esta ventana cerrará la aplicación").pack()


t1 = tk.Toplevel(root)
t1.title("TopLevel")
label2 = tk.Label(t1, text="Ventana Secundaria (Hija)").pack()

t2 = tk.Toplevel(root)
t2.title("Transitoria")
t2.geometry('300x200')
label3 = tk.Label(
    t2, text="Esta es una ventana transitoria de la principal").pack()

# Permite que una ventana permanezca siempre encima de otra
t2.transient(root)


t3 = tk.Toplevel(root)
t3.title("Ventana hja 3")
t3.geometry("400x300+100+150")
label4 = tk.Label(t3, text="Ventana hija 3").pack()
entry = tk.Entry(t3).pack(padx=50, pady=50)

# Este método no nos permite que la ventana mover y no posee barra de título.
# Es completamente dependiente de nuestra barra principal
t3.overrideredirect(1)

root.mainloop()

import tkinter as tk
from tkinter import messagebox


# Uso de messagebox

# messagebox.showinfo(
#     title='This is the title',
#     message='This is the message',
#     detail='This is the detail'
# )

# Funciones del messagebox

see_more = messagebox.askyesno(
    title='See more?',
    message='Would you like to see another box?',
    detail='Click NO to quit'
)

if not see_more:
    exit()

messagebox.showinfo(
    title='You got it',
    message="Ok, here's another dialog.",
    detail='Hope you like it!'
)

root = tk.Tk()

root.mainloop()

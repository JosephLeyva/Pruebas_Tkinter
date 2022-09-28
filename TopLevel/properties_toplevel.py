import tkinter as tk

root = tk.Tk()
root.title("Tk - TopLevel")
root.geometry("500x500")
root.config(bg="royalblue")


def open_toplevel():
    top = tk.Toplevel(root, bg="royalblue", relief=tk.FLAT, bd=5)
    top.title("tk-text window")
    top.geometry("300x300")

    button = tk.Button(top, text="Open TopLevel",
                       font="Arial 20 bold", fg="green", bg="white", command=open_toplevel)
    button.pack(padx=20, pady=20, ipadx=20, ipady=20)

    top.mainloop()


frame_hello = tk.Frame(root, bg="red1", relief=tk.SUNKEN,
                       bd=10, height=50, width=100)
frame_hello.pack(padx=20, pady=20, ipadx=20, ipady=20)


button = tk.Button(root, text="Open TopLevel",
                   font="Arial 20 bold", fg="white", bg="green", command=open_toplevel)
button.pack(padx=20, pady=20, ipadx=20, ipady=20)

root.mainloop()

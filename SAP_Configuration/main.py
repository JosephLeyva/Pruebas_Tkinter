import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


def save(top):
    global flag
    flag = True
    top.destroy()


def close(top):
    for key, variable in variables.items():
        if isinstance(variable, tk.BooleanVar):
            variable.set(False)
        elif isinstance(variable, tk.IntVar):
            variable.set(0)
        else:
            variable.set('')

    global flag
    flag = True
    top.destroy()


def verify_window():
    if flag:
        open_SAP()
    else:
        messagebox.showerror(
            title="Error!",
            message="You just have already opened the window!")


def open_SAP():

    global flag
    flag = False

    top = tk.Toplevel()
    top.title("SAP Configuration")
    top.geometry("500x500")
    top.columnconfigure(0, weight=1)

    SAP_config = ttk.Frame(top)
    SAP_config.grid(padx=10, pady=30, sticky=(tk.E+tk.W))
    for i in range(2):
        SAP_config.columnconfigure(i, weight=1)

    ##################
    # TX Information #
    ##################

    tx_info = ttk.LabelFrame(SAP_config, text="Transmission (TX) information")
    tx_info.grid(column=0, row=0, padx=10, sticky=(tk.W+tk.E))

    ttk.Checkbutton(tx_info, text="TX Port", variable=variables["TX_Port"]).grid(
        row=0, column=0, pady=20, sticky=(tk.W+tk.E))

    ttk.Label(tx_info, text="Port Name").grid(
        row=1, column=0, pady=5, sticky=(tk.W+tk.E))
    ttk.Entry(tx_info, textvariable=variables["Port_Name_tx"]).grid(
        row=2, column=0, pady=5, sticky=(tk.W+tk.E))

    ttk.Label(tx_info, text="Max Number of Messages").grid(
        row=3, column=0, pady=5, sticky=(tk.W+tk.E))
    ttk.Entry(tx_info, textvariable=variables["Number_Msg_tx"], state=tk.DISABLED).grid(
        row=4, column=0, pady=5, sticky=(tk.W+tk.E))

    ttk.Label(tx_info, text="Max Message Size").grid(
        row=5, column=0, pady=5, sticky=(tk.W+tk.E))
    ttk.Entry(tx_info, textvariable=variables["Max_Msg_tx"]).grid(
        row=6, column=0, pady=5, sticky=(tk.W+tk.E))

    ttk.Label(tx_info, text="Protocol Type").grid(
        row=7, column=0, pady=5, sticky=(tk.W+tk.E))
    ttk.Entry(tx_info, textvariable=variables["Protocol_tx"], state=tk.DISABLED).grid(
        row=8, column=0, pady=5, sticky=(tk.W+tk.E))

    ttk.Label(tx_info, text="Extended Port").grid(
        row=9, column=0, pady=5, sticky=(tk.W+tk.E))
    ttk.Checkbutton(tx_info, variable=variables["Extended_Port_tx"]).grid(
        row=10, column=0, pady=5, sticky=(tk.W+tk.E))

    ##################
    # RX Information #
    ##################

    rx_info = ttk.LabelFrame(SAP_config, text="Reception (RX) information")
    rx_info.grid(column=1, row=0, padx=10, sticky=(tk.W+tk.E))

    ttk.Checkbutton(rx_info, text="RX Port", variable=variables["RX_Port"]).grid(
        row=0, column=0, pady=20, sticky=(tk.W+tk.E))

    ttk.Label(rx_info, text="Port Name").grid(
        row=1, column=0, pady=5, sticky=(tk.W+tk.E))
    ttk.Entry(rx_info, textvariable=variables["Port_Name_rx"]).grid(
        row=2, column=0, pady=5, sticky=(tk.W+tk.E))

    ttk.Label(rx_info, text="Max Number of Messages").grid(
        row=3, column=0, pady=5, sticky=(tk.W+tk.E))
    ttk.Entry(rx_info, textvariable=variables["Number_Msg_rx"], state=tk.DISABLED).grid(
        row=4, column=0, pady=5, sticky=(tk.W+tk.E))

    ttk.Label(rx_info, text="Max Message Size").grid(
        row=5, column=0, pady=5, sticky=(tk.W+tk.E))
    ttk.Entry(rx_info, textvariable=variables["Max_Msg_rx"]).grid(
        row=6, column=0, pady=5, sticky=(tk.W+tk.E))

    ttk.Label(rx_info, text="Protocol Type").grid(
        row=7, column=0, pady=5, sticky=(tk.W+tk.E))
    ttk.Entry(rx_info, textvariable=variables["Protocol_rx"], state=tk.DISABLED).grid(
        row=8, column=0, pady=5, sticky=(tk.W+tk.E))

    ttk.Label(rx_info, text="Extended Port").grid(
        row=9, column=0, pady=5, sticky=(tk.W+tk.E))
    ttk.Checkbutton(rx_info, variable=variables["Extended_Port_rx"]).grid(
        row=10, column=0, pady=5, sticky=(tk.W+tk.E))

    ################
    # Button Frame #
    ################

    buttons = tk.Frame(top)
    buttons.grid(pady=20, padx=20, sticky=(tk.E+tk.W))
    save_button = ttk.Button(buttons, text="Save", command=lambda: save(top))
    save_button.pack(side=tk.RIGHT, padx=5)

    cancel_button = ttk.Button(
        buttons, text="Cancel", command=lambda: close(top))
    cancel_button.pack(side=tk.RIGHT, padx=5)

    top.protocol('WM_DELETE_WINDOW', lambda: close(top))


root = tk.Tk()
root.title("ConfigTool")
root.columnconfigure(0, weight=1)

variables = dict()
variables['TX_Port'] = tk.BooleanVar(value=False)
variables["Port_Name_tx"] = tk.StringVar()
variables["Number_Msg_tx"] = tk.IntVar(value=10)
variables["Max_Msg_tx"] = tk.IntVar()
variables["Protocol_tx"] = tk.StringVar(value="UDP")
variables['Extended_Port_tx'] = tk.BooleanVar(value=False)
variables['RX_Port'] = tk.BooleanVar(value=False)
variables["Port_Name_rx"] = tk.StringVar()
variables["Number_Msg_rx"] = tk.IntVar(value=10)
variables["Max_Msg_rx"] = tk.IntVar()
variables["Protocol_rx"] = tk.StringVar(value="UDP")
variables['Extended_Port_rx'] = tk.BooleanVar(value=False)

flag = True


ttk.Label(root, text="ConfigTool Application", font=("Arial", 16)).grid(row=0)

source_info = tk.LabelFrame(root, text="User Config")
source_info.grid(padx=5, pady=5, sticky=(tk.E+tk.W))

ttk.Checkbutton(source_info).grid(row=1, column=0, sticky=(tk.W+tk.E))

ttk.Label(source_info, text="IP Adress").grid(
    row=0, column=1, padx=30, sticky=(tk.W+tk.E))
ttk.Entry(source_info).grid(
    row=1, column=1, pady=3, sticky=(tk.W+tk.E))

ttk.Button(source_info, text="Configuration",
           command=verify_window).grid(row=1, column=2, padx=5, pady=5)


root.mainloop()

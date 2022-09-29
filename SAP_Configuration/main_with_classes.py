from cgitb import text
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

global flag
flag = True


def verify_window():
    if flag:
        SAPWindow()
    else:
        messagebox.showerror(
            title="Error!",
            message="You just have already opened the window!")


class LabelInput(tk.Frame):
    """A widget containing a label and input together."""

    def __init__(
        self, parent, label, var, input_class=ttk.Entry,
        input_args=None, label_args=None, **kwargs
    ):
        super().__init__(parent, **kwargs)
        input_args = input_args or {}
        label_args = label_args or {}
        self.variable = var
        self.variable.label_widget = self

        # setup the label
        if input_class in (ttk.Checkbutton, ttk.Button):
            # Buttons don't need labels, they're built-in
            input_args["text"] = label
        else:
            self.label = ttk.Label(self, text=label, **label_args)
            self.label.grid(row=0, column=0, pady=5, sticky=(tk.W + tk.E))

        # setup the variable
        if input_class in (ttk.Checkbutton, ttk.Radiobutton):
            input_args["variable"] = self.variable
        else:
            input_args["textvariable"] = self.variable

        # Setup the input
        if input_class == ttk.Radiobutton:
            # for Radiobutton, create one input per value
            self.input = tk.Frame(self)
            for v in input_args.pop('values', []):
                button = ttk.Radiobutton(
                    self.input, value=v, text=v, **input_args)
                button.pack(side=tk.LEFT, ipadx=10,
                            ipady=2, expand=True, fill='x')
        else:
            self.input = input_class(self, **input_args)

        self.input.grid(row=1, column=0, sticky=(tk.W + tk.E))
        self.columnconfigure(0, weight=1)

    def grid(self, sticky=(tk.E + tk.W), **kwargs):
        """Override grid to add default sticky values"""
        super().grid(sticky=sticky, **kwargs)


class SAPWindow(tk.Toplevel):
    """The SAP Configuration Window"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        global flag
        flag = False

        self.title("SAP Configuration")
        self.geometry("500x500")
        self.columnconfigure(0, weight=1)

        SAPRecordForm(parent=self).grid(padx=10, pady=30, sticky=(tk.E+tk.W))


class SAPRecordForm(ttk.Frame):
    "The form for the Transmission (TX) and Reception (RX) info"

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self._vars = {
            'TX_Port': tk.BooleanVar(value=False),
            'Port_Name_tx': tk.StringVar(),
            'Number_Msg_tx': tk.IntVar(value=10),
            'Max_Msg_tx': tk.IntVar(),
            'Protocol_tx': tk.StringVar(value="UDP"),
            'Extended_Port_tx': tk.BooleanVar(value=False),
            'RX_Port': tk.BooleanVar(value=False),
            'Port_Name_rx': tk.StringVar(),
            'Number_Msg_rx': tk.IntVar(value=10),
            'Max_Msg_rx': tk.IntVar(),
            'Protocol_rx': tk.StringVar(value='UDP'),
            'Extended_Port_rx': tk.BooleanVar(value=False)
        }

        for i in range(2):
            self.columnconfigure(i, weight=1)

        ##################
        # TX Information #
        ##################

        tx_info = self.add_frame(
            text="Transmission (TX) information", column=0, row=0, padx=10)

        LabelInput(tx_info, label="TX Port", var=self._vars['TX_Port'], input_class=ttk.Checkbutton).grid(
            row=0, column=0, pady=20)

        LabelInput(tx_info, label="Port Name", var=self._vars['Port_Name_tx']).grid(
            row=1, column=0, pady=5)

        LabelInput(tx_info, label="Max Number of Messages", input_args={"state": tk.DISABLED},
                   var=self._vars['Number_Msg_tx']).grid(row=2, pady=5)

        LabelInput(tx_info, label="Max Message Size",
                   var=self._vars["Max_Msg_tx"]).grid(row=3, pady=5)

        LabelInput(tx_info, label="Protocol Type", input_args={"state": tk.DISABLED},
                   var=self._vars["Protocol_tx"]).grid(row=4, pady=5)

        LabelInput(tx_info, label="Extended Port",
                   input_class=ttk.Checkbutton, var=self._vars["Extended_Port_tx"]).grid(row=5, pady=5)

        ##################
        # RX Information #
        ##################

        rx_info = self.add_frame(
            text="Reception (RX) information", column=1, row=0, padx=10)

        LabelInput(rx_info, label="RX Port", var=self._vars['RX_Port'], input_class=ttk.Checkbutton).grid(
            row=0, column=0, pady=20)

        LabelInput(rx_info, label="Port Name", var=self._vars['Port_Name_rx']).grid(
            row=1, column=0, pady=5)

        LabelInput(rx_info, label="Max Number of Messages", input_args={"state": tk.DISABLED},
                   var=self._vars['Number_Msg_rx']).grid(row=2, pady=5)

        LabelInput(rx_info, label="Max Message Size",
                   var=self._vars["Max_Msg_rx"]).grid(row=3, pady=5)

        LabelInput(rx_info, label="Protocol Type", input_args={"state": tk.DISABLED},
                   var=self._vars["Protocol_rx"]).grid(row=4, pady=5)

        LabelInput(rx_info, label="Extended Port",
                   input_class=ttk.Checkbutton, var=self._vars["Extended_Port_rx"]).grid(row=5, pady=5)

        ################
        # Button Frame #
        ################

        buttons = tk.Frame(self)
        buttons.grid(pady=20, padx=20, columnspan=2, sticky=(tk.E+tk.W))
        save_button = ttk.Button(buttons, text="Save", command=self.save)
        save_button.pack(side=tk.RIGHT, padx=5)

        cancel_button = ttk.Button(
            buttons, text="Cancel", command=self.close)
        cancel_button.pack(side=tk.RIGHT, padx=5)

        self.master.protocol('WM_DELETE_WINDOW', self.close)

    def save(self):
        global flag
        flag = True
        self.master.destroy()

    def close(self):
        for _, variable in self._vars.items():
            if isinstance(variable, tk.BooleanVar):
                variable.set(False)
            elif isinstance(variable, tk.IntVar):
                variable.set(0)
            else:
                variable.set('')

        global flag
        flag = True
        self.master.destroy()

    def add_frame(self, text='', column=0, row=0, padx=0):
        frame = ttk.LabelFrame(self, text=text)
        frame.grid(
            column=column, row=row, padx=padx, sticky=(tk.W+tk.E))
        return frame


class Application(tk.Tk):
    """Application root window"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("ConfigTool Application")
        self.columnconfigure(0, weight=1)

        ttk.Button(self, text="Configuration",
                   command=verify_window).grid(sticky=(tk.W + tk.E))


if __name__ == "__main__":
    app = Application()
    app.mainloop()

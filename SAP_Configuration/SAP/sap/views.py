import tkinter as tk
from tkinter import ttk
from . import widgets as w
from . import models as m

import sap


class SAPWindow(tk.Toplevel):
    """The SAP Configuration Window"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        sap.flag = False

        self.model = m.SAPModel()
        self.recordform = SAPRecordForm(self, self.model)

        self.title("SAP Configuration")
        self.geometry("500x500")
        self.resizable(False, False)
        self.columnconfigure(0, weight=1)

        self.recordform.grid(padx=10, pady=30, sticky=(tk.E+tk.W))


class SAPRecordForm(ttk.Frame):
    "The form for the Transmission (TX) and Reception (RX) info"

    def __init__(self, parent, model, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.model = model
        fields = self.model.fields

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

        w.LabelInput(tx_info, label="TX Port", var=self._vars['TX_Port'], field_spec=fields['TX Port']).grid(
            row=0, column=0, pady=20)

        w.LabelInput(tx_info, label="Port Name", var=self._vars['Port_Name_tx'], field_spec=fields['Port Name TX'], input_args={"max_length": 32}).grid(
            row=1, column=0, pady=5, ipadx=40)

        w.LabelInput(tx_info, label="Max Number of Messages", field_spec=fields['Max Number Msg TX'], input_args={"state": tk.DISABLED},
                     var=self._vars['Number_Msg_tx']).grid(row=2, pady=5)

        w.LabelInput(tx_info, label="Max Message Size", field_spec=fields['Max Msg Size TX'], input_args={"max_num": 32},
                     var=self._vars["Max_Msg_tx"]).grid(row=3, pady=5)

        w.LabelInput(tx_info, label="Protocol Type", field_spec=fields['Protocol Type TX'], input_args={"state": tk.DISABLED},
                     var=self._vars["Protocol_tx"]).grid(row=4, pady=5)

        w.LabelInput(tx_info, label="Extended Port", field_spec=fields['Extended Port TX'],
                     var=self._vars["Extended_Port_tx"]).grid(row=5, pady=5)

        ##################
        # RX Information #
        ##################

        rx_info = self.add_frame(
            text="Reception (RX) information", column=1, row=0, padx=10)

        w.LabelInput(rx_info, label="RX Port", var=self._vars['RX_Port'], field_spec=fields['RX Port']).grid(
            row=0, column=0, pady=20)

        w.LabelInput(rx_info, label="Port Name", var=self._vars['Port_Name_rx'], input_args={"max_length": 32}, field_spec=fields['Port Name RX']).grid(
            row=1, column=0, pady=5, ipadx=40)

        w.LabelInput(rx_info, label="Max Number of Messages", field_spec=fields['Max Number Msg RX'], input_args={"state": tk.DISABLED},
                     var=self._vars['Number_Msg_rx']).grid(row=2, pady=5)

        w.LabelInput(rx_info, label="Max Message Size", field_spec=fields['Max Msg Size RX'], input_args={"max_num": 32},
                     var=self._vars["Max_Msg_rx"]).grid(row=3, pady=5)

        w.LabelInput(rx_info, label="Protocol Type", field_spec=fields['Protocol Type RX'], input_args={"state": tk.DISABLED},
                     var=self._vars["Protocol_rx"]).grid(row=4, pady=5)

        w.LabelInput(rx_info, label="Extended Port", field_spec=fields['Extended Port RX'],
                     var=self._vars["Extended_Port_rx"]).grid(row=5, pady=5)

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
        sap.flag = True
        self.master.destroy()

    def close(self):
        for key, variable in self._vars.items():
            if key == 'Protocol_tx' or key == 'Protocol_rx':
                variable.set("UDP")
            elif key == 'Number_Msg_tx' or key == 'Number_Msg_rx':
                variable.set(10)
            if isinstance(variable, tk.BooleanVar):
                variable.set(False)
            elif isinstance(variable, tk.IntVar):
                variable.set(0)
            else:
                variable.set('')

        sap.flag = True
        self.master.destroy()

    def add_frame(self, text='', column=0, row=0, padx=0):
        frame = ttk.LabelFrame(self, text=text)
        frame.grid(
            column=column, row=row, padx=padx, sticky=(tk.W+tk.E))
        return frame

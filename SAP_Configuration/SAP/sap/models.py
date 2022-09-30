from .constants import FieldTypes as FT
import tkinter as tk


class SAPModel():
    """SAP Configuration model"""

    fields = {
        "TX Port": {'req': False, 'type': FT.boolean},
        'Port Name TX': {'req': True, 'type': FT.string, 'max_length': 32},
        'Max Number Msg TX': {'req': True, 'type': FT.integer, 'value': 10, 'state': tk.DISABLED},
        'Max Msg Size TX': {'req': True, 'type': FT.integer, 'max_num': 32},
        'Protocol Type TX': {'req': True, 'type': FT.string, 'value': 'UDP', 'state': tk.DISABLED},
        'Extended Port TX': {'req': False, 'type': FT.boolean},

        'RX Port': {'req': False, 'type': FT.boolean},
        'Port Name RX': {'req': True, 'type': FT.string, 'max_length': 32},
        'Max Number Msg RX': {'req': True, 'type': FT.integer, 'value': 10, 'state': tk.DISABLED},
        'Max Msg Size RX': {'req': True, 'type': FT.integer, 'max_num': 32},
        'Protocol Type RX': {'req': True, 'type': FT.string, 'value': 'UDP', 'state': tk.DISABLED},
        'Extended Port RX': {'req': False, 'type': FT.boolean}
    }


    def __init__(self) -> None:
        pass

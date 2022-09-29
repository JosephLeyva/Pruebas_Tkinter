import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class BoundText(tk.Text):
    """A text widget with a bound variable"""

    def __init__(self, *args, textvariable=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._variable = textvariable

        if self._variable:
            self.insert('1.0', self._variable.get())
            self._variable.trace_add('write', self._set_content)
            self.bind('<<Modified>>', self._set_var)

    def _set_content(self, *_):
        """Set the text contents to the variable"""
        self.delete('1.0', tk.END)
        self.insert('1.0', self._variable.get())

    def _set_var(self, *_):
        """Set the variable to the text contents"""

        if self.edit_modified():
            content = self.get('1.0', 'end-1chars')
            self._variable.set(content)
            self.edit_modified(False)


class LabelInput(tk.Frame):
    """A label and input combined together"""

    def __init__(self, parent, label, var, input_class=None, input_args=None, label_args=None, disable_var=None, inline: bool = True, has_label: bool = True, has_label_error: bool = True, **kwargs):
        super().__init__(parent, **kwargs)
        input_args = input_args or {}
        label_args = label_args or {}
        self.variable = var
        self.variable.label_widget = self

        # setup the label
        # if input_class in (ttk.Checkbutton, ttk.Button):
        if not input_class in (ttk.Button, ttk.Button):
            if has_label:
                self.label = ttk.Label(self, text=label, **label_args)
                self.label.grid(row=0, column=0, sticky=(tk.W + tk.E))

        # setup the variable
        if input_class in (ttk.Checkbutton, tk.Checkbutton, ttk.Radiobutton):
            input_args["variable"] = self.variable
        else:
            input_args["textvariable"] = self.variable

        # Setup the input
        if input_class == ttk.Radiobutton:
            self.input = tk.Frame(self)
            for v in input_args.pop('values', []):
                button = ttk.Radiobutton(
                    self.input, value=v, text=v, **input_args)
                button.pack(side=tk.LEFT, ipadx=10,
                            ipady=2, expand=True, fill='x')
        else:
            self.input = input_class(self, **input_args)

        # Set up error handling & display
        self.error = getattr(self.input, 'error', tk.StringVar())

        if input_class != ttk.Button:
            if not has_label:
                self.input.grid(row=0, column=0, sticky=(tk.W + tk.E))
                if has_label_error:
                    ttk.Label(self, textvariable=self.error, foreground='red', **
                              label_args).grid(row=1, column=0, sticky=(tk.W + tk.E))
            else:
                if not inline:
                    self.input.grid(row=1, column=0, sticky=(tk.W + tk.E))
                    if has_label_error:
                        ttk.Label(self, textvariable=self.error, **
                                  label_args).grid(row=2, column=0, sticky=(tk.W + tk.E))
                else:
                    self.input.grid(row=0, column=1, sticky=(tk.W + tk.E))
                    if has_label_error:
                        ttk.Label(self, textvariable=self.error, **label_args).grid(row=1,
                                                                                    column=0, columnspan=2, sticky=(tk.W + tk.E))
            self.columnconfigure(0, weight=1)
        else:
            button = input_class(self, text=input_args['text'])
            button.grid(row=0, column=0, sticky=(tk.W + tk.E))
            if has_label_error:
                ttk.Label(self, textvariable=self.error, foreground='red', **
                          label_args).grid(row=1, column=0, sticky=(tk.W + tk.E))
            button.columnconfigure(0, weight=1)

        # Set up disable variable
        if disable_var:
            self.disable_var = disable_var
            self.disable_var.trace_add('write', self._check_disable)

    def grid(self, sticky=(tk.E + tk.W), **kwargs):
        """Override grid to add default sticky values"""
        super().grid(sticky=sticky, **kwargs)

    def _check_disable(self, *_):
        if not hasattr(self, 'disable_var'):
            return

        if self.disable_var.get():
            self.input.configure(state=tk.DISABLED)
            self.variable.set('')
            self.error.set('')
        else:
            self.input.configure(state=tk.NORMAL)


class SAPRecordForm(ttk.Frame):
    """The SAP Configuration Window"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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

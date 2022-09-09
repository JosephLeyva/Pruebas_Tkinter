import tkinter as tk
from tkinter import ttk
from . import widgets as w


class DataRecordForm(tk.Frame):
    """The input form for our widgets"""

    def _add_frame(self, label, cols=3):
        """Add a labelframe to the form"""

        frame = ttk.LabelFrame(self, text=label)
        frame.grid(sticky=tk.W + tk.E)
        for i in range(cols):
            frame.columnconfigure(i, weight=1)
        return frame

    def __init__(self, parent, model, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.model = model
        fields = self.model.fields

        # Create a dict to keep track of input widgets
        self._vars = {
            'Lab': tk.StringVar(),
            'Seed': tk.StringVar(),
            'Type': tk.StringVar()
        }

        # Build the form
        self.columnconfigure(0, weight=1)

        # Record info section
        r_info = self._add_frame("Record Information")

        # line 2
        w.LabelInput(
            r_info, "Lab", field_spec=fields['Lab'], input_args={"type_var": self._vars['Type'], "focus_update_var": self._vars['Lab']},
            var=self._vars['Lab']).grid(row=1, column=0)
        w.LabelInput(
            r_info, "Seed", field_spec=fields['Seed'], input_args={"type_var": self._vars['Type'], "focus_update_var": self._vars['Seed']},
            var=self._vars['Seed']).grid(row=1, column=1),
        w.LabelInput(r_info, "Type", field_spec=fields['Type'],
                     var=self._vars['Type']).grid(
            row=1, column=2)

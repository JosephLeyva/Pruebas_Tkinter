"""ABQ Data Entry

Chapter 5 version
"""
import tkinter as tk
from tkinter import ttk


def hex_to_dec(hex): return int(hex, 16)


##################
# Widget Classes #
##################

class ValidatedMixin:
    """Adds a validation functionality to an input widget"""

    def __init__(self, *args, error_var=None, **kwargs):
        self.error = error_var or tk.StringVar()
        super().__init__(*args, **kwargs)

        vcmd = self.register(self._validate)
        invcmd = self.register(self._invalid)

        self.configure(
            validate='all',
            validatecommand=(vcmd, '%P', '%s', '%S', '%V', '%i', '%d'),
            invalidcommand=(invcmd, '%P', '%s', '%S', '%V', '%i', '%d')
        )

    def _toggle_error(self, on=False):
        self.configure(foreground='red' if on else 'black')

    def _validate(self, proposed, current, char, event, index, action):
        """The validation method.

        Don't override this, override _key_validate, and _focus_validate
        """
        self.error.set('')
        self._toggle_error()

        valid = True
        # if the widget is disabled, don't validate
        state = str(self.configure('state')[-1])
        if state == tk.DISABLED:
            return valid

        if event == 'focusout':
            valid = self._focusout_validate(event=event)
        elif event == 'key':
            valid = self._key_validate(
                proposed=proposed,
                current=current,
                char=char,
                event=event,
                index=index,
                action=action
            )
        return valid

    def _focusout_validate(self, **kwargs):
        return True

    def _key_validate(self, **kwargs):
        return True

    def _invalid(self, proposed, current, char, event, index, action):
        if event == 'focusout':
            self._focusout_invalid(event=event)
        elif event == 'key':
            self._key_invalid(
                proposed=proposed,
                current=current,
                char=char,
                event=event,
                index=index,
                action=action
            )

    def _focusout_invalid(self, **kwargs):
        """Handle invalid data on a focus event"""
        self._toggle_error(True)

    def _key_invalid(self, **kwargs):
        """Handle invalid data on a key event.  By default we want to do nothing"""
        pass

    def trigger_focusout_validation(self):
        valid = self._validate('', '', '', 'focusout', '', '')
        if not valid:
            self._focusout_invalid(event='focusout')
        return valid


class RequiredEntry(ValidatedMixin, ttk.Entry):
    """An Entry that requires a value"""

    def _focusout_validate(self, event):
        valid = True
        if not self.get():
            valid = False
            self.error.set('A value is required')
        return valid


class RequiredHexEntry(ValidatedMixin, ttk.Entry):

    def __init__(self, *args, lower_bound=None, upper_bound=None, multiple=None, **kwargs):
        super().__init__(*args, **kwargs)
        if lower_bound:
            self.lower_bound = lower_bound
        if upper_bound:
            self.upper_bound = upper_bound
        if multiple:
            self.multple = multiple

    def _focusout_validate(self, event):
        valid = True
        if not self.get():
            valid = False
            self.error.set('A value is required')
            return valid
        try:
            num = self.get()

            if hex_to_dec(self.lower_bound) <= hex_to_dec(num) <= hex_to_dec(self.upper_bound):
                if hex_to_dec(num) % hex_to_dec(self.multple) != 0:
                    self.error.set(
                        f'The value is not multiple of {self.multple}')
                    valid = False
            else:
                self.error.set(
                    f'The value must be between {self.lower_bound} and {self.upper_bound}')
                valid = False
        except ValueError:
            self.error.set('It need to be a hexadecimal number')
            valid = False

        return valid


##################
# Module Classes #
##################


class LabelInput(ttk.Frame):
    """A widget containing a label and input together."""

    def __init__(
        self, parent, label, var, input_class=ttk.Entry,
        input_args=None, label_args=None, disable_var=None,
        **kwargs
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
            self.label.grid(row=0, column=0, sticky=(tk.W + tk.E))

        # setup the variable
        if input_class in (
            ttk.Checkbutton, ttk.Button,
            ttk.Radiobutton
        ):
            input_args["variable"] = self.variable
        else:
            input_args["textvariable"] = self.variable

        # Setup the input
        if input_class == ttk.Radiobutton:
            # for Radiobutton, create one input per value
            self.input = tk.Frame(self)
            for v in input_args.pop('values', []):
                button = input_class(
                    self.input, value=v, text=v, **input_args
                )
                button.pack(side=tk.LEFT, ipadx=10,
                            ipady=2, expand=True, fill='x')
        else:
            self.input = input_class(self, **input_args)
        self.input.grid(row=1, column=0, sticky=(tk.W + tk.E))
        self.columnconfigure(0, weight=1)

        self.error = getattr(self.input, 'error', tk.StringVar())
        ttk.Label(self, textvariable=self.error, foreground='red').grid(
            row=2, column=0, sticky=(tk.W + tk.E))

    def grid(self, sticky=(tk.E + tk.W), **kwargs):
        """Override grid to add default sticky values"""
        super().grid(sticky=sticky, **kwargs)


class DataRecordForm(tk.Frame):
    """The input form for our widgets"""

    def _add_frame(self, label, cols=3):
        """Add a labelframe to the form"""

        frame = ttk.LabelFrame(self, text=label)
        frame.grid(sticky=tk.W + tk.E)
        for i in range(cols):
            frame.columnconfigure(i, weight=1)
        return frame

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Create a dict to keep track of input widgets
        self._vars = {
            'Lab': tk.StringVar(),
            'Seed': tk.StringVar(),
        }

        # Build the form
        self.columnconfigure(0, weight=1)

        # Record info section
        r_info = self._add_frame("Record Information")

        # line 2
        LabelInput(
            r_info, "Lab", input_class=RequiredHexEntry,
            input_args={'lower_bound': '0x8000_0000',
                        'upper_bound': '0xC000_0000', 'multiple': '0x1000'},
            var=self._vars['Lab']).grid(row=1, column=0)
        LabelInput(
            r_info, "Seed", input_class=RequiredHexEntry,
            input_args={'lower_bound': '0x20_8000_0000',
                        'upper_bound': '0x24_0000_0000', 'multiple': '0x20_0000'},
            var=self._vars['Seed']).grid(row=1, column=1)


class Application(tk.Tk):
    """Application root window"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("ABQ Data Entry Application")
        self.columnconfigure(0, weight=1)

        ttk.Label(
            self,
            text="ABQ Data Entry Application",
            font=("TkDefaultFont", 16)
        ).grid(row=0)

        self.form = DataRecordForm(self)
        self.form.grid(row=1, padx=10, sticky=(tk.W + tk.E))


if __name__ == "__main__":

    app = Application()
    app.mainloop()

from sys import maxsize
import tkinter as tk
from tkinter import ttk

from .constants import FieldTypes as FT


class ValidatedMixin:
    """Adds a validation functionality to an input widget"""

    def __init__(self, *args, error_var=None, **kwargs):
        self.error = error_var or tk.StringVar()
        self.detail = tk.StringVar()
        super().__init__(*args, **kwargs)

        vcmd = self.register(self._validate)
        invcmd = self.register(self._invalid)

        self.configure(
            validate='all',
            validatecommand=(vcmd, '%P', '%s', '%S', '%V', '%i', '%d'),
            invalidcommand=(invcmd, '%P', '%s', '%S', '%V', '%i', '%d')
        )

    def _toggle_error(self, on=False):
        self.configure(foreground=('red' if on else 'black'))

    def _validate(self, proposed, current, char, event, index, action):
        """ The validation method.
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
        """Handle invalid data on a key event. By default we want to do nothing"""
        pass

    def trigger_focusout_validation(self):
        valid = self._validate('', '', '', 'focusout', '', '')
        if not valid:
            self._focusout_invalid(event='focusout')
        return valid


class RequiredNumEntry(ValidatedMixin, ttk.Entry):
    """An Entry widget that only accepts numeric input"""

    def __init__(self, *args, max_num=maxsize, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_num = int(max_num)

    def _focusout_validate(self, event):
        valid = True
        if not self.get():
            valid = False
            self.error.set("A value is required")
            print(self.error.get())
        elif int(self.get()) > self.max_num:
            valid = False
            self.error.set(f"The number entered must be up to {self.max_num}")
            print(self.error.get())
        return valid

    def _key_validate(self, proposed, current, char, event, index, action):
        if action == '0':
            valid = True
        elif not char.isdigit():
            valid = False
        elif int(proposed) > self.max_num:
            valid = False
            self.error.set(f"The number entered must be up to {self.max_num}")
            print(self.error.get())
        else:
            valid = char.isdigit()

        return valid


class RequiredEntry(ValidatedMixin, ttk.Entry):
    """An Entry widget that requires a value"""

    def __init__(self, *args, max_length=float("inf"), **kwargs):
        super().__init__(*args, **kwargs)
        self.max_length = max_length

    def _focusout_validate(self, event):
        valid = True
        if not self.get():
            valid = False
            self.error.set("A value is required")
            print(self.error.get())
        return valid

    def _key_validate(self, proposed, current, char, event, index, action):
        if not len(proposed) <= self.max_length:
            self.error.set(
                f"A value must be up to {self.max_length} characters")
            print(self.error.get())
        return len(proposed) <= self.max_length


class LabelInput(tk.Frame):
    """A widget containing a label and input together."""

    field_types = {
        FT.boolean: ttk.Checkbutton,
        FT.integer: RequiredNumEntry,
        FT.string: RequiredEntry
    }

    def __init__(
        self, parent, label, var, input_class=None,
        input_args=None, label_args=None, field_spec=None, **kwargs
    ):
        super().__init__(parent, **kwargs)
        input_args = input_args or {}
        label_args = label_args or {}
        self.variable = var
        self.variable.label_widget = self

        if field_spec:
            field_type = field_spec.get('type', FT.string)
            input_class = input_class or self.field_types.get(field_type)
            if 'max_length' in field_spec and 'max_length' not in input_args:
                input_args['max_length'] = field_spec.get('max_length')
            if 'max_num' in field_spec and 'max_num' not in input_args:
                input_args['max_num'] = field_spec.get('max_num')
            if 'state' in field_spec and 'state' not in input_args:
                input_args['state'] = field_spec.get('state')

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

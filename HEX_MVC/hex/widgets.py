import tkinter as tk
from tkinter import ttk
from .constants import FieldTypes as FT


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

    def __init__(self, *args, type_var=None, focus_update_var=None,
                 lower_bound=None, upper_bound=None, multiple=None, **kwargs):
        super().__init__(*args, **kwargs)

        if not lower_bound:
            self.lower_bound = '0x0000'
        if not upper_bound:
            self.upper_bound = '0xFFFF_FFFF_FFFF_FFFF'
        if not multiple:
            self.multiple = '0x1'

        if type_var:
            self.type_var = type_var
            self.type_var.trace_add('write', self._set_range)
        self.focus_update_var = focus_update_var
        self.bind('<<FocusOut>>', self._set_focus_update_var)

    def _set_focus_update_var(self, event):
        value = self.get()
        if self.focus_update_var and not self.error.get():
            self.focus_update_var.set(value)

    def _set_range(self, *_):
        type_v = self.type_var.get()
        if type_v == 'LOG':
            self.lower_bound = '0x8000_0000'
            self.upper_bound = '0xC000_0000'
            self.multiple = '0x1000'
        elif type_v == 'DB':
            self.lower_bound = '0x20_8000_0000'
            self.upper_bound = '0x24_0000_0000'
            self.multiple = '0x20_0000'
        else:
            self.lower_bound = '0x0'
            self.upper_bound = '0xFFFF_FFFF_FFFF_FFFF'
            self.multiple = '0x1'
        self.trigger_focusout_validation()

    def _focusout_validate(self, event):

        valid = True
        if not self.get():
            valid = False
            self.error.set('A value is required')
            return valid

        try:
            num = self.get()

            if hex_to_dec(self.lower_bound) <= hex_to_dec(num) <= hex_to_dec(self.upper_bound):
                if hex_to_dec(num) % hex_to_dec(self.multiple) != 0:
                    self.error.set(
                        f'The value is not multiple of {self.multiple}')
                    valid = False
            else:
                self.error.set(
                    f'The value must be between {self.lower_bound} and {self.upper_bound}')
                valid = False
        except ValueError:
            self.error.set('It need to be a hexadecimal number')
            valid = False

        return valid


class ValidateCombobox(ValidatedMixin, ttk.Combobox):
    """A combobox that only takes values from its string list"""

    def _key_validate(self, proposed, action, **kwargs):
        valid = True
        if action == '0':
            self.set('')
            return True
        # get the values list
        values = self.cget('values')
        # Do a case-insensitive match against the entered text
        matching = [
            x for x in values
            if x.lower().startswith(proposed.lower())
        ]
        if len(matching) == 0:
            valid = False
        elif len(matching) == 1:
            self.icursor(tk.END)
            valid = False
        return valid

    def _focusout_validate(self, **kwargs):
        valid = True
        if not self.get():
            valid = False
            self.error.set('A value is required')
        return valid


##################
# Module Classes #
##################


class LabelInput(ttk.Frame):
    """A widget containing a label and input together."""

    field_types = {
        FT.string: RequiredHexEntry,
        FT.button: ttk.Button,
        FT.short_string_list: ValidateCombobox
    }

    def __init__(
        self, parent, label, var, input_class=None,
        input_args=None, label_args=None, disable_var=None,
        field_spec=None, **kwargs
    ):
        super().__init__(parent, **kwargs)
        input_args = input_args or {}
        label_args = label_args or {}
        self.variable = var
        self.variable.label_widget = self

        if field_spec:
            field_type = field_spec.get('type', FT.string)
            input_class = input_class or self.field_types.get(field_type)
            if 'values' in field_spec and 'values' not in input_args:
                input_args['values'] = field_spec.get('values')

        # setup the label
        if not input_class in (ttk.Checkbutton, ttk.Button):
            self.label = ttk.Label(self, text=label, **label_args)
            self.label.grid(row=0, column=0, sticky=(tk.W + tk.E))
        else:
            input_args['text'] = label

        # setup the variable
        if input_class in (
            ttk.Checkbutton,
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

        if  input_class != ttk.Button:
            self.input.grid(row=1, column=0, sticky=(tk.W + tk.E))
            self.columnconfigure(0, weight=1)
        else:
            button = input_class(self, text=label)
            button.grid(row=1, column=0, sticky=(tk.W + tk.E))
            button.columnconfigure(0,weight=1)

        self.error = getattr(self.input, 'error', tk.StringVar())
        ttk.Label(self, textvariable=self.error, foreground='red').grid(
            row=2, column=0, sticky=(tk.W + tk.E))

    def grid(self, sticky=(tk.E + tk.W), **kwargs):
        """Override grid to add default sticky values"""
        super().grid(sticky=sticky, **kwargs)

from .constants import FieldTypes as FT


class Model:

    fields = {
        "Lab": {'req': True, 'type': FT.string},
        "Seed": {'req': True, 'type': FT.string},
        "Type": {'req': True, 'type': FT.short_string_list, 'values': ['LOG', 'DB']}
    }

    def __init__(self) -> None:
        x = 1

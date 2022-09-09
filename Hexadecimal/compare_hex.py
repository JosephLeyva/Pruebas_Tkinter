
def hex_to_dec(hex): return int(hex, 16)


lower_bound = '0x8000_0000'
upper_bound = '0xC000_0000'

num = '0x8000_3400'

multiplo = '0x1000'


if hex_to_dec(lower_bound) <= hex_to_dec(num) <= hex_to_dec(upper_bound):
    print('está dentro del rango')

    # Lógica para determinar si el número es múltiplo
    if hex_to_dec(num) % hex_to_dec(multiplo) == 0:
        print('está permitido')
    else:
        print('no está permitido')

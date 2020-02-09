"""
Hash table for all addresses used in assembly program

Supports assembler.py
"""

addresses = {
    'SP'     : f'{0:016b}',
    'LCL'    : f'{1:016b}',
    'ARG'    : f'{2:016b}',
    'THIS'   : f'{3:016b}',
    'THAT'   : f'{4:016b}',
    'R0'     : f'{0:016b}',
    'R1'     : f'{1:016b}',
    'R2'     : f'{2:016b}',
    'R3'     : f'{3:016b}',
    'R4'     : f'{4:016b}',
    'R5'     : f'{5:016b}',
    'R6'     : f'{6:016b}',
    'R7'     : f'{7:016b}',
    'R8'     : f'{8:016b}',
    'R9'     : f'{9:016b}',
    'R10'    : f'{10:016b}',
    'R11'    : f'{11:016b}',
    'R12'    : f'{12:016b}',
    'R13'    : f'{13:016b}',
    'R14'    : f'{14:016b}',
    'R15'    : f'{15:016b}',
    'SCREEN' : f'{16384:016b}',
    'KBD'    : f'{24576:016b}'
    }

if __name__ == "__main__":

    print('Addresses:')
    for address in addresses:
        print(f'{address} : {addresses[address]}')

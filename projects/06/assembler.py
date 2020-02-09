"""
This program assembles hack assembly language to machine code.

Input: *.asm file # assembly language
Output: *.hack file # machine code

Example usage:
    $ python assembler.py input_file.asm output_file.hack

"""

import sys

from compute_hash_table import *
from address_hash_table import *
from label_hash_table import *

try: # get arguments

    input_file = sys.argv[1] # set input file var
    output_file = sys.argv[2] # set output file var

except IndexError:

    print("Insufficient arguments, example usage:")
    print("$ python assembler.py input_file.asm output_file.hack")
    sys.exit(1)

def write_to_file(instruction):
    """ writes instruction to output file """

    global of

    # wrtie instruction to file
    of.write(instruction + '\n')

def a_instruction(assembly):
    """ assembles a-instructions """

    global addy_assign

    value = assembly.lstrip('@')

    # if int, write int to intruction word
    try:
        instruction = f'{int(value):016b}'
    # otherwise, handle symbol
    except ValueError:
        if value in addresses:
        # if value already in hash table
            instruction = addresses[value] # get its addy
        elif value in labels:
        # if value is a label
            instruction = labels[value] # get its addy
        else: # otherwise
        # assign next available open address
            instruction = f'{addy_assign:016b}' # set instruction
            addy_assign += 1 # increment addy_assign address
            addresses[value] = instruction # update hash table

    # write instruction word to output file
    write_to_file(instruction)

def c_instruction(assembly):
    """ assembles c-instructions """

    assemble = {'comp' : None,
                'dest' : 'null',
                'jump' : 'null'}

    # split into dest, comp, and jump as equipped
    if '=' in assembly and ';' in assembly:
        ins_arr = assembly.replace('=', ',').replace(';', ',').split(',')
        assemble['comp'] = ins_arr[1]
        assemble['dest'] = ins_arr[0]
        assemble['jump'] = ins_arr[2]
    elif '=' in assembly:
        ins_arr = assembly.split('=')
        assemble['comp'] = ins_arr[1]
        assemble['dest'] = ins_arr[0]
    elif ';' in assembly:
        ins_arr = assembly.split(';')
        assemble['comp'] = ins_arr[0]
        assemble['jump'] = ins_arr[1]
    else:
        assemble['comp'] = assembly

    # decode instruction based on hash tables
    instruction = '111'
    instruction += computations[assemble['comp']]
    instruction += destinations[assemble['dest']]
    instruction += jumps[assemble['jump']]

    # write insturction word to output file
    write_to_file(instruction)

def label(assembly, pc=None):
    """ handles labels """
    # NOTE: whether the address is a ROM or RAM address
    # is implemented directly in the hardware via the jump
    # condition and the hardware program counter

    # strip label of parenthases
    label = assembly.lstrip('(').rstrip(')')

    # update label in hash table
    # NOTE: labels are unique so label should not
    # already be in hash table. Consider adding
    # test to raise informative error to debug
    # assembly code if already present.
    instruction = f'{pc:016b}' # set instruction
    labels[label] = instruction # update hash table

def parse(file, rc):
    """ function parses input file """

    with open(file) as f:
        # with input file open

        pc = 0 # set program count

        # iterate through file line-by-line
        for l in f:

            # strip whitespace and comments
            line = l.rstrip().split('//')[0].rstrip().lstrip()

            if line: # if line contains assembly code

                if rc == 0:
                # on first pass

                    if line[0] == '(':
                    # if label declaration
                        label(line, pc) # handle label
                        pc -= 1 # decrement program counter

                elif rc == 1 and '(' not in line:
                # on second pass, look for c- and a-instructions

                    if line[0] == '@':
                    # if a-instruction
                        a_instruction(line) # handle variable or label

                    else:
                    # otherwise, compute, handle accordingly
                        c_instruction(line)

                pc += 1 # increment program counter

if __name__ == "__main__":

    addy_assign = 16

    of = open(output_file, 'w')

    for run in range(2):
        parse(input_file, run)

    of.close()

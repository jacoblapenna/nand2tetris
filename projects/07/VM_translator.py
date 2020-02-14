#!/usr/bin/env python3

from code_writer import CodeWriter
import sys
import os

input = sys.argv[1]
output = sys.argv[2]

def get_all_VM_files(directory):

    files = []

    # iterate through each file in cwd
    for file in os.listdir(directory):
        if '.vm' in file: # if file is a vm file
            # store filename in array
            files.append(file)

    return files

if '.vm' in input:
    vm_files = [input]
else:
    if input in os.getcwd():
        vm_files = get_all_VM_files(os.getcwd())
    else:
        os.chdir(input)
        vm_files = get_all_VM_files(os.getcwd())


# create a CodeWriter instance
cw = CodeWriter(vm_files, output)

# perform translation
cw.translate()

# close the output of the CodeWriter
cw.close()

"""
try: # try to grab input argument

    arg = sys.argv[1]

except IndexError: # unless error

    # print example usage
    print('Script call takes one argument, either file or directory:')
    print()
    print('Example usage:')
    print('./VM_translator.py input_file.vm')
    print('./VM_translator.py input_directory')
    print()

    # exit script cleanly
    sys.exit(1)

def get_all_VM_files(directory):

    cwd = os.getcwd()
    vm_files = []

    if directory in cwd:
    # if we're in the directory already

        for file in os.listdir(cwd):
        # iterate through each file in cwd

            if '.vm' in file: # if file is a vm file

                # store filename in array
                vm_files.append(file)

        return vm_files

    else: # otherwise

        # try changing directories
        # exception handling is in main program should this fail
        os.chdir(directory)
        # then get all vm files
        return get_all_VM_files(directory)

try: # try to see if argument is a directory

    vm_files = get_all_VM_files(arg)

except NotADirectoryError: # if it's not a directory

    # see if its a file
    if os.path.isfile(arg):
        vm_files = [arg]
"""

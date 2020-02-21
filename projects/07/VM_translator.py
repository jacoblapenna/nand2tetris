#!/usr/bin/env python3

from code_writer import CodeWriter
import sys
import os

def get_all_VM_files(directory):

    files = []

    # iterate through each file in cwd
    for file in os.listdir(directory):
        if '.vm' in file: # if file is a vm file
            # store filename in array
            files.append(file)

    return files

def example_usage(error_str):
    print(f"Error: {error_str}!")
    print("Example usage:")
    print("    ./VM_translator.py input_file.vm output_filename")
    print("    ./VM_translator.py input_directory output_filename")
    sys.exit(1)

try:
    input = sys.argv[1]
    output = sys.argv[2]
except IndexError:
    example_usage('improper arguments')

if '.vm' in input:
    if input in os.listdir():
        vm_files = [input]
    else:
        example_usage('file not found')
else:
    if input in os.getcwd():
        vm_files = get_all_VM_files(os.getcwd())
        if len(vm_files) == 0:
            example_usage('no vm files found')
    else:
        try:
            os.chdir(input)
            vm_files = get_all_VM_files(os.getcwd())
            if len(vm_files) == 0:
                example_usage('no vm files in specified directory')
        except FileNotFoundError:
            example_usage('no such directory')

# create a CodeWriter instance
cw = CodeWriter(vm_files, output)

# perform translation
cw.translate()

# close the output of the CodeWriter
cw.close()

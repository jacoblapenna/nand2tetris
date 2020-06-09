#!/usr/bin/env python3

from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine
import sys
import os

def list_all_jack_files(directory):
    """ develop a list of all jack files to compile """

    files = []

    # iterate through each file in pwd
    for file in os.listdir(directory):
        if '.jack' in file: # if file is a jack file
            # store filename in array
            files.append(file)

    return files

def example_usage(error_str):
    """ error handling function """

    print(f"Error: {error_str}!")
    print("Example usage:")
    print("    ./JackAnalyzer.py input_file.jack")
    print("    ./JackAnalyzer.py input_directory")
    sys.exit(1)

def tokenize(file_list):
    """ create a JackTokenizer instance for each file to  be compiled """

    global tokens

    for jack_file in file_list:
        tokens[jack_file] = JackTokenizer(jack_file)

def compile(tokens):
    """ operate on each token with CompilationEngine """

    pass

if __name__ == '__main__':

    tokens = {}

    """ parse command line arguments """
    try:
        input = sys.argv[1]
    except IndexError:
        example_usage('improper arguments')

    """
    determine whether input was a file or directory
    and proceed as needed in either case
    """
    if '.jack' in input:
        if input in os.listdir():
            jack_files = [input]
        else:
            example_usage('file not found')
    else:
        if input in os.getcwd():
            jack_files = list_all_jack_files(os.getcwd())
            if len(vm_files) == 0:
                example_usage('no jack files found in present directory')
        else:
            try:
                os.chdir(input)
                jack_files = list_all_jack_files(os.getcwd())
                if not jack_files:
                    example_usage('no vm files in specified directory')
            except FileNotFoundError:
                example_usage('no such directory')

    """ get tokens from each file """
    tokenize(jack_files)

#!/usr/bin/env python3

class Parser:

    def __init__(self, input_file):
        """ initialize an instance of Parser """
        self.filename = input_file
        self.EOF = False
        self.file_stream = open(self.filename, 'r')
        self.next_line = self.file_stream.readline()

    def close(self):
        """ cleanly close the input file """
        self.file_stream.close()

    # private method to determine command type
    def __cmd_switch(self, cmd):
        """ determine what type of command """
        if cmd == 'push':
            return 'C_PUSH'
        if cmd == 'pop':
            return 'C_POP'
        if cmd == 'label':
            return 'C_LABEL'
        if cmd == 'goto':
            return 'C_GOTO'
        if cmd == 'if-goto':
            return 'C_IF'
        if cmd == 'function':
            return 'C_FUNCTION'
        if cmd == 'return':
            return 'C_RETURN'
        if cmd == 'call':
            return 'C_CALL'
        else:
            return 'C_ARITHMETIC'

    def parse(self):
        """ parses input file on command """
        # grab current line and store next one
        line = self.next_line
        self.next_line = self.file_stream.readline()

        # if nex line doesn't exist
        if not self.next_line:
            self.EOF = True # set End Of File to True

        # strip whitespace and comments from line
        command = line.rstrip().split('//')[0].rstrip().lstrip()

        # if line contained command
        if command:
            # seperate command from argument(s)
            cmd_arr = command.lower().split(' ')
            # append command type
            cmd_arr.append(self.__cmd_switch(cmd_arr[0]))
            # return command array information
            return cmd_arr

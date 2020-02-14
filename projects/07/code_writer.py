#!/usr/bin/env python3

from parser import Parser

class CodeWriter:

    def __init__(self, input_file_lst, output_file):
        """ initialize an instance of CodeWriter """
        # set static variables
        self.filename = output_file + '.asm'
        self.file_stream = open(self.filename, 'w+')
        self.input_lst = input_file_lst
        self.label_id = 0

    def close(self):
        """ cleanly close the output file """
        self.file_stream.close()

    def __write(self, code_block):
        """ write a code block to ouput """
        self.file_stream.write(code_block)

    def translate(self):
        """ translate the virtual language """
        # iterate through input files
        for file in self.input_lst:
            # create a Parser instance for each file
            parser = Parser(file)
            while not parser.EOF:
                # parse lines until end of file
                command = parser.parse()
                if command:
                    self.__cmd_switch(command)
            parser.close()

    # "private" method to route command type
    def __cmd_switch(self, cmd):
        """ route command type based on parser label """
        c_type = cmd[-1]
        if c_type == 'C_PUSH':
            self.c_push(cmd[0:-1])
        elif c_type == 'C_POP':
            self.c_pop(cmd[0:-1])
        elif c_type == 'C_LABEL':
            self.c_label(cmd[0:-1])
        elif c_type == 'C_GOTO':
            self.c_goto(cmd[0:-1])
        elif c_type == 'C_IF':
            self.c_if(cmd[0:-1])
        elif c_type == 'C_FUNCTION':
            self.c_function(cmd[0:-1])
        elif c_type == 'C_RETURN':
            self.c_return(cmd[0:-1])
        elif c_type == 'C_CALL':
            self.c_call(cmd[0:-1])
        else:
            self.c_arithmetic(cmd[0])

    def c_push(self, cmd_arr):
        """ build push assembly string """

        # create locals
        segment = cmd_arr[1] # segment argument
        indx = cmd_arr[2] # index (i) argument
        comment_cmd = ' '.join(cmd_arr) # assembly comment string

        # determine segment and handle accordingly
        if segment == 'constant': # if constant
            # create comment for code block
            ass_str = f'// {comment_cmd}\n'
            # put integer value in D register
            ass_str += f'@{indx}\nD=A\n'
            # push to present stack position as follows:
            # @SP => A=addr 0, which contains address of stack's top
            # A=M => A=addr of stack's top
            # M=D => stack's top now is whatever integer was in D
            ass_str += '@SP\nA=M\nM=D\n'
            # increment stack pointer
            ass_str += '@SP\nM=M+1\n'
            # write code block to output
            self.__write(ass_str)

    def c_pop(self, segment, indx):
        print('Pop:', segment, indx)

    def c_arithmetic(self, cmd):
        """ build arithmetic assembly string """

        # create locals
        ass_str = f'// {cmd}\n' # commont for assembly code block

        # determine arithmetic operation
        # addition (x+y)
        if cmd == 'add':
            # decrement stack address
            ass_str += '@SP\nM=M-1\n'
            # set D to value at stack pointer (D=y)
            ass_str += '@SP\nA=M\nD=M\n'
            # decrement stack address
            ass_str += '@SP\nM=M-1\n'
            # get value at top of stack and perform operation (x+y)
            # simultaniously storing result at top of stack
            ass_str += '@SP\nA=M\nM=M+D\n'
            # increment stack address
            ass_str += '@SP\nM=M+1'
            # write code block to output
            self.__write(ass_str)

        # subtraction (x-y)
        elif cmd == 'sub':
            # decrement stack address
            ass_str += '@SP\nM=M-1\n'
            # set D to value at stack pointer (D=y)
            ass_str += '@SP\nA=M\nD=M\n'
            # decrement stack address
            ass_str += '@SP\nM=M-1\n'
            # get value at top of stack and perform operation (x-y)
            # simultaniously storing result at top of stack
            ass_str += '@SP\nA=M\nM=M-D\n'
            # increment stack address
            ass_str += '@SP\nM=M+1'
            # write code block to output
            self.__write(ass_str)

        # negation (-y)
        elif cmd == 'neg':
            # decrement stack address
            ass_str += '@SP\nM=M-1\n'
            # get value at top of stack and perform operation (-y)
            # simultaniously storing result at top of stack
            ass_str += '@SP\nA=M\nM=-M\n'
            # increment stack address
            ass_str += '@SP\nM=M+1'
            # write code block to output
            self.__write(ass_str)

        # equality (x == y)
        elif cmd == 'eq':
            """
            perform subtraction and store in D (D=x-y)
            jump to true condition if D=0
            (true condition block sets value at SP's address to -1)
            if jump does not trigger, jump to false condition
            (false condition block sets value at SP's address to 0)
            both bool blocks jump to finish block when completed
            finish block increments stack address before writing
            NOTE: Keep labels unique with incrementor!
            """
            # decrement stack address
            ass_str += '@SP\nM=M-1\n'
            # set D to value at stack pointer (D=y)
            ass_str += '@SP\nA=M\nD=M\n'
            # decrement stack address
            ass_str += '@SP\nM=M-1\n'
            # subtract (x-y) and jump appropriately
            # temporarilyt store result in top of stack
            ass_str += '@SP\nA=M\nM=M-D\n'
            # set D to subtraction result
            ass_str += '@SP\nA=M\nD=M\n'
            # block routing conditional on value in D=x-y
            ass_str += f'@EQUAL{self.label_id}\nD;JEQ\n'
            ass_str += f'@NOT_EQUAL{self.label_id}\n0;JMP\n'
            # true condition destination block
            ass_str += f'(EQUAL{self.label_id})\n'
            ass_str += '@SP\nA=M\nM=-1\n'
            ass_str += f'@EQ_FINISH{self.label_id}\n0;JMP\n'
            # false condition destination block
            ass_str += f'(NOT_EQUAL{self.label_id})\n'
            ass_str += '@SP\nA=M\nM=0\n'
            ass_str += f'@EQ_FINISH{self.label_id}\n0;JMP\n'
            # finish destination block
            ass_str += f'(EQ_FINISH{self.label_id})\n'
            ass_str += '@SP\nM=M+1\n'
            # write code block to output
            self.__write(ass_str)
            # increment label_id
            self.label_id += 1

        # greater than (x > y)
        elif cmd == 'gt':
            """
            perform subtraction and store in D (D=x-y)
            jump to true condition if D>0
            (true condition block sets value at SP's address to -1)
            if jump does not trigger, jump to false condition
            (false condition block sets value at SP's address to 0)
            both bool blocks jump to finish block when completed
            finish block increments stack address before writing
            NOTE: Keep labels unique to eq!
            """
            # decrement stack address
            ass_str += '@SP\nM=M-1\n'
            # set D to value at stack pointer (D=y)
            ass_str += '@SP\nA=M\nD=M\n'
            # decrement stack address
            ass_str += '@SP\nM=M-1\n'
            # subtract (x-y) and jump appropriately
            # temporarilyt store result in top of stack
            ass_str += '@SP\nA=M\nM=M-D\n'
            # set D to subtraction result
            ass_str += '@SP\nA=M\nD=M\n'
            # block routing conditional on value in D=x-y
            ass_str += f'@GREATER_THAN{self.label_id}\nD;JGT\n'
            ass_str += f'@NOT_GREATER_THAN{self.label_id}\n0;JMP\n'
            # true condition destination block
            ass_str += f'(GREATER_THAN{self.label_id})\n'
            ass_str += '@SP\nA=M\nM=-1\n'
            ass_str += f'@GT_FINISH{self.label_id}\n0;JMP\n'
            # false condition destination block
            ass_str += f'(NOT_GREATER_THAN{self.label_id})\n'
            ass_str += '@SP\nA=M\nM=0\n'
            ass_str += f'@GT_FINISH{self.label_id}\n0;JMP\n'
            # finish destination block
            ass_str += f'(GT_FINISH{self.label_id})\n'
            ass_str += '@SP\nM=M+1\n'
            # write code block to output
            self.__write(ass_str)
            # increment label_id
            self.label_id += 1

        # less than (x < y)
        elif cmd == 'lt':
            """
            perform subtraction and store in D (D=x-y)
            jump to true condition if D<0
            (true condition block sets value at SP's address to -1)
            if jump does not trigger, jump to false condition
            (false condition block sets value at SP's address to 0)
            both bool blocks jump to finish block when completed
            finish block increments stack address before writing
            NOTE: Keep labels unique to eq!
            """
            # decrement stack address
            ass_str += '@SP\nM=M-1\n'
            # set D to value at stack pointer (D=y)
            ass_str += '@SP\nA=M\nD=M\n'
            # decrement stack address
            ass_str += '@SP\nM=M-1\n'
            # subtract (x-y) and jump appropriately
            # temporarily store result in top of stack
            ass_str += '@SP\nA=M\nM=M-D\n'
            # set D to subtraction result
            ass_str += '@SP\nA=M\nD=M\n'
            # block routing conditional on value in D=x-y
            ass_str += f'@LESS_THAN{self.label_id}\nD;JLT\n'
            ass_str += f'@NOT_LESS_THAN{self.label_id}\n0;JMP\n'
            # true condition destination block
            ass_str += f'(LESS_THAN{self.label_id})\n'
            ass_str += '@SP\nA=M\nM=-1\n'
            ass_str += f'@LT_FINISH{self.label_id}\n0;JMP\n'
            # false condition destination block
            ass_str += f'(NOT_LESS_THAN{self.label_id})\n'
            ass_str += '@SP\nA=M\nM=0\n'
            ass_str += f'@LT_FINISH{self.label_id}\n0;JMP\n'
            # finish destination block
            ass_str += f'(LT_FINISH{self.label_id})\n'
            ass_str += '@SP\nM=M+1\n'
            # write code block to output
            self.__write(ass_str)
            # increment label_id
            self.label_id += 1

        # logical and (x & y)
        elif cmd == 'and':
            # decrement stack address
            ass_str += '@SP\nM=M-1\n'
            # set D to value at stack pointer (D=y)
            ass_str += '@SP\nA=M\nD=M\n'
            # decrement stack address
            ass_str += '@SP\nM=M-1\n'
            # get value at top of stack and perform operation (x&y)
            # simultaniously storing result at top of stack
            ass_str += '@SP\nA=M\nM=D&M\n'
            # increment stack address
            ass_str += '@SP\nM=M+1'
            # write code block to output
            self.__write(ass_str)

        # logical or (x | y)
        elif cmd == 'or':
            # decrement stack address
            ass_str += '@SP\nM=M-1\n'
            # set D to value at stack pointer (D=y)
            ass_str += '@SP\nA=M\nD=M\n'
            # decrement stack address
            ass_str += '@SP\nM=M-1\n'
            # get value at top of stack and perform operation (x|y)
            # simultaniously storing result at top of stack
            ass_str += '@SP\nA=M\nM=D|M\n'
            # increment stack address
            ass_str += '@SP\nM=M+1'
            # write code block to output
            self.__write(ass_str)

        # logical not (not y)
        elif cmd == 'not':
            # single stack value (sp - 2)
            # decrement stack address
            ass_str += '@SP\nM=M-1\n'
            # get value at top of stack and perform operation (!y)
            # simultaniously storing result at top of stack
            ass_str += '@SP\nA=M\nM=!M\n'
            # increment stack address
            ass_str += '@SP\nM=M+1'
            # write code block to output
            self.__write(ass_str)

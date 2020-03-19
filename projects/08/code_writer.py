#!/usr/bin/env python3

from parser import Parser

class CodeWriter:

    def __init__(self, input_file_lst, output_file, boot=True):
        """ initialize an instance of CodeWriter """
        # set static variables
        self.filename = output_file + '.asm'
        self.file_stream = open(self.filename, 'w+')
        self.input_lst = input_file_lst
        self.label_id = 0
        self.call_cnt = 0
        self.line_number = 0

        # initialize hack's static memory map
        self.static_indx = 0
        self.static_mem_map = {}
        for file in self.input_lst:
            self.static_mem_map[file] = {}

        if boot:
            # VM initialization (bootstrap code)
            self.bootstrap()

#-------------------------------------------------------------------------------

    def close(self):
        """ cleanly close the output file """
        self.file_stream.close()

#-------------------------------------------------------------------------------

    def __write(self, code_block):
        """ write a code block to ouput """

        def add_line_numbering(code_block):
            lines = code_block.split('\n')
            for n, line in enumerate(lines):
                if line:
                    if line[0] != "(" and line[0] != "/":
                        length = len(line)
                        # add instruction number as comment
                        lines[n] = line + \
                            f"{''.join([' ' for i in range(int(40 - length))])}\
                            // {self.line_number}"
                        self.line_number += 1
            return '\n'.join(lines)

        code_block = add_line_numbering(code_block)

        self.file_stream.write(code_block)

#-------------------------------------------------------------------------------

    def translate(self):
        """ translate the virtual language """
        # iterate through input files
        for file in self.input_lst:
            # create a Parser instance for each file
            parser = Parser(file)
            while not parser.EOF:
                # parse and write lines until end of file
                try:
                    command, file = parser.parse()
                    self.__cmd_switch(command, file)
                except TypeError:
                    pass
            parser.close()

#-------------------------------------------------------------------------------

    def bootstrap(self):
        """ allocate memory for virtual machine and initialize """

        # initialize assembly string with comment for code block
        ass_str = f'// this is the bootstrap code block\n'

        # initialize SP to point to RAM[256]
        ass_str += '@256\n'
        ass_str += 'D=A\n'
        ass_str += '@SP\n'
        ass_str += 'M=D\n'
        ass_str += '// call sys.init 0\n'
        self.__write(ass_str)

        # call Sys.init() function as present
        self.c_call(['call', 'sys.init', '0'], comment=False)

#-------------------------------------------------------------------------------

    # "private" method to route command type
    def __cmd_switch(self, cmd, file):
        """ route command type based on parser label """
        c_type = cmd[-1]
        if c_type == 'C_PUSH':
            self.c_push(cmd[0:-1], file)
        elif c_type == 'C_POP':
            self.c_pop(cmd[0:-1], file)
        elif c_type == 'C_LABEL':
            self.c_label(cmd[0:-1])
        elif c_type == 'C_GOTO':
            self.c_goto(cmd[0:-1])
        elif c_type == 'C_IF':
            self.c_if(cmd[0:-1])
        elif c_type == 'C_FUNCTION':
            self.c_function(cmd[0:-1])
        elif c_type == 'C_RETURN':
            self.c_return()
        elif c_type == 'C_CALL':
            self.c_call(cmd[0:-1])
        else:
            self.c_arithmetic(cmd[0])

#-------------------------------------------------------------------------------

    def c_push(self, cmd_arr, file=None, comment=True):
        """ build push assembly string """

        # create locals
        segment = cmd_arr[1] # segment argument
        indx = int(cmd_arr[2]) # index (i) argument
        if comment:
            comment_cmd = ' '.join(cmd_arr) # assembly comment string
            # initialize assembly string with comment for code block
            ass_str = f'// {comment_cmd}\n'
        else:
            ass_str = ''

        def push_and_write(ass_str):
            """
            helper function for repetitive aspect of push
            assembly string construction
            """
            # push to present stack position as follows:
            # @SP => A=addr 0, which contains address of stack's top
            # A=M => A=addr of stack's top
            # M=D => stack's top now is whatever integer was in D
            ass_str += '@SP\nA=M\nM=D\n'
            # increment stack pointer
            ass_str += '@SP\nM=M+1\n'
            # write code block to output
            self.__write(ass_str)

        # determine segment and handle accordingly
        if segment == 'constant': # if constant
            # put integer value in D register
            ass_str += f'@{indx}\nD=A\n'
            # push to top of stack and write to output
            push_and_write(ass_str)

        elif segment == 'local': # if local
            # put value contained at LCL+indx into D
            ass_str += f'@{indx}\nD=A\n@LCL\nA=D+M\nD=M\n'
            # push to top of stack and write to ouput
            push_and_write(ass_str)

        elif segment == 'argument':
            # put value contained at ARG+indx into D
            ass_str += f'@{indx}\nD=A\n@ARG\nA=D+M\nD=M\n'
            # push to top of stack and write to ouput
            push_and_write(ass_str)

        elif segment == 'this':
            # put value contained at THIS+indx into D
            ass_str += f'@{indx}\nD=A\n@THIS\nA=D+M\nD=M\n'
            # push to top of stack and write to ouput
            push_and_write(ass_str)

        elif segment == 'that':
            # put value contained at THIS+indx into D
            ass_str += f'@{indx}\nD=A\n@THAT\nA=D+M\nD=M\n'
            # push to top of stack and write to ouput
            push_and_write(ass_str)

        elif segment == 'static':
            # memory allocation from RAM[16] to RAM[255]
            if 0 <= indx <= 239:
                # set absolute address index
                addr = self.static_mem_map[file][indx]
                # put value contained at indx into D
                ass_str += f'@{addr}\nD=M\n'
                # push to top of stack and write to ouput
                push_and_write(ass_str)

        elif segment == 'temp':
            # memory allocation from RAM[5] to RAM[12]
            if 0 <= indx <= 7:
                # set absolute address index
                indx += 5
                # put value contained at indx into D
                ass_str += f'@{indx}\nD=M\n'
                # push to top of stack and write to ouput
                push_and_write(ass_str)

        elif segment == 'pointer':
            # indx can only be 0 or 1
            if indx == 0:
                # push THIS
                ass_str += f'@THIS\nD=M\n'
            elif indx == 1:
                # push THAT
                ass_str += f'@THAT\nD=M\n'
            # push to top of stack and write to ouput
            push_and_write(ass_str)

#-------------------------------------------------------------------------------

    def c_pop(self, cmd_arr, file=None, comment=True):
        """ build pop assembly string """

        # create locals
        segment = cmd_arr[1] # segment argument
        indx = int(cmd_arr[2]) # index (i) argument
        if comment:
            comment_cmd = ' '.join(cmd_arr) # assembly comment string
            # initialize assembly string with comment for code block
            ass_str = f'// {comment_cmd}\n'
        else:
            ass_str = ''

        def pop_and_write(ass_str):
            """
            helper function for repetitive aspect of pop
            assembly string construction
            """
            # pop from last stack position as follows:
            # @SP   => A=addr 0, which contains address of stack's top
            # M=M-1 => decrement stack address to get last location
            # A=M   => store last occupied stack address in A
            # D=M   => store tha value at the last occupied stack address in D
            # @R13  => set A address where popping address is stored
            # A=M   => set A to popping address
            # M=D   => put value in D into popping address's location
            ass_str += '@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D\n'
            # write code block to output
            self.__write(ass_str)

        # determine segment and handle accordingly
        if segment == 'local':
            # put LCL+indx address into R13
            ass_str += f'@{indx}\nD=A\n@LCL\nA=D+M\nD=A\n@R13\nM=D\n'
            # pop from stack and write to ouput
            pop_and_write(ass_str)

        elif segment == 'argument':
            # put ARG+indx address into R13
            ass_str += f'@{indx}\nD=A\n@ARG\nA=D+M\nD=A\n@R13\nM=D\n'
            # pop from stack and write to ouput
            pop_and_write(ass_str)

        elif segment == 'this':
            # put THIS+indx address into R13
            ass_str += f'@{indx}\nD=A\n@THIS\nA=D+M\nD=A\n@R13\nM=D\n'
            # pop from stack and write to ouput
            pop_and_write(ass_str)

        elif segment == 'that':
            # put LCL+indx address into R13
            ass_str += f'@{indx}\nD=A\n@THAT\nA=D+M\nD=A\n@R13\nM=D\n'
            # pop from stack and write to ouput
            pop_and_write(ass_str)

        elif segment == 'static':
            # memory allocation from RAM[16] to RAM[255]
            if 0 <= indx <= 239:
                # set absolute address
                addr = 16 + self.static_indx
                self.static_indx += 1
                # map memory location
                self.static_mem_map[file][indx] = addr
                # put 16+indx address into R13
                ass_str += f'@{addr}\nD=A\n@R13\nM=D\n'
                # push to top of stack and write to ouput
                pop_and_write(ass_str)

        elif segment == 'temp':
            # memory allocation from RAM[5] to RAM[12]
            if 0 <= indx <= 7:
                # set absolute address index
                indx += 5
                # put 5+indx address into R13
                ass_str += f'@{indx}\nD=A\n@R13\nM=D\n'
                # push to top of stack and write to ouput
                pop_and_write(ass_str)

        elif segment == 'pointer':
            # indx can only be 0 or 1
            if indx == 0:
                # store THIS address into R13
                ass_str += f'@THIS\nD=A\n@R13\nM=D\n'
            elif indx == 1:
                # store THAT address into R13
                ass_str += f'@THAT\nD=A\n@R13\nM=D\n'
            # push to top of stack and write to ouput
            pop_and_write(ass_str)

#-------------------------------------------------------------------------------

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
            ass_str += '@SP\nM=M+1\n'
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
            ass_str += '@SP\nM=M+1\n'
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
            ass_str += '@SP\nM=M+1\n'
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
            ass_str += '@SP\nM=M+1\n'
            # write code block to output
            self.__write(ass_str)

        # logical or (x | y)
        elif cmd == 'or':
            # decrement stack address
            ass_str += '@SP\nM=M-1\n'
            # set D to value at stack pointer (D=y)
            ass_str += '@SP\nA=M\nD=M\n' # REPLACE WITH JUST D=M
            # decrement stack address
            ass_str += '@SP\nM=M-1\n'
            # get value at top of stack and perform operation (x|y)
            # simultaniously storing result at top of stack
            ass_str += '@SP\nA=M\nM=D|M\n'
            # increment stack address
            ass_str += '@SP\nM=M+1\n'
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
            ass_str += '@SP\nM=M+1\n'
            # write code block to output
            self.__write(ass_str)

#-------------------------------------------------------------------------------

    def c_label(self, cmd_arr, comment=True):
        """ build label assembly string """

        # create locals
        label = cmd_arr[1]
        if comment:
            comment_cmd = ' '.join(cmd_arr) # assembly comment string
            # initialize assembly string with comment for code block
            ass_str = f'// {comment_cmd}\n'
        else:
            ass_str = ''

        # create assembly string with label
        ass_str += f'({label})\n'
        # write code block to output
        self.__write(ass_str)

#-------------------------------------------------------------------------------

    def c_goto(self, cmd_arr, comment=True):
        """ build goto assembly string """

        # create locals
        label = cmd_arr[1]
        if comment:
            comment_cmd = ' '.join(cmd_arr) # assembly comment string
            # initialize assembly string with comment for code block
            ass_str = f'// {comment_cmd}\n'
        else:
            ass_str = ''

        # address instruction of jump location
        ass_str += f'@{label}\n'
        # jump to jump location
        ass_str += '0;JMP\n'
        # write code block to output
        self.__write(ass_str)

#-------------------------------------------------------------------------------

    def c_if(self, cmd_arr):
        """ build if-goto assembly string """

        # create locals
        label = cmd_arr[1]
        comment_cmd = ' '.join(cmd_arr) # assembly comment string
        # initialize assembly string with comment for code block
        ass_str = f'// {comment_cmd}\n'

        ass_str += '@SP\nM=M-1\n' # decrement SP
        ass_str += 'A=M\nD=M\n' # set D to last value in stack
        # if last stack value is true goto jump location
        ass_str += f'@{label}\n'
        ass_str += 'D;JNE\n'
        # write code block to output
        self.__write(ass_str)

#-------------------------------------------------------------------------------

    def c_function(self, cmd_arr):
        """ build function assembly string """

        # create function label to address code block
        self.c_label(cmd_arr)

        # push locals, if any, on stack
        # NOTE: Figure 8.4 shows LCL pointing to local 0,
        # therefore push constant not push local.
        for i in range(int(cmd_arr[2])):
            self.c_push(['push', 'constant', '0'], comment=False)

#-------------------------------------------------------------------------------

    def c_call(self, cmd_arr, comment=True):
        """ build call assembly string """
        # We're setting up the stack before entering into the
        # functions code block. We assume all relevant arguments
        # have already been pushed on the stack. See fig 8.5.

        # create locals
        if comment:
            comment_cmd = ' '.join(cmd_arr) # assembly comment string
            # initialize assembly string with comment for code block
            ass_str = f'// {comment_cmd}\n'
        else:
            ass_str = ''

        def push_pointer(pointer):
            return f'@{pointer}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'

        # push return address on stack
        ret_label = f'{cmd_arr[1]}.return_{str(self.call_cnt)}'
        ass_str += f'@{ret_label}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n'
        #self.__write(ass_str)
        # push LCL pointer to stack
        ass_str += push_pointer('LCL')
        # push ARG pointer to stack
        ass_str += push_pointer('ARG')
        # push THIS pointer to stack
        ass_str += push_pointer('THIS')
        # push THAT pointer to stack
        ass_str += push_pointer('THAT')

        # reposition ARG to first related argumnet pushed on stack
        # (i.e. ARG_address = SP - (5 + n))
        ass_str += '@SP\nD=M\n@5\nD=D-A\n'
        ass_str += f'@{int(cmd_arr[2])}\nD=D-A\n@ARG\nM=D\n'

        # position LCL at current stack position
        ass_str += '@SP\nD=M\n@LCL\nM=D\n'
        # write code block to output
        self.__write(ass_str)

        # goto function block
        self.c_goto(['goto', cmd_arr[1]], comment=False)

        # build return address label
        self.c_label(['label', ret_label], comment=False)

        # increment call count
        self.call_cnt += 1

#-------------------------------------------------------------------------------

    def c_return(self):
        """ build return assembly string """
        # get last value on stack and bring up to entry point.
        # the entry point is held by ARG at argument 0.
        # reposition SP to just after the entry point and restore
        # key pointers values of caller. Finally, goto return address

        # create locals
        comment_cmd = 'return' # assembly comment string
        # initialize assembly string with comment for code block
        ass_str = f'// {comment_cmd}\n'

        def pop_pointer(pointer):
            return f'@LCL\nM=M-1\n@LCL\nA=M\nD=M\n@{pointer}\nM=D\n'

        # get return address created on call
        ass_str += '@5\nD=A\n@LCL\nD=M-D\nA=D\nD=M\n@R14\nM=D\n'
        self.__write(ass_str)
        # set value at ARG to return value (pop last stack value to ARG)
        self.c_pop(['pop', 'argument', '0'], comment=False)
        # reposition stack pointer
        ass_str = '@ARG\nD=M+1\n@SP\nM=D\n'
        # restore caller stack's pointers
        # restore THAT
        ass_str += pop_pointer('THAT')
        # retore THIS
        ass_str += pop_pointer('THIS')
        # retore ARG
        ass_str += pop_pointer('ARG')
        # restore LCL
        ass_str += pop_pointer('LCL')
        # goto return address
        ass_str += '@R14\nA=M\n0;JMP\n'
        # write to output file
        self.__write(ass_str)

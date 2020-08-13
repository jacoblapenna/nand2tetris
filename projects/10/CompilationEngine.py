#!/usr/bin/env python3

import os
from JackToken import JackToken
from JackSymbols import jack_symbols_list

class CompilationEngine:
    """
    Uses recursive compilation to associate object variables and methods
    with their owners. For example, to compile a function, each variable
    and expression within the function is compiled with a call from within
    the function compilation method. In this way, the opening tag is output
    at the start of function compilation, and the closing tag is applied
    at the end of function compilation only after all the internal function
    code has been compiled from within the function.
    """

    def __init__(self, tokens, input_file):
        self.tokens = tokens
        self.token_cnt = 0
        self.token_cnt_limit = len(self.tokens) - 1
        if ('Output' not in os.listdir()):
            os.makedirs('Output')
        self.output_file = f"Output/{input_file.split('.')[0]}.xml"
        self.output_stream = open(self.output_file, 'w')

        self.compile_class()

    """---------------------------------------------------------------------"""

    def get_next_token(self, peak_at_future_token=False):

        if self.token_cnt <= self.token_cnt_limit:
            token_indx = self.token_cnt
            token = self.tokens[token_indx]
            if not peak_at_future_token:
                self.token_cnt += 1
            return token
        else:
            self.output_stream.close()
            return None

    """---------------------------------------------------------------------"""

    def output(self, string):
        """ writes string to ouput_stream with correct format """
        self.output_stream.write(f'{string}\n')

    """---------------------------------------------------------------------"""

    def write_token(self, token):
        """
        handles each token
        """

        type = token.type
        value = token.value

        if type == 'keyword': # check for keyword
            self.output(f'<keyword> {value} </keyword>')
        elif type == 'symbol': # check for symbol
            #""" start xml formatting requirements for symbols """
            if value == '<':
                self.output(f'<symbol> &lt; </symbol>')
            elif value == '>':
                self.output(f'<symbol> &gt; </symbol>')
            elif value == '&':
                self.output(f'<symbol> &amp; </symbol>')
            #""" end xml formatting requirements for symbols """
            else:
                self.output(f'<symbol> {value} </symbol>')
        elif type == 'integer': # check for integer
            self.output(f'<integerConstant> {value} </integerConstant>')
        elif type == 'identifier': # check for indentifier
            self.output(f'<identifier> {value} </identifier>')
        elif type == 'string': # it's a string
            self.output(f'<stringConstant> {value} </stringConstant>')

    """---------------------------------------------------------------------"""

    # first word/token in each .jack should be 'class'
    # call CompilationEngine.compile_class() to get the ball rolling
    def compile_class(self):
        """ compile class declaration by recursively compiling its content """

        left_bracket_cnt = 0
        right_bracket_cnt = 0

        self.output('<class>') # start class

        while not left_bracket_cnt:
            # process class declaration
            token = self.get_next_token()
            if token.value == '{':
                left_bracket_cnt += 1
            self.write_token(token)

        while left_bracket_cnt - right_bracket_cnt:
            # process contents of class until closing bracket is reached
            token = self.get_next_token()
            if token.value == '{':
                left_bracket_cnt += 1
                self.write_token(token)
            elif token.value == '}':
                right_bracket_cnt += 1
                self.write_token(token)
            elif token.value in ['field', 'static']:
                self.compile_class_var_dec(token)
            elif token.value in ['constructor', 'method', 'function']:
                self.compile_subroutine(token)

        self.output('</class>') # end class

    """---------------------------------------------------------------------"""

    def compile_class_var_dec(self, token):

        exit_var_dec = False

        self.output('<classVarDec>')

        self.write_token(token)

        while not exit_var_dec:
            token = self.get_next_token()
            if token.value == ';':
                exit_var_dec = True
            self.write_token(token)

        self.output('</classVarDec>')

    """---------------------------------------------------------------------"""

    def compile_subroutine(self, token):

        exit_subroutine_dec = False

        self.output('<subroutineDec>')
        self.write_token(token)

        while not exit_subroutine_dec:
            token = self.get_next_token()
            if token.value == '(':
                exit_subroutine_dec = True
            self.write_token(token)

        self.compile_parameter_list()

        self.output('<subroutineBody>')
        token = self.get_next_token()
        self.write_token(token)

        # compile var declarations if present
        token = self.get_next_token()
        while token.value == 'var':
            self.compile_var_dec(token)
            token = self.get_next_token()

        # statements come after var declerations
        token = self.compile_statements(token)

        # write the last '}' of the subroutine body
        self.write_token(token)

        # exit, close, and return from subroutine
        self.output('</subroutineBody>')
        self.output('</subroutineDec>')

    """---------------------------------------------------------------------"""

    def compile_parameter_list(self):

        self.output('<parameterList>')

        token = self.get_next_token()

        if token.value == ')':
            exit_param_list = True
        else:
            exit_param_list = False
            self.write_token(token)

        while not exit_param_list:
            token = self.get_next_token()
            if token.value == ')':
                exit_param_list = True
            else:
                self.write_token(token)

        self.output('</parameterList>')

        self.write_token(token)

    """---------------------------------------------------------------------"""

    def compile_var_dec(self, token):

        self.output('<varDec>')

        while True:
            if token.value == ';':
                self.write_token(token)
                break
            else:
                self.write_token(token)
                token = self.get_next_token()

        self.output('</varDec>')

    """---------------------------------------------------------------------"""

    def compile_statements(self, token=False):
        """ everything you need is in figure 10.5 of the book """

        # open statements
        self.output('<statements>')

        # if no token is passed, get next one
        if not token:
            token = self.get_next_token()

        # if token is a statement keyword
        while token.value in ['let', 'if', 'while', 'do', 'return']:
            if token.value == 'let':
                self.compile_let(token)
            elif token.value == 'if':
                self.compile_if(token)
            elif token.value == 'while':
                self.compile_while(token)
            elif token.value == 'do':
                self.compile_do(token)
            elif token.value == 'return':
                self.compile_return(token)
            token = self.get_next_token()

        self.output('</statements>')

        return token;

    """---------------------------------------------------------------------         WORK ON THIS ONE TO MAKE CLEANER """

    def compile_let(self, token):

        exit_let_statement = False

        self.output('<letStatement>')

        self.write_token(token)

        while not exit_let_statement:
            token = self.get_next_token()
            if token.value in ['=', '[']:
                self.write_token(token)
                token = self.compile_expression()

            self.write_token(token)

            if token.value == ';':
                exit_let_statement = True

        self.output('</letStatement>')

    """---------------------------------------------------------------------"""

    def compile_if(self, token):

        self.output('<ifStatement>')

        while True:
            if token.value == '(':
                self.write_token(token)
                token = self.compile_expression()
            elif token.value == '{':
                self.write_token(token)
                token = self.compile_statements()
            elif token.value == '}':
                self.write_token(token)
                future_token = self.get_next_token(peak_at_future_token=True)
                if future_token.value == "else":
                    token = self.get_next_token()
                else:
                    break
            else:
                self.write_token(token)
                token = self.get_next_token()

        self.output('</ifStatement>')

    """---------------------------------------------------------------------"""

    def compile_while(self, token):

        self.output('<whileStatement>')

        while True:
            #self.write_token(token)
            if token.value == '(':
                self.write_token(token)
                token = self.compile_expression()
            elif token.value == '{':
                self.write_token(token)
                token = self.compile_statements()
            elif token.value == '}':
                self.write_token(token)
                break
            else:
                self.write_token(token)
                token = self.get_next_token()

        self.output('</whileStatement>')

    """---------------------------------------------------------------------"""

    def compile_do(self, token):

        self.output('<doStatement>')

        while True:
            if token.value == '(':
                self.write_token(token)
                token = self.compile_expression_list()
            elif token.value == ';':
                self.write_token(token)
                break
            else:
                self.write_token(token)
                token = self.get_next_token()

        self.output('</doStatement>')

    """---------------------------------------------------------------------"""

    def compile_return(self, token):

        self.output('<returnStatement>')

        while True:
            if token.value == ';':
                self.write_token(token)
                break
            elif token.value != "return":
                token = self.compile_expression(token)
            else:
                self.write_token(token)
                token = self.get_next_token()

        self.output('</returnStatement>')

    """---------------------------------------------------------------------"""

    def compile_expression(self, token=False):

        writeable_tokens = ['+', '-', '*', '/', '&', '|', '<', '>', '~', '=']

        self.output('<expression>') # open expression

        # if no token is passed, get next one
        if not token:
            token = self.get_next_token()

        while not token.value in [')', ']', ';', ',']:
            token = self.compile_term(token)
            if token.value in writeable_tokens:
                self.write_token(token)
                token = self.get_next_token()

        self.output('</expression>') # close expression

        #self.output(f"Returning from compile_expression() with: {token.value}") #DEBUG
        return token

    """---------------------------------------------------------------------"""

    def compile_expression_list(self, token=False):

        self.output('<expressionList>')

        # if no token is passed, get next one
        if not token:
            token = self.get_next_token()

        while token.value != ')':
            if token.value == ',':
                self.write_token(token)
                token = self.get_next_token()
            token = self.compile_expression(token)

        self.output('</expressionList>')

        #self.output(f"Returning from compile_expression_list() with: {token.value}") #DEBUG
        return token

    """---------------------------------------------------------------------"""

    def compile_term(self, token):

        returnable_symbols = [')', ']', ',', ';', '+', '-', '*', '/', '&', '|', '<', '>', '~', '=']
        previous_token = JackToken(None, None)

        self.output('<term>')

        while True:
            if token.value in returnable_symbols:
                if not previous_token.value:
                    # token is unary operator
                    self.write_token(token)
                    token = self.compile_term(self.get_next_token())
                    break
                else:
                    # token is binary operator (not necessarily bitwise)
                    break
            elif token.value == '(':
                if previous_token.type == "identifier":
                    self.write_token(token)
                    token = self.compile_expression_list()
                    self.write_token(token)
                else:
                    self.write_token(token)
                    token = self.compile_expression()
                    self.write_token(token)
            elif previous_token.type == "identifier" and token.value == '[':
                self.write_token(token)
                token = self.compile_expression()
                self.write_token(token)
            else:
                self.write_token(token)
            previous_token = token
            token = self.get_next_token()

        self.output('</term>')

        #self.output(f"Returning from compile_term() with: {token.value}") #DEBUG
        return token

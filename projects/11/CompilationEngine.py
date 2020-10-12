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

    Figure 10.5 is of great help!
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
        """ grab the next token from the tokenizer """

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
        """ handles each token for output to XML file """

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
        """ copile class variable declaration """

        self.output('<classVarDec>')

        # iterate through token
        while True:
            if token.value == ';':
                # each declaration ends on a semi-colon
                self.write_token(token)
                break
            else:
                # otherwise, output token as normal
                self.write_token(token)
                token = self.get_next_token()

        self.output('</classVarDec>')

    """---------------------------------------------------------------------"""

    def compile_subroutine(self, token):
        """ compiles a subroutine declaration """

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
        """ compiles function parameter requirements """

        self.output('<parameterList>') # open parameter section

        token = self.get_next_token() # ger first param token

        while token.value != ')':
            # iterate and output tokens until end of parameter list
            self.write_token(token)
            token = self.get_next_token()

        self.output('</parameterList>') # close parameter section

        self.write_token(token) # ouput closing parenthases

    """---------------------------------------------------------------------"""

    def compile_var_dec(self, token):
        """ compiles variable declarations """

        # same as class variable declaration but with different XML tags

        self.output('<varDec>') # open variable declarions section

        # iterate through token
        while True:
            if token.value == ';':
                # each declaration ends on a semi-colon
                self.write_token(token)
                break
            else:
                # otherwise, output token as normal
                self.write_token(token)
                token = self.get_next_token()

        self.output('</varDec>') # close variable declaration section

    """---------------------------------------------------------------------"""

    def compile_statements(self, token=False):
        """ compiles statements """

        self.output('<statements>') # open statements

        # if no token is passed by caller, get next one
        if not token:
            token = self.get_next_token()

        # if token is a statement keyword
        while token.value in ['let', 'if', 'while', 'do', 'return']:
            # route to respective compiling function
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

        self.output('</statements>') # close statements

        return token; # caller is expecting a return token

    """---------------------------------------------------------------------"""

    def compile_let(self, token):
        """ compiles a let statement """

        self.output('<letStatement>') # open let statement

        while True:
            # iterate through let statement tokens
            if token.value == ';':
                # end on semi-colon
                self.write_token(token)
                break
            if token.value in ['=', '[']:
                # array index or variable set to expression
                # array index can be expression itself
                self.write_token(token)
                token = self.compile_expression()
            else:
                # otherwise, output token within let statement tags
                self.write_token(token)
                token = self.get_next_token()

        self.output('</letStatement>') # close let statement

    """---------------------------------------------------------------------"""

    def compile_if(self, token):
        """ compiles an if or if/else statement """

        self.output('<ifStatement>') # open if statement

        # itereate through statement tokens
        while True:
            if token.value == '(':
                # parenthases start expressions
                self.write_token(token)
                token = self.compile_expression()
            elif token.value == '{':
                # left braces start statements
                self.write_token(token)
                token = self.compile_statements()
            elif token.value == '}':
                # right braces end statments
                self.write_token(token)
                future_token = self.get_next_token(peak_at_future_token=True)
                # determine if statement is if/else or just if
                if future_token.value == "else":
                    token = self.get_next_token()
                else:
                    break # break if no more to if/else
            else:
                # otherwise output token
                self.write_token(token)
                token = self.get_next_token()

        self.output('</ifStatement>') # close if statement

    """---------------------------------------------------------------------"""

    def compile_while(self, token):
        """ compile while statement """

        self.output('<whileStatement>') # open while statement

        # itereate through statement's tokens
        while True:
            if token.value == '(':
                # left parent starts expressions
                self.write_token(token)
                token = self.compile_expression()
            elif token.value == '{':
                # left brace starts statements
                self.write_token(token)
                token = self.compile_statements()
            elif token.value == '}':
                # right brace ends statements, no need to detect else
                self.write_token(token)
                break
            else:
                # otherwise, output token
                self.write_token(token)
                token = self.get_next_token()

        self.output('</whileStatement>') # close while statement

    """---------------------------------------------------------------------"""

    def compile_do(self, token):
        """ compile do statement """

        self.output('<doStatement>') # open do statement

        # itereate through statement's tokens
        while True:
            if token.value == '(':
                # left parenthases start expressions
                self.write_token(token)
                token = self.compile_expression_list()
            elif token.value == ';':
                # ends on semi-colon
                self.write_token(token)
                break
            else:
                # otherwise, output token
                self.write_token(token)
                token = self.get_next_token()

        self.output('</doStatement>') # close do statement

    """---------------------------------------------------------------------"""

    def compile_return(self, token):
        """ compile return """

        self.output('<returnStatement>') # open return statement

        while True:
            if token.value == ';':
                # end on semi-colon
                self.write_token(token)
                break
            elif token.value != "return":
                # unless trying to return an expression
                token = self.compile_expression(token)
            else:
                # otherwise output token as normal
                self.write_token(token)
                token = self.get_next_token()

        self.output('</returnStatement>') # close return statement

    """---------------------------------------------------------------------"""

    def compile_expression(self, token=False):
        """ compile expressions """

        # define tokens outside terms and within expressions
        writeable_tokens = ['+', '-', '*', '/', '&', '|', '<', '>', '~', '=']

        self.output('<expression>') # open expression

        # if no token is passed, get next one
        if not token:
            token = self.get_next_token()

        # if token does not indicate closing the expression, itereate
        while not token.value in [')', ']', ';', ',']:
            token = self.compile_term(token)
            if token.value in writeable_tokens:
                self.write_token(token)
                token = self.get_next_token()

        self.output('</expression>') # close expression

        return token # caller is expecting a token back

    """---------------------------------------------------------------------"""

    def compile_expression_list(self, token=False):
        """ compile a list of expressions """

        self.output('<expressionList>') # open expression list

        # if no token is passed, get next one
        if not token:
            token = self.get_next_token()

        # iterate through tokens until list is closed
        while token.value != ')':
            # list is comma seperated
            if token.value == ',':
                self.write_token(token)
                token = self.get_next_token()
            # items in list are expressions
            token = self.compile_expression(token)

        self.output('</expressionList>') # close expression list

        return token # caller is expecting a token back

    """---------------------------------------------------------------------"""

    def compile_term(self, token):
        """ compile a term within an expression """

        # define symbols that indicate end of term
        returnable_symbols = [')', ']', ',', ';', '+', '-', '*', '/', '&', '|', '<', '>', '~', '=']
        # keep track of what's been compiled so far
        previous_token = JackToken(None, None)

        self.output('<term>') # open term

        # itereate through token within term
        while True:
            # if token indicated end of term
            if token.value in returnable_symbols:
                # detect whether it is unary or not
                if not previous_token.value:
                    # token is unary operator, write before returning
                    self.write_token(token)
                    token = self.compile_term(self.get_next_token())
                    break
                else:
                    # token is binary operator (not necessarily bitwise)
                    # return token to caller to write in expression as
                    # term seperator
                    break
            elif token.value == '(':
                # either a subroutine was called or there is some
                # parenthetical math operations going one
                if previous_token.type == "identifier":
                    # if an identifier preceeds the token, a subroutine
                    # was called, in which case an expression list follows
                    self.write_token(token)
                    token = self.compile_expression_list()
                    self.write_token(token)
                else:
                    # otherwise, parenthesis are present to define order
                    # of operations within maths, which means it is enclosing
                    # an expression rather than expression list
                    self.write_token(token)
                    token = self.compile_expression()
                    self.write_token(token)
            elif previous_token.type == "identifier" and token.value == '[':
                # if term is composed of an array access, compile expression
                # within indexing brackets, as index can itself be an
                # expression
                self.write_token(token)
                token = self.compile_expression()
                self.write_token(token)
            else:
                # otherwise, output token as nromal
                self.write_token(token)
            # keep track of last compiled token
            previous_token = token
            token = self.get_next_token() # continue with next token

        self.output('</term>') # close term

        return token # caller is expecting a token back

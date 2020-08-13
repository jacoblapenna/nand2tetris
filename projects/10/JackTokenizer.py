#!/usr/bin/env python3

from CompilationEngine import CompilationEngine
from JackKeywords import jack_keywords_list
from JackSymbols import jack_symbols_list
from JackToken import JackToken
import re
import os

class JackTokenizer:

    def __init__(self, input_file):
        self.input_stream = open(input_file, 'r')
        self.symbol_regex = fr"{'|'.join([re.escape(char) for char in jack_symbols_list])}"
        self.tokens = []

        """ output stream only needed for stage 1 """
        # if ('Output' not in os.listdir()):
        #     os.makedirs('Output')
        # self.output_file = f"Output/{input_file.split('.')[0]}T.xml"
        # self.output_stream = open(self.output_file, 'w')

        """ <tokens> xml only needed for stage 1 """
        # self.output_stream.write('<tokens>\n')

        for line_number, line in enumerate(self.input_stream):
            # get rid of whitespace and comments
            code = re.split(r'//|/\*', line)[0].strip()
            # if code is present, process it
            if code and code[0] != '*':
                tokens = self.get_tokens(code)
                for token in tokens:
                    self.tokens.append(token)
                    """ output only needed for stage 1 """
                    # output_line = self.process_token(token)
                    # self.output_stream.write(output_line + '\n')

        CompilationEngine(self.tokens, input_file)

        """ <tokens> xml only needed for stage 1 """
        # self.output_stream.write('</tokens>')

        """ output not a file for stage 2 """
        # self.output_stream.close()
        self.input_stream.close()

    def get_tokens(self, code):
        """ parse individual tokens from a string of code """

        # create dict to store tokens and their type
        token_list = [] # list of JackToken objects

        def check_for_int(token):
            # helper function to check if token is an integer
            try:
                int(token)
                return True
            except ValueError:
                return False

        # detect strings
        strings = re.findall(r'["\']([^"\']+)["\']', code)
        # remove whitespace that is not within a string and flatten result
        sub_tokens = sum([[t] if t in strings else t.split() for t in re.split(r'["\']', code)], [])
        # separate by symbols, flatten result, and lose empty tokens
        tokens = list(filter(None, sum([[t] if t in strings else re.split(fr'({self.symbol_regex})', t) for t in sub_tokens], [])))

        # get token types
        for token in tokens:
            if token in strings:
                type = 'string'
            elif token in jack_symbols_list:
                type = 'symbol'
            elif token in jack_keywords_list:
                type = 'keyword'
            elif check_for_int(token):
                type = 'integer'
            else:
                type = 'identifier'
            # put the token in the token_list
            token_list.append(JackToken(token, type))

        return token_list

    # this function is only needed for stage 1 of the project to
    # check tokenization, comment out call for final stage 2 and port
    # tokens to CompilationENgine instead
    def process_token(self, token):
        """ prepares token for entry into output stream """

        if token.type == 'keyword': # check for keyword
            return f'<keyword> {token.value} </keyword>'
        elif token.type == 'symbol': # check for symbol
            """ start xml formatting requirements for symbols """
            if token.value == '<':
                return f'<symbol> &lt; </symbol>'
            elif token.value == '>':
                return f'<symbol> &gt; </symbol>'
            elif token.value == '&':
                return f'<symbol> &amp; </symbol>'
            """ end xml formatting requirements for symbols """
            return f'<symbol> {token.value} </symbol>'
        elif token.type == 'integer': # check for integer
            return f'<integerConstant> {token.value} </integerConstant>'
        elif token.type == 'identifier': # check for indentifier
            return f'<identifier> {token.value} </identifier>'
        elif token.type == 'string': # it's a string
            return f'<stringConstant> {token.value} </stringConstant>'

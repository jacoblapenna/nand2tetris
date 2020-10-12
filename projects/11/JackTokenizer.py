#!/usr/bin/env python3

from CompilationEngine import CompilationEngine
from JackKeywords import jack_keywords_list
from JackSymbols import jack_symbols_list
from JackToken import JackToken
from SymbolTable import SymbolTable
import re
import os

class JackTokenizer:

    def __init__(self, input_file):
        self.input_stream = open(input_file, 'r')
        self.symbol_regex = fr"{'|'.join([re.escape(char) for char in jack_symbols_list])}"
        self.tokens = []
        self.scope_tracker = SymbolTable()

        for line_number, line in enumerate(self.input_stream):
            # get rid of whitespace and comments
            code = re.split(r'//|/\*', line)[0].strip()
            # if code is present, process it
            if code and code[0] != '*':
                tokens = self.get_tokens(code)
                for token in tokens:
                    self.tokens.append(token)

        print(self.scope_tracker.class_scope) # DEBUG
        print(self.scope_tracker.subroutine_scope) # DEBUG
        
        CompilationEngine(self.tokens, input_file)

        self.input_stream.close()

    def get_tokens(self, code):
        """ parse individual tokens from a line of code """

        # create dict to store tokens and their type
        token_list = [] # list of JackToken objects
        identifier_in_tokens = False # detect lines with identifiers

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
                # detect lines with identifiers
                identifier_in_tokens = True

            # put the token in the token_list
            token_list.append(JackToken(token, type))

        if identifier_in_tokens:
            # handle identifier and associated scope
            self.scope_tracker.handle_identifier(token_list)

        return token_list

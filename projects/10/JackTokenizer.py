#!/usr/bin/env python3

from JackKeywords import jack_keywords_list
from JackSymbols import jack_symbols_list
import re
import os

class JackTokenizer:

    def __init__(self, input_file):
        self.input_stream = open(input_file, 'r')
        if ('Output' not in os.listdir()):
            os.makedirs('Output')
        self.output_file = f"Output/{input_file.split('.')[0]}T.xml"
        self.output_stream = open(self.output_file, 'w')
        self.builtins_regex = self.get_builtins_regex()

        for line_number, line in enumerate(self.input_stream):
            # get rid of whitespace and comments
            code = re.split(r'//|/\*', line)[0].strip()
            # if code is present, process it
            if code:
                self.get_tokens(code)

    """
    break up line of code into individual tokens
    identify tokens
    wrap each token in corresponding xml element
    send token and element tags a a new line in output file
    """

    def get_builtins_regex(self):
        """ build regular expression for tokenizing """

        regex = r''
        regex += fr"{'|'.join([re.escape(symbol) for symbol in jack_symbols_list])}"
        for keyword in jack_keywords_list:
            regex += fr"|{keyword}"

        return regex

    def get_tokens(self, code):
        """
        parse individual tokens from a string of code

        First: each regular expression must be 'custom' for the code string to
        be parsed, as it will contain potentially custom identifiers in
        addition to standard keywords.

        Second: use this constructed regular expression to split the code
        string into a lit of tokens.
        """

        # create regex of standard keywords and symbols
        builtins_pattern = re.compile(self.builtins_regex, flags=re.I | re.X)

        # get all non-keywords (i.e. identifiers, constants, and strings)
        other_tokens_present = []
        for token in re.split(builtins_pattern, code):
            token = token.strip()
            if token:
                if (token[0] == '"'):
                    other_tokens_present.append(re.escape(token.strip('"')))
                elif (token[0] == "'"):
                    other_tokens_present.append(re.escape(token.strip("'")))
                elif (' ' in token):
                    for sub_token in token.split(' '):
                        other_tokens_present.append(sub_token.strip())
                else:
                    other_tokens_present.append(token)

        # build custom regex pattern
        regex = self.builtins_regex
        if other_tokens_present:
            for token in other_tokens_present:
                regex += fr"|{token}"
        pattern = re.compile(regex, flags=re.I | re.X) #### THIS IS IGNORING WHITESPACE SO STRINGS DO NOT GET FOUND!!!!

        return re.findall(regex, code)

    def get_token_type(self, token):
        """ detects and returns token's lexical element type """

        if (token in jack_keywords_list):
            return 'KEYWORD'
        elif (token in jack_symbols_list):
            return 'SYMBOL'
        elif ():
            """
            floats can occur:
            - after their type, which is preceded by the var keyword
            - after the '=' symbol in an expression declared by the let keyword
            - after a number of symbols within expressions
            """
            return 'INT_CONST'
        elif (): # combo of letter numbers and underscore not starting with number
            """
            can be var, class, or subroutine name
            - var names must be declared at beginning of subroutine body, always
            follow their type, which is preceded by the var keyword
            - class names always follow the class keyword
            - subroutine names always follow their return type or the void
            keyword, which is always preceded by the subroutine's type keyword
            """

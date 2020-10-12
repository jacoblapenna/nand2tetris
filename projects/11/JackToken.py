#!/usr/bin/env python3

from SymbolTable import SymbolTable

class JackToken:

    def __init__(self, value, type, scope=None, catagory=None, defined=None, index=None):
        self.value = value
        self.type = type

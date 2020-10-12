#!/usr/bin/env python3

class SymbolTable:

    def __init__(self):
        self.class_scope = {}
        self.subroutine_scope = {}
        self.static_index = 0
        self.field_index = 0
        self.var_index = 0
        self.arg_index = 0

    def reset_subroutine_scope(self):
        self.subroutine_scope = {}
        self.var_index = 0
        self.arg_index = 0

    def handle_identifier(self, tokens):

        values = [token.value for token in tokens]
        class_scope_declaration_keywords = ["static", "field"]
        subroutine_declaration_keywords = ["method", "function", "constructor"]
        subroutine_scope_declaration_keywords = ["var"]

        if values[0] in class_scope_declaration_keywords:
            self._handle_class_scope_declarations(values, tokens)
        elif values[0] in subroutine_declaration_keywords:
            self.reset_subroutine_scope()
            self._handle_subroutine_declarations(values, tokens)
        elif values[0] in subroutine_scope_declaration_keywords:
            self._handle_subroutine_scope_declarations(values, tokens)
        else:
            # deal with identifiers being used rather than declared
            pass

    def _handle_class_scope_declarations(self, values, tokens):

        if values[0] == "static":
            category = "STATIC"
            type = values[1]
            for token in tokens[2::]:
                if token.type == "identifier":
                    if not token.value in self.class_scope.keys():
                        self.class_scope[token.value] = {
                            "category" : category,
                            "type" : type,
                            "declared" : True,
                            "used" : False,
                            "index" : self.static_index
                        }
                        self.static_index += 1

        if values[0] == "field":
            category = "FIELD"
            type = values[1]
            for token in tokens[2::]:
                if token.type == "identifier":
                    if not token.value in self.class_scope.keys():
                        self.class_scope[token.value] = {
                            "category" : category,
                            "type" : type,
                            "declared" : True,
                            "used" : False,
                            "index" : self.field_index
                        }
                        self.field_index += 1

    def _handle_subroutine_declarations(self, values, tokens):

        arguments = values[values.index('(') + 1:values.index(')')]

        if arguments:
            types = arguments[::3]
            names = arguments[1::3]

            for i, name in enumerate(names):
                category = "ARG"
                type = types[i]
                if not name in self.subroutine_scope.keys():
                    self.subroutine_scope[name] = {
                        "category" : category,
                        "type" : type,
                        "declared" : True,
                        "used" : False,
                        "index" : self.arg_index
                    }
                    self.arg_index += 1

    def _handle_subroutine_scope_declarations(self, values, tokens):

        category = "VAR"
        type = values[1]

        for token in tokens[2::]:
            if token.type == "identifier":
                if not token.value in self.subroutine_scope.keys():
                    self.subroutine_scope[token.value] = {
                        "category" : category,
                        "type" : type,
                        "declared" : True,
                        "used" : False,
                        "index" : self.var_index
                    }
                    self.var_index += 1

    # function to count kind of vars in SymbolTable

    # function to return the identifier's kind

    # function to return the identifier's type

    # function to return the identifier's index

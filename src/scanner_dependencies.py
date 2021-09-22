import re

integers_number = re.compile(r'^\d$')
variables = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*$')

strings = re.compile(r'["][\w\s]+["]')

def read_file():
    with open("../materials/input_code.txt", "r") as f:
        return [line for line in f]

def keyword_list():
    return [
        'for', 'if', 'else', 'input', 'print', 'break', 'while', 'var', 'continue'
    ]

def tokens_identifications():
    return [
        # OPERATORS ARITH#
        {
            '+' : 'PLUS' ,
            '-': 'MINUS' ,
            '*': 'MULTIPLY',
            '/': 'DIVIDE',
            '%': 'MODULE',
        },

        # OPERATORS RELATIONAL#
        {
            '<': 'LT',
            '>': 'GT',
            '<=': 'LTE',
            '>=': 'GTE',
            '==': 'DOUBLEEQUAL',
            '=': 'EQUAL',
        },

        # DELIMITER #
        {
            '(': 'LPAREN',
            ')': 'RPAREN',
            ':': 'TWOP',
        },

        #bool
        {
            '!=': 'NE',
            '&&': 'AND',
            '||': 'OR',
            '!': 'NOT',
        },

        {
            '#': 'COMMENT'
        },
    ]


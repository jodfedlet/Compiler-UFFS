import re

integers_number = re.compile(r'^\d$')
float_numbers = re.compile(r'^\d\.\d$')
variables = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*$')

def read_file():
    with open("../materials/input_code.txt", "r") as f:
        return [line for line in f]

def keyword_list():
    return [
        'for', 'while', 'if', 'else', 'func', 'return', 'input', 'print', 'break', 'while', 'var', 'continue'
    ]

def tokens_identifications():
    return [
        # OPERATORS #
        {
            '+' : 'PLUS' ,
            '-': 'MINUS' ,
            '*': 'MULTIPLY',
            '/': 'DIVIDE',
            '%': 'MODULE',
            '!': 'NOT',
            '=': 'EQUAL',
        },

        # COMPARATORS #
        {
            '<': 'LT',
            '>': 'GT',
            '<=': 'LTE',
            '>=': 'GTE',
            '==': 'DOUBLEEQUAL',
            '!=': 'NE',
            '&&': 'AND',
            '||': 'OR',
        },

        # BRACKETS #
        {
            '(': 'LPAREN',
            ')': 'RPAREN',
            '[': 'LBRACE',
            ']': 'RBRACE',
            '{': 'BLOCKSTART',
            '}': 'BLOCKEND',
        },

        {
            '#': 'COMMENT'
        }
    ]

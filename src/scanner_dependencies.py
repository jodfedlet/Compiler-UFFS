import re

integers_number = re.compile(r'^\d$')
float_numbers = re.compile(r'^\d\.\d$')
variables = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*$')

def read_file():
    all_lines = []
    with open("../materials/input.txt", "r") as f:
        for line in f:
            all_lines.append(line)
    return all_lines

def keyword_list():
    return [
        'auto','break','case','char','const','continue','default','do','else','enum','float','for','if','extern','double','int','long','register','return','short',
        'signed','sizeof','static','struct','switch','continue','typedef','union','unsigned','void','print'
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

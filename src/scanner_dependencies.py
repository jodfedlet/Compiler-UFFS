import re

integers_number = re.compile(r'^\d$')
variables = re.compile(r'^[_a-d]*$')
alfa = re.compile(r'^[a-zA-Z][a-zA-Z]*$')

def keyword_list():
    return [
        'if', 'else', 'print', 'while',
    ]

def token_delimiters():
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
            ':-': 'LT',
            '+:': 'GT',
            ':-=': 'LTE',
            '+:=': 'GTE',
            '==': 'DOUBLEEQUAL',
            '=': 'EQUAL',
            '!=': 'EQUAL',
        },

        # DELIMITER #
        {
            '(': 'LPAREN',
            ')': 'RPAREN',
            '{': 'LBRACK',
            '}': 'RBRACK',
        }
    ]

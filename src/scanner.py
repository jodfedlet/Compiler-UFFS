
import re
import keyword as kw

keyword_list = kw.kwlist

token_re_and_types = [

]

with open("../materials/input.txt", "r") as f:
    all_lines = f.readlines()

tokens_identifications = [
    # OPERATORS #
    {
        '+' : 'PLUS' ,
        '-': 'MINUS' ,
        '*': 'MULTIPLY',
        '/': 'DIVIDE',
        '%': 'MODULO',
        '~': 'NOT',
        '=': 'EQUALS',
    },


    # COMPARATORS #
    {
        '<': 'LT',
        '>': 'GT',
        '<=': 'LTE',
        '>=': 'GTE',
        '==': 'DOUBLEEQUAL',
        '!=': 'NE',
        '&': 'AND',
        '|': 'OR',
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
    },

    {
        ':': 'CHAR'
    },
]

integers_number = re.compile(r'^\d$')
float_numbers = re.compile(r'^\d\.\d$')
variables = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*')

tokens = []
for index, line in enumerate(all_lines):
    for token in line.split( ):
        know_token = ()
        has_error = False
        if integers_number.match(token):
            know_token = (token, "INT")
        elif float_numbers.match(token):
            know_token = (token, "FLOAT")
        elif variables.match(token):
            know_token = (token, "ID")
        elif token in tokens_identifications[0]:
            know_token = (token, "OP")
        elif token in tokens_identifications[1]:
            know_token = (token, "COMP")
        elif token in tokens_identifications[2]:
            know_token = (token, "BRACK")
        elif token in tokens_identifications[3]:
            know_token = (token, "COMMENT")
        elif token in tokens_identifications[4]:
            know_token = (token, "CHAR")
        else:
            has_error = True
            print(f"Token {token} is not valid at line: "+str(index+1))

        if know_token and not has_error:
            tokens.append(know_token)

print(tokens)

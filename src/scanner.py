
import re


keyword_list = [
'auto','break','case','char','const','continue','default','do','else','enum','float','for','if','extern','double','int','long','register','return','short',
'signed','sizeof','static','struct','switch','continue','typedef','union','unsigned','void','volatile'
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
        known_token = ()
        has_error = False
        if integers_number.match(token):
            known_token = (token, "INT")
        elif float_numbers.match(token):
            known_token = (token, "FLOAT")
        elif variables.match(token):
            if token in keyword_list:
                know_token = (token, "keyword")
            else:
                know_token = (token, "ID")
        elif token in tokens_identifications[0]:
            known_token = (token, "OP")
        elif token in tokens_identifications[1]:
            known_token = (token, "COMP")
        elif token in tokens_identifications[2]:
            known_token = (token, "BRACK")
        elif token in tokens_identifications[3]:
            know_token = (token, "COMMENT")
        elif token in tokens_identifications[4]:
            known_token = (token, "CHAR")
        else:
            has_error = True
            print(f"Token {token} is not valid at line: "+str(index+1))

        if known_token and not has_error:
            tokens.append(known_token)

print(tokens)

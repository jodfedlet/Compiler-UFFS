
from scanner_dependencies import tokens_identifications, keyword_list, read_file,\
    integers_number, float_numbers, variables

def scanner():
    try:
        tokens = []
        tokens_identification = tokens_identifications()
        for index, line in enumerate(read_file()):
            token_line = []
            for token in line.split( ):
                known_token = ()
                has_error = False
                if integers_number.match(token):
                    known_token = (token, "Num(INT)")
                elif float_numbers.match(token):
                    known_token = (token, "Num(FL)")
                elif variables.match(token):
                    if token in keyword_list():
                        known_token = (token, "keyword")
                    else:
                        known_token = (token, "ID")
                elif token in tokens_identification[0]:
                    known_token = (token, f"OP({tokens_identification[0][token]})")
                elif token in tokens_identification[1]:
                    known_token = (token, f"COMP({tokens_identification[1][token]})")
                elif token in tokens_identification[2]:
                    known_token = (token, f"BRACK({tokens_identification[2][token]})")
                elif token in tokens_identification[3]:
                    known_token = (token, "COMMENT")
                else:
                    has_error = True
                    print(f"Token {token} at line: {str(index+1)} is not valid")

                if known_token and not has_error and known_token not in tokens:
                    token_line.append(known_token)
            tokens.append(token_line)
        return tokens
    except Exception as e:
        print('Something get wrong, retry -->'+ str(e))

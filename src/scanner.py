
from scanner_dependencies import tokens_identifications, keyword_list, read_file,\
    integers_number, float_numbers, variables

def scanner():
    try:
        table_symbols = []
        tokens_identification = tokens_identifications()
        for index, line in enumerate(read_file()):
            token_line = []
            current_line = str(index+1)
            for token in line.split( ):
                if integers_number.match(token):
                    known_token = {"Label":token,"Type":"Num(INT)","Line":current_line}
                elif float_numbers.match(token):
                    known_token = {"Label": token, "Type": "Num(FL)", "Line": current_line}
                elif variables.match(token):
                    if token in keyword_list():
                        known_token = {"Label": token, "Type": "keyword", "Line": current_line}
                    else:
                        known_token = {"Label": token, "Type": "Id", "Line": current_line}
                elif token in tokens_identification[0]:
                    known_token = {"Label": token, "Type": f"OP({tokens_identification[0][token]})", "Line": current_line}
                elif token in tokens_identification[1]:
                    known_token = {"Label": token, "Type": f"COMP({tokens_identification[1][token]})", "Line": current_line}
                elif token in tokens_identification[2]:
                    known_token = {"Label": token, "Type": f"BRACK({tokens_identification[2][token]})", "Line": current_line}
                elif token in tokens_identification[3]:
                    known_token = {"Label": token, "Type": "COMMENT", "Line": current_line}
                else:
                    known_token = {"Label": token, "Type": "Error", "Line": current_line}
                    print(f"Token {token} at line: {current_line} is not valid")

                if known_token:
                    token_line.append(known_token)
            end_of_line = {"Label": "$", "Type": "EOF", "Line": current_line}
            token_line.append(end_of_line)
            table_symbols.append(token_line)
        return table_symbols
    except Exception as e:
        print('Something get wrong, retry -->'+ str(e))

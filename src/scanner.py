import json
from scanner_dependencies import tokens_identifications, keyword_list, read_file,\
    integers_number, variables

def write_tables_of_symbles_as_json(table_symbols):
    f = open("../materials/table_of_symbols.json", "w")
    json.dump(table_symbols, f, indent=5, sort_keys=True)
    f.close()

def scanner():
    try:
        table_symbols = []
        tokens_identification = tokens_identifications()
        has_error = False
        last_line = 0
        for index, line in enumerate(read_file()):
            token_line = []
            current_line = str(index+1)
            if not line.startswith("#"):
                for token in line.split( ):
                    if integers_number.match(token):
                        known_token = {"Label":token,"Type":"Number","Line":current_line}
                    elif variables.match(token):
                        if token in keyword_list():
                            known_token = {"Label": token, "Type": "keyword", "Line": current_line}
                        else:
                            known_token = {"Label": token, "Type": "Id", "Line": current_line}
                    elif token in tokens_identification[0]:
                        known_token = {"Label": token, "Type": f"ARITH({tokens_identification[0][token]})", "Line": current_line}
                    elif token in tokens_identification[1]:
                        known_token = {"Label": token, "Type": f"RELAT({tokens_identification[1][token]})", "Line": current_line}
                    elif token in tokens_identification[2]:
                        known_token = {"Label": token, "Type": f"DELIM({tokens_identification[2][token]})", "Line": current_line}
                    elif token in tokens_identification[3]:
                        known_token = {"Label": token, "Type": f"BOOL({tokens_identification[3][token]})", "Line": current_line}
                    elif token in tokens_identification[4]:
                        known_token = {"Label": token, "Type": "COMMENT", "Line": current_line}
                    else:
                        has_error = True
                        known_token = {"Label": token, "Type": "Error", "Line": current_line}
                        print(f"Token {token} at line: {current_line} is not valid")

                    if known_token:
                        token_line.append(known_token)
                table_symbols.append(token_line)
            last_line = index
        table_symbols.append([{"Label": "$", "Type": "EOF", "Line": last_line}])
        if has_error:
            exit()
        write_tables_of_symbles_as_json(table_symbols)
        return table_symbols

    except Exception as e:
        print('Something get wrong, retry -->'+ str(e))

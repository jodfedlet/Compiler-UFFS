import json
from scanner_dependencies import tokens_identifications, keyword_list, read_file,\
    integers_number, variables, strings

from automata import main_automata, afd

token_to_state = {}

def write_tables_of_symbles_as_json(table_symbols):
    f = open("../materials/table_of_symbols.json", "w")
    json.dump(table_symbols, f, indent=5, sort_keys=True)
    f.close()

def get_final_states():
    return [state for state, value in afd.items() if "*" in value.keys()]


def verify_token(token):
    state = 0
    for char in token:
        try:
            state = afd[state][char]
        except KeyError:
            return -1, ""

    return ''.join(state)

def record_on_table(word, line, token_line):
    state = verify_token(word)
    token_line.append({"state": state, "token": word, "value": word, "line": line})
    print(token_line)
    exit()

def addState():
    f = open("automata.json", "r")
    automata = json.load(f)
    f.close()
    for state in automata:
       # try:
       print("automata.json")
       #print(automata[state])
       #token_to_state.setdefault(automata[state]["is_terminal"], state)
        # except KeyError:
        #     continue

    #print(token_to_state)
    exit()

def scanner():
    final_states = get_final_states()
    #dict_val =[vet for vet in [a for a in afd.values()]]

   # print(dict_val)
    #print(dict_val_w)
    #exit()
    #try:
    table_symbols = []
    tokens_identification = tokens_identifications()
    has_error = False
    last_line = 0
    state = 0
    for index, line in enumerate(read_file()):
        token_line = []
        current_line = str(index+1)
        if not line.startswith("#"):
            for token in line.split( ):
                if integers_number.match(token):
                    #TODO continuar com os estados
                    # if state in final_states:
                    #     print(state)
                    known_token = {"Label":token,"Type":"Number","Line":current_line}
                    known_token = record_on_table(token, current_line, token_line)
                    # print(known_token)
                    # exit()
                elif strings.match(token):
                    known_token = {"Label": token, "Type": "String", "Line": current_line}
                elif variables.match(token):
                    if token in keyword_list():
                        known_token = {"Label": token, "Type": "keyword", "Line": current_line}
                    else:
                        record_on_table(token, current_line, token_line)
                       # known_token = {"Label": token, "Type": "Id", "Line": current_line}
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

    # except Exception as e:
    #     print('Something get wrong, retry -->'+ str(e))

main_automata()
output_file = open("automata.json", "w", encoding="utf-8")
json.dump(afd, output_file, indent=2, sort_keys=True)
output_file.close()
scanner()

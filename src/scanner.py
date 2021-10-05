import json
from scanner_dependencies import tokens_identifications, keyword_list, read_file,\
    integers_number, variables, strings

from automata import main_automata, afd

def write_tables_of_symbles_as_json(table_symbols):
    f = open("../materials/table_of_symbols.json", "w")
    json.dump(table_symbols, f, indent=5, sort_keys=True)
    f.close()

def get_final_states():
    return [state for state, value in afd.items() if "*" in value.keys()]


def get_state(token):
    #print("Token: "+token)
    current_state = 0
    all_states = list(afd.keys())
    
    for char in token:
        #print("Char: "+char)
        try:
            found = False
            for a, valores in afd.items():
                for j in valores:
                    if char == j:
                        found = True
                        current_state = valores[j]
                        break 
                if found: break 
                else: current_state = -1
        except KeyError:
            return -1
        
    #current_state = all_states[all_states.index(current_state) + 1]    

    if isinstance(current_state, list):
        return ' '.join(str(etat) for etat in current_state)
    return current_state

def add_token_in_token_line(word, line, token_line, tk_type, ribbon):
    final_states = get_final_states()
    state = get_state(word)
    token_line.append({"state": state, "token": word, "type": tk_type,  "line": line})
    if int(state) in final_states:
        ribbon.append({"state": state, "token": word, "line": line})
    return (token_line, ribbon)

def scanner():
    table_symbols = []
    tokens_identification = tokens_identifications()
    has_error = False
    count_line = 0
    #state = 0
    fita = []
    for index, line in enumerate(read_file()):
        token_line = []
        current_line = str(index+1)
        if line != "\n":
            count_line += 1
            
        if not line.startswith("#"):
            for token in line.split( ):
                token_type = "";
                if integers_number.match(token):
                    token_type = "Number"
                elif strings.match(token):
                    token_type = "String"
                elif variables.match(token):
                    if token in keyword_list():
                        token_type = "Keyword"
                    else:
                        token_type = "Id"
                elif token in tokens_identification[0]:
                    token_type = f"ARITH({tokens_identification[0][token]})"
                elif token in tokens_identification[1]:
                    token_type = f"RELAT({tokens_identification[1][token]})"
                elif token in tokens_identification[2]:
                    token_type = f"DELIM({tokens_identification[2][token]})"
                elif token in tokens_identification[3]:
                    token_type = f"BOOL({tokens_identification[3][token]})"
                elif token in tokens_identification[4]:
                    token_type = "COMMENT"
                else:
                    has_error = True
                    token_line.append({"state": -1, "token": token, "type": "Error",  "line": current_line})
                    print(f"(Lexic error) --> Token {token} at line: {current_line} is not valid")
                if not has_error and token not in table_symbols:  
                    token_line, ribbon = add_token_in_token_line(token, current_line, token_line,token_type, fita)
                    if ribbon:
                        fita.append(ribbon)   
            table_symbols.append(token_line)
    table_symbols.append([{"state": -1, "token": "$", "type": "EOF",  "line": current_line+1}])
    print(table_symbols)
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

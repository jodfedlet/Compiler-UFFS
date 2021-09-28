import json
from scanner_dependencies import tokens_identifications, keyword_list, read_file,\
    integers_number, variables, strings

from automata import main_automata, afd

token_to_state = {}
current_state = 0
def write_tables_of_symbles_as_json(table_symbols):
    f = open("../materials/table_of_symbols.json", "w")
    json.dump(table_symbols, f, indent=5, sort_keys=True)
    f.close()

def get_final_states():
    return [state for state, value in afd.items() if "*" in value.keys()]


def get_state(token):
    #print("Token: "+token)
    global current_state
    all_states = list(afd.keys())
    final_states = get_final_states()
    for char in token:
        #print("Char: "+char)
        try:
            print("Antes do: "+str(char))
            print(current_state)
            print(final_states)
            # if current_state in final_states:
            #     print("Aqui: "+str(char))
            current_state = afd[current_state][char]
            # else:
            #    current_state = all_states[all_states.index(current_state) + 1]  
            # print(state) 
            #print("Depois do: "+str(char)) 
        except KeyError:
            return [-1]
    
    #current_state = current_state.replace("[","").replace("]","")
    #print(current_state)
    #TODO fix TypeError: unhashable type: 'list' and return state by token
    try:
        iter(current_state)    
        return ' '.join(str(etat) for etat in current_state)
    except:
        return current_state
    #return ' '.join(str(etat) for etat in list(current_state))

def add_token_in_token_line(word, line, token_line, tk_type):
    token_line.append({"state": get_state(word), "token": word, "type": tk_type,  "line": line})
    return token_line

def scanner():
    table_symbols = []
    tokens_identification = tokens_identifications()
    has_error = False
    last_line = 0
    #state = 0
    for index, line in enumerate(read_file()):
        token_line = []
        current_line = str(index+1)
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
                    print(f"Token {token} at line: {current_line} is not valid")
                if not has_error and token not in table_symbols:  
                    token_line = add_token_in_token_line(token, current_line, token_line,token_type)
                    print(token_line)
                
                # if token_line:
                #     token_line.append(known_token)      
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

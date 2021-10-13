import json
from scanner import scanner
import xml.etree.ElementTree as ET


def parser(table_symb, fitas):
    tree = ET.parse('../materials/lalr_table.xml')
    root = tree.getroot()

    symbols = [ {'Name':s.get('Name'), 'Index':s.get('Index'), 'Type':s.get('Type')} for s in root.iter('Symbol')]  
    productions = [ {'Index':s.get('Index'), 'SymbolCount':s.get('SymbolCount'), 'NonTerminalIndex':s.get('NonTerminalIndex')} for s in root.iter('Production')]    
    
    lalr_table = []
    for lalr_state in root.iter('LALRState'):
        lalr_table.append({})
        for lalr_action in lalr_state:
            lalr_table[int(lalr_state.get('Index'))][lalr_action.get('SymbolIndex')] = {'Action':lalr_action.get('Action'), 'Value':lalr_action.get('Value')}
    
    # print(lalr_table)

    stack = [0]
    while True:
        current_line = 0
        
        # print(fita[0])
        # exit()
        #print(lalr_table[int(stack[0])][fita[0]])
        exit()
        try:
            action = lalr_table[int(stack[0])][fita[-1]]
        except:
            for val in table_symb[current_line]:
                print(f"(Syntax error): linha {val['line']}, sentença {val['token']} não reconhecida!")
                break
            break

       
        
        # for action in lalr_table:
        #     print(action)
        #     break
        # break
       ## action = lalr_table[last]
        print(action)
        exit()
              
        
        

table, fita = scanner()
parser(table, fita)
#res_parser = parser(scanner())


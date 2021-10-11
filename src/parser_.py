import json
from scanner import scanner
import xml.etree.ElementTree as ET


def parser():
    tree = ET.parse('../materials/lalr_table.xml')
    root = tree.getroot()

    symbols = [ {'Name':s.get('Name'), 'Index':s.get('Index'), 'Type':s.get('Type')} for s in root.iter('Symbol')]  
    productions = [ {'Index':s.get('Index'), 'SymbolCount':s.get('SymbolCount'), 'NonTerminalIndex':s.get('NonTerminalIndex')} for s in root.iter('Production')]    
    
    print(productions)



scanner()
parser()
#res_parser = parser(scanner())


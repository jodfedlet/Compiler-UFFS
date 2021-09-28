'''Copyright
 Este arquivo é de terceiro(eassisv) modificado conforme a minha necessidade
'''
from re import findall as find, I

afd = {}
alfabeto = []
gramatica = []

def eliminarInalcancaveis(afnd):
    visitados = set()
    def elimina(regra, estado):        # Utiliza uma dfs para remover recursivamente
        if estado in visitados:
            return
        visitados.add(estado)
        for chave in regra.keys():
            if chave == '*':
                continue
            for i in regra[chave]:
                elimina(afnd[i], i)

    elimina(afnd[0], 0)
    x = len(afnd)
    for i in range(x):
        if i not in visitados:      # Após a dfs estados não visitados são eliminados
            del afnd[i]

def eliminarInuteis(afnd):
    visitados = set()
    uteis = set()
    for rg in afnd:
        if '*' in afnd[rg].keys():
            uteis.add(rg)
    def elimina(regra, nRegra):     # Utiliza uma dfs para encontrar os estados inuteis
        if nRegra in uteis:
            return True
        visitados.add(nRegra)
        for chave in regra.keys():
            for rg in regra[chave]:
                if rg not in visitados:
                    if elimina(afnd[rg], rg):
                        return True
        return False

    aux = list(afnd.keys())
    for regra in aux:
        if elimina(afnd[regra], regra):
            uteis.add(regra)
        visitados = set()
    for regra in aux:
        if regra not in uteis:      # Após a dfs estados que não estão em uteis são eliminados
            del afnd[regra]
    for regra in afnd.keys():       # Transições para estados não uteis também são eliminados
        aux = list(afnd[regra].keys())
        for chave in aux:
            if chave == '*':
                continue
            for rg in afnd[regra][chave]:
                if rg not in uteis:
                    del afnd[regra][chave]

def eliminarEpsilonTransicoes(afnd):
    epsilon = []
    for chave in afnd.keys():
        if '&' in afnd[chave]:
            epsilon.append(chave)
    def copiarRegras(regras, nRegra):      # Recursivamente copia regras que são acessadas por uma epsilon transição
        if nRegra not in epsilon:
            return    #Caso não tenha epsilon transições na regra
        epsilon.remove(nRegra)
        for regra in regras['&']:
            chaves = afnd[regra].keys()
            if '&' in chaves:
                copiarRegras(afnd[regra], regra)
                regras['&'] = unirListas(regras['&'], afnd[regra]['&'])
        afnd[nRegra] = unirEstados(afnd, regras['&'] + [nRegra])

    epAux = epsilon.copy()
    for ep in epAux:
        copiarRegras(afnd[ep], ep)
    for ep in epAux:
        del afnd[ep]['&']

def determinizar(afnd):
    mpRgs = {}
    visitados = set()
    def determiniza(regra, nReg):       # Recursivamente determiniza o automato
        if nReg in visitados:
            return
        visitados.add(nReg)
        chaves = list(regra.keys())
        for chave in chaves:
            if len(regra[chave]) > 1:
                regra[chave].sort()
                nRg = str(regra[chave]) # É gerada uma nova regra que será mapeada no mpReg
                if nRg not in mpRgs.keys():
                    nEst = len(afnd)    # Novo estado que será mapeado pela variavel nRg
                    mpRgs.update({nRg: nEst})
                    afnd.update({len(afnd): unirEstados(afnd, regra[chave])})
                    determiniza(afnd[nEst], nEst)
                regra.update({chave: [mpRgs[nRg]]})
    i, t = 0, len(afnd)
    while i < t:
        determiniza(afnd[i], i)
        i, t = i + 1, len(afnd)    # Cada nova regra criada também deve ser determinizada

def unirEstados(automato, estados):
    # É feita a união de todos os estados do automato que estão na lista estados
    final = {}

    def une(estado):
        for e in estado:
            if e in final:
                final[e] = unirListas(final[e], estado[e])
            else:
                final.update({e: estado[e]})

    for estado in estados:
        une(automato[estado])
    return final

def unirListas(l1, l2):
    return l1 + list(set(l2) - set(l1))

def unirAutomatos(afd, aTemp):
    mpEst = {x: x + len(afd) for x in range(len(aTemp))}
    aux = []

    if '&' in afd[0].keys():  # É criado uma nova regra S' que leva a regra S por epsilon transição
        afd[0]['&'].append(mpEst[0])
    else:
        afd[0].update({'&': [mpEst[0]]})
    for chave in aTemp.keys():
        for ch in aTemp[chave].keys():
            if ch == '*':
                continue
            aux = []
            for i in aTemp[chave][ch]:
                aux.append(mpEst[i])
            aTemp[chave][ch] = aux
    for chave in aTemp.keys():
        afd.update({mpEst[chave]: aTemp[chave]})

def exibirAutomatoDeterministico(afnd, alfabeto):
    alfabeto.sort()
    print('     {}'.format('-----' * len(alfabeto)))
    print('     |', end='')
    for i in alfabeto:
        print('  {:2}|'.format(i), end='')
    print('\n     {}'.format('-----' * len(alfabeto)))
    for i in afnd.keys():
        if '*' in afnd[i].keys():
            print('*', end='')
        else:
            print(' ', end='')
        print('{:3}:|'.format(i), end='')
        for j in alfabeto:
            if j in afnd[i].keys():
                print(' {:2} |'.format(afnd[i][j][0]), end='')
            else:
                print(' {:2} |'.format('-'), end='')
        print('')
    print('     {}'.format('-----'*len(alfabeto)))

def gerarAfndToken(afnd, token, alfabeto):
    if not afnd:
        afnd.update({len(afnd): {}})
    tkInicial = True
    for tk in token:
        if tk not in alfabeto:
            alfabeto.append(tk)
        if tkInicial:   # Token inicial vai para o primeiro estado do automato
            mp = afnd[0]
            if tk in mp.keys():
                mp[tk].append(len(afnd))
            else:
                mp.update({tk : [len(afnd)]})
            tkInicial = False
        else:
            afnd.update({len(afnd) : {tk: [len(afnd) + 1]}})
    afnd.update({len(afnd) : {'*': [1]}})

def gerarAfndGramatica(afnd, gramatica, alfabeto):
    if not afnd:
        afnd.update({0: {}})
    aTemp = {}
    mpRgs = {}
    for regra in gramatica:
        simbolos = find(r'(\w*<\w+>|\w+|&)', regra)
        if simbolos[0] in mpRgs.keys():     # Verifica se a regra já foi criada e armazena no mapa de regras
            iRg = mpRgs[simbolos[0]]    # iRg armazena o índice da regra
        else:
            iRg = len(aTemp)
            aTemp.update({iRg : {}})
            mpRgs.update({simbolos[0]: iRg})
        for simbolo in simbolos[1:]:
            term = find(r'^\w+', simbolo)
            nTerm = find(r'<\w+>', simbolo)
            term = '&' if not term else term[0]
            if term not in alfabeto:
                alfabeto.append(term)
            if not nTerm:       # produção sem não terminal, gera uma regra terminal
                rg = aTemp[iRg]
                if term in rg.keys():
                    rg[term].append(len(aTemp))
                else:
                    rg.update({term : [len(aTemp)]})
                aTemp.update({len(aTemp): {'*':[1]}})
            else:
                nTerm = nTerm[0]
                if nTerm in mpRgs.keys():
                    rg = mpRgs[nTerm]
                else:
                    rg = len(aTemp)
                    mpRgs.update({nTerm: rg})
                    aTemp.update({rg: {}})
                mp = aTemp[iRg]
                if term in mp.keys():
                    mp[term].append(rg)
                else:
                    mp.update({term: [rg]})

    unirAutomatos(afnd, aTemp)

def read_input_automata():
    with open("./entrada.in", "r") as f:
        return [line for line in f]

def main_automata():
    files = read_input_automata()
    for line in files:
        if line.startswith("#") and len(line) > 3:
            continue
        elif not line.startswith("<"):
            if line.strip():
                gerarAfndToken(afd, line, alfabeto)
        elif line.startswith("<") and len(line) > 3:
            gramatica.append(line)
    if gramatica:
        gerarAfndGramatica(afd, gramatica, alfabeto)
        
    eliminarEpsilonTransicoes(afd)
    determinizar(afd)
    eliminarInalcancaveis(afd)
    eliminarInuteis(afd)
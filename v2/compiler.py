#Copyright
#Part of this project has been cloned from project(CleissonVieira) in order to generate the FDA

import xml.etree.ElementTree as ET
import re
import sys
sys.setrecursionlimit(3000)

#print(sys.getrecursionlimit())

class Producao():
    producao = 0
    visitado = False

    def __init__(self, producao):
       self.producao = producao
       self.visitado = False
       self.chegouEstadoTerminal = False

    def temProducao(self):
        return self.producao >= 0

class Automato(object):         #carga do automato finito

    FINAL = '$'     #identifica um estado final
    EPSILON = '#'   #identifica o símbolo épsilon
    Estados = dict()                #estados do autômato
    Alfabeto = set()                #símbolos do alfabeto
    Finais = set()                  #estados que são finais
    Texto = str()                   #string de entrada
    NovosEstados = dict()           #usada para identificar a origem das novas produções criadas na determinização
    TransicoesVisitadas = list()    #indicar quais transições já foram visitadas na busca em profundidade da remoção de inúteis
    AutomatoMinimizado = dict()     #guardar o automato ao final do processo de minimização

    def __init__(self):
        self.Estados = dict()       
        self.Alfabeto = set()       
        self.Finais = set()         
        self.NovosEstados = dict()
        self.AutomatoMinimizado = dict()

    def carregaToken(self, simbolo, new):       #inserção de Tokens da Linguagem
        self.Alfabeto.add(simbolo)              #adiciona os símbolos ao alfabeto

        if new:                                                                         #se novo token:
            if simbolo in self.Estados[0]:                                              #se já existir no estado:
                self.Estados[0][simbolo].append(len(self.Estados))                      #adiciona na lista de estados destinos daquele token
            else:                                                                       #se token não existir no estado:
                self.Estados[0].update({simbolo: [len(self.Estados)]})                  #adiciona nova entrada para o token
            self.Estados.update({len(self.Estados): {}})                                #cria um estado vazio para a próxima iteração
        if not new:                                                                      #se símbolo for de um token já existente:
            self.Estados[len(self.Estados) - 1].update({simbolo: [len(self.Estados)]})  #insere no último estado criado
            self.Estados.update({len(self.Estados): {}})                                #cria um estado vazio para a próxima iteração
    

    def carregaGramatica(self, textos):         #leitura das regras da Gramática Regular
        regras = dict()         #mapeamento das regras
        estados = dict()        #estados da gramática
        ignorar = [' ', ':']      

        def novaRegra(self, texto):     #insere uma nova regra no mapa de regras
            if texto == 'S':                #se identificador do estado for S:
                estados.update({0: {}})        #add no estado inicial                
                regras.update({'S': 0})        #mapeia

            else:                #senão
                numero = len(set(list(self.Estados) + list(estados)))           
                regras.update({texto: numero})           #insere a regra com o número                
                estados.update({regras[texto]: {}})      #mapeado para o número do último estado

        def novaTransicao(self, texto, regra):      #insere nova transição nas regras
            self.Alfabeto.add(texto)           #add símbolo no alfabeto

            if regra not in regras:            #se regra não foi mapeada cria nova
                novaRegra(self, regra)       

            if texto in estados[regraAtiva]:          #se símbolo já existe no estado:
                lista = list(set(estados[regraAtiva][texto] + [regras[regra]])) #add simbolo novo aos existentes
                estados[regraAtiva][texto] = lista                           

            else:               #senao add o símbolo no estado.
                estados[regraAtiva].update({texto: [regras[regra]]})   

        for linha in textos:        #percorre as linhas do texto de entrada
            word = ''               #zera a palavra
            for caractere in linha:         #percorre os caracteres da linha
                if caractere in ignorar:        #se estiver na lista de ignorados
                    continue                    #vai para o próximo caracter

                word = word + caractere       #concatena a palavra com o caractere válido

                if re.match('<\S>', word) is not None:    #se a palavra tem o formato de um nome de regra
                    if word[1] not in regras:         #se não existe regra com esse nome
                        novaRegra(self, word[1])          #add a nova regra com esse nome
                    regraAtiva = regras[word[1]]          #marca a flag de regra ativa para add uma transição nessa regra
                    word = ''                                                  

                elif (re.match('\|\S<\S>', word) is not None or re.match('=\S<\S>', word) is not None):     #se palavra tem formato de uma transição             
                    novaTransicao(self, word[1], word[3])           #add uma nova transição à regra ativa
                    word = ''                                                

                elif (re.match('\|<\S>', word) is not None or re.match('=<\S>', word) is not None):     #se palavra tem formato de um nome de regra e está no meio da regra 
                    novaTransicao(self, self.EPSILON, word[2])      #add uma nova épsilon transição à regra ativa
                    word = ''                                                  

                elif ((word == '|' + self.FINAL) or (word == '=' + self.FINAL)):     #se encontrado um caractere que indica estado final: 
                     self.Finais.add(regraAtiva)         #marca a regra ativa como final.

            self.insereEstadosGramatica(estados)         #insere os estados nos estados do automato


    def insereEstadosGramatica(self, estados):      #inserção das regras no automato   
        for nome, estado in estados.items():                   #percore o estado temporario
            self.setAlfabetoEstado(estado)                     #coloca todos os símbolos do alfabeto em estado, até os que tem transição vazia
            for simbolo, transicoes in estado.items():         #percorre todos os itens/transições de estado
                if nome not in self.Estados:                   #se nome/número do estado não existe no automato
                    self.Estados.update({nome: {}})            #add o estado ao automato

                if simbolo in self.Estados[nome]:                               #se símbolo já existe no estado
                    lista = list(set(self.Estados[nome][simbolo] + transicoes)) #add as transições do estado temporário
                    self.Estados[nome][simbolo] = lista                         #junto às transições do estado do automato

                else:     
                    self.Estados[nome].update({simbolo: transicoes})      #senão add as novas transições no estado.


    def imprimir(self, mensagem, First = False):        #imprime o automato no terminal e no arquivo.txt
        self.imprimirTela(mensagem)            

    def imprimirTela(self, mensagem = ''):      #imprime automato deterministico
        # print(mensagem)                                             #mostra mensagem, para identificar o automato que se está imprimindo
        estados = self.pegarAutomato()                              #utiliza o estado minimiazdo se existir
        for nome, estado in sorted(estados.items()):                #PERCORRE CADA ESTADO(nome) com uma lista desse estado(estado)
            print(' *' if nome in self.Finais else '  ', end='')    #se NOME está em FINAIS, então *
            print(nome, end=' = ')                                  #imprime NOME/NUMERO do estado
            for simbolo, transicoes in estado.items():              #percorre cada estado    
                if len(transicoes) > 0:                             #se existir transições para símbolo
                    print(simbolo, transicoes, end=', ')            #imprime símbolo e lista de transições
            print('')        


    def setAlfabetoEstado(self, estado):    #em um estado é inserido todos os símbolos do alfabeto
        for simbolo in sorted(self.Alfabeto):   #percorre os símbolos do alfabeto da linguagem
            if simbolo not in estado:           #se não existir no estado:
                estado.update({simbolo: []})    #add o símbolo associado à uma lista vazia.


    def setAlfabeto(self):          #relacioana os estados com os símbolos do alfabeto
        estados = self.pegarAutomato()          #utiliza o estado minimizado se existir
        for nome, estado in estados.items():    #percorre estados
            self.setAlfabetoEstado(estado)      #relacioana o estado com os símbolos do alfabeto

    def carrega(self, arquivo):     #Insere no automato
        arquivo = open(arquivo, 'r')
        entrada = arquivo.read()                        #converte o arquivo para string
        new = True                                      #verificar se tem duas quebras de linha, significa que não tem mais tokens pra ler
        self.Estados.update({len(self.Estados): {}})    #inicializa o estado inicial com: um inteiro para chave e um dicionário vazio para conteúdo

        for simbolo in entrada:                         #percorre caractere a caractere na string da estrada
            simbolo = simbolo.lower()                   #pega todas as letras minusculas

            if simbolo == '\n':                         #verifica onde tem quebra de linha
                if new:                                 #com duas quebras de linha termina a leitura dos tokens
                    break                               
                new = True                              #verificar se ainda tem simbolos a serem lidos
                self.Finais.add(len(self.Estados) - 1)  #adiciona o simbolo final do token em um estado

            else:
                self.carregaToken(simbolo, new)         #carrega o token para o autômato.
                new = False                             #reseta a variável para o próximo símbolo

        texto = entrada.partition('\n\n')[2]            #separa o texto após as duas quebras de linha para a leitura de gramática
        self.carregaGramatica(texto.splitlines())       #envia o texto em formato de lista com as linhas do texto
        self.setAlfabeto()                              # Relaciona os estados com o alfabeto da linguagem


    def pegarAutomato(self):           #retorna automato mais atualizado existente
        if len(self.AutomatoMinimizado) > 0:    #se tamanho do dicionário de estados maior que 0 já existe um autômato minimizado
            return self.AutomatoMinimizado   
        else:                 #senão retorna o da estrutura original
            return self.Estados             

############################## Elimina Inuteis ##############################
class Inuteis(Automato):

    def __init__(self, automato):
        super(Inuteis, self).__init__()
        self.Estados = automato.Estados
        self.Alfabeto = automato.Alfabeto
        self.Finais = automato.Finais
        self.TransicoesVisitadas = automato.TransicoesVisitadas
        self.AutomatoMinimizado = automato.AutomatoMinimizado

    def gerarEstadosParaMinimizacao(self):
        estadosTemp = dict()
        AutomatoValido = self.pegarAutomato()

        for transicao in AutomatoValido:
            if (transicao in self.Finais) and (AutomatoValido[transicao] == {}):
                estadosTemp.update({transicao: {}})
                continue

            for producao in list(AutomatoValido[transicao]):
                if len(AutomatoValido[transicao][producao]) > 0:
                    if transicao not in estadosTemp: 
                        estadosTemp.update({transicao: {producao: Producao(AutomatoValido[transicao][producao][0])}})
                    else:
                        if producao not in estadosTemp[transicao]:
                            estadosTemp[transicao].update({producao: Producao(AutomatoValido[transicao][producao][0])})
                else:                    
                    if ((transicao in estadosTemp) and (producao not in estadosTemp[transicao])):
                        estadosTemp[transicao].update({producao: Producao(-1)})
                    elif transicao in self.Finais:
                        estadosTemp.update({transicao: {producao: Producao(-1)}})

        return estadosTemp

    def adicionaAutomatoMinimizado(self,transicao,producaoAtual,producaoInserir):
        if producaoAtual == -1:
            if transicao not in self.AutomatoMinimizado:
                self.AutomatoMinimizado.update({transicao: {}})
        else:
            if transicao not in self.AutomatoMinimizado:
                self.AutomatoMinimizado.update({transicao: {producaoAtual: [producaoInserir]}})
            else:
                if producaoAtual not in self.AutomatoMinimizado[transicao]:
                    self.AutomatoMinimizado[transicao].update({producaoAtual: [producaoInserir]})



############################## Organiza o automato para realizar as operacoes das classes abaixo ##############################
automato = Automato()                           
automato.carrega('./config/entrada.txt')                      
# automato.imprimir('\n\n# AUTOMATO LIDO:\n', True)  


############################## Elimina Epsilon Transição ##############################
class EpsilonTransicao(Automato):
    
    def __init__(self, automato):
        super(EpsilonTransicao, self).__init__()

        self.Estados = automato.Estados
        self.Alfabeto = automato.Alfabeto
        self.Finais = automato.Finais

    def eliminarEpsilonTransicoes(self):
        self.buscarEpsilonTransicoes() 

    def buscarEpsilonTransicoes(self):        
        if super().EPSILON not in self.Alfabeto:
            return

        producoesComEpsilon = set()
        qtdEpsilon = len(producoesComEpsilon)
        qtdEstados = len(self.Estados) 
        idxEpsilon = self.Alfabeto
        i = 0

        while i < qtdEstados:   #percorre os estados
            if i in self.Estados and len(self.Estados[i][super().EPSILON]) > 0:   #verifica se tem epsilon
                self.removerEpsilonTransicoes(i, self.Estados[i][super().EPSILON][0], producoesComEpsilon)
                qtdEstados = len(self.Estados)                        #atualiza qtd de estados
            i += 1

        self.removerEpsilonTransicoesEstados()

    def removerEpsilonTransicoes(self, transicaoOriginal, transicaoEpsilon, producoesComEpsilon):
        if len(self.Estados[transicaoOriginal][self.EPSILON]) > 0:

            for producao in list(self.Estados[transicaoEpsilon]):
                if producao != self.EPSILON and len(self.Estados[transicaoEpsilon][producao]) > 0:                    
                    self.Estados[transicaoEpsilon][producao] = (list(set(self.Estados[transicaoEpsilon][producao] + self.Estados[transicaoOriginal][producao])))                    
                    producoesComEpsilon.update(set(self.Estados[transicaoOriginal][self.EPSILON]))                    
        
        if len(self.Estados[transicaoEpsilon][self.EPSILON]) > 0:            
            if self.Estados[transicaoEpsilon][self.EPSILON][0] not in producoesComEpsilon:
                self.removerEpsilonTransicoes(transicaoEpsilon, self.Estados[transicaoEpsilon][self.EPSILON][0], producoesComEpsilon)

    def removerEpsilonTransicoesEstados(self):
        if self.EPSILON not in self.Alfabeto:
            return

        qtdEstados = len(self.Estados) 
        i = 0
        while i < qtdEstados:            #percorre estados
            if i in self.Estados:            #verifica transição com epsilon
                self.Estados[i].pop(self.EPSILON)    #remove prod do ep
                qtdEstados = len(self.Estados)       #atualiza qtd estados
            i += 1

        self.Alfabeto.remove(self.EPSILON)

livreEpsilon = EpsilonTransicao(automato)           
livreEpsilon.eliminarEpsilonTransicoes()      #busca e trata a epsilon                         

############################## Determiniza ##############################
class Determinizacao(Automato):
    def __init__(self, automato):
        super(Determinizacao, self).__init__()

        self.Estados = automato.Estados
        self.Alfabeto = automato.Alfabeto
        self.Finais = automato.Finais

    def determinizar(self):     #inicia a determinização
        self.buscarIndeterminismo() #busca indeterminismos

    def adicionaEstadoFinal(self, producoes, novaProducao): #add nova prod ao conjunto de estados finais
        for producao in producoes:          
            if producao in self.Finais:         #se é producão final
                self.Finais.add(novaProducao)   #add nova prod ao conjunto de finais

    def substituiNovaProducao(self):        #substitui um indeterminismo por string concatenando as transições
        if len(self.NovosEstados) > 0:                  #criadas novas prod na determinização
            for estado in self.Estados:                 #percorre estado do automato
                for simbolo in sorted(self.Alfabeto):          #percorre símbolos do alfabeto
                    if len(self.Estados[estado][simbolo]) > 1:       #se qtd de transições por uma prod for > 1
                        producaoAgrupada = self.geraProducaoAgrupada(self.Estados[estado][simbolo])     #gera uma prod agrupada para conhecer a origem da nova prod
                        if producaoAgrupada in self.NovosEstados:                                       #se essa prod estiver nas novas prod automato recebe a nova prod gerada
                            self.Estados[estado][simbolo] = [self.NovosEstados[producaoAgrupada][0]]    

    def buscarIndeterminismo(self):     #percorre o autômato tratando seus indeterminismos
        qtdEstados = len(self.Estados)   #marca a qtd inicial de estados
        i = 0              
        while i < qtdEstados:  
            for j in sorted(self.Alfabeto):     #percorre conjunto de símbolos do alfabeto
                if i in self.Estados and len(self.Estados[i][j]) > 1:       #se transição indeterminada:
                    self.determinizarProducao(self.Estados[i][j])           #determiniza  estado

                    qtdEstados = len(self.Estados)        #atualiza qtd de estados
            i += 1            

            if i == qtdEstados:     #se último estado
                for novoEstado in list(self.NovosEstados):          #percorre novas prod
                    if self.NovosEstados[novoEstado][0] not in self.Estados:            #se não estiver no conjunto de estados do automato
                        self.determinizarProducao(self.NovosEstados[novoEstado][1])     #determiniza
                        qtdEstados = len(self.Estados)      #atualiza qtd de estados                     

    def determinizarProducao(self, producoes):      #determiniza x estado do automato
        estadoTemporario = dict()
        producaoAgrupada = self.geraProducaoAgrupada(producoes)

        if ((producaoAgrupada not in self.NovosEstados) or (self.NovosEstados[producaoAgrupada][0] not in self.Estados)):  #se prod agrupada não existir nas novas prod ou nova regra não estiver no automato
            if (len(producoes) > 1) and (not self.existeProducaoAgrupada(producoes)):      #se tamanho for > 1 e não existe prod agrupada pra ela
                novoEstado = self.pegarNovoEstadoDetrminizacao()                              #pega o novo estado determinizado
                self.NovosEstados.update({self.geraProducaoAgrupada(producoes): [novoEstado,producoes]})    #coloca na estrutura de novos estados

            for i in producoes:             #percorre prod que contém indeterminação
                for j in sorted(self.Alfabeto):     #percorre conjunto de símbolos do alfabeto
                    if j in estadoTemporario:              #se símbolo j já estiver no estado temporário
                        lista = list(set(estadoTemporario[j] + self.pegarProducaoOriginal(self.Estados[i][j]))) #add a lista de transições de j
                        estadoTemporario[j] = lista        #ao estado criado

                        if (len(lista) > 1) and (not self.existeProducaoAgrupada(lista)):       #se largura da lista for > 1 e não existe prod agrupada pra ela
                            novoEstado = self.pegarNovoEstadoDetrminizacao()              #enumera novo estado
                            self.NovosEstados.update({self.geraProducaoAgrupada(lista): [novoEstado,lista]})    #add aos novos estados

                    else:        #se símbolo j não estiver no estado temporário
                        producaoAtual = list(set(self.Estados[i][j]))      #concatena as transições de j

                        if len(producaoAtual) > 1:           #se tiver mais de uma prod
                            producaoAgrupadaTemp = self.geraProducaoAgrupada(producaoAtual)                     #gera nova prod agrupada
                            if self.existeProducaoAgrupada(producaoAgrupadaTemp):                               #se essa prod já existe
                                estadoTemporario.update({j: list(set(self.NovosEstados[producaoAgrupada][1]))}) #atualiza o estado temporário

                        elif (len(producaoAtual) > 0) and (self.existeNovoEstado(producaoAtual[0])):     #se não se essa prod não for nula e existe um estado para essa transição
                            for prod in self.NovosEstados:              #percorre novos estados 
                                if self.NovosEstados[prod][0] == producaoAtual[0]:      #estado que for igual à transição
                                    estadoTemporario.update({j: list(set(self.NovosEstados[prod][1]))})      #atualiza
                        else:                                 
                            estadoTemporario.update({j: producaoAtual})    #add uma nova transição ao estado temporário

            self.setAlfabetoEstado(estadoTemporario);           #relaciona estado temporário com símbolos do alfabeto
            self.Estados.update({self.NovosEstados[producaoAgrupada][0]: estadoTemporario});     #add o estado temporário ao dict de estados da classe
            self.adicionaEstadoFinal(producoes, self.NovosEstados[producaoAgrupada][0])      #verifica se deve add aos estados finais
            self.substituiNovaProducao()     #verifica as prod criadas

    def geraProducaoAgrupada(self, lista):      #insere elementos de uma lista para uma string
        estado = ''
        for item in lista:      #para cada item da lista dada
            if estado == '':        #se for no inicio
                estado += str(item)     #concatena o item
            else:       #se for no meio
                estado += ',' + str(item)   #concatena com a virgula

        return estado                  

    def existeProducaoAgrupada(self, lista):        #verifica se lista dada já foi inserida em um estado novo
        retorno = False

        if len(lista) > 1:                                          #se o tamanho da lista dada for > 1
            producaoAgrupadaTemp = self.geraProducaoAgrupada(lista) #verifica pela sua possível prod agrupada
            return (producaoAgrupadaTemp in self.NovosEstados)
        else:         
            for i in self.NovosEstados:         #percorre os novos estados
                if lista[0] in self.NovosEstados[i][1]:       #verifica se a prod já existe
                    return True
        return retorno

    def pegarNovoEstadoDetrminizacao(self):     #add uma nova prod para contabilizar o novo tamanho do automato
        novasProducoes = []
        for producao in self.NovosEstados:      #pra cada prod dos novos estados
            novasProducoes.append(self.NovosEstados[producao][0])   #add um na contagem
        return len(set(list(self.Estados) + novasProducoes))     #retorna a qtd. Usa lista pra tratar repetições

    def pegarProducaoOriginal(self, producaoOrig):      #retorna a prod que está na lista de estados novos a partir de uma prod do automato
        retorno = list(set(producaoOrig))
        for producao in self.NovosEstados:
            for prod in producaoOrig:
                if self.NovosEstados[producao][0] == prod:
                    retorno = list(set(self.NovosEstados[producao][1]))

        return retorno

    def existeNovoEstado(self, producao):       #verifica se uma prod está no conjunto de novos estados
        if len(self.NovosEstados) > 0:
            for producaoAgrupada in self.NovosEstados:
                if self.NovosEstados[producaoAgrupada][0] == producao:
                    return True

        return False

determinizado = Determinizacao(automato) 
determinizado.determinizar()                   


############################## Elimina inalcançaveis ##############################
class Inalcancaveis(Inuteis):
    
    def __init__(self, automato):
        super(Inalcancaveis, self).__init__(automato)
          
    def removerInalcancaveis(self):
        estados = self.gerarEstadosParaMinimizacao()
        self.visitaNovaProducaoInalcancavel(estados, 0) #passa 0 fixo pois para remover os inalcançáveis parte do estado incial

    def visitaNovaProducaoInalcancavel(self, estados, transicao):
         if transicao in estados:
             if transicao in self.Finais:              #se a transição for um estado final
                 self.adicionaAutomatoMinimizado(transicao,-1,-1)        #add no automato pois pelo estado inicial o atual é alcançado

             for producao in estados[transicao]:                   #percorre todas as prod daquela transição e então segue com busca em profundidade
                if not estados[transicao][producao].temProducao():       #caso não tenha uma prod válida finaliza a recursão atual
                    continue
                if estados[transicao][producao].visitado:              #Se a prod já foi visitada finaliza a recursão atual
                    return
        
                estados[transicao][producao].visitado = True
                self.adicionaAutomatoMinimizado(transicao,producao,estados[transicao][producao].producao);  #add a prod no automato
                self.visitaNovaProducaoInalcancavel(estados, estados[transicao][producao].producao);     #busca recursivamente o estado final

semInalcancaveis = Inalcancaveis(automato)
semInalcancaveis.removerInalcancaveis()     


############################## Elimina mortos ##############################
class Mortos(Inuteis):
    
    def __init__(self, automato):
        super(Mortos, self).__init__(automato)
    
    def imprimir(self):
        return super().imprimir('#DETERMINIZADO, LIVRE DE EPSILON TRANSIÇÃO E LIVRE DE MORTOS E INALCANÇAVÉIS:\n')

    def removerMortos(self):
        estados = self.gerarEstadosParaMinimizacao()
        self.AutomatoMinimizado = dict()
        for transicao in estados:
            for producao in estados[transicao]:
                self.visitaNovaProducaoMortos(estados, transicao)
                estados[transicao][producao].chegouEstadoTerminal = self.adicionaAutomatoMinimizado(transicao,producao,estados[transicao][producao].producao)
    
    def visitaNovaProducaoMortos(self, estados, transicao):
        if transicao in estados:
            if (transicao in self.Finais) and (estados[transicao] == {}) :
                self.adicionaAutomatoMinimizado(transicao,-1,-1)
                return True

            for producao in estados[transicao]:
                if estados[transicao][producao].chegouEstadoTerminal or (transicao in self.Finais):
                    return True
                if not estados[transicao][producao].temProducao():      
                    return False
                if estados[transicao][producao].visitado:
                    continue
                
            estados[transicao][producao].visitado = True
            if self.visitaNovaProducaoMortos(estados, estados[transicao][producao].producao):
                estados[transicao][producao].chegouEstadoTerminal = True
                self.adicionaAutomatoMinimizado(transicao,producao,estados[transicao][producao].producao)
                return True

        return False

semMortos = Mortos(semInalcancaveis)      
semMortos.removerMortos()                 
#semMortos.imprimir()      #DEBUG AUTOMATO FINITO

############################## Analise Léxica / Sintática ##############################
class Analise(Inuteis):
    def __init__(self, automato):
        super(Analise, self).__init__(automato)
    
    def compiler(self):
        
        def scanner():
            automata = self.pegarAutomato()
            has_error = False
            symbols_table = []
            word = ''
            state = 0
            delimiters = set([" ","\n","\t"])
            for index, line in enumerate(list(open('./config/input_code.txt'))):
                current_line = str(index+1)
                column = 0
                for char in line:
                    if char in delimiters and word:
                        column += 1 
                        symbols_table.append({'Line': int(current_line), 'State': state, 'Label': word, 'Column': column})
                        state = 0
                        word = ' ' 
                    else: 
                        try:
                            state = automata[state][char][0]
                        except KeyError:
                            state = -1
                        if char != ' ':
                            word += char      
                            
            for error in symbols_table:
                if error['State'] == -1:
                    print(f"(LexicalError) --> Token {error['Label']} at line: {error['Line']} and {error['column']} is not valid")
                    has_error = True
            if has_error: exit()
            return symbols_table
        
        def parser(s_table):
            tree = ET.parse('./config/parser.xml')
            root = tree.getroot()

            symbols = [ {'Name':s.get('Name'), 'Index':s.get('Index'), 'Type':s.get('Type')} for s in root.iter('Symbol')]  
            productions = [ {'Index':s.get('Index'), 'SymbolCount':s.get('SymbolCount'), 'NonTerminalIndex':s.get('NonTerminalIndex')} for s in root.iter('Production')]    
            
            lalr_table = []
            for lalr_state in root.iter('LALRState'):
                lalr_table.append({})
                for lalr_action in lalr_state:
                    lalr_table[int(lalr_state.get('Index'))][lalr_action.get('SymbolIndex')] = {'Action':lalr_action.get('Action'), 'Value':lalr_action.get('Value')}
        
            def table_mapping():
                for symbol in symbols:
                    symbol_name = symbol['Name']
                    symbol_state = symbol['Index']
                    for x in s_table:
                        label_name = x['Label'].lstrip()
                        if label_name == symbol_name:
                            x['State'] = symbol_state 
                        elif len(label_name) > 0 and label_name[0] == '_' and symbol_name == '_ID':
                            x['State'] = symbol_state  
                      
                fita = [int(symb_['State']) for symb_ in s_table]    
                #fita.append(0) 
                return (s_table, fita)
           
            table, ribbon = table_mapping()
            table.append({"Line": "EOF", "State": "-1", "Label": "$"})
                      
            # print(table)
            # exit()          
            stack = [0]
            while True:
                #TODO finalizar reconhecimento de linguagem com if, print e gerar novo parser para as alterações da GR
                print('Fita: --> ' +str(ribbon))
                print('Fita[0]: --> ' +str(ribbon[0]))
                print('Stack: --> ' +str(stack))
                print('Stack[0]: --> ' +str(stack[0]))
                print(lalr_table[int(stack[0])])
                print()
                try:
                    action = lalr_table[int(stack[0])][str(ribbon[0])]
                except KeyError as e:
                    print("KeyError: -->"+str(e))
                    error = {"line": '' , "label": ''}
                    for tab in table:
                        if str(tab['State']) == str(e.args[0]):
                            error.update({"line": tab['Line'], "column": tab['Column'] , "label": tab['Label']})
                            break
                    print(f"(SyntaxError) --> Token {error['label']} at line: {error['line']} and column {error['column']} is not valid")
                    break
                
                current_action = int(action['Action'])
                if current_action == 1:
                    print('Shift')
                    stack.insert(0, ribbon[0])
                    stack.insert(0, action['Value'])
                    ribbon.pop(0)
                    
                elif current_action == 2:
                    print('Reduce')
                    prod = productions[int(action['Value'])]
                    countSymbol = int(prod['SymbolCount']) * 2
                    # print('Stack: --> ' +str(stack))
                    # print(countSymbol)
                    
                    for i in range(countSymbol): stack.pop(0)
                    
                    #print('Stack: --> ' +str(stack))    
                    goto = lalr_table[int(stack[1])][stack[0]]['Value']
                    stack.insert(0, prod['NonTerminalIndex'])
                    stack.insert(0, goto)
                    
                elif current_action == 3:
                    print('Action 3')
                    exit()
                    pass 
                
                elif current_action == 4:
                    print(action['Value'])
                    print('OK -> Accepted')
                    break
        parser(scanner())        
analise = Analise(semInalcancaveis)
analise.compiler()

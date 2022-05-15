from tkinter.messagebox import NO, RETRY
from wsgiref.validate import validator


class Variavel:
    INTEGER = 1
    BOLEANO = 2

    def __init__(self, nome, valor, tipo, lexval):
        self.nome = nome
        self.valor = valor
        self.tipo = tipo
        self.lexval = lexval

    def print(self):
        print("Variavel: " + str(self.nome) + ", Valor: " + str(self.valor) + ", Tipo: " + str(self.tipo) + ", Lexval: " + str(self.lexval))

    def to_string_tipo(self):
        if (self.tipo == Variavel.INTEGER):
            return 'inteiro'
        elif (self.tipo == Variavel.BOLEANO):
            return 'booleano'

    def get_tipo(tipo):
        if (tipo == 'inteiro'):
            return Variavel.INTEGER
        elif (tipo == 'booleano'):
            return Variavel.BOLEANO

    def set_valor(self, valor):
        self.valor = valor

class VariavelHash:
    def __init__(self):
        self.variaveis = []
    
    def add(self, varivel):
        self.variaveis.append(varivel)

    def print(self):
        print("========================= SEMANTICA ===========================")
        for variavel in self.variaveis:
            variavel.print()
        print("========================= X SEMANTICA X ===========================")

    def exists(self, nome):
        for i in range(len(self.variaveis)):
            if nome == self.variaveis[i].nome:
                return True

        return False

    def size(self):
        return len(self.variaveis)   

    def last(self):
        ultima = None
        for var in self.variaveis:
            ultima = var
        return ultima

    def lista_de_variaveis(self, nome):
        lista = []
        for i in range(len(self.variaveis)):
            if nome == self.variaveis[i].nome:
                lista.append(self.variaveis[i])

        return lista

    def ultima_declarada(self, nome):
        ultima = None
        for i in range(len(self.variaveis)):
            if (self.variaveis[i].nome == nome):
                ultima = self.variaveis[i]
        return ultima

    def ultima_mesmo_escopo(self, escopo, nome, funcoes=None):
        ultima = None
        dentro_de_funcao = False
        if(funcoes!=None):
            ultima_funcao = funcoes.last()
            if(ultima_funcao != None):
                escopo_funcao = ultima_funcao.lexval.escopo.split(':')
                escopo_desejado = escopo.split(':')
                if(escopo_funcao[:] == escopo_desejado[:len(escopo_funcao)] and len(escopo_desejado)>len(escopo_funcao)):
                    dentro_de_funcao = True

        for i in range(len(self.variaveis)):
            if (self.variaveis[i].nome == nome):
                variavel = self.variaveis[i]
                escopo_variavel = variavel.lexval.escopo.split(':')
                escopo_desejado = escopo.split(':')

                if(len(escopo_variavel) <= len(escopo_desejado)):
                    if(dentro_de_funcao and len(escopo_variavel) == 2 and len(escopo_desejado) > 2):
                        continue
                    if(escopo_variavel[:] == escopo_desejado[:len(escopo_variavel)]) or (len(escopo_desejado) == len(escopo_variavel) and escopo_variavel[0] == '1') or (len(escopo_desejado)-1 == len(escopo_variavel) and (escopo_variavel[:len(escopo_variavel)-1] == escopo_desejado[:len(escopo_variavel)-1])):
                        ultima = variavel

        return ultima

class Funcao:
    INTEGER = 1
    BOLEANO = 2
    VAZIO = 3

    NAO_ESCRITA = 1
    AGUARDANDO_FIM = 2
    ESCRITA = 3

    def __init__(self, nome, tipo, parametros, lexval, escrita=NAO_ESCRITA):
        self.nome = nome
        self.tipo = tipo
        self.parametros = parametros
        self.lexval = lexval
        self.escrita = escrita

    def print(self):
        print("Variavel: " + str(self.nome) + ", Tipo: " + str(self.tipo) + ", Parametros: " + str(self.parametros) + ", Lexval: " + str(self.lexval))

    def to_string_tipo(self):
        if (self.tipo == Funcao.INTEGER):
            return 'inteiro'
        elif (self.tipo == Funcao.BOLEANO):
            return 'booleano'
        elif (self.tipo == Funcao.VAZIO):
            return 'void'

        return None

    def get_tipo(tipo):
        if (tipo == 'inteiro'):
            return Funcao.INTEGER
        elif (tipo == 'booleano'):
            return Funcao.BOLEANO
        elif (tipo == 'vazio'):
            return Funcao.VAZIO

        return None

class FuncaoHash:
    def __init__(self):
        self.funcoes = {}
    
    def add(self, funcao):
        self.funcoes[funcao.nome] = funcao

    def print(self):
        print("========================= SEMANTICA ===========================")
        for i in self.funcoes:
            self.funcoes[i].print()
        print("========================= X SEMANTICA X ===========================")

    def exists(self, nome):
        return nome in self.funcoes

    def size(self):
        return len(self.funcoes)  

    def last(self):
        ultima = None
        for var in self.funcoes:
            ultima = self.funcoes[var]
        return ultima

    def get_funcao(self, nome):
        return self.funcoes[nome]

    def exists_procedimento(self, nome):
        if (not(nome in self.funcoes)):
            return False

        funcao = self.funcoes[nome]
        if funcao.tipo == Funcao.VAZIO:
            return True
        return False
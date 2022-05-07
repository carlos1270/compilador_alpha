from src.analise_semantica_classes import *
from src.Exceptions import *

def adicionar_variavel(variaveis, token, tipo, simbolo):
    variavel = None
    if tipo[0] == "inteiro":
        variavel = Variavel(token[0], None, Variavel.INTEGER, simbolo)
    elif tipo[0] == "booleano":
        variavel = Variavel(token[0], None, Variavel.BOLEANO, simbolo)

    variaveis.add(variavel)

def checar_comando_atribuicao_semantica(variaveis, token):
    checar_declaracao_semantica(variaveis, token)

def checar_declaracao_semantica(variaveis, token):
    if not variaveis.exists(token[0]):
        raise VariavelNaoDeclaradaException("Variável '" + token[0] + "' não declarada na linha " + token[1])

def mesmo_escopo(variaveis, simbolo):
    lista_de_variaveis_declaradas = variaveis.lista_de_variaveis(simbolo.identificador)
    escopo_adicionado = simbolo.escopo.split(':')

    for i in range(len(lista_de_variaveis_declaradas)):
        escopo = list(lista_de_variaveis_declaradas[i].lexval.escopo.split(':'))
        if(len(escopo_adicionado) <= len(escopo)):
            if(escopo_adicionado[:] == escopo[:len(escopo_adicionado)]):
                return True
        else:
            if escopo[0] == '1':
                return True

    
    return False 

def checar_ja_declarada(variaveis, token, simbolo):
    if variaveis.exists(token[0]) and mesmo_escopo(variaveis, simbolo):
        raise VariavelNaoDeclaradaException("Variável '" + token[0] + "' já declarada na linha " + token[1])

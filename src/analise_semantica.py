from src.analise_semantica_classes import *
from src.Exceptions import *

def adicionar_variavel(variaveis, token, tipo):
    variavel = None
    if tipo[0] == "inteiro":
        variavel = Variavel(token[0], None, Variavel.INTEGER, token)
    elif tipo[0] == "booleano":
        variavel = Variavel(token[0], None, Variavel.BOLEANO, token)

    variaveis.add(variavel)

def checar_declaracao(variaveis, token):
    if not variaveis.exists(token[0]):
        raise VariavelNaoDeclaradaException("Variável '" + token[0] + "' não declarada na linha " + token[1])

def mesmo_escopo():
    """  """

def checar_ja_declarada(variaveis, token, tipo):
    if variaveis.exists(token[0]) and mesmo_escopo(token):
        raise VariavelNaoDeclaradaException("Variável '" + token[0] + "' não declarada na linha " + token[1])

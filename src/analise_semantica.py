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

def adicionar_funcao(funcoes, token, tipo):
    funcao = None
    if tipo[0] == "inteiro":
        funcao = Funcao(token[0], Funcao.INTEGER, None, token)
    elif tipo[0] == "booleano":
        funcao = Funcao(token[0], Funcao.BOLEANO, None, token)
    elif tipo[0] == "vazio":
        funcao = Funcao(token[0], Funcao.VAZIO, None, token)

    funcoes.add(funcao)

def adicionar_parametro(funcoes, token):
    funcao = list(funcoes.funcoes)[-1]
    parametros = funcoes.funcoes[funcao].parametros
    if(parametros == None):
        parametros = [token[0]]
    else:
        parametros.append(token[0])

    funcoes.funcoes[funcao].parametros = parametros

def checar_funcao(funcoes, token):
    if not funcoes.exists(token[0]):
        raise FuncaoNaoDeclaradaException("Função ou procedimento '" + token[0] + "' não declarada (o) na linha " + token[1])

def checar_funcao_existente(funcoes, token):
    if funcoes.exists(token[0]):
        raise FuncaoJaDeclaradaException("Função ou procedimento '" + token[0] + "' já declarada (o) na linha " + token[1])

def get_tipo(variavel):
    return variavel.tipo

def checar_tipos_variaveis(variavel1, variavel2):
    if(get_tipo(variavel1) ==  get_tipo(variavel2)):
        return True
    else:
        return False

def get_simbolo_pelo_identificador_token(simbolos, token):
    for simbolo in simbolos:
        if(simbolo.identificador == token[0]):
            return simbolo

def get_simbolo_pai_funcao(simbolos, filho):
    escopo_filho = list(filho.escopo.split(':'))
    for simbolo in simbolos:
        escopo = list(simbolo.escopo.split(':'))
        if(len(escopo) <= len(escopo_filho) and 'func' in simbolo.tipo):
            if(escopo[:] == escopo_filho[:len(escopo)]):
                return simbolo
    return None

def checar_ja_declarada(variaveis, token, tipo):
    if variaveis.exists(token[0]) and mesmo_escopo(token):
        raise VariavelNaoDeclaradaException("Variável '" + token[0] + "' não declarada na linha " + token[1])

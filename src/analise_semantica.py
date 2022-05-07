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

def mesmo_escopo(variaveis, token, simbolo, funcao=False, funcoes_semanticas=None):
    if(simbolo == None):
        simbolo = variaveis.ultima_declarada(token[0]).lexval
        simbolo.print()
    lista_de_variaveis_declaradas = variaveis.lista_de_variaveis(simbolo.identificador)
    escopo_adicionado = simbolo.escopo.split(':')

    if funcao:
        func = funcoes_semanticas.last()
        escopo_funcao = func.lexval.escopo.split(':')
        escopo_funcao.append('1')
        if(escopo_funcao == escopo_adicionado):
            return True
    else:
        for i in range(len(lista_de_variaveis_declaradas)):
            escopo = list(lista_de_variaveis_declaradas[i].lexval.escopo.split(':'))
            if(len(escopo_adicionado) <= len(escopo)):
                if(escopo_adicionado[:] == escopo[:len(escopo_adicionado)]):
                    return True
                if len(escopo_adicionado) == len(escopo) and escopo[0] == '1':
                    return True
            else:
                if escopo[0] == '1':
                    return True
    
    return False 

def checar_ja_declarada(variaveis, token, simbolo, funcoes_semanticas=None, funcao=False):
    if variaveis.exists(token[0]) and mesmo_escopo(variaveis, token, simbolo, funcao=funcao, funcoes_semanticas=funcoes_semanticas):
        raise VariavelNaoDeclaradaException("Variável '" + token[0] + "' já declarada na linha " + token[1])

def adicionar_funcao(funcoes, token, tipo, simbolo):
    funcao = None
    if tipo[0] == "inteiro":
        funcao = Funcao(token[0], Funcao.INTEGER, None, simbolo)
    elif tipo[0] == "booleano":
        funcao = Funcao(token[0], Funcao.BOLEANO, None, simbolo)
    elif tipo[0] == "vazio":
        funcao = Funcao(token[0], Funcao.VAZIO, None, simbolo)

    funcoes.add(funcao)

def adicionar_parametro(funcoes, simbolo):
    funcao = list(funcoes.funcoes)[-1]
    parametros = funcoes.funcoes[funcao].parametros
    if(parametros == None):
        parametros = [simbolo]
    else:
        parametros.append(simbolo)

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
""" 
def checar_ja_declarada(variaveis, token, tipo, ):
    if variaveis.exists(token[0]) and mesmo_escopo(token, funcao):
        raise VariavelNaoDeclaradaException("Variável '" + token[0] + "' já declarada na linha " + token[1]) """


def checar_declaracao_funcao_semantica(variaveis, token, funcoes_semanticas):
    escopo_funcao = funcoes_semanticas.last().lexval.escopo.split(':')
    lista_de_identificadores = variaveis.lista_de_variaveis(token[0])
    for simbolo in lista_de_identificadores:
        escopo = list(simbolo.lexval.escopo.split(':'))
        if(len(escopo_funcao)+1 <= len(escopo)):
            if(escopo_funcao[:] == escopo[:len(escopo_funcao)]):
                return True
    return False

def varificar_tipo_retorno_funcao(variaveis, token, funcoes):
    variavel = variaveis.ultima_declarada(token[0])
    funcoes = funcoes.last()

    if(not checar_tipos_variaveis(variavel, funcoes)):
        raise RetornoInvalidoException("Tipo de retorno '" + token[0] + "' inválido na linha " + token[1])

def checar_tipo_funcao_atribuicao(variaveis, funcoes, token_variavel, token_funcao):
    funcao = funcoes.get_funcao(token_funcao[0])
    variavel = variaveis.ultima_mesmo_escopo(funcao.lexval.escopo, token_variavel[0])

    if (funcao.tipo != variavel.tipo):
        raise RetornoFuncaoTipoVariavelException("A função '" + funcao.nome + "' retorna um " + funcao.to_string_tipo() + " mas '" + variavel.nome + "' é do tipo " + variavel.to_string_tipo())

def checar_declaracao_variavel_escopo(variaveis, funcoes, token_variavel, token_funcao):
    funcao = funcoes.get_funcao(token_funcao[0])
    variavel = variaveis.ultima_mesmo_escopo(funcao.lexval.escopo, token_variavel[0])

    if variavel == None:
        raise VariavelNaoDeclaradaException("Variável '" + token_variavel[0] + "' não declarada na linha " + token_variavel[1])

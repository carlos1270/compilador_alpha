from pickletools import read_uint1
from src.Simbolo import Simbolo
from src.Exceptions import *

def init(lista_tokens, tabela_simbolos):
    global token, i_token, lista, pilha, simbolos
    simbolos = tabela_simbolos
    pilha = []
    pilha.append(("^", '-1'))
    i_token = 0
    lista = lista_tokens
    token = lista_tokens[i_token]

def ler_token():
    global i_token, lista
    if (i_token < len(lista) - 1):
        i_token += 1
    
    if (lista[i_token] == "$" or lista[i_token - 1] == "$"):
        i_token -= 1
        return lista[len(lista) - 1]
    
    print(lista[i_token])
    return lista[i_token]

def ler_proximo_token():
    global i_token, lista
    prox_token = i_token + 1
    return lista[prox_token]

def voltar_token():
    global i_token
    i_token -= 1

def analise_sintatica(lista_tokens, tabela_simbolos):
    init(lista_tokens, tabela_simbolos)
    resultado = programa()
    return resultado

def tipo_valido(token):
    tipos = ['inteiro', 'booleano']

    for i in range(len(tipos)):
        if (tipos[i] == token[0]):
            return True
    
    return False

def adicionar_simbolo(simbolo, token, tipo=None):
    global simbolos
    simbolo_ja_adicionado = False
    
    for i in range(len(simbolos)):
        if (simbolos[i].identificador == token[0]):
            if (tipo != None):
                if (simbolos[i].tipo == tipo):
                    simbolo_ja_adicionado = True
            else:
                simbolo_ja_adicionado = True
    
    if (not(simbolo_ja_adicionado)):
        simbolos.append(simbolo)

def criar_simbolo(token, tipo=None):
    simbolo = Simbolo(token[0], linha=token[1])
    
    if (simbolo.identificador != "#"):
        if (tipo_valido(lista[i_token - 1])):
            simbolo.tipo = lista[i_token - 1][0]
            adicionar_simbolo(simbolo, token)
        
        if (tipo != None):
            simbolo.tipo = tipo
            adicionar_simbolo(simbolo, token, tipo=tipo)

def programa():
    global token, simbolos
    if (token[0] == 'prog' and identificador() and ponto_virgula() and bloco()):
        return simbolos
    else: 
        raise ProgramaSemIdentificadorExeception("Esperado 'prog' mas encontrado '" + token[0] + "' na linha " + token[1])

def identificador(token=None, opcional=False, tipo=None):
    if (token == None):
        token = ler_token()
    print(token[0])
    for i in range(len(token[0])):
        if (i == 0 and letra(token[0][i])):
            continue
        elif (i > 0 and (letra(token[0][i]) or digito(token[0][i]))):
            continue
        else:
            if (opcional):
                voltar_token()
                return False
            else: 
                raise IdentificadorInvalidoExeception("Identificador '" + token[0] + "' inválido na linha " + token[1])

    criar_simbolo(token, tipo=tipo)
    return True

def letra(letra):
    letras = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if (letra in letras):
        return True
    
    return False

def digito(digito):
    digitos = "0123456789"
    if (digito in digitos):
        return True
    
    return False

def ponto_virgula():
    token = ler_token()
    
    if (token[0] == ';'):
        return True
    else:
        raise EsperaPontoVirgulaExeception("Esperado ';' no lugar de '" + token[0] + "' na linha " + token[1])

def bloco(bloco_interno=False):
    token = ler_token()
    
    if (token[0] == '$'):
        return True
    else: 
        if (token[0] == 'const'):

            if(bloco_interno):
                return declaracao_de_constante()
            else:
                declaracao_de_constante()
        elif(token[0] == 'inteiro' or token[0] == 'booleano'):

            if(bloco_interno):
                return declaracao_de_variavel()
            else:
                declaracao_de_variavel()
        elif(token[0] == 'func'):

            if(bloco_interno):
                return declaracao_de_sub_rotina()
            else:
                declaracao_de_sub_rotina()
        elif(prox_eh_comando(token=token)):

            if(bloco_interno):
                return comando(token)
            else:
                comando(token)
    
    return bloco() 


def declaracao_de_constante():
    global token 
    token_local = token
    if (tipo() and definicao_constante() and ponto_virgula()):
        return True
    else:
        raise DeclaracaoDeConstateException("Constante '" + token_local[0] + "' declarada de forma inválida na linha " + token_local[1])
        

def tipo():
    token = ler_token()

    if (token[0] == 'inteiro' or token[0] == 'booleano'):
        return True
    else:
        raise TipoConstanteInvalidoException("Tipo de dado '" + token[0] + "' inválido na linha " + token[1])

def definicao_constante():
    if (identificador() and atribuicao() and constante()):
        return True
    else:
        return False

def atribuicao():
    token = ler_token()

    if (token[0] == '='):
        return True
    else:
        raise EsperadoAtribuicaoException("Esperado '=' ao invés de '" + token[0] + "' na linha " + token[1])

def constante():
    global token
    token_local = token

    if (identificador(opcional=True) or numero_inteiro(opcional=True) or booleano(opcional=True)):
        return True
    else:
        raise ConstanteInvalidaException("Constante '" + token_local[0] + "' inválida na linha " + token_local[1])

def numero_inteiro(opcional=False):
    token = ler_token()

    for i in range(len(token[0])):
        if (digito(token[0][i])):
            continue
        else:
            if (opcional):
                voltar_token()
                return False
            else:
                raise NumeroInteiroInvalidoException("Número inteiro '" + token[0] + "' inválido na linha " + token[1])
    
    return True

def booleano(opcional=False):
    token = ler_token()

    if (token[0] == 'verdadeiro' or token[0] == 'falso'):
        return True
    else:
        if (opcional):
            voltar_token()
            return False
        else:
            raise BooleanoInvalidoException("Booleano '" + token[0] + "' inválido na linha " + token[1])

def declaracao_de_variavel():
    global token
    if (identificador()):
        if (ponto_virgula()):
            return True
        else:
            raise EsperaPontoVirgulaExeception("Esperado ';' no lugar de '" + token[0] + "' na linha " + token[1])
    else:
        return False


def declaracao_de_sub_rotina():
    token = ler_token()
    
    if (token[0] == "vazio"):
        declaracao_de_procedimento()
    elif (token[0] == "inteiro" or token[0] == "booleano"):
        declaracao_de_funcao()
    else:
        raise TipoDeSubRotinaInvalidaException("Tipo '" + token[0] + "' de sub-rotina inválida na linha " + token[1])

def declaracao_de_procedimento():
    if (identificador(tipo='func') and abre_parenteses()):
        token = ler_proximo_token()
        if (token[0] == ')'):
            token = ler_token()
            return abre_chaves() and bloco(bloco_interno=True) and fecha_chaves()
        elif(parametros_formais() and fecha_parenteses()):
            return abre_chaves() and bloco(bloco_interno=True) and fecha_chaves()
    else:
        return False

def parametros_formais():
    if (tipo() and identificador()):
        token = ler_proximo_token()
        if (token[0] == ')'):
            return True
        elif (token[0] == ','):
            token = ler_token()

    return parametros_formais()

def abre_chaves():
    token = ler_token()
    if (token[0] == "{"):
        return True
    else:
        raise EsperadoChavesExeception("Esperado '{' ao invés de '" + token[0] + "' na linha " + token[1])

def fecha_chaves():
    token = ler_token()
    if (token[0] == "}"):
        return True
    else:
        raise EsperadoChavesExeception("Esperado '}' ao invés de '" + token[0] + "' na linha " + token[1])

def abre_parenteses():
    token = ler_token()

    if (token[0] == "("):
        return True
    else:
        raise EsperadoParentesesExeception("Esperado '(' ao invés de '" + token[0] + "' na linha " + token[1])

def fecha_parenteses():
    token = ler_token()

    if (token[0] == ")"):
        return True
    else:
        raise EsperadoParentesesExeception("Esperado ')' ao invés de '" + token[0] + "' na linha " + token[1])

def declaracao_de_funcao():
    if (identificador(tipo='func') and abre_parenteses()):
        token = ler_proximo_token()
        if (token[0] == ')'):
            token = ler_token()
            return abre_chaves() and bloco(bloco_interno=True) and fecha_chaves()
        elif(parametros_formais() and fecha_parenteses()):
            return abre_chaves() and bloco(bloco_interno=True) and fecha_chaves()
    else:
        return False

def comando(token=None):
    if (token == None):
        token = ler_token() 

    if (token[0] == 'se'):
        comando_condicional_if()
        if (prox_eh_comando()):
            return comando()

    elif (token[0] == 'senao'):
        comando_condicional_else()
        if (prox_eh_comando()):
            return comando()

    elif (token[0] == 'enquanto'):
        comando_de_laco_while()
        if (prox_eh_comando()):
            return comando()

    elif (token[0] == 'retorno'):
        comando_de_retorno_de_valor()
        if (prox_eh_comando()):
            return comando()

    elif ((token[0] == 'pare') or (token[0] == 'pule')):
        comandos_de_desvio_incondicional()
        if (prox_eh_comando()):
            return comando()

    elif (token[0] == 'exibir'):
        comando_impressao_tela()
        if (prox_eh_comando()):
            return comando()

    elif (identificador(token=token)):
        comando_de_atribuicao()
        if (prox_eh_comando()):
            return comando()
    else:
        raise ComandoNaoIdentificadoExecption("Comando '" + token[0] + "' não identificado na linha " + token[1])

    return True

def comando_condicional_if():
    """ Code """

def comando_condicional_else():
    """ Code """

def comando_de_laco_while():
    """ Code """

def comando_de_retorno_de_valor():
    """ Code """

def comandos_de_desvio_incondicional():
    """ Code """

def comando_impressao_tela():
    """ Code """

def comando_de_atribuicao():
    """ Code """

def prox_eh_comando(token=None):
    if (token == None):
        token = ler_proximo_token()

    return (token[0] == 'se') or (token[0] == 'senao') or (token[0] == 'enquanto') or (token[0] == 'retorno') or (token[0] == 'pare') or (token[0] == 'pule') or (token[0] == 'exibir') or (identificador(token=token))
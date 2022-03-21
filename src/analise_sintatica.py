from src.Exceptions import *

def init(lista_tokens):
    global token, i_token, lista, pilha
    pilha = []
    pilha.append(("^", '-1'))
    i_token = 0
    lista = lista_tokens
    token = lista_tokens[i_token]

def ler_token():
    global i_token, lista
    i_token += 1
    return lista[i_token]

def ler_proximo_token():
    global i_token, lista
    prox_token = i_token + 1
    return lista[prox_token]

def voltar_token():
    global i_token
    i_token -= 1

def analise_sintatica(lista_tokens):
    init(lista_tokens)
    resultado = programa()
    return resultado

def programa():
    global token
    if (token[0] == 'prog'):
        if (identificador()):
            if (ponto_virgula()):
                bloco()

    else: 
        raise ProgramaSemIdentificadorExeception("Esperado 'prog' mas encontrado '" + token[0] + "' na linha " + token[1])

def identificador(opcional=False):
    token = ler_token()
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

def bloco():
    token = ler_token()

    if (token[0] == 'const'):
        return declaracao_de_constante()
    elif(token[0] == 'inteiro' or token[0] == 'booleano'):
        return declaracao_de_variavel()
    elif(token[0] == 'func'):
        return declaracao_de_sub_rotina()
    else:
        return comando()


def declaracao_de_constante():
    global token 
    token_local = token
    if (tipo() and definicao_constante()):
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
    token = ler_token

    if (token[0] == '='):
        return True
    else:
        raise EsperadoAtribuicaoException("Esperado '=' ao invés de '" + token[0] + "' na linha " + token[1])

def constante():
    """ Checar [+|-] e (<identificador> | <número inteiro> | <booleano>) na gramática """
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
    """ Code """

def declaracao_de_sub_rotina():
    """ Code """

def comando():
    """ Code """

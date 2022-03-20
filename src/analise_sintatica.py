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

def analise_sintatica(lista_tokens):
    init(lista_tokens)
    print(lista_tokens)
    resultado = programa()

def programa():
    global token
    if (token[0] == "prog"):
        token = ler_token()
        return identificador()
    else: 
        return ProgramaSemIdentificadorExeception("Experado prog mas encontrado '" + token[0] + "' na linha " + token[1])

def identificador():
    global token
    for i in range(len(token[0])):
        if (letra(token[0][i])):
            continue
        else:
            return IdentificadorInvalidoExeception("Identificador '" + token[0] + "' inválido na linha" + token[1])

def letra(letra):
    letras = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if (letra in letras):
        return True
    
    return False
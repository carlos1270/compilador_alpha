from pickletools import read_uint1
from threading import local
from tkinter.tix import Tree
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

def checar_comando_atribuicao(token):
    if ((token[0] == 'booleano') or (token[0] == 'inteiro') or (token[0] == 'const')):
        raise NaoEhPermitidaDeclaracaoException("Não é permitida declarações dentro de comandos, declaração '" + token[0] +"' na linha " + token[1])
    elif (palavras_reservada(token)):
        raise PalavrasReservadasComandoException("Palavras reservadas não permitidas para o comando de atribuição, palavra '" + token[0] + "' na linha " + token[1])


def palavras_reservada(token):

    palavras_reservadas = [
        'booleano', 'inteiro', 'verdadeiro', 'falso', 'nao', 'e', 'ou', 'func', 'prog'
    ]

    for palavra in palavras_reservadas:
        if (palavra == token[0]):
            return True
    
    return False

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

def identificador(token=None, opcional=False, tipo=None, comando=False):
    if (token == None):
        token = ler_token()

    if (comando):
        checar_comando_atribuicao(token)
    
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

    if (booleano(opcional=True) or numero_inteiro(opcional=True) or identificador(opcional=True)):
        return True
    else:
        raise ConstanteInvalidaException("Constante '" + token_local[0] + "' inválida na linha " + token_local[1])

def numero_inteiro(token=None, opcional=False):
    if(token == None):
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
        print("edclaração" + token[0])
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
    
    if (token[0] == '$'):
        return True
    
    elif(token[0] == '}'):
        #nao ha nada dentro do bloco do comando
        raise EsperadoComandoException("Esperado comando entre as {} encontrado '" + token[0] + "' na linha " + token[1])

    elif (token[0] == 'senao'):
        raise ComandoCondicionalElseException("Esperado comando 'se' predecedente a '" + token[0] + "' na linha " + token[1])

    elif (token[0] == 'se'):
        comando_condicional_if()
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

    elif (identificador(token=token, comando=True)):
        comando_de_atribuicao()
        if (prox_eh_comando()):
            return comando()
    else:
        raise ComandoNaoIdentificadoExecption("Comando '" + token[0] + "' não identificado na linha " + token[1])

    return True

def comando_condicional_if():
    local_token = ler_token_atual()

    if (abre_parenteses() and expressao_booleana() and fecha_parenteses() and abre_chaves() and comando() and fecha_chaves()):

        proximo_token = ler_proximo_token()

        if(proximo_token[0] == 'senao'):
            proximo_token = ler_token()
            return comando_condicional_else()
        else:
            return True
    else:
        raise ComandoCondicionalIfException("Comando condicional '" + local_token[0] + "' inválido na linha " + local_token[1])
        

def operador_opcional(token=None):
    if (token == None):
        token = ler_token()

    if (operador(token) and expressao_simples()):
        token = ler_proximo_token()

        if (token[0] == "e" or token[0] == "ou"):
            return operador_opcional()
        elif (token[0] == ")" or token[0] == ";"):
            return True
        else:
            if(token[0] == "nao"):
                raise OperadorInvalidoException("Esperado operador 'e' ou 'ou' ao invés de '" + token[0] + "' na linha " + token[1])
            else:
                raise OperadorInvalidoException("Operador '" + token[0] + "' inválido na linha " + token[1])
    
def ler_token_atual():
    global lista, i_token
    local_token = lista[i_token]
    return local_token

def expressao_booleana(opcional=False):
    global lista, i_token
    local_token = lista[i_token]

    if(expressao_aritmetica(opcional=True)):
        if (operador(opcional=True)):
            return expressao_booleana(opcional=True)

    elif (expressao_simples(opcional)):
        token_opcional = ler_proximo_token()

        if (token_opcional[0] == "e" or token_opcional[0] == "ou"):
            return operador_opcional()
        elif (token_opcional[0] == ')'):
            return True
    else:
        if (opcional):
            return False
        else:
            raise ExpressaoBooleanaInvalidaExecption("Expressão booleana '" + local_token[0] + "' inválida na linha " + local_token[1])
    
    return True

def negacao():
    token = ler_proximo_token()
    if(token[0] == "nao"):
        ler_token()
        return negacao()
    else:
        return True

def expressao_simples(opcional=False):
    if (negacao()):
        return termo(opcional)
    return termo(opcional)

def termo(opcional=False):
    global lista, i_token
    local_token = lista[i_token]

    if (booleano(opcional=True) or identificador(opcional=True)):
        proximo_token = ler_proximo_token()
        
        if (relacao(proximo_token)):
            return relacao_opcional()
        else:
            return True
    else:
        if(opcional):
            return False
        else:
            raise TermoInvalidoException("Termo '" + local_token[0] + "' inválido na linha '" + local_token[1])

def relacao_opcional(token=None):
    if (token == None):
        token = ler_token()

    if (relacao(token) and termo()):
        proximo_token = ler_proximo_token()
        
        if (relacao(proximo_token)):
            return relacao_opcional()
        else:
            return True
    else:
        return True

def relacao(token):
    print('entrou relacao')
    return (token[0] == "==") or (token[0] == "!=") or (token[0] == "<=") or (token[0] == ">=") or (token[0] == ">") or (token[0] == "<")

def operador(token=None, opcional=False):
    if (token == None):
        token = ler_token()
    
    if (token[0] == "e" or token[0] == "ou"):
        return True
    else: 
        if(opcional):
            voltar_token()
            return False
        else:
            raise OperadorInvalidoException("Operador '" + token[0] + "' inválido na linha " + token[1])

def comando_condicional_else():
    global token
    local_token = token

    if (abre_chaves() and comando() and fecha_chaves()):
        if (prox_eh_comando()):
            return comando()
        else:
            return True
    else:
        raise ComandoCondicionalElseException("Comando condicional else'" + local_token[0] + "' inválido na linha " + local_token[1])

def comando_de_laco_while():
    return abre_parenteses() and expressao_booleana() and fecha_parenteses() and abre_chaves() and comando() and fecha_chaves()

def comando_de_retorno_de_valor():
    """ Code """

def comandos_de_desvio_incondicional():
    """ Code """

def comando_impressao_tela():
    """ Code """

def comando_de_atribuicao():
    global token
    local_token = token

    if (expressao() and ponto_virgula()):
        return True
    else:
        raise ComandoAtribuicaoException("Atribuição '" + local_token[0] + "' realizada de forma inválida na linha " + local_token[1])

def expressao():
    global token
    local_token = token
    if (atribuicao()):
        if(expressao_booleana(opcional=True)):
            return True
        elif(expressao_aritmetica(opcional=True)):
            return True
    else:
        raise ExpressaoInvalidaException("Expressão '" + local_token[0] + "' inválida na linha " + local_token[1])

def eh_booleano():
    token = ler_token_atual()
    if(token[0] == "verdadeiro" or token[0] == "falso"):
        return True
    return False

def eh_operador():
    token = ler_token_atual()
    if(token[0] == "e" or token[0] == "ou"):
        return True
    return False

def expressao_aritmetica(opcional=False):
    token_atual = ler_token_atual()
    if(expressao_numerica()):
        token_opcional = ler_proximo_token()
        if (sinal(token_opcional)):
            print('é sinal')
            ler_token()
            return expressao_aritmetica()
        elif(token_opcional[0] == ";"  or token_opcional[0] == ")"):
            return True
        elif(relacao(token_opcional[0])):
            print('entrou relacao em aritimetica')
            ler_token()
            return expressao_aritmetica()
        elif(operador(token=token_opcional, opcional=True)):
            return True
    else:
        if (opcional):
            voltar_token()
            return False
        else:
            raise ExpressaoAritmeticaInvalidaException("Expressão aritmética '" + token_atual[0] + "' feita de forma inválida na linha " + token_atual[1])

def expressao_numerica():
    print('entrou para numerica')
    token = ler_token_atual()
    if(eh_booleano()):
        return False
    elif (identificador(opcional=True) or numero_inteiro(opcional=True)):
        print('passou como expressao numerica')
        return True
    else:
        if(relacao(token=token) or eh_operador()):
            raise RelacaoAritmeticaInvalidaException("Esperado fim de expressao encontrado '" + token[0] + "' na linha "+token[1])
        else:
            raise ExpressaoNumericaInvalidaException("Expressão numérica '" + token[0] + "' feita de forma inválida na linha " + token[1])


def sinal(token = None):
    if (token == None):
        token = ler_token()
    sinais = "+-*/"
    if (token[0] in sinais):
        return True
    return False

def prox_eh_comando(token=None):
    if (token == None):
        token = ler_proximo_token()
    
    if(token[0] == '$'):
        #encerrar comandos em sequencia
        return False
    
    elif(token[0] == '}'):
        #encerrar comandos em sequencia
        return False

    return (token[0] == 'se') or (token[0] == 'senao') or (token[0] == 'enquanto') or (token[0] == 'retorno') or (token[0] == 'pare') or (token[0] == 'pule') or (token[0] == 'exibir') or (identificador(token=token, comando=True))
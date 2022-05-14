from asyncio.windows_events import NULL
from glob import glob
from pickletools import read_uint1
from threading import local
from tkinter.tix import Tree
from src.Simbolo import Simbolo
from src.Exceptions import *
from src.analise_semantica_classes import *
from src.analise_semantica import *
from src.gerador_de_cte import *

def init(lista_tokens, tabela_simbolos):
    global token, i_token, lista, simbolos, variaveis_semanticas, funcoes_semanticas
    simbolos = tabela_simbolos
    i_token = 0
    lista = lista_tokens
    token = lista_tokens[i_token]
    variaveis_semanticas = VariavelHash()
    funcoes_semanticas = FuncaoHash()
    abrir_arquivo_cte_temp()

def checar_comando_atribuicao(token):
    if ((token[0] == 'booleano') or (token[0] == 'inteiro') or (token[0] == 'const')):
        raise NaoEhPermitidaDeclaracaoException("Não é permitida declarações dentro de comandos, declaração '" + token[0] +"' na linha " + token[1])
    elif (palavras_reservada(token)):
        raise PalavrasReservadasComandoException("Palavras reservadas não permitidas para o comando de atribuição, palavra '" + token[0] + "' na linha " + token[1])


def palavras_reservada(token):

    palavras_reservadas = [
        'booleano', 'inteiro', 'verdadeiro', 'falso', 'nao', 'e', 'ou', 'func', 'prog', 'retorno'
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

def ler_token_anterior():
    global i_token, lista
    return lista[i_token - 1]

def ler_token_tipo_variavel():
    global i_token, lista
    return lista[i_token - 2]

def voltar_token():
    global i_token
    i_token -= 1

def analise_sintatica(lista_tokens, tabela_simbolos):
    init(lista_tokens, tabela_simbolos)
    resultado = programa()
    variaveis_semanticas.print()
    funcoes_semanticas.print()
    return resultado

def tipo_valido(token):
    tipos = ['inteiro', 'booleano']

    for i in range(len(tipos)):
        if (tipos[i] == token[0]):
            return True
    
    return False

def adicionar_simbolo(simbolo, token, tipo=None, escopo=None):
    global simbolos
    """ simbolo_ja_adicionado = False
    for i in range(len(simbolos)):
        if (simbolos[i].identificador == token[0]):
            if (tipo != None):
                if (simbolos[i].tipo == tipo):
                    simbolo_ja_adicionado = True
            else:
                simbolo_ja_adicionado = True

    if (not(simbolo_ja_adicionado)): """

    simbolos.append(simbolo)

def adicionar_paramentro(id_func, parametro):
    global simbolos
    for simbolo in simbolos:
        if (simbolo.identificador == id_func[0]):
            simbolo.parametros.append(parametro.tipo + ':' + parametro.identificador)

def criar_simbolo(token, tipo=None, id_func=None, escopo=None, mutavel=True):
    simbolo = Simbolo(token[0], escopo=escopo, linha=token[1], mutavel=mutavel)

    if (simbolo.identificador != "#"):
        if (tipo_valido(lista[i_token - 1])):
            #modificacao para adicionar o tipo do simbolo de declaracao de funcao com func:tipo e nao so o tipo
            if(tipo != None):
                if('func' in tipo):
                    simbolo.tipo = tipo
                else:
                    simbolo.tipo = lista[i_token - 1][0]
            else:
                simbolo.tipo = lista[i_token - 1][0]
            adicionar_simbolo(simbolo, token)
        
        elif (tipo != None):
            simbolo.tipo = tipo
            adicionar_simbolo(simbolo, token, tipo=tipo)

        if (id_func != None):
            adicionar_paramentro(id_func, simbolo)

def programa():
    global token, simbolos
    if (token[0] == 'prog' and identificador() and ponto_virgula() and bloco(escopo='1:1')):
        return simbolos
    else: 
        raise ProgramaSemIdentificadorExeception("Esperado 'prog' mas encontrado '" + token[0] + "' na linha " + token[1])


def identificador(token=None, opcional=False, tipo=None, comando=False, id_func=None, escopo=None, checar_termo=False, checar_atribuicao=False, checa_funcao_declarada=False, checar_declaracao_funcao=False, bloco_interno_funcao_retorno=False, mutavel=True):
    global variaveis_semanticas, funcoes_semanticas
    
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

    criar_simbolo(token, tipo=tipo, id_func=id_func, escopo=escopo, mutavel=mutavel)

    """ Checagens semanticas """
    if checar_termo:
        checar_declaracao_semantica(variaveis_semanticas, token)
    if checar_atribuicao:
        checar_comando_atribuicao_semantica(variaveis_semanticas, token)
    if checa_funcao_declarada:
        checar_funcao_existente(funcoes_semanticas, token)
    if checar_declaracao_funcao:
        if(not checar_declaracao_funcao_semantica(variaveis_semanticas, token, funcoes_semanticas)):
           raise VariavelNaoDeclaradaException("Variável '" + token[0] + "' não declarada na linha " + token[1])

    if bloco_interno_funcao_retorno:
        if(not comando):
            checar_ja_declarada(variaveis_semanticas, token, None, funcoes_semanticas=funcoes_semanticas, funcao=bloco_interno_funcao_retorno)
        

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

def bloco(bloco_interno=False, bloco_interno_funcao_retorno=False, comando_enquanto=False, escopo=None, identacao=False):
    token = ler_token()

    if (token[0] == '$'):
        return True
    else:
        if (token[0] == 'const'):
            declaracao_de_constante(escopo=escopo, bloco_interno_funcao_retorno=bloco_interno_funcao_retorno)
            return bloco(bloco_interno_funcao_retorno=bloco_interno_funcao_retorno, comando_enquanto=comando_enquanto, escopo=escopo, identacao=identacao)
        elif(token[0] == 'inteiro' or token[0] == 'booleano'):
            declaracao_de_variavel(escopo=escopo, bloco_interno_funcao_retorno=bloco_interno_funcao_retorno)
            return bloco(bloco_interno_funcao_retorno=bloco_interno_funcao_retorno, comando_enquanto=comando_enquanto, escopo=escopo, identacao=identacao)

        elif(token[0] == 'func'):
            if(bloco_interno_funcao_retorno):
                raise NaoEhPermitidaDeclaracaoException("Não é permitida declaração de função dentro desse bloco '"+token[0]+"' na linha '"+token[1]+"'")
                #return declaracao_de_sub_rotina()
            else:
                novo_bloco = escopo[:len(escopo)-1-len((escopo[::-1][:escopo[::-1].index(":")]))]+':'+str(int((escopo[::-1][:escopo[::-1].index(":")])[::-1])+1)
                declaracao_de_sub_rotina(escopo=escopo)
                return bloco(bloco_interno_funcao_retorno=bloco_interno_funcao_retorno, comando_enquanto=comando_enquanto, escopo=novo_bloco, identacao=identacao)
        elif(token[0] == 'retorno'):
            if(bloco_interno_funcao_retorno):
                identificador(token=token, escopo=escopo)
                comando_de_retorno_de_valor()
                return bloco(bloco_interno_funcao_retorno=bloco_interno_funcao_retorno, comando_enquanto=comando_enquanto, escopo=escopo, identacao=identacao)
            else:
                raise ComandoDeRetornoDeValorInvalidoException("Comando de retorno só pode ser chamado em blocos de função com retorno. Erro na linha '"+token[1]+"'")
        elif(token[0] == 'pare' or token[0] == 'pule'):
            if(comando_enquanto):
                comandos_de_desvio_incondicional()
                return bloco(bloco_interno_funcao_retorno=bloco_interno_funcao_retorno, comando_enquanto=comando_enquanto, escopo=escopo, identacao=identacao)
            else:
                raise ComandoIncondicionalInvalidoException("Comandos 'pare' ou 'pule' devem ser utilizados dentro de blocos 'enquanto'. Erro na linha '"+token[1]+"'")
        elif(prox_eh_comando(token=token)):
            if(bloco_interno):
                return comando(token, bloco_interno_funcao_retorno=bloco_interno_funcao_retorno, comando_enquanto=comando_enquanto, escopo=escopo, identacao=identacao)
            else:
                comando(token, bloco_interno_funcao_retorno=bloco_interno_funcao_retorno, comando_enquanto=comando_enquanto, escopo=escopo, identacao=identacao)
        
        elif(token[0] == '}' or token[0] == ')'):
            if(bloco_interno):
                raise EsperadoComandoException("Esperado comando entre as {} encontrado '" + token[0] + "' na linha " + token[1])
            voltar_token()
            return True
    
    return bloco(escopo=escopo, identacao=identacao) 


def declaracao_de_constante(escopo=None, bloco_interno_funcao_retorno=None):
    global token 
    token_local = token
    if (tipo() and definicao_constante(escopo=escopo) and ponto_virgula()):
        return True
    else:
        raise DeclaracaoDeConstateException("Constante '" + token_local[0] + "' declarada de forma inválida na linha " + token_local[1])
        

def tipo():
    token = ler_token()

    if (token[0] == 'inteiro' or token[0] == 'booleano'):
        return True
    else:
        raise TipoConstanteInvalidoException("Tipo de dado '" + token[0] + "' inválido na linha " + token[1])

def definicao_constante(escopo=None):
    
    if (identificador(escopo=escopo, mutavel=False) and atribuicao() and constante(escopo=escopo)):
        return True
    else:
        return False

def atribuicao():
    token = ler_token()

    if (token[0] == '='):
        return True
    else:
        raise EsperadoAtribuicaoException("Esperado '=' ao invés de '" + token[0] + "' na linha " + token[1])

def constante(escopo=None):
    global token, simbolos, variaveis_semanticas, lista, i_token
    token_local = token

    if (booleano(opcional=True)):
        checar_tipo_constante_booleano(simbolos[len(simbolos) - 1])
        return True
    elif (numero_inteiro(opcional=True)):
        checar_tipo_constante_inteiro(simbolos[len(simbolos) - 1])
        return True
    elif identificador(opcional=True):
        checar_variavel_esta_declarada_com_mesmo_escopo(variaveis_semanticas, escopo, lista[i_token])
        checar_tipo_constante_variavel(simbolos[len(simbolos) - 1], variaveis_semanticas, escopo, lista[i_token])
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

def declaracao_de_variavel(escopo=None, bloco_interno_funcao_retorno=False):
    global token, variaveis_semanticas, simbolos
    if (identificador(escopo=escopo, bloco_interno_funcao_retorno=bloco_interno_funcao_retorno)):
        if (ponto_virgula()):
            if(not bloco_interno_funcao_retorno):
                checar_ja_declarada(variaveis_semanticas, ler_token_anterior(), simbolos[len(simbolos) - 1])
            adicionar_variavel(variaveis_semanticas, ler_token_anterior(), ler_token_tipo_variavel(), simbolos[len(simbolos) - 1])
            return True
        else:
            raise EsperaPontoVirgulaExeception("Esperado ';' no lugar de '" + token[0] + "' na linha " + token[1])
    else:
        return False


def declaracao_de_sub_rotina(escopo=None):
    token = ler_token()
    
    if (token[0] == "vazio"):
        declaracao_de_procedimento(escopo=escopo)
    elif (token[0] == "inteiro" or token[0] == "booleano"):
        declaracao_de_funcao(tipo=token[0], escopo=escopo)
    else:
        raise TipoDeSubRotinaInvalidaException("Tipo '" + token[0] + "' de sub-rotina inválida na linha " + token[1])

def declaracao_de_procedimento(escopo=None):
    global lista, i_token, simbolos, funcoes_semanticas

    if (identificador(tipo='proc:vazio', escopo=escopo, checa_funcao_declarada=True) and abre_parenteses()):
        token = ler_proximo_token()
        adicionar_funcao(funcoes_semanticas, ler_token_anterior(), ler_token_tipo_variavel(), simbolos[len(simbolos) - 1])
        if (token[0] == ')'):
            token = ler_token()
            open = abre_chaves()
            gerar_cte_inicio_funcao(funcoes_semanticas)
            interno = bloco(bloco_interno=True, escopo=escopo+':1', identacao=True)
            close = fecha_chaves()
            gerar_cte_fim_funcao(funcoes_semanticas)
            return open and interno and close
        elif(parametros_formais(lista[i_token - 1], escopo=escopo+':1') and fecha_parenteses()):
            open = abre_chaves()
            gerar_cte_inicio_funcao(funcoes_semanticas)
            interno = bloco(bloco_interno=True, escopo=escopo+':1', identacao=True)
            close = fecha_chaves()
            gerar_cte_fim_funcao(funcoes_semanticas)
            return open and interno and close
    else:
        return False

def parametros_formais(id_func, escopo=None):
    global variaveis_semanticas, funcoes_semanticas, simbolos
    if (tipo() and identificador(id_func=id_func, escopo=escopo)):
        adicionar_variavel(variaveis_semanticas, ler_token_atual(), ler_token_anterior(), simbolos[len(simbolos) - 1])
        adicionar_parametro(funcoes_semanticas, simbolos[len(simbolos) - 1])
        token = ler_proximo_token()
        if (token[0] == ')'):
            return True
        elif (token[0] == ','):
            token = ler_token()

    return parametros_formais(id_func, escopo=escopo)

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

def declaracao_de_funcao(tipo, escopo=None):
    global lista, i_token, simbolos, funcoes_semanticas

    if (identificador(tipo='func:'+tipo, escopo=escopo, checa_funcao_declarada=True) and abre_parenteses()):
        token = ler_proximo_token()
        adicionar_funcao(funcoes_semanticas, ler_token_anterior(), ler_token_tipo_variavel(), simbolos[len(simbolos) - 1])
        if (token[0] == ')'):
            token = ler_token()
            open = abre_chaves()
            gerar_cte_inicio_funcao(funcoes_semanticas)
            interno = bloco(bloco_interno=True, bloco_interno_funcao_retorno=True, escopo=escopo+':1', identacao=True)
            close = fecha_chaves()
            gerar_cte_fim_funcao(funcoes_semanticas)
            return open and interno and close
        elif(parametros_formais(lista[i_token - 1], escopo=escopo+':1') and fecha_parenteses()):
            open = abre_chaves()
            gerar_cte_inicio_funcao(funcoes_semanticas)
            interno = bloco(bloco_interno=True, bloco_interno_funcao_retorno=True, escopo=escopo+':1', identacao=True)
            close = fecha_chaves()
            gerar_cte_fim_funcao(funcoes_semanticas)
            return open and interno and close
    else:
        return False

def comando(token=None, bloco_interno_funcao_retorno=False, comando_enquanto=False, escopo=None, identacao=False):
    if (token == None):
        token = ler_token() 
    
    if (token[0] == '$'):
        return True

    elif (token[0] == 'senao'):
        raise ComandoCondicionalElseException("Esperado comando 'se' predecedente a '" + token[0] + "' na linha " + token[1])

    elif (token[0] == 'se'):
        novo_bloco = escopo[:len(escopo)-1-len((escopo[::-1][:escopo[::-1].index(":")]))]+':'+str(int((escopo[::-1][:escopo[::-1].index(":")])[::-1])+1)
        comando_condicional_if(bloco_interno_funcao_retorno=bloco_interno_funcao_retorno, comando_enquanto=comando_enquanto, escopo=escopo+':1', identacao=identacao)
        return bloco(bloco_interno_funcao_retorno=bloco_interno_funcao_retorno, comando_enquanto=comando_enquanto, escopo=novo_bloco, identacao=identacao)
    elif (token[0] == 'enquanto'):
        novo_bloco = escopo[:len(escopo)-1-len((escopo[::-1][:escopo[::-1].index(":")]))]+':'+str(int((escopo[::-1][:escopo[::-1].index(":")])[::-1])+1)
        comando_de_laco_while(bloco_interno_funcao_retorno=bloco_interno_funcao_retorno, escopo=escopo+':1', identacao=identacao)
        return bloco(bloco_interno_funcao_retorno=bloco_interno_funcao_retorno, comando_enquanto=comando_enquanto, escopo=novo_bloco, identacao=identacao)

    elif ((token[0] == 'pare') or (token[0] == 'pule')):
        comandos_de_desvio_incondicional()
        return bloco(bloco_interno_funcao_retorno=bloco_interno_funcao_retorno, comando_enquanto=comando_enquanto, escopo=escopo, identacao=identacao)
    elif (token[0] == 'exibir'):
        comando_impressao_tela()
        return bloco(bloco_interno_funcao_retorno=bloco_interno_funcao_retorno, comando_enquanto=comando_enquanto, escopo=escopo, identacao=identacao)
    elif(comando_chamada_procedimento(opcional=True)):
        token_atual = ler_token_atual()
        if (chamada(token_atual[0], procedimento=True)): 
            ponto_virgula()

        return bloco(bloco_interno_funcao_retorno=bloco_interno_funcao_retorno, comando_enquanto=comando_enquanto, escopo=escopo, identacao=identacao)
    
    elif (identificador(token=token, comando=True, bloco_interno_funcao_retorno=bloco_interno_funcao_retorno)):
        global variaveis_semanticas
        token = ler_token_atual()
        comando_de_atribuicao(identacao=identacao)
        return bloco(bloco_interno_funcao_retorno=bloco_interno_funcao_retorno, comando_enquanto=comando_enquanto, escopo=escopo, identacao=identacao)
    else:
        raise ComandoNaoIdentificadoExecption("Comando '" + token[0] + "' não identificado na linha " + token[1])

    return True

def comando_condicional_if(bloco_interno_funcao_retorno=False, comando_enquanto=False, escopo=None, identacao=False):
    global lista, i_token
    novo_bloco = escopo[:len(escopo)-1-len((escopo[::-1][:escopo[::-1].index(":")]))]+':'+str(int((escopo[::-1][:escopo[::-1].index(":")])[::-1])+1)
    local_token = ler_token_atual()

    expressao_bool = abre_parenteses() and expressao_booleana() and fecha_parenteses()
    labels = gerar_inicio_cte_if(lista, i_token, identacao=identacao)
    bloco_de_codigo = abre_chaves() and bloco(bloco_interno=True, bloco_interno_funcao_retorno=bloco_interno_funcao_retorno, comando_enquanto=comando_enquanto, escopo=escopo, identacao=identacao) and fecha_chaves()
    gerar_label_interno_cte_if(labels, identacao=identacao)
    if (expressao_bool and bloco_de_codigo):
        proximo_token = ler_proximo_token()

        if(proximo_token[0] == 'senao'):
            proximo_token = ler_token()
            retorno = comando_condicional_else(bloco_interno_funcao_retorno=bloco_interno_funcao_retorno, comando_enquanto=comando_enquanto, escopo=novo_bloco, identacao=identacao)
            gerar_label_externo_if(labels, identacao=identacao)
            return retorno
        else:
            gerar_label_externo_if(labels, identacao=identacao)
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

    if (expressao_simples(opcional)):
        token_opcional = ler_proximo_token()

        if (token_opcional[0] == "e" or token_opcional[0] == "ou"):
            return operador_opcional()
        elif (token_opcional[0] == ')'):
            return True
        elif(sinal(token_opcional)):
            if (opcional):
                voltar_token()
            return False
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

    if (booleano(opcional=True) or identificador(opcional=True, checar_termo=True) or numero_inteiro(opcional=True)):
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

def comando_condicional_else(bloco_interno_funcao_retorno=False, comando_enquanto=False, escopo=None, identacao=False):
    retorno = abre_chaves() and bloco(bloco_interno=True, bloco_interno_funcao_retorno=bloco_interno_funcao_retorno, comando_enquanto=comando_enquanto, escopo=escopo, identacao=identacao) and fecha_chaves()
    return retorno

def comando_de_laco_while(bloco_interno_funcao_retorno=False, escopo=None, identacao=False):
    global lista, i_token

    expressao_bool = abre_parenteses() and expressao_booleana() and fecha_parenteses()
    labels = gerar_cte_expressao_while(lista, i_token, identacao=identacao)
    bloco_while = abre_chaves() and bloco(bloco_interno=True, bloco_interno_funcao_retorno=bloco_interno_funcao_retorno, comando_enquanto=True, escopo=escopo, identacao=identacao) and fecha_chaves()
    gerar_cte_fim_while(labels, identacao=identacao)
    return expressao_bool and bloco_while

def comando_de_retorno_de_valor():
    global variaveis_semanticas, simbolos, funcoes_semanticas
    if (checar_chamada(opcional=True)):
        return chamada() and ponto_virgula()
    if(numero_inteiro(opcional=True)):
        token = ler_token_anterior()
        funcoes = list(funcoes_semanticas.funcoes)
        funcao_semantica = funcoes_semanticas.funcoes[funcoes[len(funcoes)-1]]

        if(not funcao_semantica.tipo == 1):
            token = ler_token_atual()
            raise RetornoInvalidoException("Tipo de retorno '" + token[0] + "' inválido na linha " + token[1])
        if(ponto_virgula()):
            return True
    elif(booleano(opcional=True)):
        token = ler_token_anterior()
        funcoes = list(funcoes_semanticas.funcoes)
        funcao_semantica = funcoes_semanticas.funcoes[funcoes[len(funcoes)-1]]

        if(not funcao_semantica.tipo == 2):
            token = ler_token_atual()
            raise RetornoInvalidoException("Tipo de retorno '" + token[0] + "' inválido na linha " + token[1])
        if(ponto_virgula()):
            return True
    elif (identificador(opcional=True, checar_declaracao_funcao=True)):
        """ print('passou como identifcador') """
        token = ler_token_atual()
        varificar_tipo_retorno_funcao(variaveis_semanticas, token, funcoes_semanticas)
        
        if(ponto_virgula()):
            return True
    return False

def comandos_de_desvio_incondicional():
    return ponto_virgula()

def comando_impressao_tela():
    if (abre_parenteses()):
        if (checar_chamada(opcional=True)):
            return chamada() and fecha_parenteses() and ponto_virgula()
        elif (identificador(opcional=True) or numero_inteiro(opcional=True) or booleano(opcional=True)) and fecha_parenteses() and ponto_virgula():
            return True
    
    return False

def comando_de_atribuicao(identacao=False):
    global variaveis_semanticas, funcoes_semanticas, lista, i_token
    token_atual = ler_token_atual()
    if (atribuicao()):
        if (checar_chamada(opcional=True)):
            token_atual = ler_token_atual()
            checar_funcao(funcoes_semanticas, token_atual)
            checar_declaracao_variavel_escopo(variaveis_semanticas, funcoes_semanticas, lista[i_token - 2], token_atual)
            checar_tipo_funcao_atribuicao(variaveis_semanticas, funcoes_semanticas, lista[i_token - 2], token_atual)
            retorno = chamada(token_atual[0]) and ponto_virgula()
            gerar_cte_chamada_atribuicao(lista, i_token, identacao=identacao)
            return retorno
        else:
            retorno = expressao() and ponto_virgula()
            gerar_cte_expressao_atribuicao(lista, i_token, identacao=identacao)
            return retorno
    else:
        raise ComandoAtribuicaoException("Atribuição '" + token_atual[0] + "' realizada de forma inválida na linha " + token_atual[1])

def expressao():
    if(expressao_booleana(opcional=True)):
        return True
    elif(expressao_aritmetica()):
        return True
    else:
        token_atual = ler_token_atual()
        raise ExpressaoInvalidaException("Expressão '" + token_atual[0] + "' inválida na linha " + token_atual[1])

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
            ler_token()
            return expressao_aritmetica()
        elif(token_opcional[0] == ";"  or token_opcional[0] == ")"):
            return True
        elif(relacao(token_opcional[0])):
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
    token = ler_token_atual()
    if(eh_booleano()):
        return False
    elif (identificador(opcional=True, checar_atribuicao=True) or numero_inteiro(opcional=True)):
        """ print("aaaa") """
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
    
    elif(token[0] == 'func'):
        return False

    return (token[0] == 'se') or (token[0] == 'senao') or (token[0] == 'enquanto') or (token[0] == 'retorno') or (token[0] == 'pare') or (token[0] == 'pule') or (token[0] == 'exibir') or (comando_chamada_procedimento(opcional=True)) or (identificador(token=token, comando=True, checar_atribuicao=True))

def chamada(nome_funcao, procedimento=False):
    global i_token, lista, funcoes_semanticas, variaveis_semanticas
    
    if procedimento:
        checar_procedimento_declarado(funcoes_semanticas, lista[i_token])

    retorno = abre_parenteses() and secao_parametros_passados() and fecha_parenteses()
    checar_quantidade_parametros_passados(funcoes_semanticas, nome_funcao, parametros_funcao(nome_funcao, i_token, lista))
    checar_tipos_paramentros_passados(variaveis_semanticas, funcoes_semanticas, nome_funcao, parametros_funcao(nome_funcao, i_token, lista))
    return retorno

def secao_parametros_passados():
    if (identificador(opcional=True)):
        token = ler_proximo_token()
        if (token[0] == ')'):
            return True
        elif (token[0] == ','):
            token = ler_token()
            token = ler_proximo_token()
            identificador(token=token)

    token = ler_proximo_token()
    if (token[0] == ')'):
        return True

    return secao_parametros_passados()

def checar_chamada(opcional=False):
    if (identificador(opcional=opcional)):
        token = ler_proximo_token()
        if (token[0] == '('):
            return True
        else:
            voltar_token()
            return False
    else:
        return False

def comando_chamada_procedimento(opcional=False):
    global lista, i_token
    token = lista[i_token]
    prox_token = ler_proximo_token()
    if (identificador(opcional=opcional, token=token) and prox_token[0] == "("):
        return True
    
    if (opcional):
        return False
    else:
        raise EsperadoParentesesExeception("Esperado '(' ao invés de '" + token[0] + "' na linha " + token[1])

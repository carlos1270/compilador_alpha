from src.Exceptions import *

def checagem_caracteres(arquivo):
    qtd_linhas = 0
    caracteres_validos = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890(){}=<>!+-*/\n; "

    for linha in arquivo:
        qtd_linhas += 1
        for caracter in linha:
            if (caracter not in caracteres_validos):
                return "Error de análise léxica: caracter '"+caracter + "' não reconhecido pela linguagem na linha: " + str(qtd_linhas)
    return True

def remover_formatacao(arquivo):
    linha_unica = ""
    qtd_linhas = 1
    for linha in arquivo:
        linha_unica += ""
        linha_unica += "|$"+str(qtd_linhas)+"|"
        qtd_linhas += 1
        for i in range(len(linha)-1):
            if (linha[i] == " " or linha[i] == "\n" or linha[i] == "\t" or linha[i] == "\r"):
                if((linha[i+1] != " ") and (linha[i+1] != "\n") and (linha[i+1] != "\t") and (linha[i+1] != "\r")):
                    linha_unica += "|"
            else:
                linha_unica += linha[i]
        if (linha[len(linha)-1] != " " and linha[len(linha)-1] != "\n" and linha[len(linha)-1] != "\t" and linha[len(linha)-1] != "\r"):
            linha_unica += "|"+linha[len(linha)-1]
    
    if(len(linha_unica) > 0):
        if(linha_unica[len(linha_unica)-1] == "|"):
            linha_unica = linha_unica[:len(linha_unica)-1]

    #print(linha_unica)

    return linha_unica

def processar_caractere(caractere_atual, caractere_proximo):
    incremento = 1
    if(caractere_atual == '=' and caractere_proximo == '='):
        retorno = "|==|"
        incremento = 2
    elif(caractere_atual == '!' and caractere_proximo == '='):
        retorno = "|!=|"
        incremento = 2
    elif(caractere_atual == '>' and caractere_proximo == '='):
        retorno = "|>=|"
        incremento = 2
    elif(caractere_atual == '<' and caractere_proximo == '='):
        retorno = "|<=|"
        incremento = 2
    else:
        retorno = "|"+caractere_atual+"|"
    return [retorno, incremento]

def adicionar_pipes(texto):
    caracteres = "(){}=<>!+-*/;"
    nova_linha = ""
    i = 0
    while(i < len(texto)-1):
        if (texto[i] in caracteres):
            retorno = processar_caractere(texto[i], texto[i+1])
            nova_linha += retorno[0]
            i += retorno[1]
        else:
            nova_linha += texto[i]
            i+=1
    if(len(texto)-1 >= 0):
        nova_linha += texto[len(texto)-1]

    nova_linha = nova_linha.replace("|||", "|")
    nova_linha = nova_linha.replace("||", "|")
    if(len(nova_linha) > 0):
        if(nova_linha[0] == '|'):
            nova_linha = nova_linha[1:]

    return nova_linha

def lista_tokens(lista):
    linha = lista[0][1:]
    lista_tokens = []
    for i in range(1, len(lista)):
        if(lista[i][0] == '$'):
            linha = lista[i][1:]
        else:
            lista_tokens.append((lista[i], linha))
    return lista_tokens


def analise_lexica(caminho_arquivo):
    arquivo = open(caminho_arquivo, "r")
    texto_arquivo = arquivo.read()
    checagem = checagem_caracteres(texto_arquivo)
    arquivo.close()
    if (checagem == True):
        arquivo = open(caminho_arquivo, "r")
        linha = remover_formatacao(arquivo)
        arquivo.close()
        linha_separada = adicionar_pipes(linha)
        tabela_tokens = lista_tokens(linha_separada.split("|"))

    else:
        raise AnaliseLexicaExeception(checagem)
    return tabela_tokens

                

    
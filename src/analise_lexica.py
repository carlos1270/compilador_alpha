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
    for linha in arquivo:
        for letra in linha:
            if (letra == " " or letra == "\n" or letra == "\t" or letra == "\r"):
                linha_unica += "|"
            else:
                linha_unica += letra

    arquivo_final = ""
    for i in range(len(linha_unica)):
        if (not(linha_unica[i] == "|" and linha_unica[i+1] == "|")):
            arquivo_final += linha_unica[i]

    return arquivo_final

def processar_caractere(caractere_atual, caractere_proximo):
    incremento = 1
    if(caractere_atual == '=' and caractere_proximo == '='):
        retorno = "|==|"
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
    return nova_linha

def analise_lexica(caminho_arquivo):
    arquivo = open(caminho_arquivo, "r")
    texto_arquivo = arquivo.read()
    arquivo.close()
    checagem = checagem_caracteres(texto_arquivo)
    if (checagem == True):
        linha = remover_formatacao(texto_arquivo)
        linha_separada = adicionar_pipes(linha)
        tabela_tokens = linha_separada.split("|")

    else:
        raise AnaliseLexicaExeception(checagem)
    
    return tabela_tokens

                

    
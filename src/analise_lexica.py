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

def analise_lexica(caminho_arquivo):
    tabela_tokens = []
    token = ""
    arquivo = open(caminho_arquivo)
    checagem = checagem_caracteres(arquivo)
    if (checagem == True):
        linha = remover_formatacao(arquivo)
        """ for i in range(len(linha.split("|"))):
        adicionar_token(tabela_tokens, linha.split("|")[i]) """

    else:
        arquivo.close()
        raise AnaliseLexicaExeception(checagem)
    
    return tabela_tokens

                

    
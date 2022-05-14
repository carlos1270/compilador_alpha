from src.analise_semantica_classes import *

def abrir_arquivo_cte_temp():
    global file
    init()
    file = open('codigo_intermediario.cte', 'w')

def fechar_arquivo_cte_temp():
    global file

    file.close() 

def init():
    global var_i, label_i
    var_i = 1
    label_i = 1

def gerar_var_temp():
    global var_i
    var = "_temp" + str(var_i)
    var_i += 1
    return var

def gerar_label():
    global label_i
    label = "_L" + str(label_i)
    label_i += 1
    return label

def gerar_cte_chamada_atribuicao(lista, i_token, identacao=False):
    global file
    i = i_token
    funcao = ''
    parametros = []
    ident = ''
    if identacao:
        ident = "    "

    while(lista[i][0] != '='):
        if (lista[i-1][0] == '='):
            funcao = lista[i][0]

        if (lista[i][0] != '(' and lista[i][0] != ',' and lista[i][0] != ')' and lista[i][0] != ';' and lista[i-1][0] != '='):
            parametros.append(lista[i][0])
    
        i -= 1

    for param in parametros:
        file.write(ident + "param " + str(param) + ";\n")
    var = gerar_var_temp()
    file.write(ident + str(var) + " := call " + str(funcao) + ", " + str(len(parametros)) + ";\n")
    file.write(ident + str(lista[i-1][0]) + " := " + str(var) + ";\n")



def gerar_cte_expressao_atribuicao(lista, i_token, identacao=False):
    i = i_token
    expressao = []
    while(lista[i][0] != '='):
        if (lista[i][0] != ';'):
            expressao.append(lista[i][0])
        i -= 1
    
    expressao = list(reversed(expressao))
    ident = ''
    if identacao:
        ident = "    "

    if len(expressao) == 1:
        file.write(ident + str(lista[i-1][0]) + " := " + str(expressao[0] + ";\n"))
    elif len(expressao) > 1:
        while(len(expressao) > 1):
            bol_exp = eh_expressao_booleana(expressao)
            if bol_exp:
                var = gerar_var_temp()
                comparacao = tem_comparacao(expressao)
                if comparacao: 
                    for s in range(len(expressao)):
                        if (((expressao[s] == '<') or (expressao[s] == '>') or (expressao[s] == '>=') or (expressao[s] == '<=') or (expressao[s] == '==') or (expressao[s] == '!=')) and (expressao[s+1] != 'nao')):
                            file.write(ident + str(var) + " := " + str(expressao[s-1]) + " " + str(expressao[s]) + " " + str(expressao[s+1]) +";\n")
                            expressao = gerar_novas_expressoes(expressao, s-1, var)
                            break
                else:
                    tem_and = tem_e(expressao)
                    if tem_and:
                        for s in range(len(expressao)):
                            if ((expressao[s] == 'e') and (expressao[s+1] != 'nao')):
                                file.write(ident + str(var) + " := " + str(expressao[s-1]) + " && " + str(expressao[s+1]) +";\n")
                                expressao = gerar_novas_expressoes(expressao, s-1, var)
                                break
                    else:
                        tem_or = tem_ou(expressao)
                        if tem_or:
                            for s in range(len(expressao)):
                                if ((expressao[s] == 'ou') and (expressao[s+1] != 'nao')):
                                    file.write(ident + str(var) + " := " + str(expressao[s-1]) + " || " + str(expressao[s+1]) +";\n")
                                    expressao = gerar_novas_expressoes(expressao, s-1, var)
                                    break
                        else:
                            for s in range(len(expressao)):
                                if ((expressao[s-1] == 'nao')):
                                    file.write(ident + str(var) + " := !" + str(expressao[s]) + ";\n")
                                    expressao = gerar_novas_expressoes(expressao, s-1, var, nao=True)
                                    break

            else:
                var = gerar_var_temp()
                mult_div = tem_mult_ou_div(expressao)
                if mult_div: 
                    for s in range(len(expressao)):
                        if ((expressao[s] == '*') or (expressao[s] == '/')):
                            file.write(ident + str(var) + " := " + str(expressao[s-1]) + " " + str(expressao[s]) + " " + str(expressao[s+1]) +";\n")
                            expressao = gerar_novas_expressoes(expressao, s-1, var)
                            break
                else:
                    for s in range(len(expressao)):
                        if ((expressao[s] == '+') or (expressao[s] == '-')):
                            file.write(ident + (var) + " := " + str(expressao[s-1]) + " " + str(expressao[s]) + " " + str(expressao[s+1]) +";\n")
                            expressao = gerar_novas_expressoes(expressao, s-1, var)
                            break

        file.write(ident + str(lista[i-1][0]) + " := " + str(expressao[0]) + ";\n")

def tem_mult_ou_div(expressoes):
    for i in expressoes:
        if i in "*/":
            return True
    return False

def gerar_novas_expressoes(expressao, i, var, nao=False):
    exp = []
    if nao:
        for s in range(len(expressao)):
            if (i == s):
                exp.append(var)

            elif ((i+1 != s)):
                exp.append(expressao[s])
    else:
        for s in range(len(expressao)):
            if (i == s):
                exp.append(var)

            elif ((i+1 != s) and (i+2 != s)):
                exp.append(expressao[s])
    return exp

def eh_expressao_booleana(expressoes):
    for i in expressoes:
        if i in ['<', '>', '<=', '>=', '==', '!=', 'nao', 'e', 'ou']:
            return True
    return False

def tem_comparacao(expressoes):
    for i in range(len(expressoes)):
        if (expressoes[i] in ['<', '>', '<=', '>=', '==', '!=']) and (expressoes[i+1] != "nao"):
            return True
    return False

def tem_e(expressoes):
    for i in range(len(expressoes)):
        if (expressoes[i] in ['e']) and (expressoes[i+1] != "nao"):
            return True
    return False

def tem_ou(expressoes):
    for i in range(len(expressoes)):
        if (expressoes[i] in ['ou']) and (expressoes[i+1] != "nao"):
            return True
    return False

def gerar_cte_inicio_funcao(funcoes):
    funcao = funcoes.last()
    if funcao.escrita == Funcao.NAO_ESCRITA:
        funcao.escrita = Funcao.AGUARDANDO_FIM

        file.write(str(funcao.nome) + ":" + "\n")
        file.write("  BeginFunc;\n")

def gerar_cte_fim_funcao(funcoes):
    funcao = funcoes.last()
    if funcao.escrita == Funcao.AGUARDANDO_FIM:
        funcao.escrita = Funcao.ESCRITA
        file.write("  EndFunc;\n")

def gerar_boolean(valor):
    if valor == "verdadeiro":
        return "TRUE"
    elif valor == "falso":
        return "FALSE"

def gerar_label_if():
    labels = []
    for i in range(2):
        labels.append(gerar_label())

    return labels

def gerar_inicio_cte_if(lista, i_token, identacao=False):
    ident = ''
    if identacao:
        ident = "    "
    i = i_token
    expressao = []
    while(lista[i][0] != 'se'):
        if ((lista[i][0] != ')') and (lista[i][0] != '(')):
            expressao.append(lista[i][0])
        i -= 1
    expressao = list(reversed(expressao))

    labels = gerar_label_if()
    if (len(expressao) == 1):        
        file.write(ident + "if !" + gerar_boolean(expressao[0]) + " goto " + str(labels[0])+"\n")
    elif (len(expressao) > 1):
        var_temp = None
        while(len(expressao) > 1):
            var = gerar_var_temp()
            comparacao = tem_comparacao(expressao)
            if comparacao: 
                for s in range(len(expressao)):
                    if (((expressao[s] == '<') or (expressao[s] == '>') or (expressao[s] == '>=') or (expressao[s] == '<=') or (expressao[s] == '==') or (expressao[s] == '!=')) and (expressao[s+1] != 'nao')):
                        file.write(ident + str(var) + " := " + str(expressao[s-1]) + " " + str(expressao[s]) + " " + str(expressao[s+1]) +";\n")
                        expressao = gerar_novas_expressoes(expressao, s-1, var)
                        break
            else:
                tem_and = tem_e(expressao)
                if tem_and:
                    for s in range(len(expressao)):
                        if ((expressao[s] == 'e') and (expressao[s+1] != 'nao')):
                            file.write(ident + str(var) + " := " + str(expressao[s-1]) + " && " + str(expressao[s+1]) +";\n")
                            expressao = gerar_novas_expressoes(expressao, s-1, var)
                            break
                else:
                    tem_or = tem_ou(expressao)
                    if tem_or:
                        for s in range(len(expressao)):
                            if ((expressao[s] == 'ou') and (expressao[s+1] != 'nao')):
                                file.write(ident + str(var) + " := " + str(expressao[s-1]) + " || " + str(expressao[s+1]) +";\n")
                                expressao = gerar_novas_expressoes(expressao, s-1, var)
                                break
                    else:
                        for s in range(len(expressao)):
                            if ((expressao[s-1] == 'nao')):
                                file.write(ident + str(var) + " := !" + str(expressao[s]) + ";\n")
                                expressao = gerar_novas_expressoes(expressao, s-1, var, nao=True)
                                break
            var_temp = var

        file.write(ident + "if !" + var_temp + " goto " + str(labels[0])+"\n")

    return labels

def gerar_label_interno_cte_if(labels, identacao=False):
    ident = ''
    if identacao:
        ident = "    "
    
    file.write(ident + "goto " +str(labels[1])+"\n")
    file.write(ident + str(labels[0])+":\n")

def gerar_label_externo_if(labels, identacao=False):
    ident = ''
    if identacao:
        ident = "    "

    file.write(ident + str(labels[1])+":\n")


def gerar_cte_expressao_while(lista, i_token, identacao=False):
    ident = ''
    if identacao:
        ident = "    "
    i = i_token
    expressao = []
    while(lista[i][0] != 'enquanto'):
        if ((lista[i][0] != ')') and (lista[i][0] != '(')):
            expressao.append(lista[i][0])
        i -= 1
    expressao = list(reversed(expressao))
    
    labels = gerar_label_if()
    if (len(expressao) == 1):        
        file.write(ident + str(labels[0]) + ": if !" + gerar_boolean(expressao[0]) + " goto " + str(labels[1])+"\n")
    elif (len(expressao) > 1):
        var_temp = None
        while(len(expressao) > 1):
            var = gerar_var_temp()
            comparacao = tem_comparacao(expressao)
            if comparacao: 
                for s in range(len(expressao)):
                    if (((expressao[s] == '<') or (expressao[s] == '>') or (expressao[s] == '>=') or (expressao[s] == '<=') or (expressao[s] == '==') or (expressao[s] == '!=')) and (expressao[s+1] != 'nao')):
                        file.write(ident + str(var) + " := " + str(expressao[s-1]) + " " + str(expressao[s]) + " " + str(expressao[s+1]) +";\n")
                        expressao = gerar_novas_expressoes(expressao, s-1, var)
                        break
            else:
                tem_and = tem_e(expressao)
                if tem_and:
                    for s in range(len(expressao)):
                        if ((expressao[s] == 'e') and (expressao[s+1] != 'nao')):
                            file.write(ident + str(var) + " := " + str(expressao[s-1]) + " && " + str(expressao[s+1]) +";\n")
                            expressao = gerar_novas_expressoes(expressao, s-1, var)
                            break
                else:
                    tem_or = tem_ou(expressao)
                    if tem_or:
                        for s in range(len(expressao)):
                            if ((expressao[s] == 'ou') and (expressao[s+1] != 'nao')):
                                file.write(ident + str(var) + " := " + str(expressao[s-1]) + " || " + str(expressao[s+1]) +";\n")
                                expressao = gerar_novas_expressoes(expressao, s-1, var)
                                break
                    else:
                        for s in range(len(expressao)):
                            if ((expressao[s-1] == 'nao')):
                                file.write(ident + str(var) + " := !" + str(expressao[s]) + ";\n")
                                expressao = gerar_novas_expressoes(expressao, s-1, var, nao=True)
                                break

            var_temp = var

        file.write(ident + str(labels[0]) + ": if !" + var_temp + " goto " + str(labels[1])+"\n")
    
    return labels

def gerar_cte_fim_while(labels, identacao=False):
    global l

    ident = ''
    if identacao:
        ident = "    "

    file.write(ident + "goto " + str(l[0]) + "\n")
    file.write(ident + str(l[1]) + ":\n")
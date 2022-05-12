def abrir_arquivo_cte_temp():
    global file
    init()
    file = open('codigo_intermediario.cte', 'w')

def fechar_arquivo_cte_temp():
    global file

    file.close() 

def init():
    global var_i 
    var_i = 1

def gerar_var_temp():
    global var_i
    var = ""
    var = "_temp" + str(var_i)
    var_i += 1
    return var

def gerar_cte_chamada_atribuicao(lista, i_token):
    global file
    i = i_token
    funcao = ''
    parametros = []
    while(lista[i][0] != '='):
        if (lista[i-1][0] == '='):
            funcao = lista[i][0]

        if (lista[i][0] != '(' and lista[i][0] != ',' and lista[i][0] != ')' and lista[i][0] != ';' and lista[i-1][0] != '='):
            parametros.append(lista[i][0])
    
        i -= 1
   
    parametros = list(reversed(parametros))

    for param in parametros:
        file.write("param " + str(param) + "\n")
    var = gerar_var_temp()
    file.write(str(var) + " := call " + str(funcao) + ", " + str(len(parametros)) + "\n")
    file.write(str(lista[i-1][0]) + " := " + str(var) + "\n")



def gerar_cte_expressao_atribuicao(lista, i_token):
    print("Gerador CTE: " + str(lista[i_token]))
    i = i_token
    expressao = []
    while(lista[i][0] != '='):
        if (lista[i][0] != ';'):
            expressao.append(lista[i][0])
        i -= 1
    
    expressao = list(reversed(expressao))
    print("Gerador CTE: " + str(expressao))
    if len(expressao) == 1:
        file.write(str(lista[i-1][0]) + " := " + str(expressao[0] + "\n"))
    elif len(expressao) > 1:
        while(len(expressao) > 1):
            bol_exp = eh_expressao_booleana(expressao)
            if bol_exp:
                var = gerar_var_temp()
                comparacao = tem_comparacao(expressao)
                if comparacao: 
                    for s in range(len(expressao)):
                        if (((expressao[s] == '<') or (expressao[s] == '>') or (expressao[s] == '>=') or (expressao[s] == '<=') or (expressao[s] == '==') or (expressao[s] == '!=')) and (expressao[s+1] != 'nao')):
                            file.write(str(var) + " := " + str(expressao[s-1]) + " " + str(expressao[s]) + " " + str(expressao[s+1]) +"\n")
                            expressao = gerar_novas_expressoes(expressao, s-1, var)
                            break
                else:
                    tem_and = tem_e(expressao)
                    if tem_and:
                        for s in range(len(expressao)):
                            if ((expressao[s] == 'e') and (expressao[s+1] != 'nao')):
                                file.write(str(var) + " := " + str(expressao[s-1]) + " AND " + str(expressao[s+1]) +"\n")
                                expressao = gerar_novas_expressoes(expressao, s-1, var)
                                break
                    else:
                        tem_or = tem_ou(expressao)
                        if tem_or:
                            for s in range(len(expressao)):
                                if ((expressao[s] == 'ou') and (expressao[s+1] != 'nao')):
                                    file.write(str(var) + " := " + str(expressao[s-1]) + " OR " + str(expressao[s+1]) +"\n")
                                    expressao = gerar_novas_expressoes(expressao, s-1, var)
                                    break
                        else:
                            for s in range(len(expressao)):
                                if ((expressao[s-1] == 'nao')):
                                    file.write(str(var) + " := NOT " + str(expressao[s]) + "\n")
                                    expressao = gerar_novas_expressoes(expressao, s-1, var, nao=True)
                                    break

            else:
                var = gerar_var_temp()
                mult_div = tem_mult_ou_div(expressao)
                if mult_div: 
                    for s in range(len(expressao)):
                        if ((expressao[s] == '*') or (expressao[s] == '/')):
                            file.write(str(var) + " := " + str(expressao[s-1]) + " " + str(expressao[s]) + " " + str(expressao[s+1]) +"\n")
                            expressao = gerar_novas_expressoes(expressao, s-1, var)
                            break
                else:
                    for s in range(len(expressao)):
                        if ((expressao[s] == '+') or (expressao[s] == '-')):
                            file.write(str(var) + " := " + str(expressao[s-1]) + " " + str(expressao[s]) + " " + str(expressao[s+1]) +"\n")
                            expressao = gerar_novas_expressoes(expressao, s-1, var)
                            break

        file.write(str(lista[i-1][0]) + " := " + str(expressao[0]) + "\n")

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
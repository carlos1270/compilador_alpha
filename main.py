from src.Exceptions import AnaliseLexicaExeception, AnaliseSintaticaExeception
from src.analise_lexica import analise_lexica
from src.analise_sintatica import analise_sintatica

global tabela_simbolos
tabela_simbolos = []

try:
    tabela_tokens = analise_lexica("palavra.ap")
    tabela_tokens.append(('$', '-1'))
    print(tabela_tokens)
    tabela_simbolos = analise_sintatica(tabela_tokens, tabela_simbolos)
    print(tabela_simbolos)
    for i in tabela_simbolos:
        i.print()
except AnaliseLexicaExeception as e:
    print(e.get_message())
except AnaliseSintaticaExeception as e:
    print(e.get_message())
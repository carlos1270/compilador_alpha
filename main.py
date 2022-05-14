from src.Exceptions import AnaliseLexicaExeception, AnaliseSintaticaExeception, AnaliseSemanticaException
from src.analise_lexica import analise_lexica
from src.analise_sintatica import analise_sintatica
from src.gerador_de_cte import fechar_arquivo_cte_temp

global tabela_simbolos
tabela_simbolos = []

try:
    tabela_tokens = analise_lexica("palavra.ap")
    tabela_tokens.append(('$', '-1'))
    tabela_simbolos = analise_sintatica(tabela_tokens, tabela_simbolos)
    print("===================== TABELA DE SIMBOLOS =====================\n")
    for i in tabela_simbolos:
        i.print()
    
    print("\n===================== X TABELA DE SIMBOLOS X =====================")
    fechar_arquivo_cte_temp()
except AnaliseLexicaExeception as e:
    print(e.get_message())
except AnaliseSintaticaExeception as e:
    print(e.get_message())
    fechar_arquivo_cte_temp()
except AnaliseSemanticaException as e:
    print(e.get_message())
    fechar_arquivo_cte_temp()
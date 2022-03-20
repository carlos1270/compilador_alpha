from src.Exceptions import AnaliseLexicaExeception, AnaliseSintaticaExeception
from src.analise_lexica import analise_lexica
from src.analise_sintatica import analise_sintatica

global tabela_identificadores
tabela_identificadores = []

try:
    tabela_tokens = analise_lexica("palavra.ap")
    arvore_sintatica = analise_sintatica(tabela_tokens)
except AnaliseLexicaExeception as e:
    print(e.get_message())
except AnaliseSintaticaExeception as e:
    print(e.get_message())
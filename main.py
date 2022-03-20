from glob import glob
from src.Exceptions import AnaliseLexicaExeception
from src.analise_lexica import analise_lexica

global tabela_identificadores
tabela_identificadores = []

try:
    tabela_tokens = analise_lexica("palavra.ap")
    print(tabela_tokens)
except AnaliseLexicaExeception as e:
    print(e.get_message())
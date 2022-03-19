from Exceptions import AnaliseLexicaExeception
from src.Exceptions import AnaliseLexicaExeception
from src.analise_lexica import analise_lexica


try:
    tabela_tokens = analise_lexica("palavra.ap")
except AnaliseLexicaExeception as e:
    print(e.get_message())
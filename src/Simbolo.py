
from asyncio.windows_events import NULL


class Simbolo:

    def __init__(self, identificador, valor=None, escopo=None, tipo=None, linha=None):
        if (self.validar_identificador(identificador)):
            self.identificador = identificador
            self.valor = valor
            self.escopo = escopo
            self.tipo = tipo
            self.linha = linha
            self.mutavel = True
            self.parametros = []
        else:
            self.identificador = "#"
            self.valor = valor
            self.escopo = escopo
            self.tipo = tipo
            self.linha = linha
            self.mutavel = True
            self.parametros = []
            

    def validar_identificador(self, identificador):
        palavras_reservadas = [
            'prog', 'const', 'verdadeiro', 'falso', 'inteiro', 'booleano',
            'func', 'vazio', 'func', 'se', 'senao', 'enquanto', 'retorno',
            'pare', 'pule', 'nao', 'e', 'ou'
        ]

        for i in range(len(palavras_reservadas)):
            if (identificador == palavras_reservadas[i]):
                return False
        
        return True

    def print(self):
        print("Identificador: " + str(self.identificador) + ", Valor: " + str(self.valor) + ", Escopo: " + str(self.escopo) + ", Tipo: " + str(self.tipo) + ", Linha: " + str(self.linha) + ", Parametros: " + str(self.parametros))
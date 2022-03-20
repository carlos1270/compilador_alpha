from distutils import extension
from shutil import ExecError

class CustomizeExeception(Exception):
    def __init__(self, message):
        super().__init__(message)

    def get_message(self):
        return super().__str__()

class AnaliseLexicaExeception(CustomizeExeception):
    def __init__(self, message):
        super().__init__(message)

class AnaliseSintaticaExeception(CustomizeExeception):
    def __init__(self, message):
        super().__init__("Erro de análise sintática:" + message)

class EsperaPontoVirgulaExeception(AnaliseSintaticaExeception):
    def __init__(self, message):
        super().__init__(message)

class IdentificadorInvalidoExeception(AnaliseSintaticaExeception):
    def __init__(self, message):
        super().__init__(message)

class ProgramaSemIdentificadorExeception(AnaliseSintaticaExeception):
    def __init__(self, message):
        super().__init__(message)
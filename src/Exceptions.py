from distutils import extension
from shutil import ExecError


class AnaliseLexicaExeception(Exception):
    def __init__(self, message):
        super().__init__(message)

    def get_message(self):
        return self.message
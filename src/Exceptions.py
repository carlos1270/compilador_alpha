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
        super().__init__("Erro de análise sintática: " + message)

class EsperaPontoVirgulaExeception(AnaliseSintaticaExeception):
    def __init__(self, message):
        super().__init__(message)

class IdentificadorInvalidoExeception(AnaliseSintaticaExeception):
    def __init__(self, message):
        super().__init__(message)

class ProgramaSemIdentificadorExeception(AnaliseSintaticaExeception):
    def __init__(self, message):
        super().__init__(message)

class TipoConstanteInvalidoException(AnaliseSintaticaExeception):
    def __init__(self, message):
        super().__init__(message)
    
class DeclaracaoDeConstateException(AnaliseSintaticaExeception):
    def __init__(self, message):
        super().__init__(message)

class EsperadoAtribuicaoException(AnaliseSintaticaExeception):
    def __init__(self, message):
        super().__init__(message)

class ConstanteInvalidaException(AnaliseSintaticaExeception):
    def __init__(self, message):
        super().__init__(message)

class NumeroInteiroInvalidoException(AnaliseSintaticaExeception):
    def __init__(self, message):
        super().__init__(message)

class BooleanoInvalidoException(AnaliseSintaticaExeception):
    def __init__(self, message):
        super().__init__(message)

class TipoDeSubRotinaInvalidaException(AnaliseSintaticaExeception):
    def __init__(self, message):
        super().__init__(message)

class EsperadoParentesesExeception(AnaliseSintaticaExeception):
    def __init__(self, message):
        super().__init__(message)

class EsperadoChavesExeception(AnaliseSintaticaExeception):
    def __init__(self, message):
        super().__init__(message)

class EsperadoChavesExeception(AnaliseSintaticaExeception):
    def __init__(self, message):
        super().__init__(message)

class ComandoNaoIdentificadoExecption(AnaliseSintaticaExeception):
    def __init__(self, message):
        super().__init__(message)

class ExpressaoBooleanaInvalidaExecption(AnaliseSintaticaExeception):
    def __init__(self, message):
        super().__init__(message)

class OperadorInvalidoException(AnaliseSintaticaExeception):
    def __init__(self, message):
        super().__init__(message)

class ComandoCondicionalIfException(AnaliseSintaticaExeception):
    def __init__(self, message):
        super().__init__(message)

class ComandoCondicionalElseException(AnaliseSintaticaExeception):
    def __init__(self, message):
        super().__init__(message)

class TermoInvalidoException(AnaliseSintaticaExeception):
    def __init__(self, message):
        super().__init__(message)

class NaoEhPermitidaDeclaracaoException(AnaliseSintaticaExeception):
    def __init__(self, message):
        super().__init__(message)

class PalavrasReservadasComandoException(AnaliseSintaticaExeception):
    def __init__(self, message):
        super().__init__(message)

class EsperadoComandoException(AnaliseSintaticaExeception):
    def __init__(self, message):
        super().__init__(message)

class ComandoAtribuicaoException(AnaliseSintaticaExeception):
    def __init__(self, message):
        super().__init__(message)

class ExpressaoNumericaInvalidaException(AnaliseSintaticaExeception):
    def __init__(self, message):
        super().__init__(message)

class ExpressaoAritmeticaInvalidaException(AnaliseSintaticaExeception):
    def __init__(self, message):
        super().__init__(message)

class ExpressaoInvalidaException(AnaliseSintaticaExeception):
    def __init__(self, message):
        super().__init__(message)

class RelacaoAritmeticaInvalidaException(AnaliseSintaticaExeception):
    def __init__(self, message):
        super().__init__(message)

class ComandoDeRetornoDeValorInvalidoException(AnaliseSintaticaExeception):
    def __init__(self, message):
        super().__init__(message)

class ComandoIncondicionalInvalidoException(AnaliseSintaticaExeception):
    def __init__(self, message):
        super().__init__(message)

class AnaliseSemanticaException(CustomizeExeception):
    def __init__(self, message):
        super().__init__("Erro de análise semântica: " + message)

class VariavelNaoDeclaradaException(AnaliseSemanticaException):
    def __init__(self, message):
        super().__init__(message)

class FuncaoNaoDeclaradaException(AnaliseSemanticaException):
    def __init__(self, message):
        super().__init__(message)

class FuncaoJaDeclaradaException(AnaliseSemanticaException):
    def __init__(self, message):
        super().__init__(message)

class RetornoInvalidoException(AnaliseSemanticaException):
    def __init__(self, message):
        super().__init__(message)

class RetornoFuncaoTipoVariavelException(AnaliseSemanticaException):
    def __init__(self, message):
        super().__init__(message) 

class QuantidadeParametrosDiferenteExeception(AnaliseSemanticaException):
    def __init__(self, message):
        super().__init__(message) 

class TipoDeParametroDiferenteExeception(AnaliseSemanticaException):
    def __init__(self, message):
        super().__init__(message) 

class TipoAtribuicaoConstanteException(AnaliseSemanticaException):
    def __init__(self, message):
        super().__init__(message) 

class VariavelNaoNumericaEmExpressaoNumericaException(AnaliseSemanticaException):
    def __init__(self, message):
        super().__init__(message)

class VariavelNumericaEmOperacaoBoolenaException(AnaliseSemanticaException):
    def __init__(self, message):
        super().__init__(message)

class ValorNumericoEmOperacaoBoolenaException(AnaliseSemanticaException):
    def __init__(self, message):
        super().__init__(message)

class RelacaoNumericaEntreTermosNaoInteirosException(AnaliseSemanticaException):
    def __init__(self, message):
        super().__init__(message)

class RelacaoEntreTermosDeTiposDiferentesException(AnaliseSemanticaException):
    def __init__(self, message):
        super().__init__(message)

class ValorDaExpressaoDiferenteDoTipoDaAtribuicaoException(AnaliseSemanticaException):
    def __init__(self, message):
        super().__init__(message)
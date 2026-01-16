class Cores:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    PRETO = '\033[30m'
    VERMELHO = '\033[31m'
    VERDE = '\033[32m'
    AMARELO = '\033[33m'
    AZUL = '\033[34m'
    MAGENTA = '\033[35m'
    CIANO = '\033[36m'
    BRANCO = '\033[37m'
    FUNDO_PRETO = '\033[40m'
    FUNDO_VERMELHO = '\033[41m'
    FUNDO_VERDE = '\033[42m'
    FUNDO_AMARELO = '\033[43m'
    FUNDO_AZUL = '\033[44m'
    FUNDO_MAGENTA = '\033[45m'
    FUNDO_CIANO = '\033[46m'
    FUNDO_BRANCO = '\033[47m'

    @staticmethod
    def texto(texto: str, cor: str = '', negrito: bool = False) -> str:
        resultado = cor
        if negrito:
            resultado += Cores.BOLD
        resultado += texto + Cores.RESET
        return resultado

    @staticmethod
    def sucesso(texto: str) -> str:
        return Cores.texto(texto, Cores.VERDE)

    @staticmethod
    def erro(texto: str) -> str:
        return Cores.texto(texto, Cores.VERMELHO)

    @staticmethod
    def aviso(texto: str) -> str:
        return Cores.texto(texto, Cores.AMARELO)

    @staticmethod
    def info(texto: str) -> str:
        return Cores.texto(texto, Cores.CIANO)

    @staticmethod
    def titulo(texto: str) -> str:
        return Cores.texto(texto, Cores.MAGENTA, negrito=True)

    @staticmethod
    def destaque(texto: str) -> str:
        return Cores.texto(texto, Cores.BRANCO, negrito=True)

    @staticmethod
    def linha_separadora() -> str:
        return Cores.texto("=" * 60, Cores.CIANO)

    @staticmethod
    def menu_item(numero: str, texto: str) -> str:
        return f"  {Cores.texto(numero, Cores.AMARELO)}. {texto}"

    @staticmethod
    def opcao_deslogar() -> str:
        return Cores.menu_item("0", Cores.texto("Deslogar", Cores.VERMELHO))

    @staticmethod
    def opcao_voltar() -> str:
        return Cores.menu_item("0", Cores.texto("Voltar", Cores.VERMELHO))

    @staticmethod
    def opcao_sair() -> str:
        return Cores.menu_item("0", Cores.texto("Sair", Cores.VERMELHO))

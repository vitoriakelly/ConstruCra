from sistema import SistemaGestaoProjetos
from interface import Interface
from cores import Cores


def main():
    sistema = SistemaGestaoProjetos()
    interface = Interface(sistema)

    if sistema.carregar_dados():
        print(f"\n{Cores.sucesso('✓ Dados carregados com sucesso!')}")
    else:
        print(f"\n{Cores.info('ℹ Nenhum dado anterior encontrado. Iniciando sistema novo.')}")

    print(f"\n{Cores.linha_separadora()}")
    print(f"  {Cores.titulo('BEM-VINDO AO SISTEMA DE GESTÃO DE PROJETOS DE ENGENHARIA')}")
    print(Cores.linha_separadora())
    print(f"\n{Cores.sucesso('Sistema iniciado com sucesso!')}")
    input(f"\n{Cores.info('Pressione Enter para continuar...')}")

    try:
        interface.executar()
    finally:
        if sistema.salvar_dados():
            print(f"\n{Cores.sucesso('✓ Dados salvos com sucesso!')}")
        else:
            print(f"\n{Cores.aviso('⚠ Aviso: Não foi possível salvar os dados.')}")


if __name__ == "__main__":
    main()

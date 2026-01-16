"""
Exemplo de uso do Sistema de Gestão de Projetos de Engenharia
Este arquivo demonstra como usar o sistema programaticamente
"""

from sistema import SistemaGestaoProjetos
from models import TipoUsuario
from datetime import datetime, timedelta


def exemplo_uso():
    """Demonstra o uso básico do sistema"""
    
    # Cria instância do sistema
    sistema = SistemaGestaoProjetos()
    
    print("=" * 60)
    print("EXEMPLO DE USO DO SISTEMA")
    print("=" * 60)
    
    # 1. Cadastro de usuários
    print("\n1. Cadastrando usuários...")
    sistema.cadastrar_usuario("João Silva", "joao@eng.com", "senha123", TipoUsuario.GESTOR)
    sistema.cadastrar_usuario("Maria Santos", "maria@eng.com", "senha456", TipoUsuario.ENGENHEIRO)
    sistema.cadastrar_usuario("Pedro Costa", "pedro@eng.com", "senha789", TipoUsuario.ENGENHEIRO)
    print("✓ Usuários cadastrados")
    
    # 2. Login
    print("\n2. Fazendo login como gestor...")
    sistema.login("joao@eng.com", "senha123")
    print(f"✓ Logado como: {sistema.usuario_logado.nome}")
    
    # 3. Criar projeto
    print("\n3. Criando projeto...")
    projeto = sistema.criar_projeto(
        "Construção de Edifício Residencial",
        "Projeto de construção de edifício de 10 andares"
    )
    print(f"✓ Projeto criado: {projeto.nome} (ID: {projeto.id})")
    
    # 4. Cadastrar engenheiro (gestor)
    print("\n4. Cadastrando engenheiro...")
    sistema.cadastrar_engenheiro("Ana Lima", "ana@eng.com", "senha321")
    print("✓ Engenheiro cadastrado")
    
    # 5. Adicionar materiais
    print("\n5. Adicionando materiais...")
    sistema.adicionar_material(projeto.id, "Cimento", 25.50, 100, "saco")
    sistema.adicionar_material(projeto.id, "Tijolo", 0.80, 5000, "un")
    sistema.adicionar_material(projeto.id, "Aço", 15.00, 200, "kg")
    print("✓ Materiais adicionados")
    
    # 6. Adicionar coordenadas
    print("\n6. Adicionando coordenadas...")
    sistema.adicionar_coordenada(projeto.id, 10.5, 20.3, 0.0, "Entrada principal")
    sistema.adicionar_coordenada(projeto.id, 15.2, 25.7, 0.0, "Área de estacionamento")
    sistema.adicionar_coordenada(projeto.id, 12.0, 18.5, 3.5, "Segundo andar")
    print("✓ Coordenadas adicionadas")
    
    # 7. Criar matriz da planta
    print("\n7. Criando matriz da planta...")
    sistema.criar_matriz_planta(projeto.id, 5, 5)
    sistema.atualizar_matriz_planta(projeto.id, 0, 0, "E")  # Entrada
    sistema.atualizar_matriz_planta(projeto.id, 2, 2, "C")  # Centro
    sistema.atualizar_matriz_planta(projeto.id, 4, 4, "S")  # Saída
    print("✓ Matriz da planta criada")
    
    # 8. Criar tarefas
    print("\n8. Criando tarefas...")
    # Buscar IDs dos engenheiros
    engenheiros = [u for u in sistema.usuarios.values() if u.tipo == TipoUsuario.ENGENHEIRO]
    maria_id = next(u.id for u in engenheiros if u.email == "maria@eng.com")
    pedro_id = next(u.id for u in engenheiros if u.email == "pedro@eng.com")
    
    prazo1 = datetime.now() + timedelta(days=7)
    prazo2 = datetime.now() + timedelta(days=14)
    
    tarefa1 = sistema.criar_tarefa(
        "Levantamento topográfico",
        "Realizar levantamento topográfico do terreno",
        maria_id,
        prazo1,
        projeto.id
    )
    
    tarefa2 = sistema.criar_tarefa(
        "Projeto estrutural",
        "Desenvolver projeto estrutural completo",
        pedro_id,
        prazo2,
        projeto.id
    )
    
    print(f"✓ Tarefas criadas: {tarefa1.titulo}, {tarefa2.titulo}")
    
    # 9. Registrar consumo semanal
    print("\n9. Registrando consumo semanal...")
    consumo_semana_0 = {
        "Cimento": 10.0,
        "Tijolo": 500.0,
        "Aço": 50.0
    }
    sistema.registrar_consumo_semanal(projeto.id, 0, consumo_semana_0)
    
    consumo_semana_1 = {
        "Cimento": 15.0,
        "Tijolo": 800.0,
        "Aço": 75.0
    }
    sistema.registrar_consumo_semanal(projeto.id, 1, consumo_semana_1)
    print("✓ Consumo semanal registrado")
    
    # 10. Gerar relatórios
    print("\n10. Gerando relatórios...")
    relatorio_semana = sistema.relatorio_soma_por_semana(projeto.id)
    relatorio_material = sistema.relatorio_soma_por_material(projeto.id)
    
    print("\nRelatório por Semana:")
    for semana, soma in relatorio_semana.items():
        print(f"  Semana {semana}: {soma:.2f}")
    
    print("\nRelatório por Material:")
    for material, soma in relatorio_material.items():
        print(f"  {material}: {soma:.2f}")
    
    # 11. Calcular custo total
    print("\n11. Calculando custo total...")
    custo_total = sistema.calcular_custo_total_projeto(projeto.id)
    print(f"✓ Custo total do projeto: R$ {custo_total:.2f}")
    
    # 12. Buscar projeto
    print("\n12. Buscando projeto...")
    resultados = sistema.buscar_projeto("edifício")
    print(f"✓ {len(resultados)} projeto(s) encontrado(s)")
    
    # 13. Verificar estoque
    print("\n13. Verificando estoque...")
    materiais_baixos = sistema.verificar_estoque_insuficiente(projeto.id)
    if materiais_baixos:
        print("⚠ Materiais com estoque baixo:")
        for material in materiais_baixos:
            print(f"  - {material.nome}: {material.estoque} {material.unidade}")
    else:
        print("✓ Todos os materiais estão com estoque adequado")
    
    # 14. Consultar coordenadas
    print("\n14. Consultando coordenadas...")
    coordenadas = sistema.consultar_coordenadas(projeto.id)
    print(f"✓ {len(coordenadas)} coordenada(s) cadastrada(s)")
    for coord in coordenadas:
        print(f"  {coord}")
    
    # 15. Imprimir matriz da planta
    print("\n15. Imprimindo matriz da planta...")
    matriz = sistema.imprimir_matriz_planta(projeto.id)
    if matriz:
        print("Layout da Planta:")
        for linha in matriz:
            print("  " + " ".join(linha))
    
    # 16. Dividir recursos
    print("\n16. Dividindo recursos...")
    quociente, resto = sistema.dividir_recursos(10000.0, 3)
    print(f"✓ R$ 10.000,00 dividido entre 3 pessoas:")
    print(f"  Quociente: R$ {quociente:.2f}")
    print(f"  Resto: R$ {resto:.2f}")
    
    # 17. Verificar notificações
    print("\n17. Verificando notificações...")
    notificacoes = sistema.obter_notificacoes(nao_lidas=True)
    print(f"✓ {len(notificacoes)} notificação(ões) não lida(s)")
    for notif in notificacoes[:3]:  # Mostra apenas as 3 primeiras
        print(f"  {notif}")
    
    # 18. Projetos mais ativos
    print("\n18. Projetos mais ativos...")
    projetos_ativos = sistema.projetos_mais_ativos(3)
    print(f"✓ Top {len(projetos_ativos)} projetos mais ativos:")
    for projeto, num_tarefas in projetos_ativos:
        print(f"  - {projeto.nome}: {num_tarefas} tarefas ativas")
    
    # 19. Tarefas por engenheiro
    print("\n19. Estatísticas de tarefas por engenheiro...")
    stats_eng = sistema.tarefas_por_engenheiro()
    print("✓ Estatísticas:")
    for nome, stats in stats_eng.items():
        print(f"  {nome}: {stats['total']} tarefas ({stats['concluidas']} concluídas)")
    
    # 20. Estatísticas gerais
    print("\n20. Estatísticas gerais da plataforma...")
    stats_gerais = sistema.estatisticas_gerais_plataforma()
    print(f"✓ Total de projetos: {stats_gerais['total_projetos']}")
    print(f"✓ Total de tarefas: {stats_gerais['total_tarefas']}")
    print(f"✓ Engenheiros ativos: {stats_gerais['engenheiros_ativos']}/{stats_gerais['total_engenheiros']}")
    print(f"✓ Taxa de conclusão: {(stats_gerais['tarefas_concluidas']/stats_gerais['total_tarefas']*100):.1f}%" if stats_gerais['total_tarefas'] > 0 else "✓ Taxa de conclusão: 0%")
    
    print("\n" + "=" * 60)
    print("EXEMPLO CONCLUÍDO COM SUCESSO!")
    print("=" * 60)


if __name__ == "__main__":
    exemplo_uso()

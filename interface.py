import os
from datetime import datetime, timedelta
from typing import Optional
from sistema import SistemaGestaoProjetos
from models import TipoUsuario, StatusTarefa, CategoriaMaterial
from cores import Cores


class Interface:
    def __init__(self, sistema: SistemaGestaoProjetos):
        self.sistema = sistema
    
    def limpar_tela(self):
        os.system('clear' if os.name != 'nt' else 'cls')
    
    def exibir_titulo(self, titulo: str):
        print(f"\n{Cores.linha_separadora()}")
        print(f"  {Cores.titulo(titulo)}")
        print(Cores.linha_separadora())
    
    def executar(self):
        while True:
            self.exibir_menu_principal()
            opcao = input(f"\n{Cores.info('Escolha uma opção: ')}")
            
            if not self.sistema.usuario_logado:
                if opcao == "1":
                    self.cadastrar_usuario()
                elif opcao == "2":
                    self.fazer_login()
                elif opcao == "0":
                    break
            else:
                usuario = self.sistema.usuario_logado
                if opcao == "1":
                    self.menu_projetos()
                elif opcao == "2":
                    self.menu_tarefas()
                elif usuario.tipo == TipoUsuario.GESTOR:
                    if opcao == "3":
                        self.menu_materiais()
                    elif opcao == "4":
                        self.menu_coordenadas()
                    elif opcao == "5":
                        self.menu_relatorios()
                    elif opcao == "6":
                        self.menu_calculos()
                    elif opcao == "7":
                        self.menu_estatisticas()
                    elif opcao == "8":
                        self.menu_funcionalidades_extras()
                    elif opcao == "9":
                        self.ver_notificacoes()
                    elif opcao == "10":
                        self.buscar_projeto_interface()
                    elif opcao == "0":
                        self.sistema.logout()
                        print(f"\n{Cores.sucesso('Deslogado com sucesso!')}")
                        input(f"{Cores.info('Pressione Enter para continuar...')}")
                else:
                    if opcao == "3":
                        self.ver_notificacoes()
                    elif opcao == "4":
                        self.buscar_projeto_interface()
                    elif opcao == "0":
                        self.sistema.logout()
                        print(f"\n{Cores.sucesso('Deslogado com sucesso!')}")
                        input(f"{Cores.info('Pressione Enter para continuar...')}")
    
    def exibir_menu_principal(self):
        self.limpar_tela()
        self.exibir_titulo("SISTEMA DE GESTÃO DE PROJETOS DE ENGENHARIA")
        
        if self.sistema.usuario_logado:
            usuario = self.sistema.usuario_logado
            tipo_cor = Cores.VERDE if usuario.tipo == TipoUsuario.GESTOR else Cores.AZUL
            print(f"\n{Cores.info('👤 Usuário logado:')} {Cores.destaque(usuario.nome)} ({Cores.texto(usuario.tipo.value, tipo_cor)})")
            print(f"\n{Cores.titulo('📋 OPÇÕES DISPONÍVEIS:')}\n")
            print(Cores.menu_item("1", "📁 Menu de Projetos"))
            print(Cores.menu_item("2", "✅ Menu de Tarefas"))
            if usuario.tipo == TipoUsuario.GESTOR:
                print(Cores.menu_item("3", "📦 Menu de Materiais"))
                print(Cores.menu_item("4", "📍 Menu de Coordenadas"))
                print(Cores.menu_item("5", "📊 Menu de Relatórios"))
                print(Cores.menu_item("6", "🔢 Menu de Cálculos"))
                print(Cores.menu_item("7", "📈 Menu de Estatísticas"))
                print(Cores.menu_item("8", "⭐ Menu de Funcionalidades Extras"))
                print(Cores.menu_item("9", "🔔 Notificações"))
                print(Cores.menu_item("10", "🔍 Buscar Projeto"))
            else:
                print(Cores.menu_item("3", "🔔 Notificações"))
                print(Cores.menu_item("4", "🔍 Buscar Projeto"))
            print(Cores.opcao_deslogar())
        else:
            print(f"\n{Cores.titulo('📋 OPÇÕES DISPONÍVEIS:')}\n")
            print(Cores.menu_item("1", "➕ Cadastrar-se"))
            print(Cores.menu_item("2", "🔐 Login"))
            print(Cores.opcao_sair())
    
    def cadastrar_usuario(self):
        self.limpar_tela()
        self.exibir_titulo("CADASTRO DE USUÁRIO")
        nome = input(f"{Cores.info('Nome: ')}")
        email = input(f"{Cores.info('Email: ')}")
        senha = input(f"{Cores.info('Senha: ')}")
        print(f"\n{Cores.info('Tipo de usuário:')}")
        print("1. Engenheiro")
        print("2. Gestor")
        tipo_op = input(f"{Cores.info('Escolha (1 ou 2): ')}")
        tipo = TipoUsuario.ENGENHEIRO if tipo_op == "1" else TipoUsuario.GESTOR
        
        if self.sistema.cadastrar_usuario(nome, email, senha, tipo):
            print(f"\n{Cores.sucesso('✓ Usuário cadastrado com sucesso!')}")
        else:
            print(f"\n{Cores.erro('✗ Erro: Email já cadastrado.')}")
        input(f"\n{Cores.info('Pressione Enter para continuar...')}")
    
    def fazer_login(self):
        self.limpar_tela()
        self.exibir_titulo("LOGIN")
        email = input(f"{Cores.info('Email: ')}")
        senha = input(f"{Cores.info('Senha: ')}")
        
        if self.sistema.login(email, senha):
            print(f"\n{Cores.sucesso('✓ Login realizado com sucesso!')}")
        else:
            print(f"\n{Cores.erro('✗ Erro: Email ou senha incorretos.')}")
        input(f"\n{Cores.info('Pressione Enter para continuar...')}")
    
    def menu_projetos(self):
        while True:
            self.limpar_tela()
            self.exibir_titulo("MENU DE PROJETOS")
            print(Cores.menu_item("1", "Criar Projeto"))
            print(Cores.menu_item("2", "Listar Projetos"))
            print(Cores.menu_item("3", "Ver Detalhes do Projeto"))
            print(Cores.opcao_voltar())
            opcao = input(f"\n{Cores.info('Escolha uma opção: ')}")
            
            if opcao == "1":
                self.criar_projeto()
            elif opcao == "2":
                self.listar_projetos()
            elif opcao == "3":
                self.ver_detalhes_projeto()
            elif opcao == "0":
                break
    
    def criar_projeto(self):
        self.limpar_tela()
        self.exibir_titulo("CRIAR PROJETO")
        nome = input(f"{Cores.info('Nome do projeto: ')}")
        descricao = input(f"{Cores.info('Descrição: ')}")
        gasto = float(input(f"{Cores.info('Gasto inicial: ')}") or "0")
        lucro = float(input(f"{Cores.info('Lucro esperado: ')}") or "0")
        
        prazo_str = input(f"{Cores.info('Prazo (DD/MM/YYYY ou Enter para pular): ')}")
        prazo = None
        if prazo_str:
            try:
                prazo = datetime.strptime(prazo_str, "%d/%m/%Y")
            except:
                print(f"{Cores.aviso('⚠ Formato inválido, ignorando prazo.')}")
        
        responsavel_id = None
        if self.sistema.usuario_logado.tipo == TipoUsuario.GESTOR:
            engenheiros = [u for u in self.sistema.usuarios.values() if u.tipo == TipoUsuario.ENGENHEIRO]
            if engenheiros:
                print(f"\n{Cores.info('Engenheiros disponíveis:')}")
                for i, eng in enumerate(engenheiros, 1):
                    print(f"  {i}. {eng.nome} ({eng.email})")
                resp_op = input(f"{Cores.info('ID do responsável (ou Enter para nenhum): ')}")
                if resp_op:
                    try:
                        responsavel_id = int(resp_op)
                    except:
                        pass
        
        projeto = self.sistema.criar_projeto(nome, descricao, gasto, lucro, prazo, responsavel_id)
        if projeto:
            print(f"\n{Cores.sucesso('✓ Projeto criado com sucesso!')}")
            print(f"  ID: {projeto.id}")
        else:
            print(f"\n{Cores.erro('✗ Erro ao criar projeto.')}")
        input(f"\n{Cores.info('Pressione Enter para continuar...')}")
    
    def listar_projetos(self):
        self.limpar_tela()
        self.exibir_titulo("LISTA DE PROJETOS")
        projetos = list(self.sistema.projetos.values())
        if not projetos:
            print(f"{Cores.aviso('⚠ Nenhum projeto cadastrado.')}")
        else:
            for i, projeto in enumerate(projetos, 1):
                status_cor = Cores.VERDE if projeto.status.value == "ativo" else Cores.AMARELO
                print(f"\n{i}. {Cores.destaque(projeto.nome)}")
                print(f"   Status: {Cores.texto(projeto.status.value.upper(), status_cor)}")
                print(f"   Descrição: {projeto.descricao}")
                print(f"   Tarefas: {len(projeto.tarefas)}")
        input(f"\n{Cores.info('Pressione Enter para continuar...')}")
    
    def ver_detalhes_projeto(self):
        self.limpar_tela()
        self.exibir_titulo("DETALHES DO PROJETO")
        projetos = list(self.sistema.projetos.values())
        if not projetos:
            print(f"{Cores.aviso('⚠ Nenhum projeto cadastrado.')}")
            input(f"\n{Cores.info('Pressione Enter para continuar...')}")
            return
        
        for i, projeto in enumerate(projetos, 1):
            print(f"{i}. {projeto.nome}")
        opcao = input(f"\n{Cores.info('Escolha o projeto: ')}")
        try:
            idx = int(opcao) - 1
            if 0 <= idx < len(projetos):
                projeto = projetos[idx]
                print(f"\n{Cores.destaque('Nome:')} {projeto.nome}")
                print(f"{Cores.destaque('Descrição:')} {projeto.descricao}")
                print(f"{Cores.destaque('Status:')} {projeto.status.value}")
                print(f"{Cores.destaque('Gasto:')} R$ {projeto.gasto:.2f}")
                print(f"{Cores.destaque('Lucro:')} R$ {projeto.lucro:.2f}")
                if projeto.prazo:
                    print(f"{Cores.destaque('Prazo:')} {projeto.prazo.strftime('%d/%m/%Y')}")
                print(f"{Cores.destaque('Tarefas:')} {len(projeto.tarefas)}")
                print(f"{Cores.destaque('Materiais:')} {len(projeto.materiais)}")
                print(f"{Cores.destaque('Coordenadas:')} {len(projeto.coordenadas)}")
        except:
            print(f"{Cores.erro('✗ Opção inválida.')}")
        input(f"\n{Cores.info('Pressione Enter para continuar...')}")
    
    def menu_tarefas(self):
        while True:
            self.limpar_tela()
            self.exibir_titulo("MENU DE TAREFAS")
            print(Cores.menu_item("1", "Criar Tarefa"))
            print(Cores.menu_item("2", "Listar Tarefas"))
            print(Cores.menu_item("3", "Concluir Tarefa"))
            print(Cores.opcao_voltar())
            opcao = input(f"\n{Cores.info('Escolha uma opção: ')}")
            
            if opcao == "1":
                self.criar_tarefa()
            elif opcao == "2":
                self.listar_tarefas()
            elif opcao == "3":
                self.concluir_tarefa()
            elif opcao == "0":
                break
    
    def criar_tarefa(self):
        self.limpar_tela()
        self.exibir_titulo("CRIAR TAREFA")
        projetos = list(self.sistema.projetos.values())
        if not projetos:
            print(f"{Cores.aviso('⚠ Nenhum projeto cadastrado.')}")
            input(f"\n{Cores.info('Pressione Enter para continuar...')}")
            return
        
        for i, projeto in enumerate(projetos, 1):
            print(f"{i}. {projeto.nome}")
        proj_op = input(f"\n{Cores.info('Escolha o projeto: ')}")
        try:
            idx = int(proj_op) - 1
            if 0 <= idx < len(projetos):
                projeto = projetos[idx]
                titulo = input(f"{Cores.info('Título: ')}")
                descricao = input(f"{Cores.info('Descrição: ')}")
                prazo_str = input(f"{Cores.info('Prazo (DD/MM/YYYY ou Enter): ')}")
                prazo = None
                if prazo_str:
                    try:
                        prazo = datetime.strptime(prazo_str, "%d/%m/%Y")
                    except:
                        pass
                
                responsavel_id = self.sistema.usuario_logado.id
                if self.sistema.usuario_logado.tipo == TipoUsuario.GESTOR:
                    engenheiros = [u for u in self.sistema.usuarios.values() if u.tipo == TipoUsuario.ENGENHEIRO]
                    if engenheiros:
                        for i, eng in enumerate(engenheiros, 1):
                            print(f"{i}. {eng.nome}")
                        resp_op = input(f"{Cores.info('Escolha o engenheiro: ')}")
                        try:
                            resp_idx = int(resp_op) - 1
                            if 0 <= resp_idx < len(engenheiros):
                                responsavel_id = engenheiros[resp_idx].id
                        except:
                            pass
                
                tarefa = self.sistema.criar_tarefa(titulo, descricao, responsavel_id, prazo, projeto.id)
                if tarefa:
                    print(f"\n{Cores.sucesso('✓ Tarefa criada com sucesso!')}")
                else:
                    print(f"\n{Cores.erro('✗ Erro ao criar tarefa.')}")
            else:
                print(f"{Cores.erro('✗ Projeto inválido.')}")
        except:
            print(f"{Cores.erro('✗ Opção inválida.')}")
        input(f"\n{Cores.info('Pressione Enter para continuar...')}")
    
    def listar_tarefas(self):
        self.limpar_tela()
        self.exibir_titulo("LISTA DE TAREFAS")
        todas_tarefas = []
        for projeto in self.sistema.projetos.values():
            todas_tarefas.extend(projeto.tarefas)
        
        if not todas_tarefas:
            print(f"{Cores.aviso('⚠ Nenhuma tarefa cadastrada.')}")
        else:
            for tarefa in todas_tarefas:
                status_cor = Cores.VERDE if tarefa.status == StatusTarefa.CONCLUIDA else Cores.AMARELO
                print(f"\n{Cores.destaque(tarefa.titulo)}")
                print(f"   Status: {Cores.texto(tarefa.status.value, status_cor)}")
                print(f"   Descrição: {tarefa.descricao}")
                if tarefa.prazo:
                    print(f"   Prazo: {tarefa.prazo.strftime('%d/%m/%Y')}")
        input(f"\n{Cores.info('Pressione Enter para continuar...')}")
    
    def concluir_tarefa(self):
        self.limpar_tela()
        self.exibir_titulo("CONCLUIR TAREFA")
        todas_tarefas = []
        for projeto in self.sistema.projetos.values():
            todas_tarefas.extend([(t, projeto) for t in projeto.tarefas if t.status != StatusTarefa.CONCLUIDA])
        
        if not todas_tarefas:
            print(f"{Cores.aviso('⚠ Nenhuma tarefa pendente.')}")
            input(f"\n{Cores.info('Pressione Enter para continuar...')}")
            return
        
        for i, (tarefa, projeto) in enumerate(todas_tarefas, 1):
            print(f"{i}. {tarefa.titulo} - {projeto.nome}")
        opcao = input(f"\n{Cores.info('Escolha a tarefa: ')}")
        try:
            idx = int(opcao) - 1
            if 0 <= idx < len(todas_tarefas):
                tarefa, projeto = todas_tarefas[idx]
                tarefa.status = StatusTarefa.CONCLUIDA
                tarefa.data_conclusao = datetime.now()
                print(f"\n{Cores.sucesso('✓ Tarefa concluída!')}")
            else:
                print(f"{Cores.erro('✗ Opção inválida.')}")
        except:
            print(f"{Cores.erro('✗ Opção inválida.')}")
        input(f"\n{Cores.info('Pressione Enter para continuar...')}")
    
    def menu_materiais(self):
        while True:
            self.limpar_tela()
            self.exibir_titulo("MENU DE MATERIAIS")
            print(Cores.menu_item("1", "Adicionar Material"))
            print(Cores.menu_item("2", "Listar Materiais"))
            print(Cores.menu_item("3", "Registrar Consumo Semanal"))
            print(Cores.opcao_voltar())
            opcao = input(f"\n{Cores.info('Escolha uma opção: ')}")
            
            if opcao == "1":
                self.adicionar_material()
            elif opcao == "2":
                self.listar_materiais()
            elif opcao == "3":
                self.registrar_consumo_semanal()
            elif opcao == "0":
                break
    
    def adicionar_material(self):
        self.limpar_tela()
        self.exibir_titulo("ADICIONAR MATERIAL")
        projetos = list(self.sistema.projetos.values())
        if not projetos:
            print(f"{Cores.aviso('⚠ Nenhum projeto cadastrado.')}")
            input(f"\n{Cores.info('Pressione Enter para continuar...')}")
            return
        
        for i, projeto in enumerate(projetos, 1):
            print(f"{i}. {projeto.nome}")
        proj_op = input(f"\n{Cores.info('Escolha o projeto: ')}")
        try:
            idx = int(proj_op) - 1
            if 0 <= idx < len(projetos):
                projeto = projetos[idx]
                nome = input(f"{Cores.info('Nome do material: ')}")
                preco = float(input(f"{Cores.info('Preço: ')}"))
                estoque = float(input(f"{Cores.info('Estoque: ')}"))
                unidade = input(f"{Cores.info('Unidade: ')}")
                print("\nCategorias:")
                for i, cat in enumerate(CategoriaMaterial, 1):
                    print(f"{i}. {cat.value}")
                cat_op = input(f"{Cores.info('Escolha a categoria: ')}")
                try:
                    cat_idx = int(cat_op) - 1
                    categoria = list(CategoriaMaterial)[cat_idx]
                except:
                    categoria = CategoriaMaterial.OUTROS
                
                if self.sistema.adicionar_material(projeto.id, nome, preco, estoque, unidade, categoria):
                    print(f"\n{Cores.sucesso('✓ Material adicionado!')}")
                else:
                    print(f"\n{Cores.erro('✗ Erro ao adicionar material.')}")
            else:
                print(f"{Cores.erro('✗ Projeto inválido.')}")
        except:
            print(f"{Cores.erro('✗ Opção inválida.')}")
        input(f"\n{Cores.info('Pressione Enter para continuar...')}")
    
    def listar_materiais(self):
        self.limpar_tela()
        self.exibir_titulo("LISTA DE MATERIAIS")
        projetos = list(self.sistema.projetos.values())
        if not projetos:
            print(f"{Cores.aviso('⚠ Nenhum projeto cadastrado.')}")
            input(f"\n{Cores.info('Pressione Enter para continuar...')}")
            return
        
        for i, projeto in enumerate(projetos, 1):
            print(f"{i}. {projeto.nome}")
        proj_op = input(f"\n{Cores.info('Escolha o projeto: ')}")
        try:
            idx = int(proj_op) - 1
            if 0 <= idx < len(projetos):
                projeto = projetos[idx]
                if not projeto.materiais:
                    print(f"{Cores.aviso('⚠ Nenhum material cadastrado.')}")
                else:
                    for material in projeto.materiais.values():
                        print(f"\n{Cores.destaque(material.nome)}")
                        print(f"   Preço: R$ {material.preco:.2f}")
                        print(f"   Estoque: {material.estoque} {material.unidade}")
                        print(f"   Categoria: {material.categoria.value}")
        except:
            print(f"{Cores.erro('✗ Opção inválida.')}")
        input(f"\n{Cores.info('Pressione Enter para continuar...')}")
    
    def registrar_consumo_semanal(self):
        self.limpar_tela()
        self.exibir_titulo("REGISTRAR CONSUMO SEMANAL")
        projetos = list(self.sistema.projetos.values())
        if not projetos:
            print(f"{Cores.aviso('⚠ Nenhum projeto cadastrado.')}")
            input(f"\n{Cores.info('Pressione Enter para continuar...')}")
            return
        
        for i, projeto in enumerate(projetos, 1):
            print(f"{i}. {projeto.nome}")
        proj_op = input(f"\n{Cores.info('Escolha o projeto: ')}")
        try:
            idx = int(proj_op) - 1
            if 0 <= idx < len(projetos):
                projeto = projetos[idx]
                semana = int(input(f"{Cores.info('Número da semana: ')}"))
                consumo = {}
                for material in projeto.materiais.values():
                    qtd = input(f"{Cores.info(f'Consumo de {material.nome} ({material.unidade}): ')}")
                    if qtd:
                        consumo[material.nome] = float(qtd)
                if self.sistema.registrar_consumo_semanal(projeto.id, semana, consumo):
                    print(f"\n{Cores.sucesso('✓ Consumo registrado!')}")
                else:
                    print(f"\n{Cores.erro('✗ Erro ao registrar consumo.')}")
        except:
            print(f"{Cores.erro('✗ Opção inválida.')}")
        input(f"\n{Cores.info('Pressione Enter para continuar...')}")
    
    def menu_coordenadas(self):
        while True:
            self.limpar_tela()
            self.exibir_titulo("MENU DE COORDENADAS")
            print(Cores.menu_item("1", "Adicionar Coordenada"))
            print(Cores.menu_item("2", "Listar Coordenadas"))
            print(Cores.menu_item("3", "Criar Matriz da Planta"))
            print(Cores.menu_item("4", "Atualizar Matriz da Planta"))
            print(Cores.menu_item("5", "Imprimir Matriz da Planta"))
            print(Cores.opcao_voltar())
            opcao = input(f"\n{Cores.info('Escolha uma opção: ')}")
            
            if opcao == "1":
                self.adicionar_coordenada()
            elif opcao == "2":
                self.listar_coordenadas()
            elif opcao == "3":
                self.criar_matriz_planta()
            elif opcao == "4":
                self.atualizar_matriz_planta()
            elif opcao == "5":
                self.imprimir_matriz_planta()
            elif opcao == "0":
                break
    
    def adicionar_coordenada(self):
        self.limpar_tela()
        self.exibir_titulo("ADICIONAR COORDENADA")
        projetos = list(self.sistema.projetos.values())
        if not projetos:
            print(f"{Cores.aviso('⚠ Nenhum projeto cadastrado.')}")
            input(f"\n{Cores.info('Pressione Enter para continuar...')}")
            return
        
        for i, projeto in enumerate(projetos, 1):
            print(f"{i}. {projeto.nome}")
        proj_op = input(f"\n{Cores.info('Escolha o projeto: ')}")
        try:
            idx = int(proj_op) - 1
            if 0 <= idx < len(projetos):
                projeto = projetos[idx]
                x = float(input(f"{Cores.info('Coordenada X: ')}"))
                y = float(input(f"{Cores.info('Coordenada Y: ')}"))
                z = float(input(f"{Cores.info('Coordenada Z: ')}"))
                descricao = input(f"{Cores.info('Descrição: ')}")
                if self.sistema.adicionar_coordenada(projeto.id, x, y, z, descricao):
                    print(f"\n{Cores.sucesso('✓ Coordenada adicionada!')}")
                else:
                    print(f"\n{Cores.erro('✗ Erro ao adicionar coordenada.')}")
        except:
            print(f"{Cores.erro('✗ Opção inválida.')}")
        input(f"\n{Cores.info('Pressione Enter para continuar...')}")
    
    def listar_coordenadas(self):
        self.limpar_tela()
        self.exibir_titulo("LISTA DE COORDENADAS")
        projetos = list(self.sistema.projetos.values())
        if not projetos:
            print(f"{Cores.aviso('⚠ Nenhum projeto cadastrado.')}")
            input(f"\n{Cores.info('Pressione Enter para continuar...')}")
            return
        
        for i, projeto in enumerate(projetos, 1):
            print(f"{i}. {projeto.nome}")
        proj_op = input(f"\n{Cores.info('Escolha o projeto: ')}")
        try:
            idx = int(proj_op) - 1
            if 0 <= idx < len(projetos):
                projeto = projetos[idx]
                coordenadas = self.sistema.consultar_coordenadas(projeto.id)
                if not coordenadas:
                    print(f"{Cores.aviso('⚠ Nenhuma coordenada cadastrada.')}")
                else:
                    for coord in coordenadas:
                        print(f"\n{coord}")
        except:
            print(f"{Cores.erro('✗ Opção inválida.')}")
        input(f"\n{Cores.info('Pressione Enter para continuar...')}")
    
    def criar_matriz_planta(self):
        self.limpar_tela()
        self.exibir_titulo("CRIAR MATRIZ DA PLANTA")
        projetos = list(self.sistema.projetos.values())
        if not projetos:
            print(f"{Cores.aviso('⚠ Nenhum projeto cadastrado.')}")
            input(f"\n{Cores.info('Pressione Enter para continuar...')}")
            return
        
        for i, projeto in enumerate(projetos, 1):
            print(f"{i}. {projeto.nome}")
        proj_op = input(f"\n{Cores.info('Escolha o projeto: ')}")
        try:
            idx = int(proj_op) - 1
            if 0 <= idx < len(projetos):
                projeto = projetos[idx]
                linhas = int(input(f"{Cores.info('Número de linhas: ')}"))
                colunas = int(input(f"{Cores.info('Número de colunas: ')}"))
                if self.sistema.criar_matriz_planta(projeto.id, linhas, colunas):
                    print(f"\n{Cores.sucesso('✓ Matriz criada!')}")
                else:
                    print(f"\n{Cores.erro('✗ Erro ao criar matriz.')}")
        except:
            print(f"{Cores.erro('✗ Opção inválida.')}")
        input(f"\n{Cores.info('Pressione Enter para continuar...')}")
    
    def atualizar_matriz_planta(self):
        self.limpar_tela()
        self.exibir_titulo("ATUALIZAR MATRIZ DA PLANTA")
        projetos = list(self.sistema.projetos.values())
        if not projetos:
            print(f"{Cores.aviso('⚠ Nenhum projeto cadastrado.')}")
            input(f"\n{Cores.info('Pressione Enter para continuar...')}")
            return
        
        for i, projeto in enumerate(projetos, 1):
            print(f"{i}. {projeto.nome}")
        proj_op = input(f"\n{Cores.info('Escolha o projeto: ')}")
        try:
            idx = int(proj_op) - 1
            if 0 <= idx < len(projetos):
                projeto = projetos[idx]
                linha = int(input(f"{Cores.info('Linha: ')}"))
                coluna = int(input(f"{Cores.info('Coluna: ')}"))
                valor = input(f"{Cores.info('Valor: ')}")
                if self.sistema.atualizar_matriz_planta(projeto.id, linha, coluna, valor):
                    print(f"\n{Cores.sucesso('✓ Matriz atualizada!')}")
                else:
                    print(f"\n{Cores.erro('✗ Erro ao atualizar matriz.')}")
        except:
            print(f"{Cores.erro('✗ Opção inválida.')}")
        input(f"\n{Cores.info('Pressione Enter para continuar...')}")
    
    def imprimir_matriz_planta(self):
        self.limpar_tela()
        self.exibir_titulo("MATRIZ DA PLANTA")
        projetos = list(self.sistema.projetos.values())
        if not projetos:
            print(f"{Cores.aviso('⚠ Nenhum projeto cadastrado.')}")
            input(f"\n{Cores.info('Pressione Enter para continuar...')}")
            return
        
        for i, projeto in enumerate(projetos, 1):
            print(f"{i}. {projeto.nome}")
        proj_op = input(f"\n{Cores.info('Escolha o projeto: ')}")
        try:
            idx = int(proj_op) - 1
            if 0 <= idx < len(projetos):
                projeto = projetos[idx]
                matriz = self.sistema.imprimir_matriz_planta(projeto.id)
                if matriz:
                    print("\nLayout da Planta:")
                    for linha in matriz:
                        print("  " + " ".join(linha))
                else:
                    print(f"{Cores.aviso('⚠ Matriz não criada.')}")
        except:
            print(f"{Cores.erro('✗ Opção inválida.')}")
        input(f"\n{Cores.info('Pressione Enter para continuar...')}")
    
    def menu_relatorios(self):
        while True:
            self.limpar_tela()
            self.exibir_titulo("MENU DE RELATÓRIOS")
            print(Cores.menu_item("1", "Relatório por Semana"))
            print(Cores.menu_item("2", "Relatório por Material"))
            print(Cores.opcao_voltar())
            opcao = input(f"\n{Cores.info('Escolha uma opção: ')}")
            
            if opcao == "1":
                self.relatorio_por_semana()
            elif opcao == "2":
                self.relatorio_por_material()
            elif opcao == "0":
                break
    
    def relatorio_por_semana(self):
        self.limpar_tela()
        self.exibir_titulo("RELATÓRIO POR SEMANA")
        projetos = list(self.sistema.projetos.values())
        if not projetos:
            print(f"{Cores.aviso('⚠ Nenhum projeto cadastrado.')}")
            input(f"\n{Cores.info('Pressione Enter para continuar...')}")
            return
        
        for i, projeto in enumerate(projetos, 1):
            print(f"{i}. {projeto.nome}")
        proj_op = input(f"\n{Cores.info('Escolha o projeto: ')}")
        try:
            idx = int(proj_op) - 1
            if 0 <= idx < len(projetos):
                projeto = projetos[idx]
                relatorio = self.sistema.relatorio_soma_por_semana(projeto.id)
                if relatorio:
                    print("\nRelatório por Semana:")
                    for semana, soma in relatorio.items():
                        print(f"  Semana {semana}: R$ {soma:.2f}")
                else:
                    print(f"{Cores.aviso('⚠ Nenhum consumo registrado.')}")
        except:
            print(f"{Cores.erro('✗ Opção inválida.')}")
        input(f"\n{Cores.info('Pressione Enter para continuar...')}")
    
    def relatorio_por_material(self):
        self.limpar_tela()
        self.exibir_titulo("RELATÓRIO POR MATERIAL")
        projetos = list(self.sistema.projetos.values())
        if not projetos:
            print(f"{Cores.aviso('⚠ Nenhum projeto cadastrado.')}")
            input(f"\n{Cores.info('Pressione Enter para continuar...')}")
            return
        
        for i, projeto in enumerate(projetos, 1):
            print(f"{i}. {projeto.nome}")
        proj_op = input(f"\n{Cores.info('Escolha o projeto: ')}")
        try:
            idx = int(proj_op) - 1
            if 0 <= idx < len(projetos):
                projeto = projetos[idx]
                relatorio = self.sistema.relatorio_soma_por_material(projeto.id)
                if relatorio:
                    print("\nRelatório por Material:")
                    for material, soma in relatorio.items():
                        print(f"  {material}: R$ {soma:.2f}")
                else:
                    print(f"{Cores.aviso('⚠ Nenhum consumo registrado.')}")
        except:
            print(f"{Cores.erro('✗ Opção inválida.')}")
        input(f"\n{Cores.info('Pressione Enter para continuar...')}")
    
    def menu_calculos(self):
        while True:
            self.limpar_tela()
            self.exibir_titulo("MENU DE CÁLCULOS")
            print(Cores.menu_item("1", "Calcular Custo Total"))
            print(Cores.menu_item("2", "Dividir Recursos"))
            print(Cores.opcao_voltar())
            opcao = input(f"\n{Cores.info('Escolha uma opção: ')}")
            
            if opcao == "1":
                self.calcular_custo_total()
            elif opcao == "2":
                self.dividir_recursos()
            elif opcao == "0":
                break
    
    def calcular_custo_total(self):
        self.limpar_tela()
        self.exibir_titulo("CALCULAR CUSTO TOTAL")
        projetos = list(self.sistema.projetos.values())
        if not projetos:
            print(f"{Cores.aviso('⚠ Nenhum projeto cadastrado.')}")
            input(f"\n{Cores.info('Pressione Enter para continuar...')}")
            return
        
        for i, projeto in enumerate(projetos, 1):
            print(f"{i}. {projeto.nome}")
        proj_op = input(f"\n{Cores.info('Escolha o projeto: ')}")
        try:
            idx = int(proj_op) - 1
            if 0 <= idx < len(projetos):
                projeto = projetos[idx]
                custo = self.sistema.calcular_custo_total_projeto(projeto.id)
                print(f"\n{Cores.sucesso(f'Custo total: R$ {custo:.2f}')}")
        except:
            print(f"{Cores.erro('✗ Opção inválida.')}")
        input(f"\n{Cores.info('Pressione Enter para continuar...')}")
    
    def dividir_recursos(self):
        self.limpar_tela()
        self.exibir_titulo("DIVIDIR RECURSOS")
        valor = float(input(f"{Cores.info('Valor total: ')}"))
        pessoas = int(input(f"{Cores.info('Número de pessoas: ')}"))
        quociente, resto = self.sistema.dividir_recursos(valor, pessoas)
        print(f"\n{Cores.sucesso(f'Quociente: R$ {quociente:.2f}')}")
        print(f"{Cores.sucesso(f'Resto: R$ {resto:.2f}')}")
        input(f"\n{Cores.info('Pressione Enter para continuar...')}")
    
    def menu_estatisticas(self):
        while True:
            self.limpar_tela()
            self.exibir_titulo("MENU DE ESTATÍSTICAS")
            print(Cores.menu_item("1", "Projetos Mais Ativos"))
            print(Cores.menu_item("2", "Tarefas por Engenheiro"))
            print(Cores.menu_item("3", "Estatísticas Gerais"))
            print(Cores.opcao_voltar())
            opcao = input(f"\n{Cores.info('Escolha uma opção: ')}")
            
            if opcao == "1":
                self.projetos_mais_ativos()
            elif opcao == "2":
                self.tarefas_por_engenheiro()
            elif opcao == "3":
                self.estatisticas_gerais()
            elif opcao == "0":
                break
    
    def projetos_mais_ativos(self):
        self.limpar_tela()
        self.exibir_titulo("PROJETOS MAIS ATIVOS")
        projetos = self.sistema.projetos_mais_ativos(5)
        if projetos:
            for projeto, num_tarefas in projetos:
                print(f"\n{Cores.destaque(projeto.nome)}: {num_tarefas} tarefas ativas")
        else:
            print(f"{Cores.aviso('⚠ Nenhum projeto encontrado.')}")
        input(f"\n{Cores.info('Pressione Enter para continuar...')}")
    
    def tarefas_por_engenheiro(self):
        self.limpar_tela()
        self.exibir_titulo("TAREFAS POR ENGENHEIRO")
        stats = self.sistema.tarefas_por_engenheiro()
        if stats:
            for nome, dados in stats.items():
                print(f"\n{Cores.destaque(nome)}:")
                print(f"   Total: {dados['total']}")
                print(f"   Pendentes: {dados['pendentes']}")
                print(f"   Em andamento: {dados['em_andamento']}")
                print(f"   Concluídas: {dados['concluidas']}")
        else:
            print(f"{Cores.aviso('⚠ Nenhum engenheiro encontrado.')}")
        input(f"\n{Cores.info('Pressione Enter para continuar...')}")
    
    def estatisticas_gerais(self):
        self.limpar_tela()
        self.exibir_titulo("ESTATÍSTICAS GERAIS")
        stats = self.sistema.estatisticas_gerais_plataforma()
        print(f"\n{Cores.destaque('Total de projetos:')} {stats['total_projetos']}")
        print(f"{Cores.destaque('Total de tarefas:')} {stats['total_tarefas']}")
        print(f"{Cores.destaque('Tarefas concluídas:')} {stats['tarefas_concluidas']}")
        print(f"{Cores.destaque('Total de engenheiros:')} {stats['total_engenheiros']}")
        print(f"{Cores.destaque('Engenheiros ativos:')} {stats['engenheiros_ativos']}")
        print(f"{Cores.destaque('Total de gestores:')} {stats['total_gestores']}")
        print(f"{Cores.destaque('Total de materiais:')} {stats['total_materiais']}")
        print(f"{Cores.destaque('Total de coordenadas:')} {stats['total_coordenadas']}")
        input(f"\n{Cores.info('Pressione Enter para continuar...')}")
    
    def menu_funcionalidades_extras(self):
        while True:
            self.limpar_tela()
            self.exibir_titulo("FUNCIONALIDADES EXTRAS")
            print(Cores.menu_item("1", "Uso Avançado de Coleções"))
            print(Cores.menu_item("2", "Relatórios Avançados"))
            print(Cores.menu_item("3", "Recomendações Inteligentes"))
            print(Cores.menu_item("4", "Funções Matemáticas Extras"))
            print(Cores.opcao_voltar())
            opcao = input(f"\n{Cores.info('Escolha uma opção: ')}")
            
            if opcao == "1":
                self.menu_uso_avancado_colecoes()
            elif opcao == "2":
                self.menu_relatorios_avancados()
            elif opcao == "3":
                self.menu_recomendacoes_inteligentes()
            elif opcao == "4":
                self.menu_funcoes_matematicas_extras()
            elif opcao == "0":
                break
    
    def menu_uso_avancado_colecoes(self):
        while True:
            self.limpar_tela()
            self.exibir_titulo("USO AVANÇADO DE COLEÇÕES")
            print(Cores.menu_item("1", "Projetos Concluídos"))
            print(Cores.menu_item("2", "Engenheiros Ativos/Inativos"))
            print(Cores.menu_item("3", "Materiais por Categoria"))
            print(Cores.opcao_voltar())
            opcao = input(f"\n{Cores.info('Escolha uma opção: ')}")
            
            if opcao == "1":
                projetos = self.sistema.obter_projetos_concluidos()
                print(f"\n{Cores.destaque('Projetos Concluídos:')} {len(projetos)}")
                for projeto in projetos:
                    print(f"  - {projeto.nome}")
                input(f"\n{Cores.info('Pressione Enter para continuar...')}")
            elif opcao == "2":
                ativos = self.sistema.obter_engenheiros_ativos()
                inativos = self.sistema.obter_engenheiros_inativos()
                print(f"\n{Cores.destaque('Engenheiros Ativos:')} {len(ativos)}")
                for eng in ativos:
                    print(f"  - {eng.nome}")
                print(f"\n{Cores.destaque('Engenheiros Inativos:')} {len(inativos)}")
                for eng in inativos:
                    print(f"  - {eng.nome}")
                input(f"\n{Cores.info('Pressione Enter para continuar...')}")
            elif opcao == "3":
                print("\nCategorias:")
                for i, cat in enumerate(CategoriaMaterial, 1):
                    print(f"{i}. {cat.value}")
                cat_op = input(f"{Cores.info('Escolha a categoria: ')}")
                try:
                    cat_idx = int(cat_op) - 1
                    categoria = list(CategoriaMaterial)[cat_idx]
                    materiais = self.sistema.obter_materiais_por_categoria(categoria)
                    print(f"\n{Cores.destaque(f'Materiais ({categoria.value}):')} {len(materiais)}")
                    for mat in materiais:
                        print(f"  - {mat.nome}")
                except:
                    print(f"{Cores.erro('✗ Opção inválida.')}")
                input(f"\n{Cores.info('Pressione Enter para continuar...')}")
            elif opcao == "0":
                break
    
    def menu_relatorios_avancados(self):
        while True:
            self.limpar_tela()
            self.exibir_titulo("RELATÓRIOS AVANÇADOS")
            print(Cores.menu_item("1", "Engenheiro com Mais Tarefas"))
            print(Cores.menu_item("2", "Materiais Mais Consumidos"))
            print(Cores.menu_item("3", "Média de Custos"))
            print(Cores.menu_item("4", "Máximo e Mínimo de Custos"))
            print(Cores.menu_item("5", "Média de Tarefas por Projeto"))
            print(Cores.opcao_voltar())
            opcao = input(f"\n{Cores.info('Escolha uma opção: ')}")
            
            if opcao == "1":
                resultado = self.sistema.engenheiro_com_mais_tarefas()
                if resultado:
                    usuario, num = resultado
                    print(f"\n{Cores.sucesso(f'{usuario.nome}: {num} tarefas')}")
                else:
                    print(f"{Cores.aviso('⚠ Nenhum engenheiro encontrado.')}")
                input(f"\n{Cores.info('Pressione Enter para continuar...')}")
            elif opcao == "2":
                materiais = self.sistema.materiais_mais_consumidos(5)
                print(f"\n{Cores.destaque('Materiais Mais Consumidos:')}")
                for nome, qtd in materiais:
                    print(f"  - {nome}: {qtd:.2f}")
                input(f"\n{Cores.info('Pressione Enter para continuar...')}")
            elif opcao == "3":
                media = self.sistema.calcular_media_custos_projetos()
                print(f"\n{Cores.sucesso(f'Média de custos: R$ {media:.2f}')}")
                input(f"\n{Cores.info('Pressione Enter para continuar...')}")
            elif opcao == "4":
                maximo, minimo = self.sistema.calcular_maximo_minimo_custos()
                print(f"\n{Cores.sucesso(f'Máximo: R$ {maximo:.2f}')}")
                print(f"{Cores.sucesso(f'Mínimo: R$ {minimo:.2f}')}")
                input(f"\n{Cores.info('Pressione Enter para continuar...')}")
            elif opcao == "5":
                media = self.sistema.calcular_media_tarefas_por_projeto()
                print(f"\n{Cores.sucesso(f'Média de tarefas por projeto: {media:.2f}')}")
                input(f"\n{Cores.info('Pressione Enter para continuar...')}")
            elif opcao == "0":
                break
    
    def menu_recomendacoes_inteligentes(self):
        self.limpar_tela()
        self.exibir_titulo("RECOMENDAÇÕES INTELIGENTES")
        categoria = input(f"{Cores.info('Categoria da tarefa: ')}")
        recomendacao = self.sistema.recomendar_engenheiro_para_tarefa(categoria)
        if recomendacao:
            print(f"\n{Cores.sucesso(f'Engenheiro recomendado: {recomendacao.nome}')}")
        else:
            print(f"{Cores.aviso('⚠ Nenhuma recomendação disponível.')}")
        input(f"\n{Cores.info('Pressione Enter para continuar...')}")
    
    def menu_funcoes_matematicas_extras(self):
        while True:
            self.limpar_tela()
            self.exibir_titulo("FUNÇÕES MATEMÁTICAS EXTRAS")
            print(Cores.menu_item("1", "Projeção de Consumo"))
            print(Cores.menu_item("2", "Simular Crescimento de Tarefas"))
            print(Cores.opcao_voltar())
            opcao = input(f"\n{Cores.info('Escolha uma opção: ')}")
            
            if opcao == "1":
                projetos = list(self.sistema.projetos.values())
                if projetos:
                    for i, projeto in enumerate(projetos, 1):
                        print(f"{i}. {projeto.nome}")
                    proj_op = input(f"{Cores.info('Escolha o projeto: ')}")
                    try:
                        idx = int(proj_op) - 1
                        if 0 <= idx < len(projetos):
                            projeto = projetos[idx]
                            semanas = int(input(f"{Cores.info('Semanas futuras: ')}"))
                            projecao = self.sistema.projecao_consumo_materiais(projeto.id, semanas)
                            if projecao:
                                for material, valores in projecao.items():
                                    print(f"\n{Cores.destaque(material)}:")
                                    for semana, valor in enumerate(valores):
                                        print(f"  Semana {semana + 1}: {valor:.2f}")
                            else:
                                print(f"{Cores.aviso('⚠ Nenhum consumo registrado.')}")
                    except:
                        print(f"{Cores.erro('✗ Opção inválida.')}")
                else:
                    print(f"{Cores.aviso('⚠ Nenhum projeto cadastrado.')}")
                input(f"\n{Cores.info('Pressione Enter para continuar...')}")
            elif opcao == "2":
                tarefas = int(input(f"{Cores.info('Número atual de tarefas: ')}"))
                semanas = int(input(f"{Cores.info('Semanas: ')}"))
                resultado = self.sistema.simular_crescimento_tarefas(tarefas, semanas)
                print(f"\n{Cores.sucesso(f'Projeção: {resultado} tarefas')}")
                input(f"\n{Cores.info('Pressione Enter para continuar...')}")
            elif opcao == "0":
                break
    
    def ver_notificacoes(self):
        self.limpar_tela()
        self.exibir_titulo("NOTIFICAÇÕES")
        notificacoes = self.sistema.obter_notificacoes(nao_lidas=True)
        if notificacoes:
            for notif in notificacoes:
                print(f"\n{notif}")
                notif.lida = True
        else:
            print(f"{Cores.aviso('⚠ Nenhuma notificação não lida.')}")
        input(f"\n{Cores.info('Pressione Enter para continuar...')}")
    
    def buscar_projeto_interface(self):
        self.limpar_tela()
        self.exibir_titulo("BUSCAR PROJETO")
        termo = input(f"{Cores.info('Digite o termo de busca: ')}")
        resultados = self.sistema.buscar_projeto(termo)
        if resultados:
            print(f"\n{Cores.sucesso(f'{len(resultados)} projeto(s) encontrado(s):')}")
            for projeto in resultados:
                print(f"  - {projeto.nome}")
        else:
            print(f"{Cores.aviso('⚠ Nenhum projeto encontrado.')}")
        input(f"\n{Cores.info('Pressione Enter para continuar...')}")

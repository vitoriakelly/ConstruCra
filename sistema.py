import os
import json
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional
from models import (
    Usuario, Tarefa, Material, Coordenada, Projeto, Notificacao,
    TipoUsuario, StatusTarefa, StatusProjeto, CategoriaMaterial
)


class SistemaGestaoProjetos:
    def __init__(self):
        self.usuarios: Dict[int, Usuario] = {}
        self.projetos: Dict[int, Projeto] = {}
        self.usuario_logado: Optional[Usuario] = None
        self.notificacoes: Dict[int, List[Notificacao]] = {}
        self.projetos_concluidos: List[Projeto] = []
        self.engenheiros_ativos: List[Usuario] = []
        self.engenheiros_inativos: List[Usuario] = []
        self.historico_tarefas_por_categoria: Dict[str, int] = {}
    
    def cadastrar_usuario(self, nome: str, email: str, senha: str, tipo: TipoUsuario) -> bool:
        for usuario in self.usuarios.values():
            if usuario.email == email:
                return False
        novo_usuario = Usuario(nome, email, senha, tipo)
        self.usuarios[novo_usuario.id] = novo_usuario
        self.notificacoes[novo_usuario.id] = []
        return True
    
    def login(self, email: str, senha: str) -> bool:
        for usuario in self.usuarios.values():
            if usuario.email == email and usuario.senha == senha:
                self.usuario_logado = usuario
                return True
        return False
    
    def logout(self):
        self.usuario_logado = None
    
    def cadastrar_engenheiro(self, nome: str, email: str, senha: str) -> bool:
        if not self.usuario_logado or self.usuario_logado.tipo != TipoUsuario.GESTOR:
            return False
        return self.cadastrar_usuario(nome, email, senha, TipoUsuario.ENGENHEIRO)
    
    def criar_projeto(self, nome: str, descricao: str, gasto: float = 0.0, lucro: float = 0.0,
                      prazo: Optional[datetime] = None, responsavel_id: Optional[int] = None) -> Optional[Projeto]:
        if not self.usuario_logado:
            return None
        if self.usuario_logado.tipo == TipoUsuario.ENGENHEIRO:
            responsavel_id = self.usuario_logado.id
        elif self.usuario_logado.tipo == TipoUsuario.GESTOR:
            if responsavel_id and responsavel_id not in self.usuarios:
                return None
            if responsavel_id and self.usuarios[responsavel_id].tipo != TipoUsuario.ENGENHEIRO:
                return None
        projeto = Projeto(nome, descricao, self.usuario_logado.id, gasto, lucro, prazo, responsavel_id)
        self.projetos[projeto.id] = projeto
        self._notificar_novo_projeto(projeto)
        return projeto
    
    def _notificar_novo_projeto(self, projeto: Projeto):
        for usuario in self.usuarios.values():
            if usuario.tipo == TipoUsuario.ENGENHEIRO:
                notif = Notificacao('novo_projeto', f'Novo projeto: {projeto.nome}', projeto.id)
                self.notificacoes[usuario.id].append(notif)
    
    def criar_tarefa(self, titulo: str, descricao: str, responsavel_id: int,
                     prazo: Optional[datetime] = None, projeto_id: Optional[int] = None,
                     categoria: Optional[str] = None) -> Optional[Tarefa]:
        if not self.usuario_logado:
            return None
        if projeto_id and projeto_id not in self.projetos:
            return None
        tarefa = Tarefa(titulo, descricao, responsavel_id, prazo, projeto_id, categoria)
        if projeto_id:
            self.projetos[projeto_id].tarefas.append(tarefa)
        self._notificar_nova_tarefa(tarefa)
        if categoria:
            self.historico_tarefas_por_categoria[categoria] = self.historico_tarefas_por_categoria.get(categoria, 0) + 1
        return tarefa
    
    def _notificar_nova_tarefa(self, tarefa: Tarefa):
        if tarefa.responsavel_id in self.usuarios:
            notif = Notificacao('nova_tarefa', f'Nova tarefa: {tarefa.titulo}', tarefa.projeto_id, tarefa.id)
            self.notificacoes[tarefa.responsavel_id].append(notif)
    
    def adicionar_material(self, projeto_id: int, nome: str, preco: float, estoque: float,
                          unidade: str, categoria: CategoriaMaterial = CategoriaMaterial.OUTROS) -> bool:
        if projeto_id not in self.projetos:
            return False
        material = Material(nome, preco, estoque, unidade, categoria)
        self.projetos[projeto_id].materiais[nome] = material
        return True
    
    def adicionar_coordenada(self, projeto_id: int, x: float, y: float, z: float, descricao: str = "") -> bool:
        if projeto_id not in self.projetos:
            return False
        coord = Coordenada(x, y, z, descricao)
        self.projetos[projeto_id].coordenadas.append(coord)
        return True
    
    def criar_matriz_planta(self, projeto_id: int, linhas: int, colunas: int) -> bool:
        if projeto_id not in self.projetos:
            return False
        self.projetos[projeto_id].matriz_planta = [['.' for _ in range(colunas)] for _ in range(linhas)]
        return True
    
    def atualizar_matriz_planta(self, projeto_id: int, linha: int, coluna: int, valor: str) -> bool:
        if projeto_id not in self.projetos:
            return False
        projeto = self.projetos[projeto_id]
        if linha < 0 or linha >= len(projeto.matriz_planta) or coluna < 0 or coluna >= len(projeto.matriz_planta[0]):
            return False
        projeto.matriz_planta[linha][coluna] = valor
        return True
    
    def imprimir_matriz_planta(self, projeto_id: int) -> Optional[List[List[str]]]:
        if projeto_id not in self.projetos:
            return None
        return self.projetos[projeto_id].matriz_planta
    
    def registrar_consumo_semanal(self, projeto_id: int, semana: int, consumo: Dict[str, float]) -> bool:
        if projeto_id not in self.projetos:
            return False
        projeto = self.projetos[projeto_id]
        while len(projeto.consumo_semanal) <= semana:
            projeto.consumo_semanal.append([0.0] * len(projeto.materiais))
        materiais_list = list(projeto.materiais.keys())
        for material_nome, quantidade in consumo.items():
            if material_nome in materiais_list:
                idx = materiais_list.index(material_nome)
                projeto.consumo_semanal[semana][idx] = quantidade
        return True
    
    def relatorio_soma_por_semana(self, projeto_id: int) -> Dict[int, float]:
        if projeto_id not in self.projetos:
            return {}
        projeto = self.projetos[projeto_id]
        resultado = {}
        materiais_list = list(projeto.materiais.keys())
        for semana, consumos in enumerate(projeto.consumo_semanal):
            soma = 0.0
            for idx, quantidade in enumerate(consumos):
                if idx < len(materiais_list):
                    material = projeto.materiais[materiais_list[idx]]
                    soma += quantidade * material.preco
            resultado[semana] = soma
        return resultado
    
    def relatorio_soma_por_material(self, projeto_id: int) -> Dict[str, float]:
        if projeto_id not in self.projetos:
            return {}
        projeto = self.projetos[projeto_id]
        resultado = {}
        materiais_list = list(projeto.materiais.keys())
        for idx, material_nome in enumerate(materiais_list):
            soma = 0.0
            for semana in projeto.consumo_semanal:
                if idx < len(semana):
                    quantidade = semana[idx]
                    material = projeto.materiais[material_nome]
                    soma += quantidade * material.preco
            resultado[material_nome] = soma
        return resultado
    
    def calcular_custo_total_projeto(self, projeto_id: int) -> float:
        if projeto_id not in self.projetos:
            return 0.0
        projeto = self.projetos[projeto_id]
        custo = 0.0
        for material in projeto.materiais.values():
            custo += material.preco * material.estoque
        return custo
    
    def buscar_projeto(self, termo: str) -> List[Projeto]:
        resultados = []
        termo_lower = termo.lower()
        for projeto in self.projetos.values():
            if termo_lower in projeto.nome.lower() or termo_lower in projeto.descricao.lower():
                resultados.append(projeto)
            for tarefa in projeto.tarefas:
                if termo_lower in tarefa.titulo.lower() or termo_lower in tarefa.descricao.lower():
                    if projeto not in resultados:
                        resultados.append(projeto)
                    break
        return resultados
    
    def verificar_estoque_insuficiente(self, projeto_id: int, limite: float = 10.0) -> List[Material]:
        if projeto_id not in self.projetos:
            return []
        projeto = self.projetos[projeto_id]
        materiais_baixos = []
        for material in projeto.materiais.values():
            if material.estoque < limite:
                materiais_baixos.append(material)
        return materiais_baixos
    
    def consultar_coordenadas(self, projeto_id: int) -> List[Coordenada]:
        if projeto_id not in self.projetos:
            return []
        return self.projetos[projeto_id].coordenadas
    
    def dividir_recursos(self, valor_total: float, num_pessoas: int) -> Tuple[float, float]:
        if num_pessoas == 0:
            return 0.0, valor_total
        quociente = valor_total / num_pessoas
        resto = valor_total % num_pessoas
        return quociente, resto
    
    def obter_notificacoes(self, nao_lidas: bool = False) -> List[Notificacao]:
        if not self.usuario_logado:
            return []
        notificacoes = self.notificacoes.get(self.usuario_logado.id, [])
        if nao_lidas:
            return [n for n in notificacoes if not n.lida]
        return notificacoes
    
    def projetos_mais_ativos(self, limite: int = 5) -> List[Tuple[Projeto, int]]:
        projetos_com_tarefas = []
        for projeto in self.projetos.values():
            tarefas_ativas = sum(1 for t in projeto.tarefas if t.status != StatusTarefa.CONCLUIDA)
            projetos_com_tarefas.append((projeto, tarefas_ativas))
        projetos_com_tarefas.sort(key=lambda x: x[1], reverse=True)
        return projetos_com_tarefas[:limite]
    
    def tarefas_por_engenheiro(self) -> Dict[str, Dict[str, int]]:
        resultado = {}
        for usuario in self.usuarios.values():
            if usuario.tipo == TipoUsuario.ENGENHEIRO:
                total = 0
                pendentes = 0
                em_andamento = 0
                concluidas = 0
                for projeto in self.projetos.values():
                    for tarefa in projeto.tarefas:
                        if tarefa.responsavel_id == usuario.id:
                            total += 1
                            if tarefa.status == StatusTarefa.PENDENTE:
                                pendentes += 1
                            elif tarefa.status == StatusTarefa.EM_ANDAMENTO:
                                em_andamento += 1
                            elif tarefa.status == StatusTarefa.CONCLUIDA:
                                concluidas += 1
                resultado[usuario.nome] = {
                    'total': total,
                    'pendentes': pendentes,
                    'em_andamento': em_andamento,
                    'concluidas': concluidas
                }
        return resultado
    
    def estatisticas_gerais_plataforma(self) -> Dict[str, any]:
        total_projetos = len(self.projetos)
        total_tarefas = sum(len(p.tarefas) for p in self.projetos.values())
        tarefas_concluidas = sum(1 for p in self.projetos.values() for t in p.tarefas if t.status == StatusTarefa.CONCLUIDA)
        total_engenheiros = sum(1 for u in self.usuarios.values() if u.tipo == TipoUsuario.ENGENHEIRO)
        engenheiros_ativos = sum(1 for u in self.usuarios.values() if u.tipo == TipoUsuario.ENGENHEIRO and any(t.responsavel_id == u.id and t.status != StatusTarefa.CONCLUIDA for p in self.projetos.values() for t in p.tarefas))
        total_gestores = sum(1 for u in self.usuarios.values() if u.tipo == TipoUsuario.GESTOR)
        total_materiais = sum(len(p.materiais) for p in self.projetos.values())
        total_coordenadas = sum(len(p.coordenadas) for p in self.projetos.values())
        return {
            'total_projetos': total_projetos,
            'total_tarefas': total_tarefas,
            'tarefas_concluidas': tarefas_concluidas,
            'total_engenheiros': total_engenheiros,
            'engenheiros_ativos': engenheiros_ativos,
            'total_gestores': total_gestores,
            'total_materiais': total_materiais,
            'total_coordenadas': total_coordenadas
        }
    
    def concluir_projeto(self, projeto_id: int) -> bool:
        if projeto_id not in self.projetos:
            return False
        projeto = self.projetos[projeto_id]
        projeto.status = StatusProjeto.CONCLUIDO
        projeto.data_conclusao = datetime.now()
        if projeto not in self.projetos_concluidos:
            self.projetos_concluidos.append(projeto)
        return True
    
    def obter_projetos_concluidos(self) -> List[Projeto]:
        return self.projetos_concluidos
    
    def atualizar_status_engenheiros(self):
        self.engenheiros_ativos = []
        self.engenheiros_inativos = []
        for usuario in self.usuarios.values():
            if usuario.tipo == TipoUsuario.ENGENHEIRO:
                tem_tarefas_ativas = any(t.responsavel_id == usuario.id and t.status != StatusTarefa.CONCLUIDA for p in self.projetos.values() for t in p.tarefas)
                if tem_tarefas_ativas:
                    if usuario not in self.engenheiros_ativos:
                        self.engenheiros_ativos.append(usuario)
                else:
                    if usuario not in self.engenheiros_inativos:
                        self.engenheiros_inativos.append(usuario)
    
    def obter_engenheiros_ativos(self) -> List[Usuario]:
        self.atualizar_status_engenheiros()
        return self.engenheiros_ativos
    
    def obter_engenheiros_inativos(self) -> List[Usuario]:
        self.atualizar_status_engenheiros()
        return self.engenheiros_inativos
    
    def obter_materiais_por_categoria(self, categoria: CategoriaMaterial) -> List[Material]:
        materiais = []
        for projeto in self.projetos.values():
            for material in projeto.materiais.values():
                if material.categoria == categoria:
                    materiais.append(material)
        return materiais
    
    def registrar_tarefa_categoria(self, categoria: str):
        self.historico_tarefas_por_categoria[categoria] = self.historico_tarefas_por_categoria.get(categoria, 0) + 1
    
    def engenheiro_com_mais_tarefas(self) -> Optional[Tuple[Usuario, int]]:
        stats = self.tarefas_por_engenheiro()
        if not stats:
            return None
        max_tarefas = max(stats.values(), key=lambda x: x['total'])
        for nome, dados in stats.items():
            if dados['total'] == max_tarefas['total']:
                usuario = next(u for u in self.usuarios.values() if u.nome == nome)
                return (usuario, max_tarefas['total'])
        return None
    
    def materiais_mais_consumidos(self, limite: int = 5) -> List[Tuple[str, float]]:
        consumo_total = {}
        for projeto in self.projetos.values():
            materiais_list = list(projeto.materiais.keys())
            for semana in projeto.consumo_semanal:
                for idx, quantidade in enumerate(semana):
                    if idx < len(materiais_list):
                        material_nome = materiais_list[idx]
                        consumo_total[material_nome] = consumo_total.get(material_nome, 0) + quantidade
        sorted_materiais = sorted(consumo_total.items(), key=lambda x: x[1], reverse=True)
        return sorted_materiais[:limite]
    
    def calcular_media_custos_projetos(self) -> float:
        if not self.projetos:
            return 0.0
        custos = [p.gasto for p in self.projetos.values()]
        return sum(custos) / len(custos) if custos else 0.0
    
    def calcular_maximo_minimo_custos(self) -> Tuple[float, float]:
        if not self.projetos:
            return (0.0, 0.0)
        custos = [p.gasto for p in self.projetos.values()]
        return (max(custos), min(custos)) if custos else (0.0, 0.0)
    
    def calcular_media_tarefas_por_projeto(self) -> float:
        if not self.projetos:
            return 0.0
        total_tarefas = sum(len(p.tarefas) for p in self.projetos.values())
        return total_tarefas / len(self.projetos)
    
    def recomendar_engenheiro_para_tarefa(self, categoria: str) -> Optional[Usuario]:
        if categoria not in self.historico_tarefas_por_categoria:
            return None
        melhor_engenheiro = None
        max_tarefas = 0
        for usuario in self.usuarios.values():
            if usuario.tipo == TipoUsuario.ENGENHEIRO:
                tarefas_categoria = sum(1 for p in self.projetos.values() for t in p.tarefas if t.responsavel_id == usuario.id and t.categoria == categoria)
                if tarefas_categoria > max_tarefas:
                    max_tarefas = tarefas_categoria
                    melhor_engenheiro = usuario
        return melhor_engenheiro
    
    def obter_recomendacoes_tarefa(self, categoria: str) -> List[Usuario]:
        recomendacoes = []
        if categoria in self.historico_tarefas_por_categoria:
            for usuario in self.usuarios.values():
                if usuario.tipo == TipoUsuario.ENGENHEIRO:
                    tarefas_categoria = sum(1 for p in self.projetos.values() for t in p.tarefas if t.responsavel_id == usuario.id and t.categoria == categoria)
                    if tarefas_categoria > 0:
                        recomendacoes.append(usuario)
        return recomendacoes
    
    def projecao_consumo_materiais(self, projeto_id: int, semanas_futuras: int, taxa_crescimento: float = 0.1) -> Dict[str, List[float]]:
        if projeto_id not in self.projetos:
            return {}
        projeto = self.projetos[projeto_id]
        if not projeto.consumo_semanal:
            return {}
        ultima_semana = projeto.consumo_semanal[-1]
        materiais_list = list(projeto.materiais.keys())
        projecao = {}
        for idx, material_nome in enumerate(materiais_list):
            if idx < len(ultima_semana):
                consumo_atual = ultima_semana[idx]
                projecao[material_nome] = []
                for semana in range(semanas_futuras):
                    consumo_projetado = consumo_atual * ((1 + taxa_crescimento) ** semana)
                    projecao[material_nome].append(consumo_projetado)
        return projecao
    
    def simular_crescimento_tarefas(self, tarefas_atuais: int, semanas: int, taxa_crescimento: float = 0.15) -> int:
        def calcular_crescimento(sem: int) -> int:
            if sem == 0:
                return tarefas_atuais
            anterior = calcular_crescimento(sem - 1)
            return int(anterior * (1 + taxa_crescimento))
        return calcular_crescimento(semanas)
    
    def salvar_dados(self, arquivo: str = 'dados_sistema.json') -> bool:
        try:
            dados = {
                'usuarios': [],
                'projetos': [],
                'tarefas': [],
                'projetos_concluidos_ids': [p.id for p in self.projetos_concluidos]
            }
            for usuario in self.usuarios.values():
                dados['usuarios'].append({
                    'id': usuario.id,
                    'nome': usuario.nome,
                    'email': usuario.email,
                    'senha': usuario.senha,
                    'tipo': usuario.tipo.value,
                    'data_cadastro': usuario.data_cadastro.isoformat()
                })
            for projeto in self.projetos.values():
                projeto_data = {
                    'id': projeto.id,
                    'nome': projeto.nome,
                    'descricao': projeto.descricao,
                    'gestor_id': projeto.gestor_id,
                    'status': projeto.status.value,
                    'data_criacao': projeto.data_criacao.isoformat(),
                    'data_conclusao': projeto.data_conclusao.isoformat() if projeto.data_conclusao else None,
                    'gasto': projeto.gasto,
                    'lucro': projeto.lucro,
                    'prazo': projeto.prazo.isoformat() if projeto.prazo else None,
                    'responsavel_id': projeto.responsavel_id,
                    'materiais': {},
                    'coordenadas': [],
                    'matriz_planta': projeto.matriz_planta,
                    'consumo_semanal': projeto.consumo_semanal
                }
                for nome, material in projeto.materiais.items():
                    projeto_data['materiais'][nome] = {
                        'preco': material.preco,
                        'estoque': material.estoque,
                        'unidade': material.unidade,
                        'categoria': material.categoria.value
                    }
                for coord in projeto.coordenadas:
                    projeto_data['coordenadas'].append({
                        'x': coord.coordenadas[0],
                        'y': coord.coordenadas[1],
                        'z': coord.coordenadas[2],
                        'descricao': coord.descricao
                    })
                dados['projetos'].append(projeto_data)
                for tarefa in projeto.tarefas:
                    dados['tarefas'].append({
                        'id': tarefa.id,
                        'titulo': tarefa.titulo,
                        'descricao': tarefa.descricao,
                        'responsavel_id': tarefa.responsavel_id,
                        'projeto_id': tarefa.projeto_id,
                        'status': tarefa.status.value,
                        'data_criacao': tarefa.data_criacao.isoformat(),
                        'data_conclusao': tarefa.data_conclusao.isoformat() if tarefa.data_conclusao else None,
                        'prazo': tarefa.prazo.isoformat() if tarefa.prazo else None,
                        'categoria': tarefa.categoria
                    })
            with open(arquivo, 'w', encoding='utf-8') as f:
                json.dump(dados, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f'Erro ao salvar: {e}')
            return False
    
    def carregar_dados(self, arquivo: str = 'dados_sistema.json') -> bool:
        try:
            if not os.path.exists(arquivo):
                return False
            with open(arquivo, 'r', encoding='utf-8') as f:
                dados = json.load(f)
            for user_data in dados.get('usuarios', []):
                tipo = TipoUsuario.GESTOR if user_data['tipo'] == 'gestor' else TipoUsuario.ENGENHEIRO
                senha = user_data.get('senha', '')
                usuario = Usuario(user_data['nome'], user_data['email'], senha, tipo)
                usuario.id = user_data['id']
                usuario.data_cadastro = datetime.fromisoformat(user_data['data_cadastro'])
                self.usuarios[usuario.id] = usuario
                self.notificacoes[usuario.id] = []
            for proj_data in dados.get('projetos', []):
                projeto = Projeto(proj_data['nome'], proj_data['descricao'], proj_data['gestor_id'],
                                 proj_data.get('gasto', 0.0), proj_data.get('lucro', 0.0),
                                 datetime.fromisoformat(proj_data['prazo']) if proj_data.get('prazo') else None,
                                 proj_data.get('responsavel_id'))
                projeto.id = proj_data['id']
                projeto.data_criacao = datetime.fromisoformat(proj_data['data_criacao'])
                if proj_data.get('data_conclusao'):
                    projeto.data_conclusao = datetime.fromisoformat(proj_data['data_conclusao'])
                projeto.status = StatusProjeto[proj_data.get('status', 'ATIVO').upper()]
                projeto.matriz_planta = proj_data.get('matriz_planta', [])
                projeto.consumo_semanal = proj_data.get('consumo_semanal', [])
                for nome, mat_data in proj_data.get('materiais', {}).items():
                    categoria = CategoriaMaterial[mat_data.get('categoria', 'OUTROS').upper()]
                    material = Material(nome, mat_data['preco'], mat_data['estoque'], mat_data['unidade'], categoria)
                    projeto.materiais[nome] = material
                for coord_data in proj_data.get('coordenadas', []):
                    coord = Coordenada(coord_data['x'], coord_data['y'], coord_data['z'], coord_data.get('descricao', ''))
                    projeto.coordenadas.append(coord)
                self.projetos[projeto.id] = projeto
            for tarefa_data in dados.get('tarefas', []):
                projeto_id = tarefa_data.get('projeto_id')
                if projeto_id and projeto_id in self.projetos:
                    projeto = self.projetos[projeto_id]
                    prazo = datetime.fromisoformat(tarefa_data['prazo']) if tarefa_data.get('prazo') else None
                    tarefa = Tarefa(tarefa_data['titulo'], tarefa_data['descricao'], tarefa_data['responsavel_id'],
                                   prazo, projeto_id, tarefa_data.get('categoria'))
                    tarefa.id = tarefa_data['id']
                    tarefa.data_criacao = datetime.fromisoformat(tarefa_data['data_criacao'])
                    if tarefa_data.get('data_conclusao'):
                        tarefa.data_conclusao = datetime.fromisoformat(tarefa_data['data_conclusao'])
                    tarefa.status = StatusTarefa[tarefa_data.get('status', 'PENDENTE').upper()]
                    projeto.tarefas.append(tarefa)
            projetos_concluidos_ids = dados.get('projetos_concluidos_ids', [])
            for projeto_id in projetos_concluidos_ids:
                if projeto_id in self.projetos:
                    self.projetos_concluidos.append(self.projetos[projeto_id])
            return True
        except Exception as e:
            print(f'Erro ao carregar: {e}')
            return False

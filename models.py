from datetime import datetime
from enum import Enum
from typing import List, Dict, Tuple, Optional


class TipoUsuario(Enum):
    ENGENHEIRO = "engenheiro"
    GESTOR = "gestor"


class StatusTarefa(Enum):
    PENDENTE = "pendente"
    EM_ANDAMENTO = "em_andamento"
    CONCLUIDA = "concluida"


class StatusProjeto(Enum):
    ATIVO = "ativo"
    CONCLUIDO = "concluido"
    PAUSADO = "pausado"


class CategoriaMaterial(Enum):
    ESTRUTURAL = "estrutural"
    ELETRICA = "eletrica"
    HIDRAULICA = "hidraulica"
    ACABAMENTO = "acabamento"
    OUTROS = "outros"


class Usuario:
    def __init__(self, nome: str, email: str, senha: str, tipo: TipoUsuario):
        self.id = hash(f"{nome}{email}{datetime.now()}")
        self.nome = nome
        self.email = email
        self.senha = senha
        self.tipo = tipo
        self.data_cadastro = datetime.now()


class Tarefa:
    def __init__(self, titulo: str, descricao: str, responsavel_id: int, prazo: Optional[datetime] = None, projeto_id: Optional[int] = None, categoria: Optional[str] = None):
        self.id = hash(f"{titulo}{descricao}{datetime.now()}")
        self.titulo = titulo
        self.descricao = descricao
        self.responsavel_id = responsavel_id
        self.projeto_id = projeto_id
        self.status = StatusTarefa.PENDENTE
        self.data_criacao = datetime.now()
        self.data_conclusao: Optional[datetime] = None
        self.prazo = prazo
        self.categoria = categoria


class Material:
    def __init__(self, nome: str, preco: float, estoque: float, unidade: str, categoria: CategoriaMaterial = CategoriaMaterial.OUTROS):
        self.nome = nome
        self.preco = preco
        self.estoque = estoque
        self.unidade = unidade
        self.categoria = categoria


class Coordenada:
    def __init__(self, x: float, y: float, z: float, descricao: str = ""):
        self.coordenadas: Tuple[float, float, float] = (x, y, z)
        self.descricao = descricao

    def __str__(self):
        return f"({self.coordenadas[0]}, {self.coordenadas[1]}, {self.coordenadas[2]}) - {self.descricao}"


class Projeto:
    def __init__(self, nome: str, descricao: str, gestor_id: int,
                 gasto: float = 0.0, lucro: float = 0.0,
                 prazo: Optional[datetime] = None, responsavel_id: Optional[int] = None):
        self.id = hash(f"{nome}{descricao}{datetime.now()}")
        self.nome = nome
        self.descricao = descricao
        self.gestor_id = gestor_id
        self.data_criacao = datetime.now()
        self.data_conclusao: Optional[datetime] = None
        self.status = StatusProjeto.ATIVO
        self.gasto = gasto
        self.lucro = lucro
        self.prazo = prazo
        self.responsavel_id = responsavel_id
        self.tarefas: List[Tarefa] = []
        self.coordenadas: List[Coordenada] = []
        self.materiais: Dict[str, Material] = {}
        self.consumo_semanal: List[List[float]] = []
        self.matriz_planta: List[List[str]] = []


class Notificacao:
    def __init__(self, tipo: str, mensagem: str, projeto_id: Optional[int] = None, tarefa_id: Optional[int] = None):
        self.id = hash(f"{tipo}{mensagem}{datetime.now()}")
        self.tipo = tipo
        self.mensagem = mensagem
        self.data = datetime.now()
        self.lida = False
        self.projeto_id = projeto_id
        self.tarefa_id = tarefa_id

    def __str__(self):
        return f"[{self.tipo}] {self.mensagem} - {self.data.strftime('%d/%m/%Y %H:%M')}"

# DOCUMENTO DE REQUISITOS
## Sistema de Gestão de Projetos de Engenharia

**Versão:** 1.0  
**Data:** 2024  
**Autor:** Equipe de Desenvolvimento

---

## 1. INTRODUÇÃO

### 1.1 Objetivo do Documento
Este documento descreve os requisitos funcionais e não funcionais do Sistema de Gestão de Projetos de Engenharia, desenvolvido em Python para gerenciar projetos, tarefas, materiais, coordenadas e relatórios em escritórios de engenharia.

### 1.2 Escopo do Projeto
O sistema permite que gestores e engenheiros gerenciem projetos de engenharia de forma organizada, incluindo:
- Cadastro e autenticação de usuários
- Gestão de projetos com informações financeiras
- Atribuição e acompanhamento de tarefas
- Controle de materiais e estoque
- Registro de coordenadas da planta
- Geração de relatórios e estatísticas
- Sistema de notificações automáticas
- Cálculos e projeções

### 1.3 Público-Alvo
- **Gestores de Projetos**: Responsáveis pela administração geral do sistema
- **Engenheiros**: Usuários que executam tarefas e projetos

---

## 2. REQUISITOS FUNCIONAIS

### 2.1 Gestão de Usuários

#### RF-001: Cadastro de Usuários
- **Descrição**: O sistema deve permitir o cadastro de usuários com os seguintes dados:
  - Nome completo
  - Email (único no sistema)
  - Senha
  - Tipo de usuário (Engenheiro ou Gestor)
- **Prioridade**: Alta
- **Regras de Negócio**:
  - Email deve ser único no sistema
  - Senha deve ser fornecida pelo usuário (não gerada automaticamente)
  - ID do usuário é gerado automaticamente usando hash

#### RF-002: Autenticação de Usuários
- **Descrição**: O sistema deve permitir login de usuários cadastrados
- **Prioridade**: Alta
- **Regras de Negócio**:
  - Login realizado através de email e senha
  - Sistema mantém sessão do usuário logado
  - Senhas são persistidas em arquivo JSON

#### RF-003: Controle de Acesso por Perfil
- **Descrição**: O sistema deve exibir menus diferentes conforme o tipo de usuário
- **Prioridade**: Alta
- **Regras de Negócio**:
  - **Gestor**: Acesso completo a todas as funcionalidades
  - **Engenheiro**: Acesso restrito a:
    - Menu de Projetos
    - Menu de Tarefas
    - Notificações
    - Buscar Projeto
  - Engenheiros NÃO têm acesso a:
    - Menu de Materiais
    - Menu de Coordenadas
    - Menu de Relatórios
    - Menu de Cálculos
    - Menu de Estatísticas
    - Menu de Funcionalidades Extras

---

### 2.2 Gestão de Projetos

#### RF-004: Cadastro de Projetos
- **Descrição**: O sistema deve permitir criar projetos com os seguintes dados:
  - Nome do projeto
  - Descrição
  - Custo do projeto (gasto)
  - Lucro esperado
  - Prazo (data limite)
  - Responsável pelo projeto
- **Prioridade**: Alta
- **Regras de Negócio**:
  - Se o cadastro for feito por um Engenheiro, ele automaticamente se torna o responsável
  - Se o cadastro for feito por um Gestor, ele pode escolher qual engenheiro será o responsável
  - Status inicial do projeto é sempre ATIVO
  - ID do projeto é gerado automaticamente

#### RF-005: Visualização de Projetos
- **Descrição**: O sistema deve permitir visualizar todos os projetos cadastrados
- **Prioridade**: Média
- **Regras de Negócio**:
  - Exibe lista de projetos com informações básicas
  - Permite visualizar detalhes completos de um projeto específico

#### RF-006: Detalhes do Projeto
- **Descrição**: O sistema deve exibir informações completas de um projeto:
  - Nome, descrição, status
  - Custo, lucro, prazo
  - Responsável
  - Lista de tarefas associadas
  - Lista de materiais
  - Lista de coordenadas
- **Prioridade**: Média

#### RF-007: Conclusão de Projetos
- **Descrição**: O sistema deve permitir marcar projetos como concluídos
- **Prioridade**: Média
- **Regras de Negócio**:
  - Projetos concluídos são movidos para lista de projetos concluídos
  - Data de conclusão é registrada automaticamente
  - Status muda para CONCLUIDO

#### RF-008: Busca de Projetos
- **Descrição**: O sistema deve permitir buscar projetos por:
  - Nome do projeto
  - Palavra-chave em descrições
  - Palavra-chave em tarefas do projeto
- **Prioridade**: Média
- **Regras de Negócio**:
  - Busca case-insensitive
  - Retorna lista de projetos que correspondem ao critério

---

### 2.3 Gestão de Tarefas

#### RF-009: Criação de Tarefas
- **Descrição**: O sistema deve permitir criar tarefas com:
  - Título
  - Descrição
  - Responsável (ID do engenheiro)
  - Prazo (opcional)
  - Projeto associado (opcional)
  - Categoria (opcional)
- **Prioridade**: Alta
- **Regras de Negócio**:
  - Status inicial é sempre PENDENTE
  - ID da tarefa é gerado automaticamente
  - Data de criação é registrada automaticamente

#### RF-010: Visualização de Tarefas
- **Descrição**: O sistema deve permitir visualizar tarefas:
  - Por projeto
  - Por engenheiro responsável
  - Por status (Pendente, Em Andamento, Concluída)
- **Prioridade**: Alta

#### RF-011: Atualização de Status de Tarefas
- **Descrição**: O sistema deve permitir alterar o status das tarefas:
  - PENDENTE → EM_ANDAMENTO
  - EM_ANDAMENTO → CONCLUÍDA
- **Prioridade**: Alta
- **Regras de Negócio**:
  - Ao concluir, data de conclusão é registrada
  - Tarefas concluídas são registradas no histórico por categoria

#### RF-012: Edição e Remoção de Tarefas
- **Descrição**: O sistema deve permitir editar e remover tarefas
- **Prioridade**: Média
- **Regras de Negócio**:
  - Apenas Gestores podem editar/remover tarefas
  - Engenheiros podem apenas visualizar e atualizar status de suas tarefas

---

### 2.4 Gestão de Materiais

#### RF-013: Cadastro de Materiais
- **Descrição**: O sistema deve permitir cadastrar materiais com:
  - Nome (único no projeto)
  - Preço unitário
  - Quantidade em estoque
  - Unidade de medida
  - Categoria (Estrutural, Elétrica, Hidráulica, Acabamento, Outros)
- **Prioridade**: Alta
- **Regras de Negócio**:
  - Materiais são armazenados em dicionário (chave: nome)
  - ID do material é gerado automaticamente
  - Apenas Gestores podem gerenciar materiais

#### RF-014: Atualização de Estoque e Preço
- **Descrição**: O sistema deve permitir atualizar:
  - Quantidade em estoque
  - Preço unitário do material
- **Prioridade**: Média

#### RF-015: Registro de Consumo Semanal
- **Descrição**: O sistema deve permitir registrar consumo de materiais por semana
- **Prioridade**: Alta
- **Regras de Negócio**:
  - Consumo é armazenado em matriz (semanas × materiais)
  - Cada linha da matriz representa uma semana
  - Cada coluna representa um material
  - Quantidades são registradas por semana

#### RF-016: Alertas de Estoque Baixo
- **Descrição**: O sistema deve gerar notificações quando estoque estiver baixo
- **Prioridade**: Média
- **Regras de Negócio**:
  - Estoque baixo: quantidade < 10 unidades (configurável)
  - Notificação é criada automaticamente

#### RF-017: Organização de Materiais por Categoria
- **Descrição**: O sistema deve permitir visualizar materiais agrupados por categoria
- **Prioridade**: Baixa

---

### 2.5 Gestão de Coordenadas

#### RF-018: Cadastro de Coordenadas
- **Descrição**: O sistema deve permitir cadastrar coordenadas da planta usando tuplas (x, y, z)
- **Prioridade**: Média
- **Regras de Negócio**:
  - Coordenadas são imutáveis (tuplas)
  - ID da coordenada é gerado automaticamente
  - Apenas Gestores podem gerenciar coordenadas

#### RF-019: Criação de Matriz da Planta
- **Descrição**: O sistema deve permitir criar uma matriz representando o layout da obra
- **Prioridade**: Média
- **Regras de Negócio**:
  - Matriz 2D (linhas × colunas)
  - Cada posição pode representar uma área da planta
  - Valores podem ser preenchidos manualmente

#### RF-020: Visualização de Coordenadas
- **Descrição**: O sistema deve permitir visualizar todas as coordenadas cadastradas
- **Prioridade**: Baixa

---

### 2.6 Relatórios e Estatísticas

#### RF-021: Relatório de Consumo por Semana
- **Descrição**: O sistema deve gerar relatório somando consumo por semana (linhas da matriz)
- **Prioridade**: Alta
- **Regras de Negócio**:
  - Soma valores de cada linha da matriz de consumo
  - Multiplica quantidade pelo preço do material
  - Retorna total por semana

#### RF-022: Relatório de Consumo por Material
- **Descrição**: O sistema deve gerar relatório somando consumo por material (colunas da matriz)
- **Prioridade**: Alta
- **Regras de Negócio**:
  - Soma valores de cada coluna da matriz de consumo
  - Multiplica quantidade pelo preço do material
  - Retorna total por material

#### RF-023: Projetos Mais Ativos
- **Descrição**: O sistema deve listar projetos ordenados por número de tarefas ativas
- **Prioridade**: Média
- **Regras de Negócio**:
  - Considera apenas tarefas não concluídas
  - Ordena do maior para o menor número de tarefas

#### RF-024: Estatísticas por Engenheiro
- **Descrição**: O sistema deve exibir estatísticas detalhadas de tarefas por engenheiro:
  - Total de tarefas
  - Tarefas pendentes
  - Tarefas em andamento
  - Tarefas concluídas
- **Prioridade**: Média

#### RF-025: Estatísticas Gerais da Plataforma
- **Descrição**: O sistema deve exibir:
  - Total de projetos, tarefas, engenheiros, gestores
  - Distribuição de tarefas por status
  - Taxa de conclusão de tarefas
  - Taxa de engenheiros ativos
  - Total de materiais e coordenadas cadastrados
- **Prioridade**: Média

#### RF-026: Estatísticas Pessoais (Engenheiro)
- **Descrição**: O sistema deve permitir que engenheiros visualizem suas próprias estatísticas
- **Prioridade**: Baixa

#### RF-027: Engenheiro com Mais Tarefas
- **Descrição**: O sistema deve identificar e exibir o engenheiro com maior número de tarefas
- **Prioridade**: Baixa

#### RF-028: Materiais Mais Consumidos
- **Descrição**: O sistema deve listar os materiais mais consumidos em um projeto
- **Prioridade**: Baixa

---

### 2.7 Cálculos

#### RF-029: Custo Total do Projeto
- **Descrição**: O sistema deve calcular o custo total somando preços × quantidades de materiais
- **Prioridade**: Alta
- **Regras de Negócio**:
  - Considera todos os materiais do projeto
  - Multiplica quantidade pelo preço unitário
  - Retorna valor total

#### RF-030: Divisão de Recursos
- **Descrição**: O sistema deve calcular divisão de recursos (quociente e resto)
- **Prioridade**: Baixa

#### RF-031: Média de Custos de Projetos
- **Descrição**: O sistema deve calcular a média de custos de todos os projetos
- **Prioridade**: Baixa

#### RF-032: Máximo e Mínimo de Custos
- **Descrição**: O sistema deve identificar projetos com maior e menor custo
- **Prioridade**: Baixa

#### RF-033: Média de Tarefas por Projeto
- **Descrição**: O sistema deve calcular a média de tarefas por projeto
- **Prioridade**: Baixa

---

### 2.8 Funcionalidades Extras

#### RF-034: Projeção de Consumo de Materiais
- **Descrição**: O sistema deve projetar consumo futuro de materiais baseado em tendências
- **Prioridade**: Baixa
- **Regras de Negócio**:
  - Usa histórico de consumo semanal
  - Projeta para N semanas futuras
  - Retorna dicionário com projeções por material

#### RF-035: Simulação de Crescimento de Tarefas
- **Descrição**: O sistema deve simular crescimento de tarefas usando recursão
- **Prioridade**: Baixa
- **Regras de Negócio**:
  - Implementa função recursiva
  - Calcula crescimento exponencial
  - Retorna número estimado de tarefas

#### RF-036: Recomendação de Engenheiros para Tarefas
- **Descrição**: O sistema deve sugerir engenheiros para tarefas baseado em histórico
- **Prioridade**: Baixa
- **Regras de Negócio**:
  - Analisa histórico de tarefas por categoria
  - Sugere engenheiro com mais experiência na categoria
  - Retorna lista ordenada de recomendações

#### RF-037: Lista de Projetos Concluídos
- **Descrição**: O sistema deve manter lista separada de projetos concluídos
- **Prioridade**: Baixa

#### RF-038: Engenheiros Ativos e Inativos
- **Descrição**: O sistema deve classificar engenheiros como ativos ou inativos
- **Prioridade**: Baixa
- **Regras de Negócio**:
  - Engenheiro ativo: possui tarefas não concluídas
  - Engenheiro inativo: não possui tarefas ativas
  - Atualização automática baseada em tarefas

---

### 2.9 Sistema de Notificações

#### RF-039: Notificações Automáticas
- **Descrição**: O sistema deve criar notificações automaticamente para:
  - Novos projetos criados
  - Novas tarefas atribuídas
  - Tarefas próximas do prazo (3 dias ou menos)
  - Estoque baixo de materiais
- **Prioridade**: Alta
- **Regras de Negócio**:
  - Notificações são armazenadas por usuário (dicionário)
  - Cada notificação possui ID, tipo, mensagem e data
  - Notificações são marcadas como lidas ao visualizar

#### RF-040: Visualização de Notificações
- **Descrição**: O sistema deve permitir visualizar todas as notificações do usuário logado
- **Prioridade**: Alta
- **Regras de Negócio**:
  - Exibe notificações novas e antigas
  - Diferencia visualmente notificações não lidas
  - Marca como lidas automaticamente ao visualizar

---

### 2.10 Persistência de Dados

#### RF-041: Salvamento Automático
- **Descrição**: O sistema deve salvar todos os dados em arquivo JSON
- **Prioridade**: Alta
- **Regras de Negócio**:
  - Salvamento ocorre ao encerrar o sistema
  - Arquivo padrão: `dados_sistema.json`
  - Serializa todos os objetos (usuários, projetos, tarefas, materiais, coordenadas, notificações)

#### RF-042: Carregamento Automático
- **Descrição**: O sistema deve carregar dados salvos ao iniciar
- **Prioridade**: Alta
- **Regras de Negócio**:
  - Carrega dados do arquivo JSON se existir
  - Restaura todos os objetos e relacionamentos
  - Se arquivo não existir, inicia sistema vazio

#### RF-043: Tratamento de Erros em Persistência
- **Descrição**: O sistema deve tratar erros ao salvar/carregar dados
- **Prioridade**: Média
- **Regras de Negócio**:
  - Exibe mensagens de erro claras
  - Sistema continua funcionando mesmo se persistência falhar
  - Usa try/except para capturar exceções

---

## 3. REQUISITOS NÃO FUNCIONAIS

### 3.1 Performance

#### RNF-001: Tempo de Resposta
- **Descrição**: Operações básicas devem responder em menos de 1 segundo
- **Prioridade**: Média

#### RNF-002: Eficiência de Busca
- **Descrição**: Busca de projetos deve usar algoritmos eficientes
- **Prioridade**: Média

### 3.2 Usabilidade

#### RNF-003: Interface Intuitiva
- **Descrição**: Interface CLI deve ser clara e fácil de usar
- **Prioridade**: Alta
- **Especificações**:
  - Menus hierárquicos organizados
  - Mensagens coloridas (verde: sucesso, vermelho: erro, amarelo: aviso)
  - Separação visual clara entre seções

#### RNF-004: Mensagens de Feedback
- **Descrição**: Sistema deve fornecer feedback claro para todas as operações
- **Prioridade**: Alta
- **Especificações**:
  - Mensagens de sucesso para operações concluídas
  - Mensagens de erro descritivas
  - Avisos para situações especiais

#### RNF-005: Nomenclatura de Menus
- **Descrição**: Menus devem usar nomenclatura consistente
- **Prioridade**: Média
- **Especificações**:
  - Menu principal: "Deslogar" (quando logado) ou "Sair" (quando não logado)
  - Submenus: "Voltar" (em vez de "Sair")

### 3.3 Confiabilidade

#### RNF-006: Validação de Dados
- **Descrição**: Sistema deve validar todos os dados de entrada
- **Prioridade**: Alta
- **Especificações**:
  - Validação de IDs existentes
  - Validação de formatos de data
  - Validação de valores numéricos

#### RNF-007: Tratamento de Erros
- **Descrição**: Sistema deve tratar erros graciosamente
- **Prioridade**: Alta
- **Especificações**:
  - Não deve encerrar inesperadamente
  - Mensagens de erro claras
  - Logs de erros para depuração

### 3.4 Manutenibilidade

#### RNF-008: Código Organizado
- **Descrição**: Código deve seguir princípios de organização
- **Prioridade**: Alta
- **Especificações**:
  - Separação de responsabilidades (models, sistema, interface)
  - Código sem comentários (conforme solicitado)
  - Nomes de variáveis e funções descritivos

#### RNF-009: Modularidade
- **Descrição**: Sistema deve ser dividido em módulos reutilizáveis
- **Prioridade**: Alta
- **Especificações**:
  - `models.py`: Classes de dados
  - `sistema.py`: Lógica de negócio
  - `interface.py`: Interface do usuário
  - `cores.py`: Formatação visual

### 3.5 Portabilidade

#### RNF-010: Compatibilidade com Python
- **Descrição**: Sistema deve funcionar em Python 3.7+
- **Prioridade**: Alta

#### RNF-011: Compatibilidade de Sistema Operacional
- **Descrição**: Sistema deve funcionar em Windows, Linux e macOS
- **Prioridade**: Média
- **Especificações**:
  - Limpeza de tela adaptada ao SO (`clear` ou `cls`)

---

## 4. REGRAS DE NEGÓCIO

### 4.1 Autenticação e Autorização

**RN-001**: Apenas usuários cadastrados podem fazer login no sistema.

**RN-002**: Senhas devem ser fornecidas pelo usuário durante o cadastro (não geradas automaticamente).

**RN-003**: Email deve ser único no sistema.

**RN-004**: Gestores têm acesso completo a todas as funcionalidades.

**RN-005**: Engenheiros têm acesso restrito apenas a:
- Menu de Projetos
- Menu de Tarefas
- Notificações
- Buscar Projeto

**RN-006**: Engenheiros NÃO podem acessar:
- Menu de Materiais
- Menu de Coordenadas
- Menu de Relatórios
- Menu de Cálculos
- Menu de Estatísticas
- Menu de Funcionalidades Extras

### 4.2 Gestão de Projetos

**RN-007**: Ao criar um projeto como Engenheiro, o próprio engenheiro se torna automaticamente o responsável.

**RN-008**: Ao criar um projeto como Gestor, o gestor pode escolher qual engenheiro será o responsável.

**RN-009**: Status inicial de um projeto é sempre ATIVO.

**RN-010**: Projetos concluídos são movidos para lista de projetos concluídos.

**RN-011**: Projetos devem ter: nome, descrição, custo, lucro, prazo e responsável.

### 4.3 Gestão de Tarefas

**RN-012**: Status inicial de uma tarefa é sempre PENDENTE.

**RN-013**: Apenas Gestores podem editar ou remover tarefas.

**RN-014**: Engenheiros podem apenas visualizar e atualizar status de suas próprias tarefas.

**RN-015**: Tarefas concluídas são registradas no histórico por categoria para recomendações futuras.

**RN-016**: Lembretes de prazo são enviados para tarefas com 3 dias ou menos até o vencimento.

### 4.4 Gestão de Materiais

**RN-017**: Apenas Gestores podem gerenciar materiais.

**RN-018**: Nome do material deve ser único dentro de um projeto.

**RN-019**: Estoque baixo é considerado quando quantidade < 10 unidades.

**RN-020**: Consumo semanal é armazenado em matriz (semanas × materiais).

**RN-021**: Materiais são organizados por categoria: Estrutural, Elétrica, Hidráulica, Acabamento, Outros.

### 4.5 Gestão de Coordenadas

**RN-022**: Apenas Gestores podem gerenciar coordenadas.

**RN-023**: Coordenadas são armazenadas como tuplas imutáveis (x, y, z).

**RN-024**: Matriz da planta representa layout 2D da obra.

### 4.6 Notificações

**RN-025**: Notificações são criadas automaticamente para:
- Novos projetos (para engenheiros do projeto)
- Novas tarefas (para o responsável)
- Tarefas próximas do prazo (3 dias ou menos)
- Estoque baixo de materiais (para gestores)

**RN-026**: Notificações são armazenadas por usuário em dicionário.

**RN-027**: Notificações são marcadas como lidas automaticamente ao visualizar.

### 4.7 Persistência

**RN-028**: Dados são salvos automaticamente ao encerrar o sistema.

**RN-029**: Dados são carregados automaticamente ao iniciar o sistema.

**RN-030**: Arquivo de persistência padrão: `dados_sistema.json`.

**RN-031**: Se arquivo não existir, sistema inicia vazio.

**RN-032**: Senhas são persistidas no arquivo JSON.

### 4.8 Interface

**RN-033**: Menu principal exibe "Deslogar" quando usuário está logado, "Sair" quando não está.

**RN-034**: Todos os submenus exibem "Voltar" em vez de "Sair".

**RN-035**: Mensagens devem usar cores apropriadas:
- Verde: sucesso
- Vermelho: erro
- Amarelo: aviso
- Azul: informação

---

## 5. ESTRUTURAS DE DADOS E CONCEITOS TÉCNICOS

### 5.1 Estruturas de Dados Obrigatórias

#### 5.1.1 Listas
- **Uso**: Armazenar coleções dinâmicas
- **Exemplos**:
  - `projeto.tarefas`: Lista de tarefas do projeto
  - `projeto.coordenadas`: Lista de coordenadas da planta
  - `projetos_concluidos`: Lista de projetos finalizados
  - `engenheiros_ativos`: Lista de engenheiros com tarefas ativas
  - `engenheiros_inativos`: Lista de engenheiros sem tarefas ativas
  - `consumo_semanal`: Matriz (lista de listas) para consumo por semana

#### 5.1.2 Tuplas
- **Uso**: Dados imutáveis
- **Exemplos**:
  - `Coordenada.coordenadas`: Tupla (x, y, z) representando coordenadas fixas da planta

#### 5.1.3 Dicionários
- **Uso**: Acesso rápido por chave
- **Exemplos**:
  - `sistema.usuarios`: Dict[int, Usuario] - acesso por ID
  - `projeto.materiais`: Dict[str, Material] - acesso por nome
  - `sistema.notificacoes`: Dict[int, List[Notificacao]] - notificações por usuário
  - `historico_tarefas_por_categoria`: Dict[str, int] - histórico para recomendações

#### 5.1.4 Matrizes
- **Uso**: Dados bidimensionais
- **Exemplos**:
  - `matriz_planta`: Matriz 2D representando layout da obra
  - `consumo_semanal`: Matriz (semanas × materiais) para consumo semanal

#### 5.1.5 Strings
- **Uso**: Busca e manipulação de textos
- **Exemplos**:
  - Busca case-insensitive em nomes e descrições
  - Manipulação de strings para formatação

### 5.2 Conceitos de Programação

#### 5.2.1 Programação Orientada a Objetos (OOP)
- **Classes**: Usuario, Tarefa, Material, Coordenada, Projeto, Notificacao
- **Encapsulamento**: Atributos e métodos organizados em classes
- **Abstração**: Classes representam entidades do domínio

#### 5.2.2 Enums
- **TipoUsuario**: ENGENHEIRO, GESTOR
- **StatusTarefa**: PENDENTE, EM_ANDAMENTO, CONCLUÍDA
- **StatusProjeto**: ATIVO, CONCLUIDO, PAUSADO
- **CategoriaMaterial**: ESTRUTURAL, ELETRICA, HIDRAULICA, ACABAMENTO, OUTROS

#### 5.2.3 Funções
- **Modularização**: Código organizado em funções reutilizáveis
- **Parâmetros e Retorno**: Funções com tipos definidos
- **Recursão**: Implementada em `simular_crescimento_tarefas()`

#### 5.2.4 Estruturas de Controle
- **Seleção**: if/else para validações e controle de fluxo
- **Repetição**: for/while para processamento de listas e matrizes
- **Tratamento de Exceções**: try/except para erros

#### 5.2.5 Persistência de Dados
- **Serialização JSON**: Conversão de objetos Python para JSON
- **Deserialização JSON**: Conversão de JSON para objetos Python
- **File I/O**: Leitura e escrita de arquivos

---

## 6. PERFIS DE USUÁRIO

### 6.1 Gestor

**Permissões**:
- ✅ Cadastrar usuários (engenheiros e gestores)
- ✅ Criar, editar e remover projetos
- ✅ Criar, editar e remover tarefas
- ✅ Atribuir tarefas a engenheiros
- ✅ Gerenciar materiais (adicionar, editar, remover)
- ✅ Registrar consumo semanal
- ✅ Gerenciar coordenadas
- ✅ Criar matriz da planta
- ✅ Visualizar todos os relatórios
- ✅ Executar cálculos
- ✅ Visualizar estatísticas completas
- ✅ Acessar funcionalidades extras
- ✅ Visualizar notificações
- ✅ Buscar projetos

**Restrições**: Nenhuma

### 6.2 Engenheiro

**Permissões**:
- ✅ Cadastrar-se no sistema
- ✅ Criar projetos (torna-se automaticamente responsável)
- ✅ Visualizar projetos
- ✅ Criar tarefas próprias
- ✅ Visualizar tarefas atribuídas
- ✅ Atualizar status de tarefas (Pendente → Em Andamento → Concluída)
- ✅ Visualizar notificações
- ✅ Buscar projetos
- ✅ Visualizar estatísticas pessoais

**Restrições**:
- ❌ Não pode gerenciar materiais
- ❌ Não pode gerenciar coordenadas
- ❌ Não pode visualizar relatórios gerais
- ❌ Não pode executar cálculos avançados
- ❌ Não pode visualizar estatísticas de outros engenheiros
- ❌ Não pode acessar funcionalidades extras
- ❌ Não pode editar/remover tarefas de outros
- ❌ Não pode escolher responsável ao criar projeto (sempre será ele mesmo)

---

## 7. CASOS DE USO PRINCIPAIS

### 7.1 UC-001: Cadastro e Login de Usuário

**Ator**: Usuário (Engenheiro ou Gestor)

**Fluxo Principal**:
1. Usuário escolhe opção "Cadastrar-se"
2. Sistema solicita: nome, email, senha, tipo
3. Sistema valida email único
4. Sistema cria usuário e exibe mensagem de sucesso
5. Usuário escolhe opção "Login"
6. Sistema solicita email e senha
7. Sistema valida credenciais
8. Sistema autentica usuário e exibe menu apropriado

**Fluxos Alternativos**:
- 3a. Email já existe: sistema exibe erro e solicita novo email
- 7a. Credenciais inválidas: sistema exibe erro e solicita novamente

### 7.2 UC-002: Criar Projeto

**Ator**: Usuário logado (Engenheiro ou Gestor)

**Fluxo Principal**:
1. Usuário escolhe "Menu de Projetos" → "Criar Projeto"
2. Sistema solicita: nome, descrição, custo, lucro, prazo
3. Se Gestor: sistema solicita escolher responsável (engenheiro)
4. Se Engenheiro: sistema atribui automaticamente o próprio usuário como responsável
5. Sistema cria projeto com status ATIVO
6. Sistema notifica engenheiros do projeto
7. Sistema exibe mensagem de sucesso

**Fluxos Alternativos**:
- 3a. Gestor escolhe engenheiro inexistente: sistema exibe erro

### 7.3 UC-003: Atribuir Tarefa a Engenheiro

**Ator**: Gestor

**Fluxo Principal**:
1. Gestor escolhe "Menu de Tarefas" → "Criar Tarefa"
2. Sistema solicita: título, descrição, prazo (opcional), projeto (opcional), categoria (opcional)
3. Sistema lista engenheiros disponíveis
4. Gestor escolhe engenheiro responsável
5. Sistema cria tarefa com status PENDENTE
6. Sistema notifica engenheiro responsável
7. Sistema exibe mensagem de sucesso

### 7.4 UC-004: Registrar Consumo Semanal de Materiais

**Ator**: Gestor

**Fluxo Principal**:
1. Gestor escolhe "Menu de Materiais" → "Registrar Consumo Semanal"
2. Sistema lista projetos disponíveis
3. Gestor escolhe projeto
4. Sistema exibe materiais do projeto
5. Sistema solicita número da semana
6. Para cada material, sistema solicita quantidade consumida
7. Sistema atualiza matriz de consumo semanal
8. Sistema verifica estoque e gera alertas se necessário
9. Sistema exibe mensagem de sucesso

**Fluxos Alternativos**:
- 8a. Estoque baixo: sistema cria notificação de alerta

### 7.5 UC-005: Visualizar Relatório de Consumo

**Ator**: Gestor

**Fluxo Principal**:
1. Gestor escolhe "Menu de Relatórios" → "Relatório por Semana" ou "Relatório por Material"
2. Sistema lista projetos disponíveis
3. Gestor escolhe projeto
4. Sistema processa matriz de consumo
5. Sistema calcula totais (por semana ou por material)
6. Sistema exibe relatório formatado
7. Gestor visualiza relatório

### 7.6 UC-006: Buscar Projeto

**Ator**: Usuário logado

**Fluxo Principal**:
1. Usuário escolhe "Buscar Projeto"
2. Sistema solicita termo de busca
3. Sistema busca em nomes, descrições e tarefas dos projetos
4. Sistema exibe lista de projetos encontrados
5. Usuário pode escolher visualizar detalhes de um projeto

**Fluxos Alternativos**:
- 4a. Nenhum projeto encontrado: sistema exibe mensagem informativa

### 7.7 UC-007: Visualizar Notificações

**Ator**: Usuário logado

**Fluxo Principal**:
1. Usuário escolhe "Notificações"
2. Sistema busca notificações do usuário
3. Sistema exibe lista de notificações (novas primeiro)
4. Sistema marca notificações como lidas
5. Usuário visualiza notificações

---

## 8. RESTRIÇÕES E LIMITAÇÕES

### 8.1 Restrições Técnicas

**R-001**: Sistema funciona apenas em ambiente CLI (linha de comando).

**R-002**: Persistência de dados utiliza formato JSON (não utiliza banco de dados).

**R-003**: Sistema suporta apenas um usuário logado por vez.

**R-004**: IDs são gerados usando hash, podendo haver colisões em sistemas muito grandes.

### 8.2 Limitações Funcionais

**L-001**: Sistema não possui recuperação de senha automática.

**L-002**: Sistema não possui histórico de alterações (auditoria).

**L-003**: Sistema não possui exportação de relatórios em formatos externos (PDF, Excel).

**L-004**: Sistema não possui backup automático de dados.

**L-005**: Sistema não possui validação de formato de email.

**L-006**: Sistema não possui criptografia de senhas (armazenadas em texto plano no JSON).

---

## 9. GLOSSÁRIO

- **CLI**: Command Line Interface (Interface de Linha de Comando)
- **Enum**: Tipo de dado que define um conjunto fixo de valores
- **Hash**: Função que mapeia dados de tamanho arbitrário para valores de tamanho fixo
- **JSON**: JavaScript Object Notation, formato de dados leve e legível
- **Matriz**: Estrutura de dados bidimensional (lista de listas)
- **OOP**: Object-Oriented Programming (Programação Orientada a Objetos)
- **Serialização**: Processo de converter objetos em formato que pode ser armazenado ou transmitido
- **Tupla**: Estrutura de dados imutável e ordenada

---

## 10. APÊNDICES

### 10.1 Estrutura de Arquivos do Projeto

```
projeto/
├── models.py              # Classes de dados (Usuario, Tarefa, Material, etc.)
├── sistema.py             # Lógica de negócio (SistemaGestaoProjetos)
├── interface.py           # Interface do usuário (menus e interações)
├── cores.py               # Formatação visual (cores e estilos)
├── main.py                # Ponto de entrada do sistema
├── exemplo_uso.py         # Exemplos de uso programático
├── dados_sistema.json     # Arquivo de persistência (gerado automaticamente)
├── README.md              # Documentação geral
└── REQUISITOS.md          # Este documento
```

### 10.2 Dependências

- **Python**: 3.7 ou superior
- **Módulos padrão utilizados**:
  - `datetime`: Manipulação de datas
  - `enum`: Definição de enums
  - `typing`: Tipagem estática
  - `os`: Operações do sistema operacional
  - `json`: Serialização JSON
  - `hash`: Geração de IDs

### 10.3 Convenções de Código

- Nomes de classes: PascalCase (ex: `SistemaGestaoProjetos`)
- Nomes de funções e variáveis: snake_case (ex: `criar_projeto`)
- Nomes de constantes: UPPER_SNAKE_CASE (ex: `TipoUsuario`)
- Código sem comentários (conforme solicitado)
- Separação de responsabilidades por módulo

---

**Fim do Documento de Requisitos**

# Sistema de Gestão de Projetos de Engenharia

Sistema desenvolvido em Python para gerenciar projetos de engenharia, permitindo que engenheiros e gestores organizem e acompanhem projetos, incluindo cadastro de responsáveis, tarefas, materiais, coordenadas da planta e relatórios de insumos.

## Funcionalidades Principais

### 1. Cadastro de Usuários e Tarefas

#### Engenheiro
- Pode se cadastrar no sistema
- Pode visualizar tarefas atribuídas
- Pode adicionar ou remover tarefas
- Possui histórico de tarefas concluídas

#### Gestor
- Pode cadastrar engenheiros
- Pode atribuir tarefas a engenheiros
- Pode editar ou remover tarefas
- Pode visualizar relatórios gerais do projeto

### 2. Coordenadas da Planta
- Inserir coordenadas fixas usando tuplas
- Representar a planta em uma matriz (layout da obra)
- Consultar e imprimir coordenadas cadastradas

### 3. Gestão de Materiais
- Usar dicionários para armazenar materiais com preço e estoque
- Permitir atualização de estoque e preço
- Registrar consumo semanal em uma matriz
- Emitir alerta se o estoque for insuficiente

### 4. Relatórios de Insumos
- Gerar relatórios com funções:
  - Soma por semana (linhas da matriz)
  - Soma por material (colunas da matriz)
- Exibir relatórios organizados para análise do gestor

### 5. Busca por Projeto
- Permitir busca por nome do projeto ou palavra-chave em tarefas
- Usar strings para verificar se uma palavra aparece em descrições
- Exibir todas as informações do projeto encontrado

### 6. Cálculos
- Criar funções para cálculos específicos:
  - Custo total do projeto (somando preços × quantidades)
  - Divisão de recursos (quociente e resto)

### 7. Notificações
- Avisos sobre novos projetos ou tarefas
- Lembretes de tarefas próximas do prazo
- Alertas de estoque baixo
- Interface melhorada para visualização de notificações

### 8. Relatórios e Estatísticas
- **Projetos Mais Ativos**: Lista os projetos com mais tarefas ativas
- **Tarefas por Engenheiro**: Estatísticas detalhadas de tarefas por engenheiro (pendentes, em andamento, concluídas)
- **Estatísticas Gerais da Plataforma**: 
  - Total de projetos, tarefas, engenheiros e gestores
  - Distribuição de tarefas por status
  - Taxa de conclusão de tarefas
  - Taxa de engenheiros ativos
  - Total de materiais e coordenadas cadastrados
- **Estatísticas Pessoais**: Para engenheiros visualizarem suas próprias estatísticas

## Estrutura do Projeto

```
gestao_projetos_engenharia/
├── models.py          # Modelos de dados (Usuario, Tarefa, Material, etc.)
├── sistema.py         # Lógica principal do sistema
├── interface.py       # Interface de usuário (menus e interações)
├── main.py            # Arquivo principal para execução
└── README.md          # Documentação
```

## Como Executar

1. Certifique-se de ter Python 3.7+ instalado
2. Navegue até o diretório do projeto:
   ```bash
   cd gestao_projetos_engenharia
   ```
3. Execute o arquivo principal:
   ```bash
   python main.py
   ```

## Uso do Sistema

### Primeiro Acesso

1. **Cadastre-se**: Escolha a opção 1 no menu principal e crie sua conta
   - Escolha entre Engenheiro ou Gestor
2. **Login**: Faça login com seu email e senha

### Para Gestores

- Criar projetos
- Cadastrar engenheiros
- Atribuir tarefas a engenheiros
- Visualizar relatórios gerais
- Gerenciar materiais e coordenadas
- Visualizar projetos mais ativos
- Analisar estatísticas de tarefas por engenheiro
- Acompanhar estatísticas gerais da plataforma

### Para Engenheiros

- Visualizar tarefas atribuídas
- Adicionar suas próprias tarefas
- Concluir tarefas
- Visualizar histórico de tarefas concluídas
- Consultar materiais e coordenadas
- Visualizar estatísticas pessoais
- Receber notificações sobre novas tarefas e prazos

## Estruturas de Dados Utilizadas

- **Tuplas**: Para coordenadas fixas (x, y, z)
- **Listas**: Para armazenar tarefas, coordenadas, etc.
- **Dicionários**: Para materiais (chave: nome do material)
- **Matrizes**: Para layout da planta e consumo semanal de materiais
- **Strings**: Para busca e comparação de textos

## Exemplos de Uso

### Criar um Projeto (Gestor)
1. Menu Principal → Menu de Projetos → Criar Projeto
2. Informe nome e descrição

### Adicionar Material
1. Menu Principal → Menu de Materiais → Adicionar Material
2. Selecione o projeto
3. Informe nome, preço, estoque e unidade

### Registrar Consumo Semanal
1. Menu Principal → Menu de Materiais → Registrar Consumo Semanal
2. Selecione o projeto
3. Informe a semana e o consumo de cada material

### Buscar Projeto
1. Menu Principal → Buscar Projeto
2. Digite o nome ou palavra-chave
3. Visualize os resultados

### Visualizar Estatísticas (Gestor)
1. Menu Principal → Menu de Estatísticas
2. Escolha uma opção:
   - Projetos Mais Ativos: Ver projetos com mais tarefas ativas
   - Tarefas por Engenheiro: Estatísticas detalhadas por engenheiro
   - Estatísticas Gerais: Visão geral da plataforma

### Visualizar Estatísticas (Engenheiro)
1. Menu Principal → Menu de Estatísticas
2. Escolha uma opção:
   - Minhas Estatísticas: Ver suas próprias estatísticas
   - Estatísticas Gerais: Visão geral da plataforma

### Ver Notificações
1. Menu Principal → Notificações
2. Visualize todas as suas notificações (novas e antigas)
3. Notificações são marcadas como lidas automaticamente ao visualizar

## Notas Técnicas

- O sistema utiliza hash para gerar IDs únicos
- Estoque baixo é considerado quando < 10 unidades (configurável)
- Lembretes de prazo são enviados para tarefas com 3 dias ou menos
- Todas as datas são armazenadas como objetos `datetime`
- Notificações são criadas automaticamente para novos projetos e tarefas
- Estatísticas são calculadas em tempo real baseadas nos dados atuais
- Projetos mais ativos são ordenados por número de tarefas não concluídas

## Desenvolvido em Python

Este sistema foi desenvolvido como uma simulação de ambiente digital para escritórios de engenharia, utilizando estruturas de dados fundamentais do Python (listas, tuplas, dicionários, matrizes) e programação orientada a objetos.

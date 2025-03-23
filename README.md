# AI-HACKAGENTS - Sistema Inteligente de Gerenciamento de Chamados

![Logo do Projeto](https://i.imgur.com/1QgrNNf.png)

https://www.mermaidchart.com/raw/9220e014-cbb2-4c68-9a56-b365ba3c186b?theme=light&version=v0.1&format=svg
## 📋 Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Arquitetura do Sistema](#arquitetura-do-sistema)
- [Requisitos](#requisitos)
- [Configuração Passo a Passo](#configuração-passo-a-passo)
- [Como Executar](#como-executar)
- [Componentes Detalhados](#componentes-detalhados)
- [Solução de Problemas](#solução-de-problemas)
- [Exemplos de Uso](#exemplos-de-uso)
- [FAQ](#faq)

## 📖 Sobre o Projeto

O AI-HACKAGENTS é um sistema inteligente de gerenciamento de chamados que utiliza múltiplos agentes de IA trabalhando em conjunto para automatizar o processamento de tickets de suporte. O sistema é capaz de:

- **Classificar chamados** por setor (Financeiro, Jurídico, Marketing, Vendas)
- **Definir prioridades** (Urgente, Intermediário, Normal)
- **Realizar análise técnica** detalhada
- **Gerenciar o fluxo** de processamento do chamado
- **Gerar relatórios** consolidados

Os agentes trabalham de forma colaborativa, como uma equipe real de suporte, para processar e encaminhar chamados com eficiência e precisão.

## 🏗️ Arquitetura do Sistema

### Diagrama de Fluxo

```
┌─────────────────┐     ┌──────────────────────────────────────────────────────┐
│                 │     │                                                      │
│  Banco de Dados │◄────┤                  Sistema de Agentes                  │
│   (Neon DB)     │     │                                                      │
│                 │     │  ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────┐  │
└────────┬────────┘     │  │         │   │         │   │         │   │     │  │
         │              │  │  AG1:   │   │  AG2:   │   │  AG3:   │   │     │  │
         │              │  │ Classi- │   │ Classi- │   │ Análise │   │ ... │  │
         │              │  │ ficador │──►│ ficador │──►│ Técnica │──►│     │  │
         │              │  │  Setor  │   │ Priori- │   │         │   │     │  │
┌────────▼────────┐     │  │         │   │  dade   │   │         │   │     │  │
│                 │     │  └─────────┘   └─────────┘   └─────────┘   └─────┘  │
│    Pinecone     │◄────┤                                                      │
│ (Vector Store)  │     └──────────────────────────────────────────────────────┘
│                 │
└─────────────────┘
```

### Fluxo de Processamento

1. O sistema obtém chamados abertos do banco de dados Neon
2. Cada chamado passa por uma sequência de agentes especializados:
   - **AG1**: Classifica o chamado por setor
   - **AG2**: Define a prioridade do chamado
   - **AG3**: Realiza análise técnica detalhada
   - **AG4**: Gerencia o fluxo do chamado
   - **AG5**: Gera relatório final consolidado
3. Os resultados de cada etapa são armazenados no banco de dados
4. Os vetores de embeddings são armazenados no Pinecone para busca semântica

## 🛠️ Requisitos

### Serviços Externos

- Conta na [OpenAI](https://platform.openai.com) (para acesso aos modelos GPT)
- Conta no [Neon DB](https://neon.tech) (banco de dados PostgreSQL serverless)
- Conta no [Pinecone](https://www.pinecone.io) (armazenamento de vetores)

### Requisitos Técnicos

- Python 3.9+
- Ambiente virtual (venv)
- Dependências listadas em `requirements.txt`

## 🚀 Configuração Passo a Passo

### 1. Preparação do Ambiente Local


```

#### 1.2. Configure o Ambiente Virtual

**Windows:**
```powershell
# Criar ambiente virtual
python -m venv .venv

# Ativar ambiente virtual
.venv\Scripts\Activate.ps1

# Instalar dependências
uv pip install --system -r requirements.txt
```

**Linux/Mac:**
```bash
# Criar ambiente virtual
python -m venv .venv

# Ativar ambiente virtual
source .venv/bin/activate

# Instalar dependências
uv pip install --system -r requirements.txt
```

### 2. Configuração dos Serviços Externos

#### 2.1. Configuração do Neon DB

1. **Criar uma Conta no Neon DB**
   - Acesse [https://neon.tech](https://neon.tech)
   - Registre-se para uma nova conta
   - Faça login na sua conta

2. **Criar um Novo Projeto**
   - No painel do Neon, clique em "New Project"
   - Dê um nome ao projeto (ex: "ai-hackagents")
   - Selecione uma região próxima à sua localização

   ![Neon DB - Criar Projeto](https://i.imgur.com/lM8T1JD.png)

3. **Obter a URL de Conexão**
   - Após a criação do projeto, clique em "Connection Details"
   - Selecione "Connection String"
   - Copie a string de conexão completa

   ![Neon DB - Connection String](https://i.imgur.com/6rjDGLP.png)

#### 2.2. Configuração do Pinecone

1. **Criar uma Conta no Pinecone**
   - Acesse [https://www.pinecone.io](https://www.pinecone.io)
   - Registre-se para uma nova conta
   - Faça login na sua conta

2. **Criar um Novo Índice**
   - No painel do Pinecone, clique em "Create Index"
   - Preencha os campos:
     - **Nome do índice**: "suporte-chamados"
     - **Dimensão**: 1536 (para embeddings da OpenAI)
     - **Métrica**: "cosine"
     - **Ambiente**: "us-east-1"

   ![Pinecone - Criar Índice](https://i.imgur.com/sB5XE6e.png)

3. **Obter a API Key**
   - No painel do Pinecone, vá para "API Keys"
   - Copie a API Key

   ![Pinecone - API Key](https://i.imgur.com/PRTUM58.png)

#### 2.3. Configuração da OpenAI

1. **Obter uma API Key da OpenAI**
   - Acesse [https://platform.openai.com](https://platform.openai.com)
   - Crie uma conta ou faça login
   - Vá para "API Keys"
   - Clique em "Create new secret key"
   - Dê um nome à chave e copie-a

   ![OpenAI - API Key](https://i.imgur.com/DIdQNdh.png)

### 3. Configuração do Projeto

#### 3.1. Criar o Arquivo .env

Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

```
OPENAI_API_KEY=sua_chave_da_openai
PINECONE_API_KEY=sua_chave_do_pinecone
NEON_DB_URL=sua_url_do_neon_db
OPENAI_API_BASE=https://api.openai.com/v1
```

Substitua os valores pelos que você obteve nas etapas anteriores.

### 4. Preparação do Banco de Dados

#### 4.1. Criar e Popular o Banco de Dados

Execute o script de criação e população do banco de dados:

```powershell
python tools/code_popular_neon.py
```

Este script irá:
- Conectar-se ao seu banco Neon DB
- Criar a tabela de chamados
- Inserir chamados de exemplo

> **Nota:** Certifique-se de que a conexão com o Neon DB está funcionando corretamente. Verifique os logs para confirmar que os chamados foram inseridos com sucesso.

#### 4.2. Criar as Tabelas Adicionais

O SQL para criar as tabelas está no arquivo `tools/neon_chamados.sql`. Você pode executar esses comandos diretamente no editor SQL do Neon DB, ou usar um cliente PostgreSQL como o psql:

```bash
psql "sua_url_do_neon_db" -f tools/neon_chamados.sql
```

Isso criará todas as tabelas necessárias para o sistema:
- `chamados`: Armazena os chamados iniciais
- `classificacao_setor`: Armazena a classificação por setor
- `classificacao_prioridade`: Armazena a classificação por prioridade
- `analise_tecnica`: Armazena a análise técnica detalhada
- `andamento_chamados`: Armazena o andamento dos chamados
- `relatorio_final`: Armazena os relatórios finais

### 5. Configuração do Pinecone

Execute o script para configurar o Pinecone:

```powershell
python tools/code_popular_pinecone.py
```

Este script irá:
- Conectar-se ao seu índice no Pinecone
- Configurar os embeddings iniciais para os chamados

## ▶️ Como Executar

Há duas maneiras de executar o sistema:

### Opção 1: Usando CrewAI Puro

```powershell
python agents/crewai_agents.py
```

### Opção 2: Usando LangGraph com CrewAI

```powershell
python teste_crewai_agents.py
```

## 🧩 Componentes Detalhados

### Agentes e suas Funções

#### AG1: Classificador de Setor
- **Função**: Analisa o chamado e classifica em um dos setores
- **Comportamento**: Examina o conteúdo e identifica se pertence a Financeiro, Jurídico, Marketing ou Vendas
- **Resultado**: Setor + justificativa da classificação

#### AG2: Classificador de Prioridade
- **Função**: Define a prioridade do chamado
- **Comportamento**: Avalia o impacto e urgência para classificar como Urgente, Intermediário ou Normal
- **Resultado**: Nível de prioridade + justificativa

#### AG3: Analista Técnico
- **Função**: Fornece análise técnica detalhada
- **Comportamento**: Identifica o sistema afetado, problema específico, impacto e propõe soluções
- **Resultado**: Análise técnica estruturada

#### AG4: Gerenciador de Chamado
- **Função**: Coordena o fluxo do chamado
- **Comportamento**: Verifica as classificações, define próximos passos e responsáveis
- **Resultado**: Status e plano de ação

#### AG5: Gerador de Relatório
- **Função**: Cria relatório final consolidado
- **Comportamento**: Integra todas as informações em um relatório estruturado
- **Resultado**: Relatório completo com todos os detalhes

### Arquitetura de Bancos de Dados

#### Banco de Dados Relacional (Neon DB)

```
┌─────────────┐       ┌─────────────────────┐       ┌────────────────────────┐
│             │       │                     │       │                        │
│  chamados   │──┐    │ classificacao_setor │       │ classificacao_prioridade│
│             │  │    │                     │       │                        │
└─────────────┘  │    └─────────────────────┘       └────────────────────────┘
                 │                 ▲                              ▲
                 │                 │                              │
                 └─────────────────┴──────────────────────────────┘
                                   │
                                   │
                 ┌────────────────┐│┌────────────────┐    ┌──────────────┐
                 │                ││││                │    │              │
                 │analise_tecnica ││││andamento_chamados   │relatorio_final
                 │                ││││                │    │              │
                 └────────────────┘│└────────────────┘    └──────────────┘
                                   │                              ▲
                                   │                              │
                                   └──────────────────────────────┘
```

#### Banco de Vetores (Pinecone)
- Armazena embeddings de chamados para busca semântica
- Permite encontrar chamados similares rapidamente
- Utiliza embeddings da OpenAI para representação vetorial

### Fluxo dos Dados

```
┌─────────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐
│  Chamado    │────►│          │────►│          │────►│          │
│  Inicial    │     │   AG1    │     │   AG2    │     │   AG3    │
│             │     │          │     │          │     │          │
└─────────────┘     └──────────┘     └──────────┘     └──────────┘
                     Classificar      Definir          Análise
                       Setor         Prioridade        Técnica
                         │               │                │
                         ▼               ▼                ▼
                    ┌─────────────────────────────────────────┐
                    │                                         │
                    │               Banco de                  │
                    │                Dados                    │
                    │                                         │
                    └─────────────────────────────────────────┘
                              ▲                ▲
                              │                │
                     ┌────────┴───┐      ┌────┴────────┐
                     │            │      │             │
                     │    AG4     │      │    AG5      │
                     │            │      │             │
                     └────────────┘      └─────────────┘
                      Gerenciar           Gerar
                       Chamado            Relatório
```

## 🔧 Solução de Problemas

### Problemas com a Conexão ao Neon DB

**Sintoma**: Erros como "could not connect to server" ou "timeout expired"

**Solução**:
1. Verifique se a string de conexão está correta no arquivo .env
2. Certifique-se de que seu IP está permitido no firewall do Neon DB
3. Verifique se o banco de dados está ativo (não em modo suspenso)

### Problemas com a API da OpenAI

**Sintoma**: Erros como "API key invalid" ou "Rate limit exceeded"

**Solução**:
1. Verifique se a API key está correta no arquivo .env
2. Verifique se há créditos disponíveis na sua conta
3. Implemente backoff exponencial para lidar com limites de taxa

### Problemas com o Pinecone

**Sintoma**: Erros ao conectar ou ao realizar operações no índice

**Solução**:
1. Verifique se a API key está correta
2. Confirme se o nome do índice está correto (deve ser "suporte-chamados")
3. Verifique se o índice está ativo e configurado com a dimensão correta (1536)

## 📊 Exemplos de Uso

### Exemplo de Chamado Processado

#### Entrada: Chamado Original
```
"Erro ao acessar o sistema de pagamento. Não consigo visualizar os pagamentos recebidos este mês e precisamos fechar o balanço até amanhã."
```

#### Processamento por Agentes

**AG1: Classificador de Setor**
```
FINANCEIRO - O chamado menciona sistema de pagamento, pagamentos recebidos e balanço, que são termos claramente relacionados à área financeira.
```

**AG2: Classificador de Prioridade**
```
URGENTE - O chamado menciona a necessidade de fechar o balanço até amanhã, indicando um prazo crítico.
```

**AG3: Analista Técnico**
```
Sistema: Sistema de Pagamentos
Problema: Falha no acesso às visualizações de pagamentos recebidos
Impacto: Impede o fechamento do balanço financeiro mensal
Solução: Verificar permissões de acesso e integridade do banco de dados financeiro
```

**AG4: Gerenciador de Chamado**
```
Status: Em andamento
Próxima Ação: Escalar para equipe de suporte financeiro
Responsável: Departamento Financeiro - Suporte Técnico
Observações: Prioridade máxima devido ao prazo de fechamento do balanço
```

**AG5: Gerador de Relatório**
```
=== RELATÓRIO DO CHAMADO ===
Setor: FINANCEIRO
Prioridade: URGENTE
Análise Técnica: Falha no acesso ao sistema de pagamentos impedindo visualização de pagamentos recebidos
Status: Em andamento - Escalado para suporte técnico financeiro
Ações: Verificação de permissões e integridade do banco de dados em curso
Conclusão: Problema crítico para fechamento do balanço mensal, sendo tratado com máxima prioridade
```

## ❓ FAQ

### Posso usar outros modelos além do GPT-4?

Sim, você pode configurar outros modelos no arquivo de agentes. Para isso, altere o parâmetro `model` na configuração do LLM:

```python
llm = ChatOpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_API_BASE,
    model="gpt-4o-mini",  # Altere para o modelo desejado
    temperature=0.7
)
```

### Como adicionar novos agentes ao sistema?

Para adicionar um novo agente:

1. Defina o agente no arquivo `agents/crewai_agents.py`:
```python
AG6 = Agent(
    name="Nome do Agente",
    role="Papel do Agente",
    goal="Objetivo do Agente",
    backstory="História e comportamento do agente",
    llm=llm
)
```

2. Crie uma tarefa para o agente:
```python
Task_AG6 = Task(
    description="Descrição da tarefa",
    expected_output="Formato esperado de saída",
    agent=AG6
)
```

3. Adicione o agente à equipe:
```python
crew = Crew(
    agents=[AG1, AG2, AG3, AG4, AG5, AG6],  # Adicione o novo agente
    tasks=[Task_AG1, Task_AG2, Task_AG3, Task_AG4, Task_AG5, Task_AG6],  # Adicione a nova tarefa
    verbose=True,
    max_iter=15,
    memory=True
)
```

### Como personalizar as classificações de setor?

Para alterar os setores disponíveis, modifique o backstory do AG1 (Classificador de Setor):

```python
backstory="""Especialista em triagem de chamados para os setores A, B, C, D.
Analiso o conteúdo do chamado e classifico baseado nas seguintes regras:
- A: Questões relacionadas a X
- B: Questões relacionadas a Y
- C: Questões relacionadas a Z
- D: Questões relacionadas a W"""
```

---

## 📜 Licença

[MIT License](LICENSE) - Sinta-se livre para usar, modificar e distribuir conforme as regras da licença.

## 📮 Contato

Para dúvidas ou sugestões, entre em contato através de [email@exemplo.com](mailto:email@exemplo.com).

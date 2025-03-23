from crewai import Agent, Task, Crew
import os
import psycopg2
import logging
from dotenv import load_dotenv
import openai
from langchain.chat_models import ChatOpenAI
import litellm

# Configuração de logs
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

# Carregar variáveis do .env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
NEON_DB_URL = os.getenv("NEON_DB_URL")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")

# Configuração explícita do OpenAI
openai.api_key = OPENAI_API_KEY
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# Configuração explícita do LiteLLM
litellm.api_key = OPENAI_API_KEY
litellm.set_verbose = False  # Desativar logs verbosos que podem causar problemas

# Configurar o modelo LLM base para todos os agentes
llm = ChatOpenAI(
    model="gpt-4-turbo",
    temperature=0.7,
    api_key=OPENAI_API_KEY,
    openai_api_base=OPENAI_API_BASE
)

# Criar os agentes
AG1 = Agent(
    name="Classificador de Setor",
    role="Classificação de chamados por setor",
    goal="Classificar corretamente os chamados nos setores adequados.",
    backstory="""Especialista em triagem de chamados para setores Financeiro, Jurídico, Marketing ou Vendas.
    Analiso o conteúdo do chamado e classifico baseado nas seguintes regras:
    - Financeiro: Questões relacionadas a pagamentos, notas fiscais, orçamentos
    - Jurídico: Questões legais, contratos, acessos restritos
    - Marketing: Questões de publicidade, campanhas, relatórios de marketing
    - Vendas: Questões comerciais, propostas, atendimento ao cliente""",
    llm=llm
)

AG2 = Agent(
    name="Classificador de Prioridade",
    role="Classificação de chamados por prioridade",
    goal="Definir a prioridade dos chamados.",
    backstory="""Avaliador da urgência de chamados como Urgente, Intermediário ou Normal.
    Analiso o conteúdo e classifico baseado nas seguintes regras:
    - Urgente: Problemas que impedem operações críticas, causam perdas financeiras ou afetam muitos usuários
    - Intermediário: Problemas que afetam parcialmente as operações ou têm workaround disponível
    - Normal: Dúvidas gerais, melhorias ou problemas com baixo impacto""",
    llm=llm
)

AG3 = Agent(
    name="Analista Técnico",
    role="Análise técnica dos chamados",
    goal="Fornecer uma análise técnica detalhada.",
    backstory="""Especialista técnico que analisa problemas e propõe soluções.
    Para cada chamado, devo:
    1. Identificar o sistema ou área afetada
    2. Avaliar o impacto técnico do problema
    3. Propor possíveis soluções ou próximos passos
    4. Documentar qualquer informação técnica relevante""",
    llm=llm
)

AG4 = Agent(
    name="Gerenciador de Chamado",
    role="Gerenciamento do fluxo de chamados",
    goal="Encaminhar chamados e monitorar andamento.",
    backstory="""Coordenador que garante o fluxo correto do chamado.
    Minhas responsabilidades incluem:
    1. Verificar se o setor designado é apropriado
    2. Confirmar se a prioridade está adequada
    3. Garantir que a análise técnica está completa
    4. Definir próximos passos e responsáveis""",
    llm=llm
)

AG5 = Agent(
    name="Gerador de Relatório",
    role="Geração de relatórios finais",
    goal="Criar um relatório detalhado para cada chamado resolvido.",
    backstory="""Responsável por documentar todo o processo do chamado.
    Meu relatório deve incluir:
    1. Setor classificado e justificativa
    2. Nível de prioridade e motivo
    3. Análise técnica detalhada
    4. Ações tomadas ou recomendadas
    5. Status atual e próximos passos""",
    llm=llm
)

# Criar as tasks com expected_output
Task_AG1 = Task(
    description="""Analise o chamado e classifique em um dos setores: Financeiro, Jurídico, Marketing ou Vendas.
    Use o formato exato:
    Thought: Analiso o conteúdo do chamado...
    Final Answer: [SETOR] - Justificativa da classificação""",
    expected_output="SETOR (em maiúsculo) seguido de justificativa",
    agent=AG1
)

Task_AG2 = Task(
    description="""Defina a prioridade do chamado como Urgente, Intermediário ou Normal.
    Use o formato exato:
    Thought: Considerando o impacto e urgência...
    Final Answer: [PRIORIDADE] - Justificativa da classificação""",
    expected_output="PRIORIDADE (em maiúsculo) seguido de justificativa",
    agent=AG2
)

Task_AG3 = Task(
    description="""Faça uma análise técnica detalhada do problema.
    Use o formato exato:
    Thought: Analisando tecnicamente o problema...
    Final Answer: 
    Sistema: [sistema afetado]
    Problema: [descrição técnica]
    Impacto: [avaliação do impacto]
    Solução: [proposta de solução]""",
    expected_output="Análise técnica estruturada com os campos acima",
    agent=AG3
)

Task_AG4 = Task(
    description="""Gerencie o fluxo do chamado verificando classificações e definindo ações.
    Use o formato exato:
    Thought: Avaliando o encaminhamento...
    Final Answer:
    Status: [status atual]
    Próxima Ação: [ação necessária]
    Responsável: [setor/pessoa]
    Observações: [notas importantes]""",
    expected_output="Status e plano de ação estruturado",
    agent=AG4
)

Task_AG5 = Task(
    description="""Gere um relatório final consolidando todas as informações do chamado.
    Use o formato exato:
    Thought: Consolidando informações...
    Final Answer:
    === RELATÓRIO DO CHAMADO ===
    Setor: [setor classificado]
    Prioridade: [nível de prioridade]
    Análise Técnica: [resumo da análise]
    Status: [situação atual]
    Ações: [ações tomadas/planejadas]
    Conclusão: [resumo final]""",
    expected_output="Relatório estruturado com todos os campos acima",
    agent=AG5
)

def processar_chamados():
    try:
        # Conectar ao NeonDB
        conn = psycopg2.connect(NEON_DB_URL)
        cur = conn.cursor()
        
        # Verificar se há chamados abertos
        cur.execute("SELECT COUNT(*) FROM chamados WHERE status = 'Aberto';")
        total_abertos = cur.fetchone()[0]
        
        if total_abertos == 0:
            logger.info("ℹ️ Nenhum chamado aberto encontrado")
            return

        logger.info(f"📊 Total de chamados abertos: {total_abertos}")
        
        # Criar a equipe com configurações de tempo limite
        crew = Crew(
            agents=[AG1, AG2, AG3, AG4, AG5],
            tasks=[Task_AG1, Task_AG2, Task_AG3, Task_AG4, Task_AG5],
            verbose=True,
            max_iter=15,  # Limite de iterações por agente
            memory=True   # Habilita memória entre agentes
        )

        # Processar cada chamado
        cur.execute("SELECT id, descricao FROM chamados WHERE status = 'Aberto';")
        chamados = cur.fetchall()
        
        for chamado in chamados:
            chamado_id = chamado[0]
            chamado_data = {
                "descricao": chamado[1],
                "ID": str(chamado_id)
            }
            
            logger.info(f"\n🚀 INICIANDO CHAMADO {chamado_id}")
            logger.info(f"📝 DESCRIÇÃO: {chamado_data['descricao']}")
            
            try:
                # Executar com timeout de 3 minutos
                resultado = crew.kickoff(
                    inputs=chamado_data
                )
                logger.info(f"✅ Processamento do chamado {chamado_id} concluído!")
                logger.info(f"📜 Resultado final do chamado: {resultado}")
                
                # Atualizar status do chamado no banco
                cur.execute(
                    "UPDATE chamados SET status = 'Processado' WHERE id = %s",
                    (chamado_id,)
                )
                conn.commit()
                
            except Exception as e:
                logger.error(f"❌ Erro no processamento do chamado {chamado_id}: {str(e)}")
                logger.error("⚠️ Marcando chamado como 'Erro' para revisão manual")
                cur.execute(
                    "UPDATE chamados SET status = 'Erro' WHERE id = %s",
                    (chamado_id,)
                )
                conn.commit()
                conn.rollback()

    except Exception as e:
        logger.error(f"❌ Erro na conexão com o banco de dados: {str(e)}")
        logger.error("⚠️ Verifique as configurações de conexão no arquivo .env")
    
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()
        logger.info("🏁 Processamento finalizado")

if __name__ == "__main__":
    processar_chamados()

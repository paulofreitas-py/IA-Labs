import os
import pinecone
import psycopg2
from dotenv import load_dotenv
from openai import OpenAI
from pathlib import Path

dotenv_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=dotenv_path)

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
NEON_DB_URL = os.getenv("NEON_DB_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Inicializar Pinecone corretamente
pc = pinecone.Pinecone(api_key=PINECONE_API_KEY)

# Verificar se o índice já existe
index_name = "suporte-chamados"
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=1536,
        metric="cosine"  # Certifique-se de que esta métrica corresponde ao modelo de embeddings usado
    )

index = pc.Index(index_name)

# Inicializar OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

# Função para obter chamados do NeonDB
def buscar_chamados_do_neon():
    query = "SELECT id, descricao FROM chamados WHERE status = 'Aberto';"
    try:
        conn = psycopg2.connect(NEON_DB_URL)
        cur = conn.cursor()
        cur.execute(query)
        chamados = cur.fetchall()
        cur.close()
        conn.close()
        return [{"id": row[0], "descricao": row[1]} for row in chamados]
    except Exception as e:
        print("Erro ao buscar chamados do NeonDB:", str(e))
        return []

# Função para indexar chamados no Pinecone
def indexar_chamados_no_pinecone():
    chamados = buscar_chamados_do_neon()
    if not chamados:
        print("Nenhum chamado encontrado para indexação.")
        return

    vectors = []
    for chamado in chamados:
        response = client.embeddings.create(input=chamado["descricao"], model="text-embedding-ada-002")
        embedding = response.data[0].embedding  # Acesso corrigido

        vectors.append((str(chamado["id"]), embedding))

    index.upsert(vectors=vectors)
    print(f"{len(chamados)} chamados indexados no Pinecone.")


# Executar a indexação
if __name__ == "__main__":
    indexar_chamados_no_pinecone()

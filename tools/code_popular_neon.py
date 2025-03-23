import psycopg2
import os
from dotenv import load_dotenv

# Caminho absoluto para o .env na raiz do projeto
from pathlib import Path
dotenv_path = Path(__file__).resolve().parents[1] / ".env"

# Carregar variáveis do arquivo .env
load_dotenv(dotenv_path=dotenv_path)
DB_URL = os.getenv("NEON_DB_URL")

def popular_banco():
    try:
        # Conecta ao banco
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        
        # Drop na tabela se existir
        cur.execute("DROP TABLE IF EXISTS chamados CASCADE;")
        print("Tabela antiga removida.")
        
        # Cria a tabela
        cur.execute("""
            CREATE TABLE chamados (
                id SERIAL PRIMARY KEY,
                descricao TEXT NOT NULL,
                cliente VARCHAR(255) NOT NULL,
                status VARCHAR(50) DEFAULT 'Aberto',
                data_abertura TIMESTAMP DEFAULT NOW()
            );
        """)
        print("Nova tabela criada.")
        
        # Insere os dados um por um
        chamados = [
            ("Erro ao acessar o sistema de pagamento", "Cliente A"),
            ("Problema com nota fiscal eletrônica", "Cliente B"),
            ("Dúvida sobre orçamento de marketing", "Cliente C"),
            ("Sistema travando ao gerar relatórios", "Cliente D"),
            ("Solicitação de acesso a dados jurídicos", "Cliente E")
        ]
        
        for descricao, cliente in chamados:
            cur.execute(
                "INSERT INTO chamados (descricao, cliente) VALUES (%s, %s) RETURNING id;",
                (descricao, cliente)
            )
            id_inserido = cur.fetchone()[0]
            print(f"Chamado inserido com ID: {id_inserido}")
        
        # Commit das alterações
        conn.commit()
        
        # Verifica os dados inseridos
        cur.execute("SELECT * FROM chamados ORDER BY id;")
        resultados = cur.fetchall()
        print("\nChamados inseridos:")
        for row in resultados:
            print(f"ID: {row[0]}, Cliente: {row[2]}, Descrição: {row[1]}")
        
        cur.close()
        conn.close()
        print("\nProcesso concluído com sucesso!")
        
    except Exception as e:
        print(f"Erro durante a operação: {str(e)}")
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    print("🔍 Iniciando processo de população do banco...")
    popular_banco()

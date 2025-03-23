
/* Tabela de chamados*/
CREATE TABLE chamados (
    id SERIAL PRIMARY KEY,
    descricao TEXT NOT NULL,
    cliente VARCHAR(255) NOT NULL,
    status VARCHAR(50) DEFAULT 'Aberto',
    data_abertura TIMESTAMP DEFAULT NOW()
);

/*Classificação por setor*/
CREATE TABLE classificacao_setor (
    id SERIAL PRIMARY KEY,
    chamado_id INT REFERENCES chamados(id),
    setor VARCHAR(50) NOT NULL,
    data_classificacao TIMESTAMP DEFAULT NOW()
);

/* Classificação por prioridade*/
CREATE TABLE classificacao_prioridade (
    id SERIAL PRIMARY KEY,
    chamado_id INT REFERENCES chamados(id),
    prioridade VARCHAR(20) NOT NULL CHECK (prioridade IN ('Urgente', 'Intermediário', 'Normal')),
    data_classificacao TIMESTAMP DEFAULT NOW()
);

/* Análise técnica*/
CREATE TABLE analise_tecnica (
    id SERIAL PRIMARY KEY,
    chamado_id INT REFERENCES chamados(id),
    descricao_tecnica TEXT NOT NULL,
    tecnico_responsavel VARCHAR(255),
    data_analise TIMESTAMP DEFAULT NOW()
);

/* Andamento dos chamados*/
CREATE TABLE andamento_chamados (
    id SERIAL PRIMARY KEY,
    chamado_id INT REFERENCES chamados(id),
    responsavel VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL CHECK (status IN ('Em andamento', 'Aguardando resposta', 'Concluído')),
    data_atualizacao TIMESTAMP DEFAULT NOW()
);

/* Relatório final*/
CREATE TABLE relatorio_final (
    id SERIAL PRIMARY KEY,
    chamado_id INT REFERENCES chamados(id),
    conclusao TEXT NOT NULL,
    resolvido BOOLEAN DEFAULT FALSE,
    data_conclusao TIMESTAMP DEFAULT NOW()
);

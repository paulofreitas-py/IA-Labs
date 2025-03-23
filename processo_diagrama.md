```mermaid
flowchart TD
    A[Entrada do Chamado] --> B[Banco de Dados Neon]
    B --> C[Indexação Pinecone]
    B --> D[Processamento Agentes]
    
    subgraph "Processamento de Chamados"
        D --> E[AG1: Classificador de Setor]
        E --> F[AG2: Classificador de Prioridade]
        F --> G[AG3: Analista de Chamados]
        G --> H[AG4: Gerador de Relatórios]
    end
    
    C -.-> G
    H --> I[Relatório Final]
    
    subgraph "Base de Conhecimento"
        J[OpenAI API]
        K[Vector Store - Pinecone]
        L[DB Relacional - Neon]
    end
    
    J -.-> E
    J -.-> F
    J -.-> G
    J -.-> H
    K -.-> G
    L --> B
    
    style A fill:#f9d5e5,stroke:#333,stroke-width:2px
    style I fill:#ade8f4,stroke:#333,stroke-width:2px
    style J fill:#f0ad4e,stroke:#333,stroke-width:2px
    style K fill:#5bc0de,stroke:#333,stroke-width:2px
    style L fill:#5cb85c,stroke:#333,stroke-width:2px
```

## Explicação do Fluxo de Processamento

1. **Entrada do Chamado**: Um novo ticket de suporte é registrado no sistema.

2. **Banco de Dados Neon**: Os dados do chamado são armazenados no banco PostgreSQL da Neon.

3. **Indexação Pinecone**: Paralelamente, o conteúdo textual do chamado é convertido em embeddings e indexado no Pinecone para pesquisas semânticas.

4. **Processamento por Agentes**:
   - **AG1 (Classificador de Setor)**: Analisa o conteúdo do chamado e determina a qual setor ele pertence (TI, Financeiro, RH, etc.).
   - **AG2 (Classificador de Prioridade)**: Determina a urgência e prioridade do chamado.
   - **AG3 (Analista de Chamados)**: Analisa o conteúdo completo, podendo consultar a base vetorial no Pinecone para encontrar casos similares.
   - **AG4 (Gerador de Relatórios)**: Compila todas as informações e gera um relatório final.

5. **Relatório Final**: Documento com a análise completa e recomendações é gerado e disponibilizado.

O diagrama também mostra as interações com:
- **OpenAI API**: Fornece os modelos de IA para todos os agentes.
- **Vector Store (Pinecone)**: Armazena embeddings para consulta semântica.
- **DB Relacional (Neon)**: Armazena todos os dados estruturados dos chamados.

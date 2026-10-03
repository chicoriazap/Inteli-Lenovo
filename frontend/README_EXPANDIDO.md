# Squad Expandido de 5 Agentes de IA: Retenção, Finanças, Storytelling e Governança

Esta versão expandida do painel executivo eleva a capacidade analítica e persuasiva do sistema de apoio à decisão em vendas e retenção B2B (Módulo 2 - Inteli x Lenovo).

---

## 👥 A Arquitetura do Squad de 5 Agentes

Em vez da cadeia simples de 3 agentes, o squad expandido divide a inteligência em 5 especializações complementares:

```
                                [ Webhook Input ]
                                        │
                                        ▼
   ┌─────────────────────────────────────────────────────────────────────────┐
   │ 1. ATLAS (Análise & Métricas)                                           │
   │    • Extração estrita de dados quantitativos, receita em risco e escore.│
   └─────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
   ┌─────────────────────────────────────────────────────────────────────────┐
   │ 2. DANTE (Valoração Financeira & Risco)                                 │
   │    • Avalia viabilidade econômica, margem e custo de churn vs. desconto.  │
   └─────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
   ┌─────────────────────────────────────────────────────────────────────────┐
   │ 3. VERA (Playbooks & Réguas EWS)                                        │
   │    • Mapeia planos operacionais (Onboarding D+30, Gatilho P90, CRM Gap). │
   └─────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
   ┌─────────────────────────────────────────────────────────────────────────┐
   │ 4. LIVIA (Executive Storyteller)                                        │
   │    • Constrói o Pitch Executivo (Dor -> Impacto -> Proposta de Valor).  │
   └─────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
   ┌─────────────────────────────────────────────────────────────────────────┐
   │ 5. CIRO (Revisor Executivo & Guardião da Memória)  ◄── [Buffer Memory]  │
   │    • Fact-checking, governança, veredito final e portador do contexto. │
   └─────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
                                [ Webhook Output ]
```

---

## 🧠 Por que o CIRO foi Selecionado como Portador da Memória?

1. **Síntese de Contexto Completo**: Ciro é o agente final da cadeia. Ao conectar o nó `memoryBufferWindow` diretamente ao Ciro, ele armazena a conversa completa acumulada após ter acesso a todas as análises anteriores (Atlas, Dante, Vera e Livia).
2. **Continuidade de Perguntas Subsequentes**: Quando o Account Manager faz perguntas de acompanhamento (ex: *"E se oferecermos um desconto menor para essa mesma conta?"* ou *"Qual era a receita da conta anterior?"*), Ciro consulta o histórico da sessão e mantém a consistência temporal sem alucinações.
3. **Qualidade do Fact-Checking**: Com memória ativa, Ciro verifica se os números informados pelos outros agentes no turno atual divergem do que foi dito nos turnos anteriores.

---

## 📁 Arquivos do Squad Expandido

- **Frontend**: `frontend/index_expandido.html` (Interface completa com gráficos Chart.js, filtros executivos e chat para os 5 agentes).
- **Workflow n8n**: `frontend/workflow_n8n_expandido.json` (Export do workflow do n8n com a cadeia dos 5 agentes e nó de memória do Ciro).

---

## 🚀 Como Executar

1. **Importar o Workflow no n8n**:
   - Abra o n8n -> Workflows -> Import from File.
   - Selecione `frontend/workflow_n8n_expandido.json`.
   - Configure a credencial OpenRouter nos nós de modelo LLM.
   - Ative o workflow e copie a URL de Produção do Webhook.

2. **Abrir o Painel**:
   - Abra `frontend/index_expandido.html` no navegador.
   - Carregue a planilha `datasets_case_modulo2.xlsx`.
   - Cole a URL do Webhook no bloco 03 e clique em **Testar Conexão**.
   - Faça perguntas sobre as contas e receba o parecer sincronizado dos 5 agentes.

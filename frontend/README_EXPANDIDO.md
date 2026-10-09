# Squad de 5 Sub-Agentes de Customer Success (CS) no n8n

Esta versão expandida do workflow n8n alinha os 5 subagentes especialistas com as réguas EWS e playbooks de retenção da Kovan Technologies (MBA Inteli x Lenovo).

---

## 👥 A Arquitetura do Squad de 5 Sub-Agentes de CS

O fluxo encadeia os 5 agentes de forma sequencial e sinérgica:

```
                                [ Webhook Input ]
                                        │
                                        ▼
   ┌─────────────────────────────────────────────────────────────────────────┐
   │ 1. CS-ONBOARD (Onboarding D+30 & Adoção Inicial - Régua 1)              │
   │    • Foco em contas novas, primeira entrega, validação técnica e 2ª compra│
   └─────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
   ┌─────────────────────────────────────────────────────────────────────────┐
   │ 2. CS-EWS (Early Warning System & Monitor P90 - Régua 2)                │
   │    • Monitora intervalo entre pedidos e alertas de quebra de ritmo P90. │
   └─────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
   ┌─────────────────────────────────────────────────────────────────────────┐
   │ 3. DANTE (Valoração Financeira & Risco - Régua 3)                       │
   │    • Perda esperada em dólares, ROI da retenção e limites de orçamento.  │
   └─────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
   ┌─────────────────────────────────────────────────────────────────────────┐
   │ 4. LIVIA (Executive Storyteller & Pitch Consultivo)                     │
   │    • Constrói o Pitch Executivo B2B (Dor -> Risco/Impacto -> Proposta). │
   └─────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
   ┌─────────────────────────────────────────────────────────────────────────┐
   │ 5. CIRO (Orquestrador, Compliance & Memória)     ◄── [Buffer Memory]    │
   │    • Fact-checking, governança, veredito final e portador do contexto.  │
   └─────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
                                [ Webhook Output ]
```

---

## 🧠 Por que o CIRO é o Portador da Memória?

1. **Síntese de Contexto Completo**: Ciro é o agente final da cadeia. Ao conectar o nó `memoryBufferWindow` diretamente ao Ciro, ele armazena a conversa completa acumulada após ter acesso a todas as análises anteriores (CS-Onboard, CS-EWS, Dante e Livia).
2. **Continuidade de Perguntas Subsequentes**: Quando o Account Manager faz perguntas de acompanhamento (ex: *"E se oferecermos um desconto menor para essa mesma conta?"* ou *"Qual era a receita da conta anterior?"*), Ciro consulta o histórico da sessão e mantém a consistência temporal sem alucinações.
3. **Qualidade do Fact-Checking**: Com memória ativa, Ciro verifica se os números informados pelos outros agentes no turno atual divergem do que foi dito nos turnos anteriores.

---

## 📁 Arquivos do Squad

- **Frontend**: `frontend/index_expandido.html` (Interface completa com gráficos SVG/Chart.js, filtros de segmento, download de CSV e tooltips explicativos).
- **Workflow n8n**: `frontend/workflow_n8n_expandido.json` (Export do workflow do n8n com a cadeia dos 5 agentes e nó de memória do Ciro).

---

## 🚀 Como Executar

1. **Importar o Workflow no n8n**:
   - Abra o n8n -> Workflows -> Import from File.
   - Selecione `workflow_n8n_expandido.json`.
   - Configure a credencial OpenRouter nos nós de modelo LLM.
2. **Ativar o Webhook**:
   - O webhook responde em `POST` no path `/kovan-chat-grupo-3-expandido`.
3. **Conectar ao Painel**:
   - Insira a URL do webhook no painel web e inicie a interação consultiva.

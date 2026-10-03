# frontend: o painel do grupo

Uma página só, sem build. Carrega a planilha da fila, guarda os planos de ação
de cada área (Comercial, Atendimento, Pós-vendas) e conversa com o agente do
n8n. A cada pergunta ela envia ao n8n a planilha e os três planos, e o agente
responde apoiado só nesse material.

## Usar a versão pronta

<https://josercf.github.io/inteli-2026-2-pos-m02/painel/>

1. `python -m app.publicar --grupo NOME_DO_GRUPO` grava `saida/fila_publicada.csv`
   e `saida/workflow_n8n.json`.
2. Importe o workflow no n8n, escolha a credencial OpenRouter nos dois nós
   OpenRouter e ative.
3. No painel, cole a URL de produção do nó **API do painel**
   (`https://inteli.app.n8n.cloud/webhook/kovan-chat-NOME_DO_GRUPO`), carregue
   o CSV e escreva os planos de ação do grupo.

## Criar a versão do grupo

Abra esta pasta no Antigravity e peça a mudança. Exemplos de pedido:

- "Acrescente um gráfico de barras com as dez contas de maior valor esperado."
- "Mostre, ao clicar numa linha da tabela, a conta com os quatro sinais."
- "Acrescente uma quarta área, Financeiro, e mande o plano dela ao n8n."

Para abrir: `python -m http.server 8000` nesta pasta e
<http://localhost:8000>. O n8n aceita a chamada de qualquer origem
(`allowedOrigins: *` no nó API do painel).

Contrato com o n8n, que qualquer versão precisa manter:

```json
POST { "sessionId": "...", "pergunta": "...", "contas": [ ... ], "planos": { "comercial": "...", "atendimento": "...", "pós-vendas": "..." } }
200  { "resposta": "..." }
```

A planilha fica no navegador e só sai para o endpoint configurado. A fila tem
identificador anonimizado e nenhum dado de cadastro, e mesmo assim a URL do
n8n é pública: não divulgue fora da turma.

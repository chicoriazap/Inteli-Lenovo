# -*- coding: utf-8 -*-
"""Monta o workflow do n8n com a fila do grupo dentro.

Chamado por `python -m app.publicar --grupo <nome>`, que grava `saida/workflow_n8n.json`. O
grupo importa esse arquivo no n8n (Workflows > Import from File), escolhe a
credencial OpenRouter e ativa.

Um workflow, dois gatilhos:

- `GET /webhook/kovan-fila-<grupo>` é o modelo publicado. Qualquer sistema
  (a tela do Streamlit, o CRM, uma planilha) consulta a fila por ali.
- O Chat Trigger é a conversa. O agente consulta a mesma URL como ferramenta,
  e por isso só cita número que a API devolveu.
- `POST /webhook/kovan-chat-<grupo>` atende o painel web (frontend/index.html).
  O painel manda a pergunta, a planilha carregada e os planos de ação de cada
  área, e o agente responde apoiado só nesse material.
"""

from __future__ import annotations

import json
import uuid

MODELO_PADRAO = "openai/gpt-4o-mini"

SISTEMA = """Você é o assistente da fila de retenção da Kovan Technologies LATAM. Quem conversa com você é um Account Manager.

Fonte única: a ferramenta consultar_fila. Ela devolve a fila do ciclo, ordenada por valor esperado (escore vezes receita dos 12 meses anteriores ao corte de 07/03/2024), ou os dados de uma conta pelo account_id.

Regras:
1. Todo número da resposta sai da ferramenta. Se a ferramenta não devolveu o número, diga que não tem esse dado. Nunca estime receita, escore ou posição.
2. O escore é a probabilidade de a conta parar de comprar depois do corte. Ele não mede conta que encolhe e continua comprando.
3. Ao explicar uma conta, cite a posição por valor, a posição por probabilidade, o escore, o valor em risco e os sinais (dias desde a última compra, meses com compra nos últimos 12, razão entre recência e cadência, queda contra o pico).
4. Quando pedirem roteiro de intervenção, escreva três passos para a próxima ligação, cada um apoiado em um sinal da conta. Não prometa desconto nem condição comercial.
5. Conta fora da fila: diga que ela não está entre as contas do ciclo e não invente posição.
6. Responda em português, em no máximo oito linhas, sem emoji."""

CODIGO = """// A fila foi gerada por python -m app.publicar, a partir do modelo do grupo.
const fila = __FILA__;

const q = $input.first().json.query || {};
const conta = String(q.conta || '').trim().toUpperCase();
if (conta) {
  const r = fila.find(x => x.account_id === conta);
  return [{ json: r ? { encontrada: true, ...r }
                    : { encontrada: false, account_id: conta,
                        mensagem: 'Conta fora da fila do ciclo.' } }];
}
const n = Math.max(1, Math.min(parseInt(q.n || '10', 10) || 10, fila.length));
return [{ json: { capacidade: fila.length, devolvidas: n, contas: fila.slice(0, n) } }];
"""


SISTEMA_PAINEL = """Você é o assistente de retenção da Kovan Technologies LATAM. Quem conversa com você usa o painel web da fila de churn.

Fonte única: a planilha e os planos de ação abaixo, enviados pelo painel a cada pergunta.

Regras:
1. Todo número da resposta sai da planilha. Se a planilha não tem o número, diga que não tem esse dado. Nunca estime.
2. O escore é a probabilidade de a conta parar de comprar. Ele não mede conta que encolhe e continua comprando.
3. Ao recomendar ação, use só os planos de ação das áreas abaixo. Diga qual área executa e qual item do plano se aplica, apoiado em um sinal da conta.
4. Se nenhum plano cobre o caso, diga isso e sugira levar ao Comitê de Receita. Não invente ação, desconto nem condição comercial.
5. Responda em português, em no máximo dez linhas, sem emoji.

PLANOS DE AÇÃO POR ÁREA:
{{ JSON.stringify($json.body.planos || {}, null, 1) }}

PLANILHA ({{ ($json.body.contas || []).length }} linhas):
{{ JSON.stringify($json.body.contas || []) }}"""


def _id() -> str:
    return str(uuid.uuid4())


def montar(fila: list[dict], grupo: str = "grupo", modelo: str = MODELO_PADRAO,
           base_url: str = "https://inteli.app.n8n.cloud") -> dict:
    caminho = f"kovan-fila-{grupo}"
    codigo = CODIGO.replace("__FILA__", json.dumps(fila, ensure_ascii=False))
    nos = [
        {"id": _id(), "name": "API da fila", "type": "n8n-nodes-base.webhook",
         "typeVersion": 2, "position": [0, 0], "webhookId": _id(),
         "parameters": {"path": caminho, "responseMode": "responseNode", "options": {}}},
        {"id": _id(), "name": "Consultar fila", "type": "n8n-nodes-base.code",
         "typeVersion": 2, "position": [240, 0],
         "parameters": {"jsCode": codigo}},
        {"id": _id(), "name": "Responder", "type": "n8n-nodes-base.respondToWebhook",
         "typeVersion": 1.1, "position": [480, 0],
         "parameters": {"respondWith": "json", "responseBody": "={{ $json }}", "options": {}}},
        {"id": _id(), "name": "Chat do Account Manager",
         "type": "@n8n/n8n-nodes-langchain.chatTrigger", "typeVersion": 1.1,
         "position": [0, 320], "webhookId": _id(),
         "parameters": {"public": True, "mode": "hostedChat",
                        "initialMessages": "Olá. Pergunte pela fila do ciclo ou por uma conta, pelo account_id.",
                        "options": {"title": "Fila de retenção Kovan LATAM",
                                    "subtitle": "Respostas apoiadas na fila publicada pelo modelo"}}},
        {"id": _id(), "name": "Agente da fila", "type": "@n8n/n8n-nodes-langchain.agent",
         "typeVersion": 1.7, "position": [300, 320],
         "parameters": {"options": {"systemMessage": SISTEMA}}},
        {"id": _id(), "name": "OpenRouter", "type": "@n8n/n8n-nodes-langchain.lmChatOpenRouter",
         "typeVersion": 1, "position": [160, 560],
         "parameters": {"model": modelo, "options": {"temperature": 0.2}}},
        {"id": _id(), "name": "Memória da conversa",
         "type": "@n8n/n8n-nodes-langchain.memoryBufferWindow", "typeVersion": 1.3,
         "position": [340, 560], "parameters": {"contextWindowLength": 6}},
        {"id": _id(), "name": "consultar_fila", "type": "n8n-nodes-base.httpRequestTool",
         "typeVersion": 4.2, "position": [520, 560],
         "parameters": {
             "toolDescription": "Consulta a fila de retenção publicada pelo modelo. Passe conta com o account_id (ex.: CLI052938) para os dados de uma conta, ou deixe conta vazio e passe n para as n primeiras da fila.",
             "url": f"{base_url}/webhook/{caminho}",
             "sendQuery": True,
             "queryParameters": {"parameters": [
                 {"name": "conta", "value": "={{ $fromAI('conta', 'account_id da conta, ou vazio para a fila', 'string') }}"},
                 {"name": "n", "value": "={{ $fromAI('n', 'quantas contas do topo da fila devolver', 'number') }}"},
             ]},
             "options": {}}},
        {"id": _id(), "name": "API do painel", "type": "n8n-nodes-base.webhook",
         "typeVersion": 2, "position": [0, 820], "webhookId": _id(),
         "parameters": {"httpMethod": "POST", "path": f"kovan-chat-{grupo}",
                        "responseMode": "responseNode",
                        "options": {"allowedOrigins": "*"}}},
        {"id": _id(), "name": "Agente do painel", "type": "@n8n/n8n-nodes-langchain.agent",
         "typeVersion": 1.7, "position": [300, 820],
         "parameters": {"promptType": "define", "text": "={{ $json.body.pergunta }}",
                        "options": {"systemMessage": "=" + SISTEMA_PAINEL}}},
        {"id": _id(), "name": "OpenRouter do painel",
         "type": "@n8n/n8n-nodes-langchain.lmChatOpenRouter", "typeVersion": 1,
         "position": [220, 1060],
         "parameters": {"model": modelo, "options": {"temperature": 0.2}}},
        {"id": _id(), "name": "Memória do painel",
         "type": "@n8n/n8n-nodes-langchain.memoryBufferWindow", "typeVersion": 1.3,
         "position": [420, 1060],
         "parameters": {"sessionIdType": "customKey",
                        "sessionKey": "={{ $json.body.sessionId }}",
                        "contextWindowLength": 6}},
        {"id": _id(), "name": "Responder ao painel", "type": "n8n-nodes-base.respondToWebhook",
         "typeVersion": 1.1, "position": [660, 820],
         "parameters": {"respondWith": "json",
                        "responseBody": "={{ { resposta: $json.output } }}", "options": {}}},
    ]
    conexoes = {
        "API da fila": {"main": [[{"node": "Consultar fila", "type": "main", "index": 0}]]},
        "Consultar fila": {"main": [[{"node": "Responder", "type": "main", "index": 0}]]},
        "Chat do Account Manager": {"main": [[{"node": "Agente da fila", "type": "main", "index": 0}]]},
        "OpenRouter": {"ai_languageModel": [[{"node": "Agente da fila", "type": "ai_languageModel", "index": 0}]]},
        "Memória da conversa": {"ai_memory": [[{"node": "Agente da fila", "type": "ai_memory", "index": 0}]]},
        "consultar_fila": {"ai_tool": [[{"node": "Agente da fila", "type": "ai_tool", "index": 0}]]},
        "API do painel": {"main": [[{"node": "Agente do painel", "type": "main", "index": 0}]]},
        "Agente do painel": {"main": [[{"node": "Responder ao painel", "type": "main", "index": 0}]]},
        "OpenRouter do painel": {"ai_languageModel": [[{"node": "Agente do painel", "type": "ai_languageModel", "index": 0}]]},
        "Memória do painel": {"ai_memory": [[{"node": "Agente do painel", "type": "ai_memory", "index": 0}]]},
    }
    return {"name": f"Kovan · Agente da fila · {grupo}", "nodes": nos,
            "connections": conexoes, "settings": {"executionOrder": "v1"}}

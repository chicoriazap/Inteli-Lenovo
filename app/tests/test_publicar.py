# -*- coding: utf-8 -*-
"""O que sai da máquina para o n8n."""

from __future__ import annotations

import json

import pandas as pd

from app import publicar
from app.churn import lista


def _carteira():
    idx = pd.Index(list("abcd"), name="account_id")
    escore = pd.Series([0.9, 0.7, 0.5, 0.3], index=idx, name="escore")
    X = pd.DataFrame({c: [10.0, 20.0, 30.0, 40.0] for c in publicar.SINAIS}, index=idx)
    X["receita_12m"] = [1.0, 1.0, 1.0, 1000.0]
    X["coluna_que_nao_sai"] = [1, 2, 3, 4]
    return escore, X


def test_a_fila_publicada_segue_o_valor_esperado():
    escore, X = _carteira()
    t = lista.priorizar(escore, valor_em_risco=X.receita_12m, capacidade=2)
    fila = publicar.registros(t, X, capacidade=2)
    assert [r["account_id"] for r in fila] == ["d", "a"]
    assert [r["posicao_por_valor"] for r in fila] == [1, 2]
    assert fila[0]["posicao_por_probabilidade"] == 4


def test_so_sai_o_que_a_lista_autoriza():
    escore, X = _carteira()
    t = lista.priorizar(escore, valor_em_risco=X.receita_12m, capacidade=4)
    fila = publicar.registros(t, X, capacidade=4)
    permitido = {"account_id", "posicao_por_valor", "posicao_por_probabilidade",
                 "escore", "valor_em_risco_usd", "valor_esperado_usd", *publicar.SINAIS}
    for r in fila:
        assert set(r) == permitido


def test_o_registro_vira_json_sem_tipo_do_numpy():
    """int64 do pandas não serializa em JSON. O registro precisa sair em int nativo."""
    escore, X = _carteira()
    t = lista.priorizar(escore, valor_em_risco=X.receita_12m, capacidade=4)
    texto = json.dumps(publicar.registros(t, X, capacidade=4))
    assert json.loads(texto)[0]["valor_esperado_usd"] == 300


def test_o_workflow_leva_a_fila_e_liga_o_agente_a_ferramenta():
    from app import workflow_n8n
    escore, X = _carteira()
    t = lista.priorizar(escore, valor_em_risco=X.receita_12m, capacidade=2)
    wf = workflow_n8n.montar(publicar.registros(t, X, capacidade=2), grupo="g3")
    nos = {n["name"]: n for n in wf["nodes"]}
    codigo = nos["Consultar fila"]["parameters"]["jsCode"]
    assert "__FILA__" not in codigo and '"account_id": "d"' in codigo
    assert nos["API da fila"]["parameters"]["path"] == "kovan-fila-g3"
    assert nos["consultar_fila"]["parameters"]["url"].endswith("/webhook/kovan-fila-g3")
    assert wf["connections"]["consultar_fila"]["ai_tool"][0][0]["node"] == "Agente da fila"
    # o agente só cita número que veio da ferramenta
    assert "Todo número da resposta sai da ferramenta" in nos["Agente da fila"]["parameters"]["options"]["systemMessage"]


def test_o_painel_manda_planilha_e_planos_ao_agente():
    from app import workflow_n8n
    wf = workflow_n8n.montar([], grupo="g3")
    nos = {n["name"]: n for n in wf["nodes"]}
    assert nos["API do painel"]["parameters"]["path"] == "kovan-chat-g3"
    assert nos["API do painel"]["parameters"]["httpMethod"] == "POST"
    sistema = nos["Agente do painel"]["parameters"]["options"]["systemMessage"]
    assert sistema.startswith("=") and "$json.body.planos" in sistema and "$json.body.contas" in sistema
    assert wf["connections"]["Agente do painel"]["main"][0][0]["node"] == "Responder ao painel"

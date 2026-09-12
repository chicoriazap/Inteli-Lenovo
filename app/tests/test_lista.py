# -*- coding: utf-8 -*-
"""Da probabilidade para a fila de trabalho."""

from __future__ import annotations

import numpy as np
import pandas as pd

from app.churn import lista
from app.tests.conftest import precisa_da_base


def _escore():
    return pd.Series([0.9, 0.7, 0.5, 0.3], index=list("abcd"), name="escore")


def test_a_fila_tem_o_tamanho_da_capacidade():
    t = lista.priorizar(_escore(), capacidade=2)
    assert int(t.na_fila.sum()) == 2
    assert list(t[t.na_fila].index) == ["a", "b"]


def test_o_valor_esperado_reordena_a_fila():
    valor = pd.Series([1.0, 1.0, 1.0, 1000.0], index=list("abcd"))
    t = lista.priorizar(_escore(), valor_em_risco=valor, capacidade=1)
    assert list(t[t.na_fila].index) == ["a"]
    assert list(t[t.na_fila_por_valor].index) == ["d"]


def test_valor_ausente_ou_infinito_nao_derruba_a_ordenacao():
    """Regressão. A primeira versão estourava com IntCastingNaNError quando a
    receita anualizada dividia por tempo de casa igual a zero."""
    valor = pd.Series([np.inf, np.nan, 0.0, 100.0], index=list("abcd"))
    t = lista.priorizar(_escore(), valor_em_risco=valor, capacidade=1)
    assert list(t[t.na_fila_por_valor].index) == ["d"]
    assert t.valor_em_risco.isna().sum() == 0


def test_a_matriz_de_confusao_soma_a_populacao():
    churn = pd.Series([1, 0, 1, 0], index=list("abcd"))
    t = lista.priorizar(_escore(), capacidade=2)
    c = lista.matriz_de_confusao(t, churn)
    assert sum(c[k] for k in ("verdadeiros_positivos", "falsos_positivos",
                              "falsos_negativos", "verdadeiros_negativos")) == 4
    assert c["precisao"] == 0.5


# ---------------------------------------------------------------------------
# O achado da aula, contra a base de verdade
# ---------------------------------------------------------------------------

@precisa_da_base
def test_a_fila_por_escore_acerta_mais_contas(tabela, escore):
    X, y = tabela
    t = lista.priorizar(escore, valor_em_risco=X.receita_12m)
    por_escore = lista.matriz_de_confusao(t, y, "na_fila")
    por_valor = lista.matriz_de_confusao(t, y, "na_fila_por_valor")
    assert por_escore["verdadeiros_positivos"] > por_valor["verdadeiros_positivos"] * 2
    assert por_escore["precisao"] > 0.8
    assert por_valor["precisao"] < 0.4


@precisa_da_base
def test_a_fila_por_valor_alcanca_quase_toda_a_receita_em_risco(tabela, escore):
    """O achado que fecha o arco da Aula 06. Uma fila com precisão de 85% pode
    recuperar quase nada de dinheiro, e uma com precisão de 30% pode recuperar
    dois terços."""
    X, y = tabela
    perdidas = y[y == 1].index
    risco_total = X.loc[perdidas, "receita_12m"].sum()
    t = lista.priorizar(escore, valor_em_risco=X.receita_12m)
    alcance = {}
    for coluna in ("na_fila", "na_fila_por_valor"):
        fila = t[t[coluna]].index.intersection(perdidas)
        alcance[coluna] = X.loc[fila, "receita_12m"].sum() / risco_total
    assert alcance["na_fila"] < 0.01
    assert alcance["na_fila_por_valor"] > 0.60

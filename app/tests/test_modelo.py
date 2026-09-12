# -*- coding: utf-8 -*-
"""Treino, reprodutibilidade e avaliação honesta."""

from __future__ import annotations

import pandas as pd

from app.churn import modelo
from app.tests.conftest import precisa_da_base


@precisa_da_base
def test_a_auc_fora_da_amostra_passa_de_08(tabela, escore):
    X, y = tabela
    assert modelo.auc(escore, y) > 0.80


@precisa_da_base
def test_o_escore_fora_da_amostra_e_menor_que_o_de_dentro(tabela, escore):
    """Se os dois derem igual, a validação cruzada não está separando nada."""
    X, y = tabela
    m = modelo.treinar(X, y)
    dentro = pd.Series(m.predict_proba(X)[:, 1], index=X.index)
    assert modelo.auc(dentro, y) > modelo.auc(escore, y)


@precisa_da_base
def test_o_treino_e_reproduzivel(tabela):
    X, y = tabela
    a = modelo.treinar(X, y).predict_proba(X)[:, 1]
    b = modelo.treinar(X, y).predict_proba(X)[:, 1]
    assert (a == b).all()


@precisa_da_base
def test_a_recencia_e_a_coluna_mais_importante(tabela):
    X, y = tabela
    m = modelo.treinar(X, y)
    imp = modelo.importancia(m, X, y, repeticoes=3)
    assert imp.coluna.iloc[0] == "dias_desde_ultima_compra"


@precisa_da_base
def test_o_modelo_gravado_devolve_o_mesmo_escore(tabela, tmp_path):
    X, y = tabela
    m = modelo.treinar(X, y)
    caminho = modelo.salvar(m, tmp_path / "m.joblib")
    recarregado = modelo.carregar(caminho)
    assert (m.predict_proba(X)[:, 1] == recarregado.predict_proba(X)[:, 1]).all()

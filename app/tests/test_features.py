# -*- coding: utf-8 -*-
"""A tabela de entrada não pode enxergar depois do corte."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from app.churn import features, rotulo
from app.churn.dados import pedidos
from app.tests.conftest import precisa_da_base


def _pedidos_de_brinquedo() -> pd.DataFrame:
    linhas = [
        # conta com duas compras antes do corte e uma depois
        ("A", "2023-01-10", 100.0, "F1"),
        ("A", "2023-07-10", 300.0, "F2"),
        ("A", "2024-06-01", 999.0, "F3"),
        # conta com uma compra só, dentro da janela de 12 a 24 meses
        ("B", "2022-05-05", 50.0, "F4"),
        # conta que só existe depois do corte
        ("C", "2024-08-01", 70.0, "F5"),
        # conta cuja única compra é anterior às três janelas de comparação
        ("D", "2020-02-01", 80.0, "F6"),
    ]
    df = pd.DataFrame(linhas, columns=["account_id", "billing_dt",
                                       "total_value_usd", "invoice_no"])
    df["billing_dt"] = pd.to_datetime(df.billing_dt)
    return df


CORTE = pd.Timestamp("2024-03-07")


def test_a_conta_posterior_ao_corte_nao_entra():
    f = features.construir(_pedidos_de_brinquedo(), CORTE)
    assert list(f.index) == ["A", "B", "D"]


def test_a_compra_posterior_ao_corte_nao_muda_nada():
    """O teste que pega o vazamento. Apagar tudo depois do corte não pode
    alterar nenhuma coluna de nenhuma conta.

    Visto falhando: trocar `billing_dt <= corte` por `<=` no fim do painel faz
    dias_desde_ultima_compra da conta A cair de 241 para 0.
    """
    ped = _pedidos_de_brinquedo()
    completo = features.construir(ped, CORTE)
    truncado = features.construir(ped[ped.billing_dt <= CORTE], CORTE)
    pd.testing.assert_frame_equal(completo, truncado)


def test_a_data_de_corte_muda_a_tabela():
    """Corte como parâmetro precisa ter efeito, senão ele é decorativo."""
    ped = _pedidos_de_brinquedo()
    antes = features.construir(ped, "2023-03-01")
    depois = features.construir(ped, CORTE)
    assert antes.loc["A", "dias_desde_ultima_compra"] != depois.loc["A", "dias_desde_ultima_compra"]


def test_conta_com_uma_compra_so_nao_gera_cadencia_invalida():
    f = features.construir(_pedidos_de_brinquedo(), CORTE)
    b = f.loc["B"]
    assert b.desvio_padrao_intervalo_dias == 0.0
    assert b.gap_maximo_historico_dias == 0.0
    # A razão cai perto de 1,0 porque o intervalo típico vira o tempo de casa.
    assert 0.9 < b.razao_recencia_cadencia <= 1.0


def test_a_razao_distingue_queda_a_zero_de_ausencia_de_base():
    """Dois casos que a mesma coluna precisa separar.

    A conta B comprou entre 12 e 24 meses atrás e nada depois: ela caiu a zero,
    e a razão é 0,0. A conta D comprou antes das três janelas: não há com o que
    comparar, e a razão é 1,0, o valor neutro. Preencher as duas com zero diria
    'caiu 100%' para quem nunca teve base de comparação.

    Escrevi este teste esperando 1,0 para a conta B e ele reprovou: era o teste
    que estava errado, e não a coluna.
    """
    f = features.construir(_pedidos_de_brinquedo(), CORTE)
    assert f.loc["B", "razao_receita_12m"] == 0.0
    assert f.loc["D", "razao_receita_12m"] == 1.0
    assert f.loc["D", "razao_receita_24m"] == 1.0


def test_nenhuma_coluna_sai_como_nula_ou_infinita():
    f = features.construir(_pedidos_de_brinquedo(), CORTE)
    assert np.isfinite(f.to_numpy(dtype=float)).all()


def test_o_dicionario_cobre_todas_as_colunas():
    d = features.dicionario()
    assert list(d.coluna) == features.FEATURES
    assert (d["data mais recente"] == "o corte").all()


# ---------------------------------------------------------------------------
# Contra a base de verdade
# ---------------------------------------------------------------------------

@precisa_da_base
def test_a_tabela_real_tem_4708_contas_e_11_colunas(tabela):
    X, y = tabela
    assert X.shape == (4708, 11)
    assert int(y.sum()) == 2456


@precisa_da_base
def test_nenhuma_feature_real_muda_com_o_painel_truncado():
    ped = pedidos()
    contas = rotulo.elegiveis()
    completo = features.construir(ped, rotulo.CORTE, contas=contas)
    truncado = features.construir(
        ped[ped.billing_dt <= rotulo.CORTE], rotulo.CORTE, contas=contas)
    pd.testing.assert_frame_equal(completo, truncado)

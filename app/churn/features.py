# -*- coding: utf-8 -*-
"""A tabela de entrada do modelo, com data de corte no argumento.

Três mudanças em relação ao script exportado do Gemini:

1. **A data de corte é parâmetro.** Sem isso não dá para auditar a função nem
   reexecutá-la em outro recorte, que é o que a Aula 06 cobrou.
2. **Tudo vetorizado.** O `groupby.apply` que calculava a cadência conta a conta
   era o gargalo: com 7.259 contas ele roda um laço Python por grupo. As mesmas
   medidas saem de `diff` e `groupby.agg`.
3. **As colunas de erosão entram declaradas.** Elas medem variação de receita
   entre janelas, e não o nível. A Aula 06 mostrou que a tabela só media parada
   de compra.

Nenhuma coluna lê dado posterior ao corte. `tests/test_features.py` recalcula a
tabela sobre um histórico truncado e exige que nenhum valor mude.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

# As oito que vieram do Gemini, com os nomes preservados.
FEATURES_BASE = [
    "dias_desde_ultima_compra",
    "gap_maximo_historico_dias",
    "dias_desde_primeira_compra",
    "desvio_padrao_intervalo_dias",
    "meses_com_compra_12m",
    "razao_recencia_cadencia",
    "qtd_pedidos_3m",
    "receita_12m",
]

# As três que a Aula 06 pediu, medindo variação em vez de nível.
FEATURES_EROSAO = ["razao_receita_12m", "razao_receita_24m", "queda_contra_pico"]

FEATURES = FEATURES_BASE + FEATURES_EROSAO

TETO_DA_RAZAO = 10.0


def _receita_entre(hist: pd.DataFrame, contas: pd.Index,
                   inicio: pd.Timestamp, fim: pd.Timestamp) -> pd.Series:
    faixa = hist[(hist.billing_dt > inicio) & (hist.billing_dt <= fim)]
    return faixa.groupby("account_id").total_value_usd.sum().reindex(contas).fillna(0.0)


def _razao(numerador: pd.Series, denominador: pd.Series) -> np.ndarray:
    """Razão entre duas janelas, limitada e com o caso sem base declarado.

    Denominador zero significa que não havia com o que comparar. A razão vira
    1,0, que é o valor neutro, e a leitura correta é que a coluna não fala nada
    sobre essa conta. Preencher com zero diria "caiu 100%", que é outra coisa.
    """
    den = denominador.to_numpy(dtype=float)
    num = numerador.to_numpy(dtype=float)
    r = np.divide(num, den, out=np.ones(len(den)), where=den > 0)
    return np.clip(r, 0.0, TETO_DA_RAZAO)


def construir(pedidos: pd.DataFrame, corte: pd.Timestamp | str,
              contas: pd.Index | None = None) -> pd.DataFrame:
    """Uma linha por conta, com as onze colunas fechadas no corte."""
    corte = pd.Timestamp(corte)
    hist = pedidos[pedidos.billing_dt <= corte]
    if contas is None:
        contas = pd.Index(sorted(hist.account_id.unique()), name="account_id")

    por_conta = hist.groupby("account_id")
    f = pd.DataFrame(index=contas)
    f["dias_desde_ultima_compra"] = (corte - por_conta.billing_dt.max()).dt.days
    f["dias_desde_primeira_compra"] = (corte - por_conta.billing_dt.min()).dt.days

    doze = hist[hist.billing_dt > corte - pd.DateOffset(months=12)]
    tres = hist[hist.billing_dt > corte - pd.DateOffset(months=3)]
    f["receita_12m"] = doze.groupby("account_id").total_value_usd.sum()
    f["qtd_pedidos_3m"] = tres.groupby("account_id").invoice_no.nunique()
    f["meses_com_compra_12m"] = (
        doze.assign(_m=doze.billing_dt.dt.to_period("M"))
        .groupby("account_id")._m.nunique())

    # Cadência: intervalo entre dias distintos de compra, sem laço por grupo.
    dias = (hist[["account_id", "billing_dt"]].drop_duplicates()
            .sort_values(["account_id", "billing_dt"]))
    dias["intervalo"] = dias.groupby("account_id").billing_dt.diff().dt.days
    intervalos = dias.groupby("account_id").intervalo
    f["desvio_padrao_intervalo_dias"] = intervalos.std()
    f["gap_maximo_historico_dias"] = intervalos.max()
    intervalo_medio = intervalos.mean()

    f = f.fillna({"receita_12m": 0.0, "qtd_pedidos_3m": 0, "meses_com_compra_12m": 0,
                  "desvio_padrao_intervalo_dias": 0.0, "gap_maximo_historico_dias": 0.0})
    # Conta com uma compra só não tem cadência. O tempo de casa é o melhor
    # substituto disponível, e é o que o script original também fazia.
    medio = intervalo_medio.reindex(contas)
    f["intervalo_medio_dias"] = medio.fillna(f.dias_desde_primeira_compra)
    f["razao_recencia_cadencia"] = (
        f.dias_desde_ultima_compra / (f.intervalo_medio_dias + 1))

    r12 = _receita_entre(hist, contas, corte - pd.DateOffset(months=12), corte)
    r24 = _receita_entre(hist, contas, corte - pd.DateOffset(months=24),
                         corte - pd.DateOffset(months=12))
    r36 = _receita_entre(hist, contas, corte - pd.DateOffset(months=36),
                         corte - pd.DateOffset(months=24))
    f["razao_receita_12m"] = _razao(r12, r24)
    f["razao_receita_24m"] = _razao(r12 + r24, r36)
    pico = np.maximum.reduce([r12.to_numpy(), r24.to_numpy(), r36.to_numpy()])
    f["queda_contra_pico"] = np.divide(r12.to_numpy(), pico, out=np.ones(len(pico)),
                                       where=pico > 0)

    return f[FEATURES].fillna(0.0)


def dicionario() -> pd.DataFrame:
    """Nome, o que mede e a data mais recente que a coluna usa.

    O dicionário é entregável, e não comentário: sem ele ninguém audita a
    tabela seis meses depois.
    """
    linhas = [
        ("dias_desde_ultima_compra", "recência", "o corte"),
        ("gap_maximo_historico_dias", "maior silêncio já observado", "o corte"),
        ("dias_desde_primeira_compra", "tempo de casa", "o corte"),
        ("desvio_padrao_intervalo_dias", "irregularidade da cadência", "o corte"),
        ("meses_com_compra_12m", "frequência nos 12 meses finais", "o corte"),
        ("razao_recencia_cadencia", "silêncio atual sobre o silêncio típico", "o corte"),
        ("qtd_pedidos_3m", "atividade nos 3 meses finais", "o corte"),
        ("receita_12m", "nível de receita nos 12 meses finais", "o corte"),
        ("razao_receita_12m", "12 meses finais sobre os 12 anteriores", "o corte"),
        ("razao_receita_24m", "24 meses finais sobre os 12 anteriores a eles", "o corte"),
        ("queda_contra_pico", "receita atual sobre o melhor ano do histórico", "o corte"),
    ]
    return pd.DataFrame(linhas, columns=["coluna", "o que mede", "data mais recente"])

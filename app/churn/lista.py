# -*- coding: utf-8 -*-
"""Da probabilidade para a lista de trabalho.

O script exportado devolvia a probabilidade e parava ali. Probabilidade não é
decisão: o Account Manager precisa saber quais contas atender esta semana, e a
fila tem tamanho fixo.

O limiar sai da capacidade operacional, medida na Aula 04 em 138 contas por
ciclo, e não do 0,5 que vem por padrão em qualquer biblioteca.
"""

from __future__ import annotations

import pandas as pd

CAPACIDADE = 138


def priorizar(escore: pd.Series, valor_em_risco: pd.Series | None = None,
              capacidade: int = CAPACIDADE) -> pd.DataFrame:
    """Ordena a carteira e marca quem cabe na fila do ciclo.

    Quando `valor_em_risco` é passado, a tabela também traz o valor esperado,
    que é o que o Comitê olha: probabilidade sozinha trata uma conta de mil
    dólares como uma de um milhão.
    """
    t = pd.DataFrame({"escore": escore})
    # method="first" e nao "min": com "min" oito contas empatadas recebem
    # todas a posicao 1, e uma fila de trabalho com oito primeiros lugares
    # nao e uma fila.
    t["posicao"] = t.escore.rank(ascending=False, method="first").astype(int)
    t["na_fila"] = t.posicao <= capacidade
    if valor_em_risco is not None:
        # Valor ausente ou infinito vira zero, e a conta desce na ordenação por
        # valor. Sem esta linha o `rank(...).astype(int)` estoura com
        # IntCastingNaNError, e foi assim que a primeira versão quebrou quando a
        # receita anualizada dividiu por tempo de casa igual a zero.
        valor = (valor_em_risco.reindex(t.index)
                 .replace([float("inf"), float("-inf")], pd.NA)
                 .fillna(0.0).astype(float))
        t["valor_em_risco"] = valor
        t["valor_esperado"] = t.escore * valor
        t["posicao_por_valor"] = (
            t.valor_esperado.rank(ascending=False, method="first").astype(int))
        t["na_fila_por_valor"] = t.posicao_por_valor <= capacidade
    return t.sort_values("escore", ascending=False)


def matriz_de_confusao(t: pd.DataFrame, churn: pd.Series,
                       coluna: str = "na_fila") -> dict[str, int | float]:
    """O que a fila acerta e o que ela deixa passar."""
    real = churn.reindex(t.index).to_numpy(dtype=int)
    previsto = t[coluna].to_numpy(dtype=int)
    vp = int(((previsto == 1) & (real == 1)).sum())
    fp = int(((previsto == 1) & (real == 0)).sum())
    fn = int(((previsto == 0) & (real == 1)).sum())
    vn = int(((previsto == 0) & (real == 0)).sum())
    return {"verdadeiros_positivos": vp, "falsos_positivos": fp,
            "falsos_negativos": fn, "verdadeiros_negativos": vn,
            "precisao": vp / (vp + fp) if vp + fp else float("nan"),
            "revocacao": vp / (vp + fn) if vp + fn else float("nan"),
            "acuracia": (vp + vn) / len(t)}


def concorda_com_a_capacidade(t: pd.DataFrame, capacidade: int = CAPACIDADE) -> bool:
    """A fila precisa ter exatamente o tamanho da capacidade, salvo empate."""
    return int(t.na_fila.sum()) >= capacidade

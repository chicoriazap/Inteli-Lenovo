# -*- coding: utf-8 -*-
"""O rótulo do case e a população que ele alcança.

O script exportado do Gemini inventava o próprio alvo: cortava em 2022-06-30 e
chamava de perdida a conta sem compra até 2024-12-31. Isso é um alvo defensável,
mas não é o alvo do case, e um modelo avaliado contra um rótulo diferente do que
o Comitê aprovou não pode ser comparado com nada do que a turma produziu antes.

Aqui o rótulo vem da coluna `churn_label` do painel, que marca a conta cuja
última compra é até 07/03/2024.
"""

from __future__ import annotations

import pandas as pd

from .dados import carregar

CORTE = pd.Timestamp("2024-03-07")
MES_DO_CORTE = "2024-03"
FIM_DO_PAINEL = "2026-08"


def rotulo() -> pd.Series:
    """Uma linha por conta, com 1 para perdida."""
    painel = carregar()["painel"]
    return painel.groupby("account_id").churn_label.max().rename("churn")


def elegiveis() -> pd.Index:
    """As contas que o rótulo consegue alcançar.

    Conta cuja primeira compra é posterior ao corte não teve como acumular o
    silêncio que o rótulo exige. Medir modelo nelas mede data de entrada.
    """
    painel = carregar()["painel"]
    primeira = painel.groupby("account_id").periodo.min()
    return primeira[primeira <= MES_DO_CORTE].index

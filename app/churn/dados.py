# -*- coding: utf-8 -*-
"""Carga das abas do case, com cache local.

O xlsx tem 69 MB e a aba de pedidos tem quase meio milhão de linhas. Ler direto
custa mais de um minuto, e um aplicativo que faz isso a cada clique não é
utilizável. O cache em pickle é derivado do xlsx e não entra no controle de
versão.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
XLSX = RAIZ / "dados" / "datasets_case_modulo2_5yrs.xlsx"
CACHE = RAIZ / "dados" / ".cache"

ABAS = {"painel": "Dataset 1", "mix": "Dataset 2", "engajamento": "Dataset 3",
        "cadastro": "Dataset 4", "pedidos": "raw data"}


class DatasetAusente(FileNotFoundError):
    """O xlsx não está em dados/. Não é erro de código."""


@lru_cache(maxsize=1)
def carregar() -> dict[str, pd.DataFrame]:
    if all((CACHE / f"{nome}.pkl").exists() for nome in ABAS):
        return {nome: pd.read_pickle(CACHE / f"{nome}.pkl") for nome in ABAS}
    if not XLSX.exists():
        raise DatasetAusente(
            f"{XLSX} não encontrado. A base não é versionada: peça o arquivo "
            "pelo canal da turma e coloque-o em dados/.")
    xl = pd.ExcelFile(XLSX)
    dados = {nome: xl.parse(aba) for nome, aba in ABAS.items()}
    CACHE.mkdir(exist_ok=True)
    for nome, df in dados.items():
        df.to_pickle(CACHE / f"{nome}.pkl")
    return dados


@lru_cache(maxsize=1)
def pedidos() -> pd.DataFrame:
    """Linha de pedido, com data já convertida e valor já numérico.

    A conversão acontece uma vez. O script exportado do Gemini refazia as duas
    conversões sobre as 492.393 linhas a cada previsão, e era isso que fazia
    cada consulta custar meio segundo.
    """
    p = carregar()["pedidos"].copy()
    p["billing_dt"] = pd.to_datetime(p["billing_dt"])
    p["total_value_usd"] = pd.to_numeric(
        p["total_value_usd"].astype(str).str.replace(",", "."), errors="coerce").fillna(0.0)
    return p

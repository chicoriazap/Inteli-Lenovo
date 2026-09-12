# -*- coding: utf-8 -*-
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))

XLSX = RAIZ / "dados" / "datasets_case_modulo2_5yrs.xlsx"
CACHE = RAIZ / "dados" / ".cache"

precisa_da_base = pytest.mark.skipif(
    not (XLSX.exists() or CACHE.exists()),
    reason="a base não é versionada: coloque o xlsx em dados/")


@pytest.fixture(scope="session")
def tabela():
    from app.treinar import preparar

    return preparar()


@pytest.fixture(scope="session")
def escore(tabela):
    from app.churn import modelo

    X, y = tabela
    return modelo.escore_fora_da_amostra(X, y)

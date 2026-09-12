# -*- coding: utf-8 -*-
"""Treino, persistência e avaliação honesta do modelo.

O script exportado treinava a cada chamada. Aqui o modelo é treinado uma vez,
gravado em disco e carregado pronto. O aplicativo abre em menos de um segundo.

A avaliação usa predição fora da amostra por validação cruzada: a probabilidade
de cada conta é produzida por um modelo que não a viu no treino. Sem isso, o
escore da conta que o Account Manager está olhando na tela foi ajustado com o
desfecho dela dentro.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold

RAIZ = Path(__file__).resolve().parents[2]
MODELO = RAIZ / "app" / "modelo.joblib"

SEMENTE = 42
DOBRAS = 5

# Os mesmos hiperparâmetros que saíram do Gemini. Trocá-los é exercício da
# Aula 06: sem uma busca com validação, mexer aqui é chute.
HIPERPARAMETROS = dict(learning_rate=0.05, max_depth=5, min_samples_leaf=5,
                       max_iter=100, random_state=SEMENTE)


def novo() -> HistGradientBoostingClassifier:
    return HistGradientBoostingClassifier(**HIPERPARAMETROS)


def treinar(X: pd.DataFrame, y: pd.Series):
    modelo = novo()
    modelo.fit(X, y)
    return modelo


def salvar(modelo, caminho: Path = MODELO) -> Path:
    import joblib

    caminho.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(modelo, caminho)
    return caminho


def carregar(caminho: Path = MODELO):
    import joblib

    if not caminho.exists():
        raise FileNotFoundError(
            f"{caminho} não existe. Rode `python -m app.treinar` antes de abrir a tela.")
    return joblib.load(caminho)


def escore_fora_da_amostra(X: pd.DataFrame, y: pd.Series) -> pd.Series:
    """Probabilidade de cada conta por um modelo que não a viu no treino."""
    valores = np.zeros(len(X))
    dobras = StratifiedKFold(DOBRAS, shuffle=True, random_state=SEMENTE)
    for treino, teste in dobras.split(X, y):
        m = novo()
        m.fit(X.iloc[treino], y.iloc[treino])
        valores[teste] = m.predict_proba(X.iloc[teste])[:, 1]
    return pd.Series(valores, index=X.index, name="escore")


def auc(escore: pd.Series, y: pd.Series) -> float:
    return float(roc_auc_score(y, escore))


def importancia(modelo, X: pd.DataFrame, y: pd.Series, repeticoes: int = 5) -> pd.DataFrame:
    """Importância por permutação, que é a que vale para árvore.

    Ela mede quanto a métrica cai quando a coluna é embaralhada. Diferente do
    coeficiente da logística, não tem sinal: ela diz o quanto a coluna importa,
    e não para que lado ela empurra.
    """
    from sklearn.inspection import permutation_importance

    r = permutation_importance(modelo, X, y, n_repeats=repeticoes,
                               random_state=SEMENTE, scoring="roc_auc")
    return (pd.DataFrame({"coluna": X.columns, "queda_de_auc": r.importances_mean,
                          "desvio": r.importances_std})
            .sort_values("queda_de_auc", ascending=False)
            .reset_index(drop=True))

# -*- coding: utf-8 -*-
"""Treina o modelo, grava em disco e imprime a avaliação.

Rodar uma vez antes de abrir a tela:

    python -m app.treinar

O aplicativo carrega o arquivo gravado aqui. Treinar dentro da tela faria cada
abertura custar o treino inteiro, e faria cada usuário ver um modelo diferente.
"""

from __future__ import annotations

import time

import pandas as pd

from .churn import features, lista, modelo, rotulo
from .churn.dados import pedidos


def preparar():
    ped = pedidos()
    elegiveis = rotulo.elegiveis()
    X = features.construir(ped, rotulo.CORTE, contas=elegiveis)
    y = rotulo.rotulo().reindex(X.index).astype(int)
    return X, y


def main() -> None:
    inicio = time.time()
    X, y = preparar()
    print(f"tabela: {len(X)} contas x {X.shape[1]} colunas "
          f"({time.time() - inicio:.1f}s)")
    print(f"perdidas: {int(y.sum())} ({y.mean():.1%})")

    escore = modelo.escore_fora_da_amostra(X, y)
    print(f"AUC fora da amostra: {modelo.auc(escore, y):.4f}")

    m = modelo.treinar(X, y)
    caminho = modelo.salvar(m)
    print(f"modelo gravado em {caminho.relative_to(caminho.parents[1])}")

    t = lista.priorizar(escore, valor_em_risco=X.receita_12m)
    c = lista.matriz_de_confusao(t, y)
    print(f"fila de {lista.CAPACIDADE}: {c['verdadeiros_positivos']} acertos, "
          f"precisão {c['precisao']:.1%}, revocação {c['revocacao']:.1%}")
    cv = lista.matriz_de_confusao(t, y, coluna="na_fila_por_valor")
    print(f"fila por valor esperado: {cv['verdadeiros_positivos']} acertos, "
          f"precisão {cv['precisao']:.1%}")

    imp = modelo.importancia(m, X, y)
    print("\nimportância por permutação:")
    print(imp.to_string(index=False, float_format=lambda v: f"{v:.4f}"))

    escore.to_frame().join(t[["posicao", "na_fila"]]).to_csv(
        caminho.parent / "escores.csv")
    print(f"\ntempo total: {time.time() - inicio:.1f}s")


if __name__ == "__main__":
    main()

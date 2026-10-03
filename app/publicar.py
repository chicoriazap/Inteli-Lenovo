# -*- coding: utf-8 -*-
"""Publica a fila do ciclo num arquivo que o n8n consegue servir.

Rodar depois de `python -m app.treinar`:

    python -m app.publicar --grupo g3      # grava saida/fila_publicada.json,
                                           # saida/fila_publicada.csv (a planilha
                                           # do painel) e saida/workflow_n8n.json

O n8n não roda scikit-learn. O que vai para lá é o resultado do modelo, uma
linha por conta da fila, e não o modelo. É inferência em lote: o escore muda
uma vez por ciclo, quando a base é recarregada, e não a cada pergunta feita ao
agente.

Só sai o que a tela já mostra: identificador anonimizado, escore, posições e
valores arredondados, e as quatro colunas que o Account Manager usa para
justificar a ligação. Nenhum pedido, nome ou campo de cadastro.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from . import workflow_n8n
from .churn import lista

SAIDA = Path(__file__).resolve().parents[1] / "saida" / "fila_publicada.json"
WORKFLOW = SAIDA.with_name("workflow_n8n.json")

# O que o agente pode citar. Coluna fora desta lista não sai da máquina.
SINAIS = ["dias_desde_ultima_compra", "meses_com_compra_12m",
          "razao_recencia_cadencia", "queda_contra_pico"]


def registros(tabela: pd.DataFrame, X: pd.DataFrame,
              capacidade: int = lista.CAPACIDADE) -> list[dict]:
    """A fila por valor esperado, em ordem, uma linha por conta.

    `tabela` é a saída de `lista.priorizar` com `valor_em_risco` preenchido.
    """
    fila = (tabela[tabela.posicao_por_valor <= capacidade]
            .sort_values("posicao_por_valor"))
    saida = []
    for conta, linha in fila.iterrows():
        sinais = X.loc[conta, SINAIS]
        saida.append({
            "account_id": str(conta),
            "posicao_por_valor": int(linha.posicao_por_valor),
            "posicao_por_probabilidade": int(linha.posicao),
            "escore": round(float(linha.escore), 3),
            "valor_em_risco_usd": int(round(float(linha.valor_em_risco))),
            "valor_esperado_usd": int(round(float(linha.valor_esperado))),
            **{c: round(float(sinais[c]), 2) for c in SINAIS},
        })
    return saida


def main() -> None:
    from .churn import modelo
    from .treinar import preparar

    p = argparse.ArgumentParser()
    p.add_argument("--capacidade", type=int, default=lista.CAPACIDADE)
    p.add_argument("--grupo", default="grupo",
                   help="vai para a URL do webhook; dois grupos com o mesmo nome colidem")
    p.add_argument("--modelo", default=workflow_n8n.MODELO_PADRAO,
                   help="identificador do modelo no OpenRouter")
    args = p.parse_args()

    X, y = preparar()
    escore = modelo.escore_fora_da_amostra(X, y)
    tabela = lista.priorizar(escore, valor_em_risco=X.receita_12m,
                             capacidade=args.capacidade)
    fila = registros(tabela, X, args.capacidade)
    SAIDA.parent.mkdir(exist_ok=True)
    SAIDA.write_text(json.dumps(fila, ensure_ascii=False, indent=1), encoding="utf-8")
    pd.DataFrame(fila).to_csv(SAIDA.with_suffix(".csv"), index=False)
    wf = workflow_n8n.montar(fila, grupo=args.grupo, modelo=args.modelo)
    WORKFLOW.write_text(json.dumps(wf, ensure_ascii=False, indent=1), encoding="utf-8")
    total = sum(r["valor_esperado_usd"] for r in fila)
    print(f"{len(fila)} contas gravadas em {SAIDA.relative_to(SAIDA.parents[1])}")
    print(f"workflow para importar no n8n em {WORKFLOW.relative_to(WORKFLOW.parents[1])}")
    print(f"valor esperado somado: USD {total:,}".replace(",", "."))


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""Saída de emergência: os números da Aula 03, lidos do dataset oficial.

Este script existe para que uma mesa com o ambiente travado continue a aula. Ele
não substitui a análise do grupo: o artefato é o código que vocês escreverem.

O arquivo `datasets_case_modulo2.xlsx` não está neste repositório. Coloque-o em
`dados/` antes de executar.

Uso: python analise_referencia.py
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parent
XLSX = RAIZ / "dados" / "datasets_case_modulo2.xlsx"

# O painel termina em 2026-03. A recência de uma conta é contada a partir daí,
# e é essa âncora que torna comparáveis os cortes de inatividade.
FIM_DO_PAINEL = "2026-03"

ABAS = {
    "painel": "Dataset 1",
    "mix": "Dataset 2",
    "engajamento": "Dataset 3",
    "cadastro": "Dataset 4",
    "pedidos": "raw data",
}


class DatasetAusente(FileNotFoundError):
    """O xlsx oficial não está em dados/. Não é erro de código."""


@lru_cache(maxsize=1)
def carregar() -> dict[str, pd.DataFrame]:
    """Lê as cinco abas. Nenhuma limpeza acontece aqui: o dado cru é o material
    da aula, e limpar antes esconderia as advertências que a turma precisa achar."""
    if not XLSX.exists():
        raise DatasetAusente(
            f"{XLSX} não encontrado. O dataset oficial não é versionado (ADR-005): "
            "peça o arquivo pelo canal da turma e coloque-o em dados/."
        )
    xl = pd.ExcelFile(XLSX)
    return {nome: xl.parse(aba) for nome, aba in ABAS.items()}


def _meses_desde(periodo: str, referencia: str = FIM_DO_PAINEL) -> int:
    """Distância em meses entre dois rótulos 'YYYY-MM'."""
    ay, am = (int(p) for p in periodo.split("-"))
    by, bm = (int(p) for p in referencia.split("-"))
    return (by - ay) * 12 + (bm - am)


@lru_cache(maxsize=1)
def contas() -> pd.DataFrame:
    """Uma linha por conta: o grão em que o rótulo vive.

    O `churn_label` do painel é constante dentro da conta, então agregar por
    `max` não perde informação. Conferido em `perfil_do_rotulo`.
    """
    d = carregar()
    painel, cadastro = d["painel"], d["cadastro"]
    c = painel.groupby("account_id").agg(
        churn=("churn_label", "max"),
        segmento=("segmento_lenovo", "first"),
        regiao=("regiao", "first"),
        receita=("receita_usd", "sum"),
        pedidos=("qtd_pedidos", "sum"),
        meses_ativos=("periodo", "nunique"),
        ultimo_mes=("periodo", "max"),
        primeiro_mes=("periodo", "min"),
    )
    c["inatividade"] = c.ultimo_mes.map(_meses_desde)
    # O cadastro tem account_id repetido com setor e região divergentes: a
    # primeira linha é uma escolha declarada, não um fato do dado.
    cad = cadastro.drop_duplicates("account_id").set_index("account_id")
    return c.join(cad[["setor", "tempo_como_cliente", "porte"]])


# ---------------------------------------------------------------------------
# Perfil e qualidade
# ---------------------------------------------------------------------------

def formato_das_abas() -> dict[str, tuple[int, int]]:
    return {nome: df.shape for nome, df in carregar().items()}


def qualidade() -> dict[str, int | float]:
    d = carregar()
    painel, mix, engaj, cad = d["painel"], d["mix"], d["engajamento"], d["cadastro"]
    contas_painel = set(painel.account_id)
    return {
        "contas": painel.account_id.nunique(),
        "meses": painel.periodo.nunique(),
        "primeiro_mes": painel.periodo.min(),
        "ultimo_mes": painel.periodo.max(),
        "receita_negativa": int((painel.receita_usd < 0).sum()),
        "receita_zero": int((painel.receita_usd == 0).sum()),
        "cadastro_duplicado": int(cad.account_id.duplicated().sum()),
        "mix_pct_nulo": int(mix.pct_receita.isna().sum()),
        "engaj_contas": engaj.account_id.nunique(),
        "engaj_fora_do_painel": len(set(engaj.account_id) - contas_painel),
        "engaj_dentro_do_painel": len(set(engaj.account_id) & contas_painel),
        "engaj_cobertura": len(set(engaj.account_id) & contas_painel) / len(contas_painel),
        "engaj_periodos": engaj.periodo.nunique(),
    }


# ---------------------------------------------------------------------------
# Univariada
# ---------------------------------------------------------------------------

def receita_univariada() -> dict[str, float]:
    r = contas().receita
    return {
        "media": float(r.mean()),
        "mediana": float(r.median()),
        "desvio": float(r.std()),
        "minimo": float(r.min()),
        "maximo": float(r.max()),
        "assimetria": float(r.skew()),
        "curtose": float(r.kurtosis()),
        "assimetria_log10": float(np.log10(r.clip(lower=1)).skew()),
    }


def pareto(fracoes=(0.01, 0.05, 0.10, 0.20)) -> dict[float, float]:
    """Participação na receita das contas do topo. A cauda é o assunto do dia:
    com assimetria de 44, a média por conta não descreve conta nenhuma."""
    r = contas().receita.sort_values(ascending=False)
    total = r.sum()
    return {f: float(r.head(int(len(r) * f)).sum() / total) for f in fracoes}


# ---------------------------------------------------------------------------
# Bivariada
# ---------------------------------------------------------------------------

def prevalencia_por(coluna: str) -> pd.DataFrame:
    c = contas()
    t = c.groupby(coluna).agg(contas=("churn", "size"), perdidas=("churn", "sum"),
                              receita=("receita", "sum"))
    t["prevalencia"] = t.perdidas / t.contas
    t["participacao_receita"] = t.receita / t.receita.sum()
    return t.sort_values("prevalencia", ascending=False)


def contingencia_rotulo() -> pd.DataFrame:
    """Último mês com receita contra o rótulo. É a tabela que entrega o corte."""
    c = contas()
    return pd.crosstab(c.ultimo_mes, c.churn)


def perfil_do_rotulo() -> dict[str, object]:
    d = carregar()
    por_conta = d["painel"].groupby("account_id").churn_label.nunique()
    c = contas()
    perdidas, ativas = c[c.churn == 1], c[c.churn == 0]
    return {
        "rotulo_constante_na_conta": bool((por_conta == 1).all()),
        "contas_perdidas": int(c.churn.sum()),
        "prevalencia": float(c.churn.mean()),
        "ultimo_mes_maximo_das_perdidas": perdidas.ultimo_mes.max(),
        "ultimo_mes_minimo_das_ativas": ativas.ultimo_mes.min(),
        "inatividade_minima_das_perdidas": int(perdidas.inatividade.min()),
        "inatividade_maxima_das_ativas": int(ativas.inatividade.max()),
        "mes_de_sobreposicao": "2025-02",
    }


def limiar_de_inatividade(cortes=(6, 9, 12, 13)) -> dict[int, dict[str, float]]:
    """O que cada corte de inatividade marcaria, contra o rótulo entregue.

    É o exercício do dia: o rótulo oficial não é um fato do sistema, é um corte
    que alguém escolheu. Trocar o corte troca o tamanho da fila e troca quantas
    das contas hoje marcadas continuam marcadas.
    """
    c = contas()
    oficial = c.churn == 1
    saida = {}
    for corte in cortes:
        marcado = c.inatividade >= corte
        saida[corte] = {
            "fila": int(marcado.sum()),
            "captura_do_rotulo_oficial": float((marcado & oficial).sum() / oficial.sum()),
            "receita_da_fila": float(c.receita[marcado].sum()),
        }
    return saida


def corte_diario_do_rotulo() -> dict[str, object]:
    """A data exata em que o rótulo separa, recuperada da aba de pedidos.

    O painel mensal leva a turma até "inatividade de 13 meses" e para ali, com
    382 contas que o corte marca e o rótulo não. A separação é perfeita no dia:
    a regra foi construída sobre a data do pedido, que o agregado mensal não
    expõe. É o argumento de por que a aba `raw data` entra na aula.
    """
    d = carregar()
    ultima = d["pedidos"].groupby("account_id")["Order Date"].max()
    c = contas().join(ultima.rename("ultima_compra"))
    perdidas, ativas = c[c.churn == 1], c[c.churn == 0]
    limite_perdidas = perdidas.ultima_compra.max()
    limite_ativas = ativas.ultima_compra.min()
    return {
        "ultima_compra_maxima_das_perdidas": limite_perdidas.strftime("%Y-%m-%d"),
        "ultima_compra_minima_das_ativas": limite_ativas.strftime("%Y-%m-%d"),
        "separacao_perfeita": bool(limite_perdidas < limite_ativas),
        "contas_no_mes_de_sobreposicao": int((c.ultimo_mes == "2025-02").sum()),
        "sobra_do_corte_mensal": int(((c.inatividade >= 13) & (c.churn == 0)).sum()),
    }


def tempo_de_casa_por_rotulo() -> dict[str, int | float]:
    c = contas()
    novas = c[c.tempo_como_cliente < 17]
    return {
        "piso_de_tempo_das_perdidas": int(c.tempo_como_cliente[c.churn == 1].min()),
        "contas_com_menos_de_17_meses": int(len(novas)),
        "perdidas_entre_elas": int(novas.churn.sum()),
    }


def main() -> None:
    q, r, p = qualidade(), receita_univariada(), perfil_do_rotulo()
    print("=== formato das abas ===")
    for nome, (linhas, colunas) in formato_das_abas().items():
        print(f"  {nome:12} {linhas:>7} linhas x {colunas:>2} colunas")
    print("\n=== qualidade ===")
    for k, v in q.items():
        print(f"  {k:26} {v}")
    print("\n=== receita por conta ===")
    for k, v in r.items():
        print(f"  {k:18} {v:,.4f}")
    print("\n=== pareto ===")
    for f, v in pareto().items():
        print(f"  top {f:.0%}: {v:.4%}")
    print("\n=== rotulo ===")
    for k, v in p.items():
        print(f"  {k:34} {v}")
    print("\n=== tempo de casa ===")
    for k, v in tempo_de_casa_por_rotulo().items():
        print(f"  {k:30} {v}")
    print("\n=== prevalencia por segmento ===")
    print(prevalencia_por("segmento").to_string())
    print("\n=== prevalencia por setor ===")
    print(prevalencia_por("setor").to_string())
    print("\n=== contingencia ultimo mes x rotulo ===")
    print(contingencia_rotulo().to_string())
    print("\n=== corte diario ===")
    for k, v in corte_diario_do_rotulo().items():
        print(f"  {k:36} {v}")
    print("\n=== cortes de inatividade ===")
    for corte, v in limiar_de_inatividade().items():
        print(f"  >= {corte:>2} meses: fila {v['fila']:>5}  "
              f"captura {v['captura_do_rotulo_oficial']:.4%}  "
              f"receita {v['receita_da_fila']:,.0f}")


if __name__ == "__main__":
    main()

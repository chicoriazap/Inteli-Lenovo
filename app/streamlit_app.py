# -*- coding: utf-8 -*-
"""A tela que o Account Manager abriria.

Rodar:

    python -m app.treinar        # uma vez, grava app/modelo.joblib
    streamlit run app/streamlit_app.py

A tela não treina nada. Ela carrega o modelo gravado e os escores calculados
fora da amostra. Treinar aqui faria cada abertura custar o treino inteiro e
faria cada usuário ver um modelo diferente.
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from app.churn import features, lista, modelo, rotulo
from app.churn.dados import pedidos

st.set_page_config(page_title="Kovan LATAM: fila de retenção", layout="wide")


@st.cache_data(show_spinner="Carregando a carteira...")
def carregar_tudo():
    ped = pedidos()
    contas = rotulo.elegiveis()
    X = features.construir(ped, rotulo.CORTE, contas=contas)
    y = rotulo.rotulo().reindex(X.index).astype(int)
    escore = modelo.escore_fora_da_amostra(X, y)
    cadastro = pedidos().drop_duplicates("account_id").set_index("account_id")
    return ped, X, y, escore, cadastro


@st.cache_resource
def carregar_modelo():
    return modelo.carregar()


ped, X, y, escore, cadastro = carregar_tudo()

st.title("Fila de retenção da Kovan LATAM")
st.caption(
    f"Corte em {rotulo.CORTE:%d/%m/%Y}. {len(X):,} contas elegíveis, "
    f"{int(y.sum()):,} marcadas como perdidas. Escores calculados fora da "
    "amostra, por validação cruzada de 5 dobras."
    .replace(",", "."))

with st.sidebar:
    st.header("Como montar a fila")
    capacidade = st.number_input(
        "Capacidade do ciclo, em contas", min_value=10, max_value=1000,
        value=lista.CAPACIDADE, step=1,
        help="Medido na Aula 04: o time atende 138 contas por ciclo.")
    criterio = st.radio(
        "Ordenar por",
        ["Probabilidade de perda", "Valor esperado em risco"],
        help="Probabilidade acha quem sai. Valor esperado acha quanto sai junto.")
    st.divider()
    st.caption(
        "O escore é a probabilidade de a conta não comprar mais depois do "
        "corte. O valor em risco é a receita dos 12 meses anteriores ao corte.")

tabela = lista.priorizar(escore, valor_em_risco=X.receita_12m, capacidade=int(capacidade))
coluna_fila = "na_fila" if criterio.startswith("Probabilidade") else "na_fila_por_valor"
coluna_pos = "posicao" if coluna_fila == "na_fila" else "posicao_por_valor"
fila = tabela[tabela[coluna_fila]].sort_values(coluna_pos)

perdidas = y[y == 1].index
acertos = fila.index.intersection(perdidas)
risco_total = X.loc[perdidas, "receita_12m"].sum()
risco_na_fila = X.loc[acertos, "receita_12m"].sum()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Contas na fila", f"{len(fila)}")
c2.metric("Acertos", f"{len(acertos)}",
          help="Contas da fila que estavam mesmo se perdendo.")
c3.metric("Precisão", f"{len(acertos) / max(len(fila), 1):.1%}")
c4.metric("Receita em risco alcançada", f"{risco_na_fila / max(risco_total, 1):.1%}",
          help=f"USD {risco_na_fila:,.0f} de USD {risco_total:,.0f}".replace(",", "."))

st.info(
    "Troque o critério na barra lateral e compare os dois últimos cartões. "
    "A fila por probabilidade acerta mais contas; a fila por valor esperado "
    "alcança mais dinheiro.")

st.subheader("A fila do ciclo")
visao = fila.join(cadastro[["segment", "country", "industry"]])
visao = visao.assign(
    escore=lambda d: d.escore.round(3),
    valor_em_risco=lambda d: d.valor_em_risco.round(0),
    valor_esperado=lambda d: d.valor_esperado.round(0),
)
st.dataframe(
    visao[[coluna_pos, "escore", "valor_em_risco", "valor_esperado",
           "segment", "country", "industry"]],
    use_container_width=True, height=380,
    column_config={
        coluna_pos: st.column_config.NumberColumn("posição"),
        "escore": st.column_config.ProgressColumn("escore", min_value=0.0, max_value=1.0),
        "valor_em_risco": st.column_config.NumberColumn("receita 12m", format="$ %d"),
        "valor_esperado": st.column_config.NumberColumn("valor esperado", format="$ %d"),
    })

st.divider()
st.subheader("Abrir uma conta")
conta = st.selectbox("Conta", options=list(tabela.index),
                     index=list(tabela.index).index(fila.index[0]) if len(fila) else 0)

linha = tabela.loc[conta]
d1, d2, d3 = st.columns(3)
d1.metric("Escore", f"{linha.escore:.3f}")
d2.metric("Posição por probabilidade", f"{int(linha.posicao)}º")
d3.metric("Posição por valor esperado", f"{int(linha.posicao_por_valor)}º")

if int(linha.posicao) > len(X) / 2 and linha.valor_em_risco > X.receita_12m.median() * 10:
    st.warning(
        "Conta de valor alto com escore baixo. O histórico de compra desta "
        "conta não traz o sinal que o modelo usa, e a lista por probabilidade "
        "vai deixá-la passar. Olhe a série abaixo antes de descartar.")

esq, dir = st.columns([2, 1])
with esq:
    st.markdown("**Compras por mês, até o corte**")
    serie = ped[(ped.account_id == conta) & (ped.billing_dt <= rotulo.CORTE)]
    if len(serie):
        mensal = (serie.assign(mes=serie.billing_dt.dt.to_period("M").astype(str))
                  .groupby("mes").total_value_usd.sum())
        st.bar_chart(mensal, height=240)
    else:
        st.caption("Sem compras até o corte.")
with dir:
    st.markdown("**As onze colunas de entrada**")
    st.dataframe(X.loc[[conta]].T.rename(columns={conta: "valor"}),
                 use_container_width=True, height=240)

with st.expander("O que esta tela não sabe"):
    st.markdown(
        "- O escore mede **parada de compra**. Conta que encolhe e continua "
        "comprando não aparece como risco, e esse é o Caminho B do case.\n"
        "- A base de engajamento cobre 33,8% das contas antes do corte, então "
        "contato comercial não entra como coluna.\n"
        "- O valor em risco é a receita dos 12 meses anteriores ao corte. Conta "
        "parada há mais de um ano tem valor zero por construção.\n"
        "- Nenhuma coluna usa dado posterior ao corte. Isso é verificado em "
        "`app/tests/test_features.py`.")

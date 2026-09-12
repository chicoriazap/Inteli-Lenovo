# app: do modelo à fila de trabalho

Este diretório transforma o script exportado do Gemini em um aplicativo que
alguém consegue abrir, auditar e reexecutar.

## Rodar

```bash
pip install -r requirements.txt
python -m app.treinar                  # grava app/modelo.joblib
streamlit run app/streamlit_app.py     # abre a tela
python -m pytest app/tests -q          # trava o que não pode quebrar
```

A base fica em `dados/datasets_case_modulo2_5yrs.xlsx` e não é versionada. A
primeira execução converte as cinco abas para `dados/.cache/` e leva cerca de
três minutos; as seguintes levam segundos.

## O que mudou em relação ao script exportado

| Problema no script | O que foi feito |
|---|---|
| Alvo próprio, com corte em 2022-06-30 | usa o `churn_label` do case, com corte em 07/03/2024 |
| `groupby.apply` conta a conta na cadência | tudo vetorizado, com `diff` e `agg` |
| Reprocessava 492.393 linhas a cada previsão | conversão uma vez, com cache em disco |
| Treinava a cada chamada | treino uma vez, modelo gravado em `modelo.joblib` |
| Devolvia probabilidade solta | devolve a fila do ciclo, com o limiar vindo da capacidade |
| Avaliação dentro da amostra | escore fora da amostra, por validação cruzada |
| Sem colunas de variação de receita | três colunas de erosão declaradas |

## Estrutura

- `churn/dados.py`: carga das cinco abas, com cache.
- `churn/rotulo.py`: o rótulo do case e a população elegível.
- `churn/features.py`: as onze colunas, com a data de corte no argumento.
- `churn/modelo.py`: treino, persistência, escore fora da amostra e importância.
- `churn/lista.py`: da probabilidade para a fila, por escore ou por valor esperado.
- `treinar.py`: roda tudo e imprime a avaliação.
- `streamlit_app.py`: a tela.

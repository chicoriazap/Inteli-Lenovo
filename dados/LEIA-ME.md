# Estrutura da Pasta `dados/`

Esta pasta contém os arquivos de microdados transacionais e cadastrais do Case Lenovo / Kovam.

> ⚠️ **AVISO DE SEGURANÇA E PRIVACIDADE**: Os arquivos `.xlsx`, `.csv` e `.parquet` contidos nesta pasta representam dados reais de carteira e **não são versionados no Git** (bloqueados via `.gitignore`).

---

## 📁 Arquivos Disponíveis

| Arquivo | Período Temporal | Descrição |
|---|---|---|
| **`datasets_case_modulo2.xlsx`** | 2024-04 a 2026-03 (24 meses) | **Dataset padrão oficial** de 2 anos (utilizado por `analise_referencia.py` e rotinas padrão). |
| **`datasets_case_modulo2_2yrs.xlsx`** | 2024-04 a 2026-03 (24 meses) | Dataset de 2 anos obtido a partir da divisão do histórico de 5 anos. |
| **`datasets_case_modulo2_3yrs.xlsx`** | 2021-04 a 2024-03 (36 meses) | Dataset dos 3 anos iniciais obtido a partir da divisão do histórico de 5 anos. |
| **`datasets_case_modulo2_5yrs.xlsx`** | 2021-04 a 2026-08 (65 meses) | Dataset histórico completo acumulado de 5 anos. |

---

## 📄 As 5 Abas Presentes em Todos os Arquivos

1. **`Dataset 1` (Painel):** Faturamento mensal por conta com indicador de churn (`churn_label`).
2. **`Dataset 2` (Mix):** Participação de receita e mix de marcas por conta.
3. **`Dataset 3` (Engajamento):** Atividades e oportunidades comerciais no CRM.
4. **`Dataset 4` (Cadastro):** Informações cadastrais (porte, setor, canal de aquisição, tempo de casa).
5. **`raw data` (Pedidos):** Microdados das linhas de pedidos e faturamento.

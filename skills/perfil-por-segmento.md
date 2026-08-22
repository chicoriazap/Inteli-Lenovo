# Skill: perfil de compra por segmento

O objetivo é descrever como cada segmento compra, sobre a população que o
rótulo consegue marcar, antes de testar qualquer hipótese de causa.

## Passo 1: restrinja à população elegível

O `churn_label` exige treze meses sem compra e o painel termina em 2026-03.
Uma conta cuja primeira compra é posterior a 2025-02 não tem como estar
marcada, qualquer que seja o comportamento dela. Calcule o primeiro mês com
receita de cada conta e separe:

- elegíveis: primeiro mês até 2025-02;
- não elegíveis: primeiro mês de 2025-03 em diante.

Informe quantas contas ficam em cada grupo e a prevalência em cada um. A
prevalência das não elegíveis precisa ser zero; se não for, o critério do
rótulo que você recuperou está errado.

Todo passo seguinte roda sobre as elegíveis.

## Passo 2: as cinco medidas, no grão da conta

Para cada conta elegível, calcule a partir das abas correspondentes:

| Medida | Aba | Como |
|---|---|---|
| receita mediana | Dataset 1 | soma da `receita_usd` nos 24 meses, depois mediana por segmento |
| dias de compra | raw data | número de datas distintas em `Order Date` |
| marcas | Dataset 2 | número de `Brand` distintas |
| intervalo entre compras | raw data | mediana, em dias, da diferença entre datas de compra consecutivas; só existe para contas com duas ou mais datas |
| marca dominante | Dataset 2 | a `Brand` com maior `pct_receita` |

Agregue por `segmento_lenovo` com mediana (e moda, para a marca dominante).
Traga também contas, perdidas e prevalência na mesma tabela.

## Passo 3: declare o que a tabela não mede

A conta mediana da carteira tem dois meses ativos em 24. Intervalo entre
compras só existe para quem comprou em duas datas distintas; diga quantas
contas ficaram sem essa medida em cada segmento. Canal de aquisição tem um
único valor na base e não entra. Engajamento comercial (Dataset 3) cobre menos
de metade das contas e entra marcado como parcial.

## Saída

`perfil_por_segmento.csv` em `analises/` e uma leitura escrita de duas frases
por segmento: como ele compra e o que isso não permite concluir sobre churn.

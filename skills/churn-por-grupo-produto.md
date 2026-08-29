# Skill: análise de churn por agrupamento de produto

O objetivo é cruzar o rótulo de churn com grupos de produto derivados da coluna
`Brand` da aba raw data, para entender se o mix de produtos comprados está
associado à retenção ou à perda do cliente.

## Passo 1: mapear Brand para grupos de produto

Normalize a coluna `Brand` (casing inconsistente na base) e agrupe em categorias
de negócio. O mapeamento padrão é:

| Grupo | Brands incluídas |
|---|---|
| PC | NOTEBOOK, SMB NOTEBOOK, DESKTOP, WORKSTATION, ALL-IN-ONE |
| Tablet | TABLET, TABLET & SMART DEVICE, TAB WIN |
| Monitores | VISUALS |
| Serviços | SERVICES |
| Periféricos/Outros | THINK PERIPHERALS, SSP, S&P, BUNDLE, SMART HUB, PHONE |

Brands com valor `0`, `OTHERS`, `LCS 其它` e `OPTIONAL` entram como "Sem
Classificação". Registre quantas linhas caem nesta categoria e mantenha-as fora
dos gráficos principais.

Antes de prosseguir, confirme que o mapeamento foi aceito ou peça ajustes ao
grupo.

## Passo 2: construir a tabela de flags por conta

No grão `account_id`, crie uma flag binária para cada grupo: a conta comprou ou
não comprou aquele tipo de produto ao longo de todo o histórico. Junte com o
`churn_label`.

## Passo 3: taxa de churn — comprou vs. não comprou cada grupo

Para cada grupo de produto, compare a taxa de churn entre quem comprou e quem não
comprou. Traga na mesma tabela: contagem, churns e taxa de churn. Inclua a taxa
global como referência.

Marque com alerta qualquer grupo com menos de 100 contas compradoras (base
pequena, taxa volátil).

## Passo 4: penetração de produto — churn vs. não-churn

Inverta a pergunta: entre as contas que churnaram, qual % comprou cada grupo?
E entre as que ficaram? Isso mostra se o mix de produto difere entre os dois
grupos.

## Passo 5: receita mediana por grupo

Para cada grupo de produto, compare a receita mediana acumulada entre contas
churn e não-churn. Traga a razão churn/não-churn.

Obrigatoriamente registre a ressalva de vazamento: a receita acumulada é menor em
contas churn porque elas pararam de comprar antes, logo acumularam menos. Essa
correlação não pode ser lida como causa.

## Passo 6: perfis de compra combinados

Para cada conta, construa o "perfil" indicando quais grupos comprou (ex: "PC +
Monitores + Serviços"). Cruze com churn e ordene por contagem. Traga os 10-15
perfis mais frequentes.

Essa é a tabela mais reveladora: ela mostra se contas com mix mais diversificado
têm churn sistematicamente menor.

## Passo 7: a leitura escrita

Abaixo de cada gráfico e tabela, escreva:
- O que o dado mostra;
- O que ele não permite concluir (correlação ≠ causa);
- A ressalva de vazamento do rótulo (conforme documentado na análise bivariada).

## Saída

Script em `analises/churn_por_grupo_produto.py`, figuras em `figuras/` e
relatório descritivo com tabelas e leituras.

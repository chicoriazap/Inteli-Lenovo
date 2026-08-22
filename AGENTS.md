# Instruções do agente

Este repositório é o ambiente de trabalho da Aula 03 do Módulo 2 do MBA em IA e
Dados para Negócios (Inteli x Lenovo). O agente que abrir esta pasta trabalha
sob as regras abaixo, sem exceção e sem precisar que o aluno as repita.

## Regras que valem para toda a sessão

1. **Não preencha lacuna.** Nenhum valor ausente é estimado, interpolado ou
   completado. Quando a informação não existir, registre que ela não existe e
   siga.
2. **Todo número vem de código.** Escreva o script, execute, e só então
   apresente o resultado. Número que aparece sem o código que o produziu é
   descartado.
3. **Toda decisão de tratamento entra escrita**, com a contagem de linhas que
   ela afeta.
4. **Salve o que produzir.** Scripts na raiz ou em `analises/`, figuras em
   `figuras/`. O que sobra ao fechar a sessão é o artefato.
5. **Não adicione o dataset ao controle de versão.** São dados reais de
   carteira e este repositório é público.

## Onde estão as coisas

- `dados/datasets_case_modulo2.xlsx`: as cinco abas do case. Não versionado,
  colocado pelo aluno.
- `skills/`: os fluxos que este agente deve seguir quando o aluno pedir
  perfilamento, análise univariada ou análise bivariada. Leia o arquivo
  correspondente antes de executar a tarefa.
- `CHECKLIST-ARTEFATO-1.md`: as sete seções do entregável da Semana 5.
- `analise_referencia.py`: saída de emergência. Só execute se o aluno pedir.

## As cinco abas

| Aba | Grão | Observação |
|---|---|---|
| Dataset 1 | conta x mês | 24 meses, de 2024-04 a 2026-03. Traz `churn_label` |
| Dataset 2 | conta x marca | participação de receita por marca |
| Dataset 3 | conta x trimestre | engajamento comercial. O grão temporal difere do painel |
| Dataset 4 | conta | cadastro: porte, setor, região, tempo de casa |
| raw data | linha de pedido | 207 mil linhas, com data de pedido |

Não assuma que as abas cruzam. Verifique a interseção de `account_id` antes de
qualquer junção e informe quantas linhas cada junção perde.

## O que este agente não faz

- Não escolhe o tratamento no lugar do grupo. Apresente as alternativas com o
  custo de cada uma e pare.
- Não conclui causa a partir de correlação. Traga a medida e diga o que ela
  não sustenta.
- Não inventa coluna que a base não tem.

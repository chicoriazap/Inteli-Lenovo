# Skill: análise univariada

Uma variável por vez. O objetivo é descrever a distribuição e dizer o que ela
permite afirmar, não comparar grupos ainda.

## Passo 1: declare o grão antes de medir

Antes de qualquer estatística, diga em que grão a variável está sendo medida:
por linha, por conta, por conta e mês. A mesma coluna em dois grãos devolve dois
números, e trocar um pelo outro no meio do relatório é o erro mais comum aqui.

## Passo 2: as três perguntas

Para cada variável numérica, traga na mesma tabela:

- **Tendência central:** média e mediana. Quando as duas divergem por mais de
  uma ordem de grandeza, a média deixa de descrever qualquer caso individual e o
  relatório precisa dizer isso em texto.
- **Dispersão:** desvio padrão, mínimo, máximo e os quartis.
- **Forma:** assimetria e curtose. Assimetria acima de 1 indica cauda longa à
  direita; curtose alta indica que os extremos dominam a variância.

## Passo 3: a figura que corresponde à pergunta

- **Histograma** quando a pergunta é sobre o formato da distribuição.
- **Boxplot** quando a pergunta é sobre onde está a maioria e quem está fora.
- **Curva de concentração** quando a pergunta é quanto do total está no topo.

Escala logarítmica quando a assimetria passa de 3. Declare a transformação na
legenda: um eixo em log sem aviso é um gráfico que engana quem lê rápido.

## Passo 4: a leitura escrita

Abaixo de cada figura, escreva duas frases: o que ela mostra, e o que ela não
permite concluir. Figura sem leitura escrita não entra no artefato.

## Passo 5: a leitura para quem não é da área

Reescreva a leitura de cada figura em linguagem de negócio, sem usar termo
técnico que não seja explicado na mesma frase. Quartil, mediana e desvio travam
mais gente numa reunião do que o raciocínio em si.

## Saída

Figuras em `figuras/`, com nome que descreve o conteúdo, e um `univariada.md`
com a tabela de medidas e a leitura de cada figura.

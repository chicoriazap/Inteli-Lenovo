# Skill: análise bivariada contra um alvo binário

O objetivo é medir se uma variável separa os dois grupos do rótulo, e dizer o
que essa separação sustenta.

## Passo 1: um corte por vez

Cruze o alvo com uma variável de cada vez. Dois cortes simultâneos escondem qual
dos dois produziu o efeito, e desfazer isso depois custa mais do que fazer na
ordem certa.

## Passo 1a: quem pode exibir o desfecho

Antes de cruzar, pergunte se toda conta da base tinha como receber o rótulo.
Um rótulo que depende de tempo decorrido (treze meses sem compra, no caso da
Kovan) não alcança conta que entrou tarde. Restrinja à população que pode
exibir o desfecho e informe quantas contas saíram. Hipótese testada na base
inteira mistura "não perdeu" com "não teve tempo de perder".

## Passo 2: a tabela de contingência

Para variável categórica, traga na mesma tabela:

- contagem absoluta em cada célula;
- prevalência do alvo dentro de cada categoria;
- participação da categoria no total, e no indicador de negócio que importa.

Prevalência sem tamanho de base engana: 100% de churn em três contas não é
achado. Categoria com menos de 30 observações entra marcada como tal.

## Passo 3: variável contínua contra alvo binário

Compare a distribuição da variável nos dois grupos. Traga mediana e quartis de
cada grupo, não só a média. Boxplots lado a lado, mesma escala nos dois.

## Passo 4: correlação, e o que ela não diz

Quando calcular correlação, informe o coeficiente, o método e o número de
observações. Depois escreva, obrigatoriamente, uma frase dizendo qual explicação
alternativa a correlação não descarta.

Correlação alta entre uma variável e o alvo pode significar três coisas
diferentes: a variável antecipa o alvo, a variável é consequência do alvo, ou as
duas dependem de um terceiro fator. Diga qual das três você consegue descartar
com esta base e qual você não consegue.

## Passo 4a: estratifique antes de concluir

Para toda associação que sobreviver ao ruído (intervalos de confiança que não
se cruzam, qui-quadrado com p abaixo de 0,05), repita a medida dentro de cada
estrato de um terceiro fator plausível: segmento, coorte de entrada, faixa de
frequência de compra. Três desfechos possíveis, e o relatório diz qual ocorreu:

- a diferença se mantém em todos os estratos: sobrevive;
- a diferença some dentro dos estratos: a variável era proxy do fator de
  estratificação;
- a diferença inverte em algum estrato: a associação no total é composição.

Estrato com menos de 30 contas em qualquer dos grupos entra marcado.

## Passo 5: o teste de vazamento

Para toda variável que separa o alvo muito bem, pergunte antes de comemorar:
essa informação estaria disponível no momento em que a decisão precisa ser
tomada? Variável construída depois do desfecho não é preditor, e um modelo
treinado com ela funciona no teste e falha em produção.

Sinais de vazamento a investigar sempre:

- separação perfeita ou quase perfeita entre os dois grupos;
- valor da variável que muda de significado conforme o rótulo;
- data ou contagem que só existe porque o desfecho já aconteceu.

## Passo 6: o rótulo entregue pronto

Quando o alvo já vem como coluna na base, reconstrua o critério que o define
antes de usá-lo. Cruze o rótulo com as variáveis temporais e procure o ponto em
que a separação acontece. Um rótulo cujo critério você não conseguiu recuperar
entra no relatório como critério desconhecido.

## Saída

Figuras em `figuras/` e um `bivariada.md` com cada tabela de contingência, a
leitura escrita e a seção de vazamento investigado.

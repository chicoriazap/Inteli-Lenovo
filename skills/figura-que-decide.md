# Skill: a figura que decide

Uma figura entra no relatório quando ela sustenta uma decisão que o texto
sozinho não sustenta. Esta skill produz essa figura a partir de uma hipótese
que já passou pelos testes de `bivariada.md`.

## Passo 1: escreva a pergunta antes de escolher a forma

A forma da figura é escolhida pela pergunta, nunca pelo gosto:

| Pergunta | Forma |
|---|---|
| Como uma variável se distribui? | Histograma, com a escala declarada |
| Onde está a maioria e quem está fora, em vários grupos? | Boxplot lado a lado, mesma escala |
| Duas variáveis andam juntas? | Scatterplot, com o número de pontos na legenda |
| Uma proporção difere entre categorias? | Barras horizontais com intervalo de confiança |
| Duas contas se comportaram diferente no tempo? | Séries lado a lado, mesmo eixo, com o corte do rótulo marcado |

## Passo 2: o título é a conclusão, com o número dentro

O título da figura declara o que ela prova, com o número que prova. "Uma
marca perde 66,4% e quatro ou mais perdem 16,1%" é título. "Prevalência por
número de marcas" é rótulo de eixo.

## Passo 3: desenhe o ruído e o limite

- Toda proporção leva o intervalo de confiança de 95% desenhado.
- Toda contagem de contas para intervenção leva a linha da capacidade
  operacional (138 planos por trimestre, no case da Kovan).
- O tamanho da base de cada categoria aparece na figura ou na legenda.

## Passo 4: o teste escrito embaixo

Abaixo da figura, em uma linha: o teste que a sustenta (intervalo de confiança,
qui-quadrado com graus de liberdade, ou estratificação), a população (elegíveis
ou carteira) e o que a figura não permite concluir. Figura sem essa linha não
entra no artefato.

## Passo 5: o que a figura não faz

Figura de dado observacional mostra associação. Ela não mostra causa, mesmo
quando a associação sobrevive à estratificação. A linha embaixo diz isso
quando for o caso.

## Saída

Figuras em `figuras/`, com nome que diz o que elas provam, e `visuais.md` com
uma entrada por figura: pergunta, forma, título, teste embaixo.

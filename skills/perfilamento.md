# Skill: perfilamento de base desconhecida

Execute este fluxo antes de qualquer análise, sempre que uma base nova entrar na
pasta. Ele não trata nada: ele descreve o que existe e nomeia o que está errado.

## Regra de execução

Nenhum valor ausente é preenchido. Nenhuma linha é descartada. O resultado deste
fluxo é um diagnóstico, não uma base limpa.

## Passo 1: o que o arquivo tem

Para cada aba, informe número de linhas, número de colunas e o nome de cada
coluna com o tipo de dado. Compare o número de linhas com o que a fonte declara.
Divergência aqui significa que o arquivo chegou quebrado, e nada adiante vale.

## Passo 2: o grão de cada aba

Para cada aba, responda: uma linha representa o quê? Verifique procurando a
combinação de colunas que não se repete. Uma aba cujo grão você não conseguiu
determinar entra no relatório como grão indeterminado.

## Passo 3: as chaves cruzam?

Para cada par de abas que compartilha um identificador, informe:

- quantos identificadores distintos existem em cada aba;
- quantos estão nas duas;
- quantos estão só na primeira e quantos só na segunda.

Junção que perde linha precisa aparecer com o número de linhas perdidas antes de
ser usada.

## Passo 4: o grão temporal cruza?

Quando duas abas têm coluna de período, informe o formato de cada uma, o número
de períodos distintos e o intervalo coberto. Formatos diferentes não são
detalhe de digitação: eles impedem a junção temporal e a decisão de como
compatibilizá-los é do grupo.

## Passo 5: as seis dimensões de qualidade

Coluna a coluna, meça e traga a contagem:

1. **Completude:** quantos nulos, e o nulo significa zero ou desconhecido?
2. **Validade:** existe valor impossível? Receita negativa, percentual acima de
   1, tempo de casa negativo.
3. **Consistência:** a mesma entidade aparece com dois valores diferentes para
   um atributo que deveria ser único?
4. **Unicidade:** existe linha duplicada, e existe identificador repetido?
5. **Acurácia:** os totais batem com o que outra aba afirma sobre o mesmo fato?
6. **Temporalidade:** o intervalo coberto é o que a fonte promete?

## Passo 6: o que você não conseguiu verificar

Liste o que ficou de fora e por quê. Esta seção é obrigatória e não pode sair
vazia: uma base sem limitação declarada é uma base que ninguém olhou.

## Saída

Um arquivo `perfil.md` na raiz da pasta, com uma seção por aba, e uma tabela
final com as advertências encontradas ordenadas pelo número de linhas afetadas.

# Skill: limpeza de dados

Fluxo de tratamento de uma base antes de qualquer análise. O agente lê este
arquivo da pasta e o executa sem que você repita as instruções.

Este arquivo é reutilizável em qualquer projeto e em qualquer base. Nada aqui é
específico da Kovan: o que a base tem de errado vem do perfilamento, e o que
fazer a respeito vem de quem responde pelo número.

**Como executar:** peça ao agente "execute skills/limpeza-de-dados.md sobre
dados/<arquivo>".

---

## 1. Quando usar

Sempre que uma base nova entrar no projeto, e antes de qualquer número sair
dela. Execute `skills/perfilamento.md` primeiro: esta skill trata o que aquela
encontrou.

## 2. Regras que valem para toda a execução

1. **Não preencha lacuna.** Nenhum valor ausente é estimado, interpolado ou
   completado. Quando a informação não existir, registre que ela não existe.
2. **Mostre o código antes do número.** Número apresentado sem o código que o
   produziu é descartado.
3. **Toda decisão de tratamento entra escrita**, com a contagem de linhas que
   ela afeta.
4. **Não decida no lugar de quem responde pelo número.** Meça, apresente as
   alternativas com o custo de cada uma, e pare para perguntar. Só siga depois
   da resposta.

## 3. As três decisões possíveis, e o que cada uma assume

Para toda advertência de qualidade existem três tratamentos, e cada um assume
uma coisa diferente sobre o mundo:

| Decisão | O que assume | Custo típico |
|---|---|---|
| **Excluir** a linha ou a coluna | que o que falta é aleatório, e o resto continua representativo | perde tamanho de amostra e enviesa quando a ausência é condicionada |
| **Imputar** um valor | que existe um valor plausível derivável do que está na base | inventa variação que não foi observada e suaviza o que o dado mostraria |
| **Sinalizar** com uma coluna indicadora | que a própria ausência é informação | mantém o tamanho da base e transfere a decisão para a análise seguinte |

Omissão conta como decisão de manter o dado como veio, e entra no registro com
esse nome.

## 4. O procedimento, advertência por advertência

Para cada advertência que o perfilamento devolveu, nesta ordem:

**Passo 1. Meça o tamanho.** Quantas linhas, quantas contas ou quantas colunas a
advertência atinge, em número absoluto e em proporção da base.

**Passo 2. Teste se a ausência é condicionada.** Compare a taxa da advertência
entre grupos formados por colunas que estão na base (segmento, região, porte,
período). Taxas próximas entre todos os grupos sustentam ausência aleatória;
taxa que acompanha uma coluna observada indica ausência condicionada, e nesse
caso excluir enviesa.

**Passo 3. Escolha o indicador de negócio** que a decisão altera. Precisa ser um
número que alguém usa para decidir, não uma métrica interna do tratamento.

**Passo 4. Calcule o indicador sob cada uma das três decisões.** Reaproveite o
mesmo código, trocando apenas a linha do tratamento. Apresente os três valores
lado a lado, com a contagem de linhas afetadas em cada caso.

**Passo 5. Pare e pergunte.** Apresente a tabela do passo 4 e a pergunta: qual
das três, e por quê? Não escolha. Quando a diferença entre as três for menor que
a precisão com que o indicador é usado, diga isso: significa que a discussão não
precisa acontecer, e essa também é uma informação útil.

**Passo 6. Registre a resposta** no formato da seção 5, com a justificativa que
a pessoa deu, em uma frase.

## 5. A saída

Ao final, escreva `registro-de-tratamento.md` com uma linha por advertência:

| advertência | tamanho | decisão | justificativa | indicador | valor | valor sob a alternativa |
|---|---|---|---|---|---|---|

E salve a base tratada em `dados/base_tratada.parquet`.

O registro é o artefato. A base tratada pode ser gerada de novo a partir dele; o
contrário não é verdade.

## 6. O que esta skill nunca faz

- Não preenche valor ausente por conta própria, em nenhuma circunstância.
- Não escolhe entre excluir, imputar e sinalizar sem resposta humana.
- Não descarta linha silenciosamente numa junção: junção que perde linha aparece
  com o número antes de ser usada.
- Não trata duas advertências no mesmo passo, porque aí o custo de cada uma
  deixa de ser separável.

---

## Critério de aceite

Outra pessoa copia esta skill e o `registro-de-tratamento.md` para a pasta dela,
executa contra a base crua e obtém os mesmos números que você apresentou.

Se não obtiver, o registro está incompleto, e o passo que divergiu é o que
precisa de mais uma linha. Essa é a diferença entre uma decisão que você tomou e
uma decisão que outra pessoa consegue repetir.

# Checklist do Artefato 1, Trilha de Tecnologia

**Análise Exploratória de Dados** · entrega 05/09/2026 · critério binário,
entregou ou não entregou. O foco é o feedback.

O artefato é a pasta que o grupo produzir: o código que carrega, limpa e
visualiza a base, mais as figuras que ele gera e o relatório que as lê.

Grupo: ____________________________   Data: ____ / ____ / 2026

---

## Fecha na oficina de hoje

### 1. CARGA
As cinco abas carregadas, com a contagem de linhas de cada uma conferida contra
a fonte. Se algum número não bater, o arquivo chegou quebrado e nada adiante
vale.

- [ ] Linhas e colunas por aba, conferidas
- [ ] O grão de cada aba declarado em uma frase
- [ ] Quantas contas cada aba tem e quantas cruzam com o painel

### 2. QUALIDADE
O `registro-de-tratamento.md` que a skill de limpeza produz: cada advertência, a
decisão tomada e o custo dela em número de linhas.

- [ ] As seis dimensões medidas coluna a coluna
- [ ] Uma decisão declarada por advertência, com justificativa em uma frase
- [ ] O custo de cada decisão, medido no indicador que ela altera
- [ ] O mesmo indicador recalculado sob a alternativa descartada
- [ ] O que não foi possível verificar, e por quê

**Teste da troca de pastas.** A mesa ao lado copia a skill e o registro de
vocês, executa contra a base crua e chega aos mesmos números. Número que não
bate aponta o passo do registro que só fazia sentido para quem escreveu.

### 3. UNIVARIADA
Distribuição das variáveis principais, com a leitura escrita de cada figura.

- [ ] Tendência central, dispersão e forma, na mesma tabela
- [ ] O grão de medição declarado antes de cada número
- [ ] Uma figura por pergunta, com a transformação de escala declarada
- [ ] Duas frases por figura: o que ela mostra e o que ela não permite concluir

### 4. BIVARIADA
Cruzamentos contra o `churn_label`, com tabela de contingência.

- [ ] Um corte por vez, com tamanho de base em cada célula
- [ ] Prevalência do alvo por categoria, ao lado da participação na receita
- [ ] Correlação com método e número de observações, quando calculada
- [ ] A explicação alternativa que a medida não descarta, escrita

---

## Vai para o autoestudo da semana

### 5. RÓTULO
O critério que o `churn_label` usa, reconstruído a partir do dado, e o efeito de
cortes alternativos.

- [ ] O critério recuperado, com a evidência que o sustenta
- [ ] O que o critério deixa de fora
- [ ] Pelo menos três cortes alternativos, com o tamanho da fila de cada um
- [ ] O teste de vazamento aplicado a toda variável que separa bem demais

### 6. VISUAIS
As figuras que sustentam a segmentação e as personas da manhã.

- [ ] Uma figura por segmento da segmentação do grupo
- [ ] Faixas reais das variáveis usadas em cada persona
- [ ] Cada característica de persona apontando para o número que a produziu

### 7. LIMITAÇÕES
O que a base não permite responder.

- [ ] As perguntas do Comitê que esta base não fecha
- [ ] O dado que faltaria para fechá-las
- [ ] O que a análise assume e não conseguiu verificar

---

## Critério de aceite

Outra pessoa clona a pasta do grupo, coloca o dataset em `dados/`, executa, e
obtém os mesmos números do relatório. Se não obtiver, o artefato não está
pronto, mesmo que o relatório esteja bonito.

# Kovan: análise exploratória

Ambiente de trabalho das Aulas 03 e 04 da Trilha de Tecnologia, Módulo 2 do MBA
em IA e Dados para Negócios (Inteli x Lenovo, turma 2026.2A).

## Setup, três passos

```bash
git clone https://github.com/josercf/inteli-pos-2026-2a-eda.git
cd inteli-pos-2026-2a-eda
```

1. Copie `datasets_case_modulo2.xlsx` para a pasta `dados/`.
2. Abra esta pasta no Antigravity.
3. Confirme que o agente leu o `AGENTS.md`, pedindo a ele que resuma as regras
   da sessão.

O dataset não está aqui e não deve ser adicionado: são dados reais de carteira
LATAM e este repositório é público.

## O contrato do dia

Toda seção do artefato entra com o número e a figura que a sustentam,
produzidos por código que roda nesta pasta.

## O que tem aqui

| Arquivo | Para quê |
|---|---|
| `AGENTS.md` | as regras que o agente carrega ao abrir a pasta |
| `skills/perfilamento.md` | o fluxo de perfilamento de uma base desconhecida |
| `skills/limpeza-de-dados.md` | o tratamento das advertências, com o custo medido |
| `skills/univariada.md` | o fluxo de análise de uma variável por vez |
| `skills/bivariada.md` | o fluxo de cruzamento contra o rótulo |
| `CHECKLIST-ARTEFATO-1.md` | as sete seções do entregável da Semana 5 |
| `analise_referencia.py` | saída de emergência, se o ambiente travar |

## As skills

Os quatro arquivos em `skills/` são instruções que o agente lê da pasta e
executa sem que você as repita na conversa. Eles são reutilizáveis fora deste
curso: `limpeza-de-dados.md` e `perfilamento.md` não têm nada específico da
Kovan, e servem para qualquer base que chegar na sua mesa.

Para executar, peça ao agente pelo caminho do arquivo:

    execute skills/perfilamento.md sobre dados/datasets_case_modulo2.xlsx

A skill de limpeza mede, apresenta as três decisões possíveis com o custo de
cada uma, e **para para perguntar**. A decisão continua sendo de quem responde
pelo número. O que ela produz é o `registro-de-tratamento.md`, que é o artefato.

## Saída de emergência

Se o ambiente travar, os números do dia saem de:

```bash
pip install -r requirements.txt
python analise_referencia.py
```

O script não substitui a análise do grupo. Ele existe para que uma mesa parada
continue a aula.

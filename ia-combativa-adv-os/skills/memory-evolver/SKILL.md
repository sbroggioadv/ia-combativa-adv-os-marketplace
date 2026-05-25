---
name: memory-evolver
description: >
  MEMORY-EVOLVER — Skill de infraestrutura para auto-melhoria dos arquivos MEMORY.md dentro do workspace COWORK. Acionada automaticamente pelo hook PostToolUse(Edit|Write) quando o arquivo editado esta dentro do COWORK e a edicao e significativa (diff > 50 chars). Decide se a edicao merece registro em MEMORY.md da area correspondente, aplica regra de bloat (<= 200 linhas, consolidacao periodica), migra entradas antigas para `<COWORK>/.dev-adv/.snapshots/` e mantem o MEMORY.md conciso e util. Tambem acionavel manualmente via `/cowork-doctor --memory-gc`. Use quando o usuario pedir para "atualizar memoria", "limpar MEMORY.md", "consolidar memoria", "memoria esta grande demais", ou quando o hook PostToolUse disparar.
---

# MEMORY-EVOLVER — Auto-melhoria dos MEMORY.md

## 1. POSICAO NO BATALHAO

**Skill de infraestrutura**, subordinada ao `firm-master` mas tipicamente acionada por **hooks automaticos** em vez de prompt direto. Nao produz output juridico — produz manutencao silenciosa dos arquivos de memoria de cada area do COWORK.

**Principio central:** a memoria do workspace deve crescer com utilidade, nao com ruido. Cada entrada em MEMORY.md precisa ter valor de retomada em sessao futura. Entradas obsoletas, duplicadas ou triviais sao consolidadas ou movidas para snapshots.

---

## 2. QUANDO ESTA SKILL E ACIONADA

### 2.1 Automaticamente (via hook PostToolUse)

O hook `post-edit-evolve-memory.py` chama esta skill quando:
- Ferramenta Edit ou Write foi usada.
- O arquivo modificado esta **dentro** do COWORK conhecido.
- A mudanca e significativa: diff > 50 chars (nao whitespace).
- Passou mais de 60 segundos desde o ultimo disparo da skill no mesmo path (anti-flap).
- O arquivo modificado **NAO** e o proprio MEMORY.md (evita loop).

### 2.2 Manualmente

Via `/cowork-doctor --memory-gc`, via `/cowork-memory --consolidate <area>`, ou quando o usuario pedir explicitamente.

---

## 3. REGRAS DE ADMISSAO (e uma entrada digna de MEMORY.md?)

Admitir entrada quando:
- E **decisao de arquitetura** ou padrao local adotado.
- E **contexto de cliente/processo** nao derivavel do codigo/dados (ex: "este cliente prefere comunicacao via WhatsApp, nao email").
- E **estado de sprint/tarefa em andamento** (ex: "peticao inicial do processo X pendente de juntada de 3 documentos").
- E **aviso operacional** (ex: "prazo fatal do processo X em 3 dias — ja no calendario").
- E **feedback do titular** sobre preferencia futura (ex: "evitar termo Y em replicas de agora em diante").

NAO admitir entrada quando:
- E apenas edicao de texto em documento final (a propria peca ja e o registro).
- E conteudo ja presente em CLAUDE.md ou em README (evitar duplicacao).
- E ruido temporario (ex: typo corrigido).
- E informacao sensivel que nao deve viver em arquivo local nao-criptografado (ex: senha, token, credencial).

---

## 4. ESTRUTURA CANONICA DE MEMORY.md (por area)

Cada pasta de area do COWORK tem seu proprio MEMORY.md com a estrutura:

```markdown
# MEMORY.md — [Nome da Area]

## Estado Atual
<1-3 paragrafos sobre onde a area esta — em que fase, o que esta em aberto>

## Decisoes Recentes
- [data] decisao X — razao Y
- [data] decisao Z — razao W

## Avisos e Prazos Operacionais
- [data] [processo N] — prazo Y em DD/MM/{{ANO_VIGENTE}}
- [data] [cliente Z] — follow-up pendente

## Feedbacks do Titular
- [data] "evitar termo X em ..."
- [data] "priorizar canal Y com cliente Z"

## Historico (snapshots)
> Entradas anteriores consolidadas em `.snapshots/MEMORY-<timestamp>.md`
```

---

## 5. REGRA DE BLOAT

Quando o MEMORY.md de uma area atingir **mais de 200 linhas**:

1. Calcular checksum do arquivo atual (SHA256).
2. Mover copia para `<COWORK>/.dev-adv/.snapshots/MEMORY-<area-slug>-<timestamp>-<sha8>.md`.
3. Consolidar o MEMORY.md aplicando regras:
   - Manter sempre as secoes **Estado Atual** e **Avisos e Prazos Operacionais** completas.
   - Manter **Decisoes Recentes** dos ultimos 90 dias; consolidar as antigas em bullet resumo.
   - Manter **Feedbacks do Titular** (essas nao expiram — sao preferencias permanentes).
   - Remover duplicatas textuais.
   - Remover entradas resolvidas (prazos vencidos sem consequencia, tarefas concluidas > 30 dias).
4. Adicionar nota ao final: "Historico consolidado em `.snapshots/MEMORY-<area>-<timestamp>-<sha8>.md`".
5. Validar que o MEMORY.md resultante tem < 150 linhas.

---

## 6. FLUXO DA SKILL QUANDO ACIONADA

### 6.1 Acionamento automatico (pelo hook)

O hook chama a skill passando:
- Path do arquivo editado.
- COWORK_ROOT identificado.
- Area correspondente (slug).
- Diff resumo (primeiros/ultimos 200 chars).

A skill:
1. Le o MEMORY.md da area (ou cria se nao existir, com template Secao 4).
2. Avalia se a mudanca atende as Regras de Admissao (Secao 3).
3. Se sim:
   - Adiciona entrada na secao correspondente do MEMORY.md.
   - Aplica timestamp.
   - Aplica deduplicacao (se entrada ja existir semelhante, apenas atualizar timestamp).
   - Se apos adicionar o MEMORY.md > 200 linhas, dispara Regra de Bloat (Secao 5).
4. Se nao: silencio. Nenhuma alteracao.
5. Atualiza `<COWORK>/.dev-adv/.hook-state.json` registrando timestamp do ultimo disparo para este path.

### 6.2 Acionamento manual (via comando)

1. Le todos os MEMORY.md do COWORK.
2. Aplica analise + consolidacao em cada um.
3. Reporta ao usuario: quantos arquivos analisados, quantos consolidados, quantos snapshots criados.

---

## 7. ANTI-LOOP E ANTI-FLAP

Esta skill NUNCA pode:
- Editar o proprio MEMORY.md que ela mesma acabou de tocar em loop.
- Ser acionada pelo hook em resposta a uma edicao que ela mesma fez.
- Disparar se o ultimo disparo no mesmo path foi ha menos de 60 segundos.
- Disparar em rename, chmod, delete (apenas Edit/Write).

O hook filtra esses casos via `<COWORK>/.dev-adv/.hook-state.json`. A skill valida novamente antes de qualquer escrita.

---

## 8. PROIBICOES ABSOLUTAS

- NUNCA escrever em MEMORY.md dados sensiveis (senhas, tokens, credenciais, dados pessoais completos de cliente).
- NUNCA remover secao "Feedbacks do Titular" — essas preferencias sao permanentes.
- NUNCA consolidar sem criar snapshot prévio.
- NUNCA escrever sem checar a regra de 60s de debouncing.
- NUNCA alterar arquivos fora do COWORK.
- NUNCA responder ao usuario quando acionada por hook — a operacao e silenciosa.

---

## 9. OUTPUT DA SKILL

### Modo automatico (hook)
Output **silencioso** — apenas escrita em arquivo. Nenhuma mensagem no chat, a menos que erro critico.

### Modo manual (comando)
Report estruturado:
```
MEMORY EVOLVER — Relatorio
Arquivos analisados: N
Entradas adicionadas: N
Entradas consolidadas: N
Snapshots criados: N
Arquivos sem mudanca: N
Proximo bloat estimado em: [area X] — +N linhas ate threshold
```

---

## 10. INTEGRACAO

- **Hook `PostToolUse(Edit|Write)`** — acionamento automatico principal.
- **Command `/cowork-doctor --memory-gc`** — acionamento manual de limpeza.
- **Skill `cowork-onboarding`** — cria MEMORY.md inicial em cada area durante o `/start`.
- **Script `scripts/evolve-memory.py`** — helper que o hook executa antes de chamar a skill (deteccao de area, calculo de diff, validacao de debouncing).

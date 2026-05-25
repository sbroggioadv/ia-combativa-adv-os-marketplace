---
description: Controla a skill memory-evolver. Subcomandos "off" (mute session), "on" (unmute), "status", "gc" (consolidacao imediata).
allowed-tools: Bash, Read, Edit, Write
---

Voce foi acionado pelo comando `/memory-evolver`. Dispatch o subcomando passado como argumento.

**Regra importante:** `memory-evolver` e skill **invariante** — nao pode ser removida permanentemente. Este comando apenas controla escape session-only (equivalente a `/corte off` para Suprema Corte).

## SUBCOMANDOS

### `/memory-evolver off` — mute session

Desativa a skill ate o fim da sessao. Hook PostToolUse continua disparando (pois hooks sao independentes), mas o hook le o mute flag e volta cedo sem registrar pending.

Acao:
1. Localizar COWORK via `python "${CLAUDE_PLUGIN_ROOT}/scripts/find-cowork.py"`.
2. Set flag: `python "${CLAUDE_PLUGIN_ROOT}/scripts/state.py" set "$COWORK" preferences.memory_evolver_session_muted true`.
3. Reportar:
   ```
   [memory-evolver] Silenciada ate fim da sessao.
   Para reativar agora: /memory-evolver on
   (Reseta automaticamente na proxima sessao ao carregar a persona.)
   ```

### `/memory-evolver on` — unmute

Reativa a skill na sessao atual.

Acao:
1. Localizar COWORK.
2. Set flag: `python "${CLAUDE_PLUGIN_ROOT}/scripts/state.py" set "$COWORK" preferences.memory_evolver_session_muted false`.
3. Reportar:
   ```
   [memory-evolver] Ativa. Edicoes dentro do COWORK voltam a gerar pending para consolidacao.
   ```

### `/memory-evolver status`

Mostra estado atual:
- Skill ativa? (leitura de `skills.invariants`).
- Mutada na sessao? (leitura de `preferences.memory_evolver_session_muted`).
- Quantidade de entradas pending em `<COWORK>/.dev-adv/.memory-evolver-pending.json`.
- MEMORY.md de cada area: tamanho em linhas + proximidade do threshold (200).
- Snapshots em `.snapshots/` (contagem).

Exemplo de output:
```
MEMORY-EVOLVER — Status

Skill:               INVARIANTE (sempre carregada)
Session mute:        [ ] off
Pending entries:     3
  - CONTENCIOSO/processo-XYZ.md (registrado 2026-04-17T18:32Z)
  - ...

MEMORY.md por area:
  (root)           45 linhas / 200  OK
  CONTENCIOSO     187 linhas / 200  ATENCAO (proximo do bloat)
  CONSULTIVO       23 linhas / 200  OK

Snapshots:           7 arquivos (max 20 retidos)
```

### `/memory-evolver gc [--area <slug>] [--force]`

Forca consolidacao imediata — equivalente a `/cowork-doctor --memory-gc`, mas focado apenas no memory-evolver.

1. Se `--area <slug>`, consolida apenas aquela area. Sem flag, todas.
2. Chama a skill `memory-evolver` internamente com instrucao "aplicar regra de bloat em [area]".
3. Report: quantos arquivos consolidados, quantos snapshots criados, quantas entradas pending processadas.

### (sem argumento) — help inline

Mostra tabela com subcomandos disponiveis e exemplos.

## PROIBICOES

- NUNCA marcar a skill como removida (`/cowork-remove-skill memory-evolver` e rejeitado — ela e invariante).
- NUNCA apagar snapshots sem confirmacao explicita.
- NUNCA processar pending de COWORK diferente do ativo.

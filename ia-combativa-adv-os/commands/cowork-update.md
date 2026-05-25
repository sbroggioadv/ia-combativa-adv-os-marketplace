---
description: Re-renderiza seletivamente arquivos do workspace COWORK (persona, CLAUDE.md por area, MEMORY, settings-local). Respeita edicoes manuais do usuario, exceto com --force.
allowed-tools: Bash, Read
---

Voce foi acionado pelo comando `/cowork-update`. Re-renderize arquivos do workspace COWORK conforme solicitado. **Operacao padrao e idempotente** — nao sobrescreve edicoes manuais do usuario a menos que `--force`.

## FLAGS SUPORTADAS

- `--persona` — re-renderiza somente `<COWORK>/.dev-adv/persona.md`.
- `--areas` — re-renderiza `CLAUDE.md` de cada area.
- `--memory` — re-renderiza `MEMORY.md` de cada area (apenas arquivos ausentes; nunca sobrescreve).
- `--settings` — re-renderiza `<workspace>/.claude/settings.local.json`.
- `--fingerprint` — atualiza `<COWORK>/.dev-adv/AUTO-DEPLOY.md` com snapshot atual.
- `--all` — equivalente a --persona + --areas + --memory + --settings + --fingerprint.
- `--force` — sobrescreve persona e MEMORY.md manuais sem perguntar.
- `--dry-run` — mostra o que seria feito sem aplicar.

Se nenhuma flag for passada, assumir `--persona --settings` (renovacao mais comum).

## PROTOCOLO

### 1. Localizar COWORK

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/find-cowork.py"
```

Guardar como `$COWORK`. Se nao encontrar, abortar com orientacao para rodar `/start`.

### 2. Dispatchar acoes

#### --persona
```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/render.py" "$COWORK" --only persona.md [--force] [--dry-run]
```

#### --areas
```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/render.py" "$COWORK" --only area-CLAUDE.md [--dry-run]
```
(Nota: area-CLAUDE.md e idempotente — nunca sobrescreve conteudo do usuario fora dos blocos marcados).

#### --memory
```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/render.py" "$COWORK" --only MEMORY.md [--dry-run]
```
(Cria MEMORY.md apenas em areas que nao tem. Nunca sobrescreve existentes sem `--force`.)

#### --settings
```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/render.py" "$COWORK" --only settings-local.json [--force] [--dry-run]
```

#### --fingerprint
```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/fingerprint.py" --plugin-root "${CLAUDE_PLUGIN_ROOT}" --cowork "$COWORK" --update-auto-deploy
```

#### --all
Executar todas as acoes acima em sequencia.

### 3. Reportar

Para cada operacao:
- Mostrar arquivo afetado.
- Classificar: **ATUALIZADO / INALTERADO / CRIADO / PULADO (manual)**.
- Em `--dry-run`: mostrar o diff proposto sem aplicar.

### 4. Integracao

- Apos atualizar com sucesso, sugerir `/cowork-doctor` se houve mudanca estrutural relevante.
- Apos `--fingerprint`, AUTO-DEPLOY.md fica sincronizado — `/cowork-sync` deve reportar sem divergencia.

## PROIBICOES

- NUNCA sobrescrever `persona.md` ou `MEMORY.md` manuais sem `--force`.
- NUNCA aplicar mudancas fora do COWORK alvo.
- NUNCA invocar `git` automaticamente.
- NUNCA aplicar `--force` silenciosamente — sempre mostrar quais arquivos serao sobrescritos antes.

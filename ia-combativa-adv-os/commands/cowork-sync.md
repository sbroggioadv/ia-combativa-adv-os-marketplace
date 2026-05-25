---
description: Controla a skill cowork-sync (fingerprint multi-dispositivo). Flags --status, --diff, --refresh, --mute, --unmute.
allowed-tools: Bash, Read, Edit, Write
---

Voce foi acionado pelo comando `/cowork-sync`. Dispatch a flag passada.

**Regra importante:** `cowork-sync` e skill **invariante** — nao pode ser removida permanentemente. Este comando controla operacao + escape session-only.

## FLAGS SUPORTADAS

- `--status` (ou sem flag) — mostra estado resumido, se ha divergencia.
- `--diff` — mostra diferencas detalhadas entre baseline e estado atual (JSON bonito).
- `--refresh` — aceita o plugin atual como novo baseline. Atualiza `<COWORK>/.dev-adv/AUTO-DEPLOY.md`.
- `--mute` — silencia avisos automaticos de divergencia ate o fim da sessao.
- `--unmute` — reativa avisos automaticos na sessao atual.

## PROTOCOLO

### 1. Localizar COWORK

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/find-cowork.py"
```
Se nao encontrar: "Nenhum workspace COWORK. Rode `/start` primeiro."

Guardar como `$COWORK`.

### 2. Dispatch

#### `--status` (default)

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/fingerprint.py" \
  --plugin-root "${CLAUDE_PLUGIN_ROOT}" \
  --cowork "$COWORK" \
  --diff
```

Parsear JSON e mostrar resumo:
```
COWORK-SYNC — Status
  Baseline AUTO-DEPLOY.md: 2026-04-15T10:00Z
  Plugin atual:            2026-04-17T14:25Z
  Divergencia:             3 modificadas, 2 adicionadas, 0 removidas
  Session mute:            [ ] off

Acao sugerida:
  /cowork-sync --diff      (inspecionar detalhes)
  /cowork-sync --refresh   (aceitar baseline atual)
```

Se nao houver divergencia:
```
COWORK-SYNC — Status
  Baseline AUTO-DEPLOY.md: 2026-04-17T14:25Z
  Plugin atual:            2026-04-17T14:25Z
  Divergencia:             nenhuma — em sincronia
```

#### `--diff`

Rodar o mesmo script com `--diff` e mostrar o JSON inteiro em bloco de codigo + interpretacao. Para cada item em `modified`, mostrar:
- Nome da skill.
- SHA256 baseline vs atual.
- Sugestao: `git log -- skills/<nome>/SKILL.md` para ver o que mudou (executar APENAS se o mentorado confirmar).

#### `--refresh`

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/fingerprint.py" \
  --plugin-root "${CLAUDE_PLUGIN_ROOT}" \
  --cowork "$COWORK" \
  --update-auto-deploy
```

Reportar:
```
[cowork-sync] AUTO-DEPLOY.md atualizado.
Baseline atual:       2026-04-17T14:25Z
Proxima verificacao:  SessionStart da proxima sessao
```

#### `--mute`

Set flag no state:
```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/state.py" set "$COWORK" preferences.cowork_sync_session_muted true
```
Reportar:
```
[cowork-sync] Avisos de divergencia silenciados ate fim da sessao.
Para reativar agora: /cowork-sync --unmute
```

#### `--unmute`

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/state.py" set "$COWORK" preferences.cowork_sync_session_muted false
```
Reportar "[cowork-sync] Avisos reativados."

## CENARIO TIPICO MULTI-DISPOSITIVO

1. Mentorado no **desktop** roda `git pull` no clone do plugin → atualiza para versao nova.
2. Na proxima sessao do desktop, SessionStart detecta divergencia e avisa:
   ```
   [cowork-sync] Divergencia em 3 skills. Rode /cowork-sync para detalhes.
   ```
3. Mentorado roda `/cowork-sync --diff`, ve o que mudou, e depois `/cowork-sync --refresh` para aceitar baseline.
4. Uma semana depois, mentorado abre o **notebook**. SessionStart detecta que AUTO-DEPLOY.md do notebook ainda esta com baseline antigo → avisa de novo.
5. Mentorado roda `git pull` no notebook tambem, depois `/cowork-sync --refresh`.

**A skill NUNCA puxa git automaticamente.** Acao sempre manual do mentorado — preserva controle + auditoria.

## PROIBICOES

- NUNCA executar `git pull` ou `git checkout` automaticamente.
- NUNCA remover AUTO-DEPLOY.md sem confirmacao.
- NUNCA sobrescrever AUTO-DEPLOY.md com `--refresh` se houver uncommitted changes no clone do plugin (avisar primeiro).
- NUNCA processar COWORK de outro mentorado.

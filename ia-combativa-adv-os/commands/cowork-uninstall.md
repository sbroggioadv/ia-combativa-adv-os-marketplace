---
description: Desinstala o plugin Ia Combativa-Adv-OS. PRESERVA o COWORK (pasta de trabalho do usuario) e seus dados. Imprime comandos para o usuario rodar — nunca apaga automaticamente sem confirmacao dupla.
allowed-tools: Bash, Read
---

Voce foi acionado pelo comando `/cowork-uninstall`. Conduza o usuario pela remocao do plugin. **O COWORK e sempre preservado** — apenas o plugin e removido da instalacao do Claude Code.

## PROTOCOLO

### 1. Aviso inicial

```
COWORK-UNINSTALL — Remocao do plugin Ia Combativa-Adv-OS

O QUE SERA REMOVIDO:
  - Clone local do plugin (~/dev/plugins/ia-combativa-adv-os/ ou onde instalado)
  - Entrada do plugin em ~/.claude/plugins/
  - Hook SessionStart + PostToolUse + UserPromptSubmit + PreCompact
  - Comandos /start, /cowork-* (deixam de estar disponiveis)

O QUE SERA PRESERVADO (INTOCADO):
  ✓ Pasta COWORK do usuario (<cowork_path>)
  ✓ Todos os dados em <COWORK>/<areas>/
  ✓ persona.md, MEMORY.md de cada area, snapshots
  ✓ cron jobs registrados no OS (voce precisa remover manualmente se quiser)
  ✓ Qualquer arquivo em <COWORK>/.dev-adv/ (state, pending, backups)

Voce confirma a desinstalacao? (s/n)
```

Se `n`, abortar.
Se `s`, seguir.

### 2. Listar cron jobs a remover (opcional)

Listar tarefas registradas em `state.automations.*.enabled = true` e gerar os comandos de remocao por plataforma:

**Windows:**
```powershell
schtasks /delete /tn "ia-combativa-<task_id>" /f
```

**macOS:**
```bash
launchctl unload ~/Library/LaunchAgents/com.ia-combativa.<task_id>.plist
rm ~/Library/LaunchAgents/com.ia-combativa.<task_id>.plist
```

**Linux:**
```bash
crontab -l | grep -v "ia-combativa-<task_id>" | crontab -
```

Avisar:
```
[cowork-uninstall] Detectei N tarefas agendadas registradas. Execute os comandos acima ANTES de prosseguir — o plugin nao remove crons automaticamente.

Confirmado que removeu (ou nao ha crons)? (s/n)
```

### 3. Remover configuracao local

Imprimir (NAO executar):
```bash
# Remover entrada do plugin de ~/.claude/plugins/
# (ou onde quer que tenha sido instalado via `/plugin install`)
# Verificar primeiro o path exato:
ls ~/.claude/plugins/ | grep ia-combativa-adv-os

# Se instalado via path local, remover:
/plugin remove ia-combativa-adv-os
```

### 4. Opcao: remover tambem settings.local.json do workspace

Se o workspace atual tem `.claude/settings.local.json` com env `COWORK_PERSONA`, oferecer:

```
Detectei .claude/settings.local.json neste workspace apontando para {{COWORK_PERSONA}}.
Remover esse arquivo? (s/n)
  [s] remove o arquivo (pode afetar outros plugins se houver)
  [n] deixa intacto (recomendado se nao tem certeza)
```

### 5. Opcao: remover clone local do repo

```bash
# Se clonou o plugin em um path local (ex: ~/dev/plugins/ia-combativa-adv-os):
rm -rf ~/dev/plugins/ia-combativa-adv-os
```

**Dupla confirmacao necessaria:**
```
ATENCAO: voce tem certeza que quer deletar ~/dev/plugins/ia-combativa-adv-os?
  [s] deletar
  [n] preservar (recomendado — permite reinstalar sem reclone)
```

### 6. Confirmacao final

```
[cowork-uninstall] Plugin desinstalado.

Seu COWORK permanece intocado em:
  {{COWORK_PATH}}

Para reinstalar no futuro:
  1. Clonar o repo: git clone <url>
  2. /plugin install <path-do-clone>
  3. /start (vai detectar o state existente e retomar)

Obrigado por usar o Plugin Ia Combativa-Adv-OS.
```

## PROIBICOES

- NUNCA apagar arquivos do COWORK.
- NUNCA remover clone do plugin sem confirmacao DUPLA.
- NUNCA remover cron jobs silenciosamente — sempre mostrar os comandos.
- NUNCA remover `.claude/settings.local.json` sem confirmacao.
- NUNCA executar `rm -rf` em path que nao foi explicitamente confirmado pelo usuario.

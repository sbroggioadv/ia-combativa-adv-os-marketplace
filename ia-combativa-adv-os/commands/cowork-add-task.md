---
description: Wizard para registrar uma tarefa agendada (cron) no ambiente do usuario. Oferece os 8 templates incluidos + custom. NUNCA registra cron automaticamente — sempre imprime o comando para o usuario rodar.
allowed-tools: Bash, Read
---

Voce foi acionado pelo comando `/cowork-add-task`. Conduza o usuario pela selecao + configuracao de uma tarefa agendada.

**Regra inviolavel:** este comando NAO executa `schtasks`, `launchctl load`, `crontab -e` automaticamente — apenas **imprime o comando que o usuario deve rodar manualmente**. Isso preserva auditoria + controle.

## PROTOCOLO

### 1. Listar templates disponiveis

Ler `${CLAUDE_PLUGIN_ROOT}/templates/scheduled-tasks/*.md.tpl` e extrair frontmatter YAML de cada (campos: task_id, display_name, description, cron_default, opt_in, requires_connectors, requires_tools).

Mostrar menu:

```
TAREFAS AGENDADAS DISPONIVEIS

Ativas por default (recomendadas):
  [1] relatorio-semanal         Relatorio Executivo da Semana       (cron: 0 8 * * 1)
  [2] atualizacao-memoria       Consolidacao semanal de MEMORY.md   (cron: 0 22 * * 0)
  [3] cowork-sync-diario        Checagem diaria multi-dispositivo   (cron: 0 8 * * *)

Opt-in (selecione conforme uso):
  [4] daily-skills-tracker      Rastreio diario de uso de skills    (cron: 0 8 * * *)
  [5] monday-marketing-pipeline Pipeline de conteudo segunda-feira  (cron: 0 14 * * 1)
       requer: skill `marketing-juridico` ativa
  [6] dashboard-data-refresh    Refresh diario de dashboards         (cron: 0 7 * * *)
  [7] email-triage              Triagem diaria de email              (cron: 0 8 * * *)
       requer: conector gmail OU microsoft-outlook
       ATENCAO LGPD: leitura de email — requer aceite explicito
  [8] meeting-triage            Triagem de reunioes pos-transcricao  (cron: */30 * * * *)
       requer: tools.transcricao_reunioes (LOCAL, nunca cloud)

Custom:
  [9] Definir tarefa propria (prompt livre + cron)

[0] Cancelar
```

### 2. Validar pre-requisitos

Apos o usuario escolher, ler o state e validar:
- Se `requires_connectors` especificado, conferir se esta em `connectors.available`.
- Se `requires_skills` especificado, conferir se esta em `skills.invariants + skills.opt_in_active`.
- Se `requires_tools` especificado, conferir se o campo correspondente em `tools` esta preenchido (nao null).

Se algum pre-req nao atende, oferecer correcao guiada:
- Conector faltando → instrucoes para ativar via Claude.ai + `/start --update`.
- Skill opt-in faltando → oferecer `/cowork-add-skill <nome>`.
- Ferramenta faltando → oferecer `/cowork-set tools.<campo> "<nome>"`.

Se warning LGPD obrigatorio (email-triage, meeting-triage), mostrar o texto integral do warning + pedir aceite explicito via flag em `preferences`.

### 3. Confirmar cron

Mostrar o cron default do template e perguntar se usuario aceita ou quer customizar.

Traduzir cron para linguagem natural: `0 8 * * 1` → "Toda segunda-feira as 08:00".

### 4. Imprimir comando para rodar

Detectar plataforma (Win/Mac/Linux via `python -c "import platform; print(platform.system())"`) e imprimir o comando correspondente:

**Windows (Task Scheduler):**
```powershell
# Copie e cole no PowerShell como ADMIN:
schtasks /create ^
  /tn "ia-combativa-<task_id>" ^
  /tr "cd /d <cowork_path> && claude --prompt \"@${CLAUDE_PLUGIN_ROOT}/templates/scheduled-tasks/<task_id>.md.tpl\"" ^
  /sc <schedule> /st <time> /d <day-if-weekly>
```

**macOS (launchd):**
```bash
# Criar plist em ~/Library/LaunchAgents/com.ia-combativa.<task_id>.plist
cat > ~/Library/LaunchAgents/com.ia-combativa.<task_id>.plist <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>com.ia-combativa.<task_id></string>
  <key>ProgramArguments</key>
  <array>
    <string>/bin/sh</string>
    <string>-c</string>
    <string>cd <cowork_path> && claude --prompt "@${CLAUDE_PLUGIN_ROOT}/templates/scheduled-tasks/<task_id>.md.tpl"</string>
  </array>
  <key>StartCalendarInterval</key><dict>
    <!-- ajustar conforme cron escolhido -->
  </dict>
</dict>
</plist>
EOF
launchctl load ~/Library/LaunchAgents/com.ia-combativa.<task_id>.plist
```

**Linux:**
```bash
# Adicionar a crontab:
(crontab -l 2>/dev/null; echo "<cron_schedule> cd <cowork_path> && claude --prompt '@${CLAUDE_PLUGIN_ROOT}/templates/scheduled-tasks/<task_id>.md.tpl'") | crontab -
```

### 5. Registrar no state

Apos o usuario confirmar que rodou o comando, registrar em `state.json`:

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/state.py set <cowork> automations.<task_id>.enabled true
python ${CLAUDE_PLUGIN_ROOT}/scripts/state.py set <cowork> automations.<task_id>.cron "<cron>"
```

Isso permite que `cowork-doctor` conferir depois se o cron esta realmente registrado no OS.

### 6. Custom task (opcao 9)

Se usuario escolheu custom:
1. Perguntar nome da tarefa (sera usado como task_id — validar formato kebab-case).
2. Perguntar prompt livre (pode referenciar placeholders da persona).
3. Perguntar cron.
4. Criar arquivo em `<COWORK>/.dev-adv/custom-tasks/<task_id>.md` (NAO no plugin — evita contaminar repo com dados do usuario).
5. Imprimir comando de cron apontando para esse arquivo.
6. Registrar em state como o item 5.

## PROIBICOES

- NUNCA executar `schtasks`, `launchctl`, `crontab` automaticamente.
- NUNCA habilitar email-triage ou meeting-triage sem aceite explicito do warning LGPD.
- NUNCA permitir transcricao cloud em meeting-triage.
- NUNCA escrever tarefa custom dentro do plugin — sempre em `<COWORK>/.dev-adv/custom-tasks/`.

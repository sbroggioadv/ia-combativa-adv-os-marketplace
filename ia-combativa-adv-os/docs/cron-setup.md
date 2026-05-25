# Cron Setup — Tarefas Agendadas por Plataforma

Guia para registrar cron jobs em Windows, macOS e Linux para as 8 tarefas agendadas do plugin.

**Regra central:** o comando `/cowork-add-task` **imprime** o comando para voce rodar. **Nunca** executa automaticamente. Isso preserva auditoria + controle + reversibilidade.

---

## Windows — Task Scheduler

### Via linha de comando (schtasks)

**Tarefa diaria as 08:00:**
```powershell
schtasks /create ^
  /tn "ia-combativa-<task_id>" ^
  /tr "cd /d <cowork_path> && claude --prompt \"@<path-to-template>\"" ^
  /sc daily /st 08:00
```

**Tarefa semanal (segunda-feira 08:00):**
```powershell
schtasks /create ^
  /tn "ia-combativa-<task_id>" ^
  /tr "cd /d <cowork_path> && claude --prompt \"@<path-to-template>\"" ^
  /sc weekly /d MON /st 08:00
```

**Tarefa a cada 30 minutos:**
```powershell
schtasks /create ^
  /tn "ia-combativa-<task_id>" ^
  /tr "cd /d <cowork_path> && claude --prompt \"@<path-to-template>\"" ^
  /sc minute /mo 30
```

### Via GUI

`Win + R` → `taskschd.msc` → Create Basic Task → seguir wizard.

### Listar tarefas do plugin

```powershell
schtasks /query /tn "ia-combativa-*"
```

### Remover tarefa

```powershell
schtasks /delete /tn "ia-combativa-<task_id>" /f
```

---

## macOS — launchd

### Criar plist

Criar arquivo em `~/Library/LaunchAgents/com.ia-combativa.<task_id>.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.ia-combativa.<task_id></string>

  <key>ProgramArguments</key>
  <array>
    <string>/bin/sh</string>
    <string>-c</string>
    <string>cd <cowork_path> && claude --prompt "@<path-to-template>"</string>
  </array>

  <key>StartCalendarInterval</key>
  <dict>
    <key>Hour</key><integer>8</integer>
    <key>Minute</key><integer>0</integer>
    <!-- Para semanal, adicionar: -->
    <!-- <key>Weekday</key><integer>1</integer>  (1=segunda) -->
  </dict>

  <key>StandardOutPath</key>
  <string><cowork_path>/.dev-adv/.logs/launchd-<task_id>.log</string>
  <key>StandardErrorPath</key>
  <string><cowork_path>/.dev-adv/.logs/launchd-<task_id>.err</string>
</dict>
</plist>
```

### Carregar

```bash
launchctl load ~/Library/LaunchAgents/com.ia-combativa.<task_id>.plist
```

### Verificar se esta ativo

```bash
launchctl list | grep ia-combativa
```

### Remover

```bash
launchctl unload ~/Library/LaunchAgents/com.ia-combativa.<task_id>.plist
rm ~/Library/LaunchAgents/com.ia-combativa.<task_id>.plist
```

---

## Linux — crontab

### Adicionar

```bash
crontab -e
```

Inserir linha no formato cron padrao:
```
0 8 * * 1  cd <cowork_path> && claude --prompt '@<path-to-template>'  # ia-combativa-relatorio-semanal
0 22 * * 0  cd <cowork_path> && claude --prompt '@<path-to-template>'  # ia-combativa-atualizacao-memoria
0 8 * * *  cd <cowork_path> && claude --prompt '@<path-to-template>'  # ia-combativa-cowork-sync-diario
```

### Listar

```bash
crontab -l | grep ia-combativa
```

### Remover uma linha especifica

```bash
crontab -l | grep -v "ia-combativa-<task_id>" | crontab -
```

---

## Tabela de referencia — as 8 tarefas

| Task ID | Cron default | Descricao | Plataforma (windows schtasks) |
|---|---|---|---|
| relatorio-semanal | `0 8 * * 1` | Segunda 08:00 | `/sc weekly /d MON /st 08:00` |
| atualizacao-memoria | `0 22 * * 0` | Domingo 22:00 | `/sc weekly /d SUN /st 22:00` |
| cowork-sync-diario | `0 8 * * *` | Diario 08:00 | `/sc daily /st 08:00` |
| daily-skills-tracker | `0 8 * * *` | Diario 08:00 | `/sc daily /st 08:00` |
| monday-marketing-pipeline | `0 14 * * 1` | Segunda 14:00 | `/sc weekly /d MON /st 14:00` |
| dashboard-data-refresh | `0 7 * * *` | Diario 07:00 | `/sc daily /st 07:00` |
| email-triage | `0 8 * * *` | Diario 08:00 | `/sc daily /st 08:00` |
| meeting-triage | `*/30 * * * *` | A cada 30min | `/sc minute /mo 30` |

---

## Verificacao apos registro

Depois de registrar qualquer cron, rode:

```
/cowork-doctor
```

Entre os 17 checks, ele lista as tarefas declaradas em `state.automations` e reporta se encontrou o cron correspondente no OS (com ressalva: no Mac/Linux, isso requer permissoes de leitura do crontab/launchctl).

---

## Variaveis importantes

- `<cowork_path>` — substituir pelo path absoluto do seu COWORK.
- `<path-to-template>` — substituir pelo path absoluto do template:
  - Windows: `C:\Users\<user>\dev\plugins\Plugin-Ia-Combativa-Adv-OS\templates\scheduled-tasks\<task_id>.md.tpl`
  - Mac/Linux: `$HOME/dev/plugins/Plugin-Ia-Combativa-Adv-OS/templates/scheduled-tasks/<task_id>.md.tpl`
- `<task_id>` — um dos 8 IDs da tabela acima (ou custom).

---

## Logs e debug

Recomendamos redirecionar stdout/stderr de cada tarefa para logs locais:

- **Windows:** Task Scheduler → aba "History" do task; ou redirecionar no comando com `> <path> 2>&1`.
- **macOS:** campos `StandardOutPath` e `StandardErrorPath` no plist (ver exemplo acima).
- **Linux:** `MAILTO=""` no topo do crontab + append ` >> <path> 2>&1` em cada linha.

Os logs vao idealmente para `<COWORK>/.dev-adv/.logs/` (ja gitignored por padrao).

---
description: Inicia o onboarding do workspace COWORK ou atualiza configuracao existente.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
argument-hint: [--update] [--skills] [--areas]
---

Voce foi acionado pelo comando `/start` do plugin Ia Combativa-Adv-OS.

Argumento recebido: `$ARGUMENTS`

**Objetivo:** conduzir o usuario pelo wizard de onboarding do workspace COWORK, coletar respostas estruturadas, e gerar toda a estrutura operacional via `scripts/render.py`.

## PROTOCOLO DE EXECUCAO

### 1. Acionar a skill `cowork-onboarding`

**IMPORTANTE:** Use Skill(skill="cowork-onboarding") imediatamente. Ela contem o fluxo completo do wizard e TODAS as perguntas a fazer ao usuario. Este comando `/start` e apenas o trigger — a logica vive na skill.

### 2. Parsear argumentos

- Sem argumento → wizard completo (primeira instalacao ou reinicio)
- `--update` → re-executar wizard mantendo respostas anteriores como defaults
- `--skills` → rodar apenas a secao de selecao de skills
- `--areas` → rodar apenas a secao de selecao de areas

Passe esse modo para a skill `cowork-onboarding` ao aciona-la.

### 3. Se o usuario ja tem state configurado

Antes de sobrescrever: ler `${CLAUDE_PLUGIN_ROOT}` nao se aplica aqui — buscar cowork-state.json via:
1. Env var `COWORK_PATH` se existir
2. `<CWD>/.dev-adv/cowork-state.json`
3. `<CWD>/.claude/settings.local.json` → campo `env.COWORK_PATH`

Se encontrado, informar ao usuario:

> "Encontrei configuracao existente em `<path>`. Firma: `<firm_name>`. Areas ativas: `<N>`. Quer (a) continuar de onde parou, (b) atualizar configuracao, ou (c) criar nova COWORK em outro diretorio?"

### 4. Produtos esperados ao final do wizard

Apos o wizard, os seguintes arquivos devem existir no COWORK do usuario:

- `<COWORK>/.dev-adv/cowork-state.json` (state completo)
- `<COWORK>/.dev-adv/persona.md` (identidade gerada)
- `<COWORK>/CLAUDE.md` (workspace)
- `<COWORK>/MEMORY.md` (memoria do workspace)
- `<COWORK>/<AREA>/CLAUDE.md` para cada area ativada
- `<COWORK>/<AREA>/MEMORY.md` idem
- `<COWORK>/<AREA>/<subfolders>/` (Clientes, Processos, Modelos, Pesquisas, Pareceres)
- `<workspace>/.claude/settings.local.json` apontando `COWORK_PERSONA` para a persona gerada

Tudo isso e criado pelo `python scripts/render.py <COWORK>` apos o wizard popular o state.

### 5. Encerramento

Ao terminar, apresentar resumo:

```
Workspace COWORK configurado!

Escritorio: <firm_name>
Titular: <advogado_nome>
Areas ativas: <N>
Skills ativas: <N> invariantes + <M> opt-in
Suprema Corte: <ATIVA/DESATIVADA>

Proximos passos:
1. Reiniciar a sessao do Claude Code (o hook SessionStart passara a injetar sua persona)
2. Comecar a trabalhar em uma das pastas de area criadas
3. Rode `/cowork-status` a qualquer momento para ver estado atual
```

**Skill a acionar:** `cowork-onboarding`.

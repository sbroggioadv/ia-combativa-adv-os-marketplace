# CLAUDE.md — Plugin Ia Combativa-Adv-OS

> Instruções para futuras sessões neste repositório. Ler PRIMEIRO ao retomar trabalho aqui.

---

## Identidade do Projeto

- **Nome:** Plugin Ia Combativa-Adv-OS
- **Slug:** `ia-combativa-adv-os`
- **Tipo:** plugin oficial do Claude Code (`.claude-plugin/plugin.json`)
- **Audiência:** advogados que estão começando a usar IA na advocacia
- **Repo:** https://github.com/sbroggioadv/Plugin-Ia-Combativa-Adv-OS

---

## ⚠️ REGRA DE OURO — DESPERSONALIZAÇÃO ABSOLUTA

**Este plugin é 100% standard/neutro.** Como se fosse um download genérico da internet.

**ZERO menções permitidas:**
- Nome do criador da mentoria
- Nome do escritório-modelo de origem
- OAB original (número e UF)
- Email/contato pessoal
- Dados de clientes (reais ou fictícios identificáveis)
- Ferramentas proprietárias usadas pelo escritório-modelo ([sistema de gestao processual], [transcritor de reunioes], [CRM do escritorio], [provedor de email], [banco/PSP do escritorio], [provedor de infra], [processador de pagamentos], etc.) — todas viram **slots de extensão genéricos**
- Apelidos pessoais (Mentor, etc.)
- Padrões nomeados pessoalmente ("Padrão do Escritório", etc.)

**Defesa em profundidade:**

```bash
# Antes de CADA commit
bash audit/audit-script.sh

# Configure pre-commit hook
ln -sf ../../audit/audit-script.sh .git/hooks/pre-commit
chmod +x audit/audit-script.sh
```

Catálogo completo de termos proibidos: `audit/forbidden-terms.json`.

**Exceção única:** URLs do GitHub (`https://github.com/sbroggioadv/Plugin-Ia-Combativa-Adv-OS`) são permitidas — workspace de publicação. Nome do org no path é **infraestrutura**, não conteúdo.

---

## Regra Inviolável Adicional — Pasta Fonte Externa é READ-ONLY

Existe uma pasta de referência externa ao repo (configurada localmente no ambiente de desenvolvimento) que serve como base de extração de skills. Esta pasta é **READ-ONLY ABSOLUTO** durante o desenvolvimento:

**Permissão:** LER tudo, livremente, para extrair conteúdo.
**Proibição absoluta:** ESCREVER NADA. Nem criar, nem modificar, nem deletar. Nem mesmo rodar scripts com output nessa pasta.

Se precisar testar contra a fonte real, copie arquivos relevantes para `_sandbox/` neste repo (gitignored).

---

## Como Retomar Trabalho

1. **Ler `MEMORY.md`** (raiz deste repo) — estado executivo, sprint ativa, próximo passo
2. **Ler `.planning/DECISIONS.md`** — overlay autoritativo das decisões finais (sobrescreve docs antigos)
3. **Ler `.planning/PLAN.md` seção 2** se precisar revisar visão arquitetural
4. **Ler `.planning/ROADMAP.md`** para saber onde estamos no plano
5. **`git status` + `git log -5`** para estado real do repo
6. **`bash audit/audit-script.sh`** para verificar despersonalização

## Para criar/atualizar plugins Cowork (Claude Desktop)

**Sempre** consultar primeiro: **`.planning/COWORK-PUBLISHING-GUIDE.md`** — manual canônico com todos os limites técnicos descobertos via decompile do app.asar (description ≤ 1024 chars, SKILL.md ≤ 11 KB, constraint UNIQUE no nome, whitelist unicode, pipeline de build, troubleshooting). Aplica-se a este plugin pai E a qualquer plugin derivado em `plugins-adicionais/`.

---

## Arquitetura em Uma Frase

**Plugin único estável** (atualizado via `git pull`) com **23 skills extraídas + 3 novas** (`cowork-onboarding`, `cowork-sync`, `memory-evolver`), onde **placeholders `{{...}}` ficam literais nas skills do plugin** e a resolução acontece **em runtime pelo LLM**, que lê o contexto YAML da persona **local do usuário** (em `<COWORK>/.dev-adv/persona.md`, injetada via hook SessionStart).

---

## Padrões a Seguir

### 1. Privacidade é inegociável (LGPD/sigilo profissional)

- Toda pasta `<COWORK>/` do usuário é gitignored por default
- Warning LGPD obrigatório se usuário escolher pasta sincronizada (<sincronizador>/OneDrive/Dropbox/Google Drive)
- Transcrição de áudio APENAS local (faster-whisper) — nunca cloud
- MCPs externos (Gmail, Calendar, etc.) sempre opt-in com warning

### 2. Despersonalização é bloqueante (audit antes de cada release)

```bash
bash audit/audit-script.sh
```

Zero matches em `audit/forbidden-terms.json` = OK. Qualquer match bloqueia release.

### 3. Idempotência sempre

`/start` rodado 2x, 10x, 100x deve produzir mesmo estado coerente. Nunca duplicar, nunca corromper. Testar obrigatoriamente em S1.

### 4. Portabilidade Win + Mac + Linux

- Scripts em bash (Git Bash no Windows)
- Python 3.11+ preferido; fallback bash documentado
- `${CLAUDE_PLUGIN_ROOT}` em TODOS os paths de hook
- `${COWORK_PERSONA}` env var resolvida em runtime via fallback chain

### 5. Skills no formato canônico Anthropic

Apenas `SKILL.md` com frontmatter YAML:

```markdown
---
name: firm-master
description: >
  Descrição longa com keywords de ativação...
---

# Conteúdo da skill...
```

Não criar SKILL.md + CLAUDE.md + memory.md por skill — usar formato simples Anthropic.

### 6. Placeholders literais nas skills

`{{PLACEHOLDER}}` permanecem LITERAIS no disco. Resolução pelo LLM usando YAML de contexto na persona injetada. **Não há render.py reescrevendo skills no install.**

Catálogo de placeholders em `.planning/EXTRACTION-PLAN.md` e `.planning/TEMPLATING-SYSTEM.md`.

Templates QUE são renderizados no disco (uma vez, no `/start`):
- `templates/persona.md.tpl` → `<COWORK>/.dev-adv/persona.md`
- `templates/cowork-CLAUDE.md.tpl` → `<COWORK>/CLAUDE.md`
- `templates/area-CLAUDE.md.tpl` → `<COWORK>/<area>/CLAUDE.md`
- `templates/AUTO-DEPLOY.md.tpl` → `<COWORK>/.dev-adv/AUTO-DEPLOY.md`
- `templates/settings-local.json.tpl` → `<workspace>/.claude/settings.local.json`

### 7. Hooks anti-flap obrigatórios

Todo hook que modifica arquivo deve ter:
- Debouncing (não dispara se alvo modificado nos últimos 60s)
- Filter por path (só dispara em paths dentro de COWORK conhecida)
- Skip em diffs triviais (<50 chars)

### 8. Hook SessionStart é o coração da personalização

```bash
cat ${COWORK_PERSONA}
```

`${COWORK_PERSONA}` resolvido em runtime via fallback chain (env var → `settings.local.json` → `~/.config/dev-adv/active-cowork.json` → `context/persona-fallback.md`).

Esta inversão viabiliza o caminho arquitetural híbrido C+. NÃO alterar sem ADR novo.

### 9. Commits semânticos com marcador de sprint

```
chore(s0): bootstrap inicial do plugin
feat(s1): /start funcional end-to-end [S1/FASE5]
feat(s2): extração firm-master despersonalizada [S2/FASE1]
fix(hooks): anti-flap em post-edit-evolve-memory [S3/FASE2]
chore(release): v1.0.0 [S4/FASE5]
```

### 10. Sempre atualizar MEMORY.md ANTES de push

Ordem obrigatória:
1. Editar `MEMORY.md` (raiz) — estado, sprint, próximo passo
2. Rodar `bash audit/audit-script.sh` (deve passar)
3. `git add`
4. `git commit` semântico
5. `git push`

---

## Decisões Cravadas (referência rápida)

Ver `.planning/DECISIONS.md` para detalhe completo.

| ID | Decisão |
|---|---|
| D1 | Nome `Plugin Ia Combativa-Adv-OS`, slug `ia-combativa-adv-os` |
| D2 | Repo privado, MIT |
| D3 | Tom `tecnico-combativo` default + adaptação dinâmica (NÃO 4 perfis fixos) |
| D4 | Todas áreas no plugin (wizard escolhe). 5 skills invariantes (firm-master + 4 Suprema Corte) + 18 opt-in |
| D5 | Suprema Corte default-on com bypass (`--no-corte`, `/corte off`) |
| **REGRA DE OURO** | Despersonalização absoluta. Zero menções pessoais. Audit obrigatório antes de cada commit. |

---

## Proibições

1. **NÃO** começar a implementar Sprint sem autorização (ou gatilho explícito `CTO orquestre Sprint X`)
2. **NÃO** incluir voz, identidade, OAB, nome, marca, ferramentas ou padrões pessoais do criador da mentoria nas skills (audit obrigatório bloqueia)
3. **NÃO** publicar em marketplace público antes de v1.0 GA com métricas
4. **NÃO** habilitar MCP externo por default (sempre opt-in com warning LGPD)
5. **NÃO** fazer transcrição cloud — sempre local
6. **NÃO** pular pause entre sprints
7. **NÃO** sobrescrever customização do usuário sem perguntar
8. **NÃO** escrever em pastas de fonte externa READ-ONLY
9. **NÃO** colocar persona renderizada DENTRO do plugin instalado — vive em `<COWORK>/.dev-adv/persona.md`
10. **NÃO** incluir ferramentas específicas do escritório-modelo no plugin — usar slots de extensão genéricos
11. **NÃO** criar SKILL.md + CLAUDE.md + memory.md por skill (usar apenas SKILL.md com frontmatter)
12. **NÃO** alterar nome do plugin sem nova decisão

---

## Estrutura do Repo

```
Plugin-Ia-Combativa-Adv-OS/
├── .claude-plugin/
│   └── plugin.json              # Manifest oficial
├── .planning/                    # Planejamento mestre (9 docs)
├── commands/                     # Slash commands (S1)
├── skills/                       # 23 skills extraídas + 3 novas (S2)
├── hooks/                        # SessionStart + PostToolUse + UserPromptSubmit (S1+S3)
├── context/                      # persona-fallback.md (S1)
├── templates/                    # .tpl renderizados no /start (S1+S2)
├── scripts/                      # render.py, fingerprint.py, gerar_docx.py (S1+S2+S3)
├── audit/                        # forbidden-terms.json + audit-script.sh
├── README.md
├── LICENSE                       # MIT
├── .gitignore                    # LGPD-aware
├── CLAUDE.md                     # este arquivo
└── MEMORY.md                     # estado executivo
```

---

## Comunicação

- **Idioma:** Português (Brasil)
- **Tom dos docs internos:** técnico, direto, sem enrolação, **sem identificadores pessoais**
- **Tom das mensagens pro usuário (skills, commands, wizard):** acolhedor, didático, respeita `tom_voz` configurado dinamicamente
- **Reportes:** ✅ concluído / 🔴 erro / 🏁 sprint finalizada

---

## Checklist de Retomada em Nova Sessão

```markdown
- [ ] Li MEMORY.md (raiz)
- [ ] Sei em qual sprint estamos
- [ ] Sei se há pendência aguardando aprovação
- [ ] Conferi DECISIONS.md (sobrescreve docs antigos)
- [ ] Rodei git status / git log -5
- [ ] Rodei bash audit/audit-script.sh (deve passar)
- [ ] Confirmei que NÃO vou escrever em pasta de fonte externa READ-ONLY
- [ ] Se vou tocar em skills: li EXTRACTION-PLAN.md da skill específica
- [ ] Se vou tocar em engine: li TEMPLATING-SYSTEM.md
```

---

**Última atualização:** 2026-04-17 (bootstrap inicial + despersonalização aplicada)

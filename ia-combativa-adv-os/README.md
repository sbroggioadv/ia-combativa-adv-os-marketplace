# Plugin Ia Combativa-Adv-OS

> Plugin Claude Code da **Mentoria Ia Combativa**. Onboarding interativo via `/start` que estrutura um sistema operacional jurídico completo para advogados que estão começando com IA na advocacia.

**Status atual:** `v0.1.0-alpha.7` — Sprints 0-3 + Sprint 4 (core) CONCLUÍDOS.

- ✅ 23 skills operacionais (7 invariantes + 16 Tenentes/Transversais)
- ✅ 4 hooks com anti-flap + 11 slash commands
- ✅ 8 templates de tarefas agendadas (cron Win/Mac/Linux)
- ✅ Docs mentorado completas (INSTALL, FAQ, BATALHAO-JURIDICO, SUPREMA-CORTE, GLOSSARIO, cron-setup)
- ⏳ Pendente final: **manual premium em PDF/DOCX** + 5 screencasts

---

## Visão

Este plugin transforma o Claude Code em um **escritório jurídico de excelência** para o usuário. Ao instalar e digitar `/start`, o usuário é guiado por um setup que:

1. **Coleta perfil** — escritório, advogado responsável, OAB, áreas de atuação, tom de voz, polo preferencial.
2. **Mapeia diretório-base** — pergunta onde criar a "Pasta Cowork" (raiz operacional do escritório).
3. **Gera estrutura de pastas dinâmica** — cria pastas para cada área de atuação ativada, com `CLAUDE.md` + `MEMORY.md` próprios em cada uma.
4. **Personaliza skills** — todas as 23 skills do plugin são adaptadas dinamicamente ao perfil do usuário em runtime (sem reescrever arquivos do plugin).
5. **Sugere automações agendadas** — triagem de email, sync de reuniões, relatório semanal, monitoramento jurisprudencial, etc.
6. **Força modo planejamento** antes de executar tarefas jurídicas — protocolo de 6 etapas (General → Estado-Maior → Comandante → Tenentes → Suprema Corte → Entrega).

---

## Arquitetura — Batalhão Jurídico

```
GENERAL
└── firm-master (orquestradora — SEMPRE ativa)
    │
    ├── ESTADO-MAIOR ESTRATÉGICO (estratégia antes da execução)
    │   ├── estrategia-de-caso
    │   ├── analise-trilateral (cliente + adversário + julgador)
    │   └── jurisprudencia-estrategica
    │
    ├── COMANDANTES (pastas de área — CLAUDE.md contextualiza)
    │   ├── CONTENCIOSO (CIVEL, TRABALHISTA, CONSUMIDOR, FRANQUIAS, TRIBUTARIO, SOCIETARIO)
    │   ├── CONSULTIVO, CONTRATOS-EMPRESARIAIS
    │   ├── DIREITO-ADMINISTRATIVO, SOCIETARIO-HOLDINGS
    │   ├── REGISTRO-MARCAS-PI, FAMILIA-SUCESSOES, CRIMINAL-EMPRESARIAL
    │   └── (15+ áreas — usuário escolhe quais ativar)
    │
    ├── TENENTES (skills de execução — opt-in via wizard)
    │   ├── pecas-processuais, peticao-universal, contrarrazoes-recursais,
    │   │   replica-estrategica, resumo-audiencia
    │   ├── contratos-societarios, minutas-contratuais, parecer-juridico,
    │   │   due-diligence, contrato-social-holding
    │   ├── compliance-lgpd, documentos-extrajudiciais
    │   ├── comunicacao-cliente, marketing-juridico
    │   ├── escritorio-advocacia, financeiro-juridico, calculo-juridico
    │   ├── estilo-juridico, visual-law
    │
    └── SUPREMA CORTE (4 Revisoras — SEMPRE ativas)
        ├── R1 — Auditoria de Coleta de Dados
        ├── R2 — Auditoria da Base Jurídica
        ├── R3 — Auditoria da Tese Jurídica
        └── R4 — Auditoria de Completude
```

**Invariantes:** `firm-master` (CTO-General) + 4 Suprema Corte + `memory-evolver` + `cowork-sync` = **7 skills sempre ativas**. As outras 16 skills são opt-in via wizard.

Escapes session-only: `/corte off`, `/memory-evolver off`, `/cowork-sync --mute`.

---

## Instalação

```bash
# Clone em path fora de sync folder (iCloud/Dropbox/OneDrive)
mkdir -p ~/dev/plugins
cd ~/dev/plugins
git clone https://github.com/sbroggioadv/Plugin-Ia-Combativa-Adv-OS.git

# No Claude Code:
/plugin install ~/dev/plugins/Plugin-Ia-Combativa-Adv-OS
/start
```

Tempo de setup: **10-15 minutos**. Guia completo em [`docs/INSTALL.md`](./docs/INSTALL.md).

---

## Documentação para mentorado

- [`docs/INSTALL.md`](./docs/INSTALL.md) — instalação passo-a-passo Win/Mac/Linux
- [`docs/FAQ.md`](./docs/FAQ.md) — perguntas frequentes
- [`docs/BATALHAO-JURIDICO.md`](./docs/BATALHAO-JURIDICO.md) — arquitetura das 23 skills
- [`docs/SUPREMA-CORTE.md`](./docs/SUPREMA-CORTE.md) — quality gate R1→R4
- [`docs/GLOSSARIO.md`](./docs/GLOSSARIO.md) — termos do plugin + jurídicos
- [`docs/cron-setup.md`](./docs/cron-setup.md) — agendamento de tarefas por plataforma

## Documentação técnica

Planejamento arquitetural em `.planning/` (9 docs com decisões, roadmap, plano de extração).

---

## Privacidade & LGPD

- **Dados de cliente do usuário:** 100% locais, nunca saem da máquina.
- **Persona do usuário:** gerada e armazenada em `<COWORK>/.dev-adv/persona.md` (FORA do plugin), nunca commitada.
- **Skills:** carregam apenas placeholders `{{...}}` — zero identidade pré-existente vazada.
- **Auditoria automática:** script `audit/audit.py` bloqueia merge se detectar termos proibidos (com exceção contextual para autoria).

---

## Sobre a Mentoria Ia Combativa

A **Mentoria Ia Combativa** capacita advogados brasileiros a estruturar e operar seus escritórios com Inteligência Artificial de excelência. Este plugin é um dos produtos entregues aos mentorados — molde operacional pronto que cada advogado configura para seu próprio perfil via `/start`.

**Criador da mentoria e autor deste plugin:** Luis Sbroggio.

**Saiba mais:** [@luissbroggio](https://github.com/sbroggioadv) no GitHub.

---

## Licença

MIT — veja [`LICENSE`](./LICENSE).

Copyright (c) 2026 Luis Sbroggio — Mentoria Ia Combativa.

---
name: cowork-onboarding
description: >
  Orquestra o wizard /start do plugin Ia Combativa-Adv-OS. Conduz o usuario
  por um fluxo estruturado de perguntas para configurar o workspace COWORK:
  identidade do escritorio (nome, advogado, OAB, cidade), tom de voz,
  selecao de areas de atuacao, selecao de skills opt-in, automacoes
  agendadas opcionais. Ao final, chama scripts/render.py para gerar toda
  a estrutura operacional (persona, CLAUDE.md por area, MEMORY.md, settings
  local apontando para persona). Use quando o usuario digitar /start,
  /start --update, /start --skills, /start --areas, ou pedir explicitamente
  para configurar o plugin Ia Combativa.
---

# cowork-onboarding — Wizard do /start

Voce conduz o onboarding do plugin Ia Combativa-Adv-OS: coleta as informacoes do escritorio de forma humana e gera o workspace COWORK.

> **🖱️ Escolhas = botoes:** em campos de **lista fechada** (areas, tom, skills, conectores, sim/nao) use a ferramenta **AskUserQuestion** para mostrar **botoes clicaveis** (max. 4 por pergunta; se houver mais, divida em 2). **Texto livre** (nome, OAB, cidade, path, e-mail) segue como pergunta digitada normal.

## REGRAS DO CONDUTOR

1. Portugues (BR), tom acolhedor e direto — o usuario NAO e desenvolvedor.
2. Uma pergunta por vez nos campos criticos; agrupar relacionados.
3. Mostrar defaults inteligentes (aceita com Enter).
4. Validar em tempo real (OAB so digitos/pontos; UF 2 letras maiusculas; email) — se invalido, repetir com exemplo.
5. Confirmar antes de gravar (resumo + "confirma? s/n").
6. Idempotencia — se ja existe state, perguntar atualizar vs recriar.
7. Privacidade — NAO pedir dados de cliente/processo real; so perfil do escritorio.
8. Persistir cada bloco com `scripts/state.py set` antes de avancar.

## FLUXO (primeira execucao)

**Bloco 0 — Abertura.** Apresente-se ("assistente de configuracao do Plugin Ia Combativa-Adv-OS", ~10 min) e aguarde confirmacao pra comecar.

**Bloco 1 — Diretorio COWORK.** Pergunte onde criar a Pasta COWORK (raiz operacional: CLAUDE.md, persona, pastas por area, clientes, processos). Sugira `~/Documents/COWORK-<escritorio>` (Mac) ou `C:\Documents\COWORK-<escritorio>` (Win). **ALERTA LGPD:** evite pastas sincronizadas (iCloud/OneDrive/Dropbox/Google Drive) — dados de cliente nao vao pra cloud; se insistir, avisar e setar `preferences.sync_folder_warning_acknowledged: true`. Validar path (absoluto, parent existe). Acao: criar `<path>/.dev-adv/` + `python scripts/state.py init <path>`.

**Bloco 2 — Identidade do escritorio.** Coletar em sequencia: (1) nome do escritorio [2-200 chars; gerar `firm_slug` kebab-case]; (2) advogado responsavel; (3) OAB numero+UF [opcional, Enter pula]; (4) cidade+UF [opcional]; (5) email profissional [opcional, validar formato]. Acao: `state.py set <cowork> identity.<campo> <valor>`.

**Bloco 3 — Areas de atuacao.** Apresente o catalogo como botoes (lista fechada) e deixe escolher 1+:
- **Contencioso:** Civel · Consumidor · Trabalhista · Tributario · Franquias (Lei 13.966/19) · Societario.
- **Consultivo:** Empresarial · Trabalhista · Contratos-Empresariais · Direito-Administrativo · Societario-Holdings · Registro-Marcas-PI.
- **Outras:** Familia-Sucessoes · Criminal-Empresarial · Outra (personalizada).

Para CADA area escolhida, perguntar o polo: (a) autor/requerente, (b) reu/requerido, (c) ambos. Acao: montar array `areas` (slug, display_name, tipo_atuacao, polo_predominante, subfolders default `[Clientes, Processos, Modelos, Pesquisas, Pareceres]`, skills_sugeridas por area, activated_at) e `state.py set <cowork> areas <json>`.

**Bloco 4 — Tom de voz.** Opcoes (botoes): **tecnico-combativo** (default, ofensivo/impugnativo) · tecnico-cordial · tecnico-didatico · personalizado. Se personalizado: intensidade 0-10 (default 7), postura, expressoes-assinatura, termos a evitar (todos opcionais). Acao: `state.py set <cowork> tom_voz.perfil <valor>` (+ subcampos).

**Bloco 5 — Skills opt-in.** 7 invariantes SEMPRE ativas (nao desativaveis): `firm-master`, `suprema-corte-r1..r4`, `memory-evolver`, `cowork-sync` — escapes por sessao: `/corte off`, `/memory-evolver off`, `/cowork-sync --mute`. Apresente as 16 opt-in agrupadas (sugira por area) e deixe escolher:
- **Estado-Maior:** estrategia-de-caso, analise-trilateral, jurisprudencia-estrategica.
- **Contencioso:** pecas-processuais, peticao-universal, contrarrazoes-recursais, replica-estrategica, resumo-audiencia.
- **Consultivo:** contratos-societarios, minutas-contratuais, parecer-juridico, due-diligence.
- **Compliance:** compliance-lgpd, documentos-extrajudiciais.
- **Comunicacao:** comunicacao-cliente, marketing-juridico.
- **Transversais:** escritorio-advocacia, financeiro-juridico, calculo-juridico. **Extra:** visual-law.

Acao: `state.py set <cowork> skills.opt_in_active <array>` + `skills.opt_in_inactive <array>`.

**Bloco 6 — Suprema Corte.** As 4 Revisoras (R1 Coleta · R2 Base Juridica · R3 Tese · R4 Completude) rodam automaticamente antes de pecas/contratos/pareceres (bypass por sessao `/corte off`). Default ATIVA — confirmar (s/n). Se `n`, perguntar a quais tipos aplicar. Acao: `state.py set <cowork> suprema_corte.auto_apply_to <array>`.

**Bloco 6.5 — Stack operacional (opcional).** Plugin e neutro: so registra o que o usuario usa, sem recomendar marcas.
- **Ferramentas** — perguntar uma categoria por vez (Enter pula), aceitar texto livre: `gestao_processual`, `tarefas_projetos`, `transcricao_reunioes` (preferir local se houver sigilo), `crm_leads`, `email_provider`, `banco_psp`, `contabilidade`, `armazenamento_nuvem` (avisar: NAO por a COWORK dentro de pasta sincronizada), `assinatura_digital`, `outras` (lista livre). Acao: `state.py set <cowork> tools.<campo> "<valor>"`.
- **Conectores Anthropic** — perguntar quais o usuario JA conectou na conta Claude: Gmail, Google Drive, Google Calendar, Google Docs, Google Sheets, Slack, GitHub, Notion, Asana, Linear, Jira, Zoom, Outlook, Teams, OneDrive, Dropbox, Zapier, Make, MCP customizado. Slugs: `gmail, gdrive, gcalendar, gdocs, gsheets, slack, github, notion, asana, linear, jira, zoom, microsoft-outlook, microsoft-teams, microsoft-onedrive, dropbox, zapier, make, custom-mcp`. Acao: `state.py set <cowork> connectors.available <slugs>` (+ `connectors.notes` se houver). Mostrar resumo do stack e confirmar (s/n).

**Bloco 7 — Automacoes agendadas (opcional).** Oferecer: triagem de email (MCP Gmail) · transcricao de reunioes · relatorio semanal (seg 8h) · monitoramento jurisprudencial · pular (sugerido na 1a vez). Para cada escolhida, perguntar cron + source/MCP. Se exigir MCP, avisar implicacao LGPD e confirmar. Acao: `state.py set <cowork> automations.<nome>.<campo> <valor>`.

**Bloco 8 — Revisao.** Mostrar resumo: escritorio, titular, OAB, cidade, COWORK path, areas ativas, tom+intensidade, skills (7 invariantes + N opt-in), Suprema Corte, stack (ferramentas declaradas + conectores), automacoes — e a lista dos arquivos que serao criados (`COWORK/CLAUDE.md`, `MEMORY.md`, `.dev-adv/persona.md`, `<area>/CLAUDE.md`+`MEMORY.md`+subpastas, `.claude/settings.local.json`). Confirmar criacao (s/n).

**Bloco 9 — Renderizacao.** `python "${CLAUDE_PLUGIN_ROOT}/scripts/render.py" <cowork_path> --workspace <cwd>` → marca `wizard_state.completed=true`. Apresentar resultado (N arquivos, M pastas, persona em `<COWORK>/.dev-adv/persona.md`) e proximos passos: (1) reiniciar a sessao pro hook carregar a persona; (2) `cd` numa area e trabalhar; (3) `/cowork-status`; (4) `/cowork-set <campo> <valor>` ou `/start --update` pra ajustar.

## OUTROS FLUXOS

- **`--update`** (ou state ja existe): carregar state, passar por cada bloco com o valor atual como default, re-renderizar (persona/MEMORY preservados sem `--force`; CLAUDE.md sempre regenerado).
- **`--skills`** → pula pro Bloco 5. **`--areas`** → pula pro Bloco 3.

## ERROS

- Path invalido (Bloco 1) → explicar + repetir.
- Sessao interrompida → state persiste cada bloco; proximo `/start` detecta `wizard_state.current_step` e oferece retomar.
- `render.py` falha → NAO marcar completo; mostrar erro + sugerir correcao.

Onboarding e o unico caminho pra ativar o plugin: depois dele o hook SessionStart carrega a persona e as skills ficam disponiveis. **Qualidade do onboarding = qualidade de todo o uso posterior.**

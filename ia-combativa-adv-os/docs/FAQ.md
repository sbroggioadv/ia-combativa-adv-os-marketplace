# FAQ — Plugin Ia Combativa-Adv-OS

## Instalacao

**P: O plugin funciona sem internet?**
R: Sim, apos a instalacao. Skills usam o LLM do Claude Code — se o Claude Code funciona, o plugin funciona. Apenas `cowork-sync-diario` e automacoes com conectores dependem de internet.

**P: Posso instalar em Windows e Mac simultaneamente?**
R: Sim. Cada maquina tem seu proprio COWORK local (nao sincroniza entre maquinas). A skill `cowork-sync` alerta quando o plugin em uma maquina esta em versao diferente da outra.

**P: Preciso ser advogado pra usar?**
R: O plugin foi desenhado para advogados. Nao-advogados podem instalar, mas skills usam terminologia juridica brasileira e muitas operacoes pressupoem contexto de escritorio.

---

## Configuracao

**P: Posso mudar o tom de voz depois do /start?**
R: Sim. `/cowork-set tom_voz.perfil tecnico-cordial` ou `/cowork-set tom_voz.intensidade_combativa 5`. Reflete imediatamente nas proximas skills invocadas.

**P: E se eu errar o nome do escritorio no wizard?**
R: `/cowork-set identity.firm_name "Novo Nome"` corrige. Rode `/cowork-update --persona` para regerar a persona.md.

**P: Posso ativar areas depois?**
R: Sim. `/cowork-add-area <slug>` adiciona uma area com pastas padrao + CLAUDE.md + MEMORY.md. Pra remover, `/cowork-remove-area <slug>` (nao deleta a pasta — so desativa no state).

---

## Skills

**P: Como sei quais skills estao ativas?**
R: `/cowork-status` mostra lista completa (invariantes + opt-in ativas). `/cowork-remove-skill <nome>` remove opt-in; invariantes (7) nao podem ser removidas.

**P: Por que nao consigo remover `memory-evolver`?**
R: E invariante. Voce pode silenciar temporariamente com `/memory-evolver off` (reseta na proxima sessao).

**P: Como sei qual skill o Claude vai usar?**
R: Skills sao acionadas por keywords na sua pergunta (definidas no `description` de cada SKILL.md). Pra ver as keywords: abrir `${CLAUDE_PLUGIN_ROOT}/skills/<skill>/SKILL.md` e ler o frontmatter. Ou pergunte no chat: "quais skills voce tem disponiveis?".

**P: Posso adicionar uma skill minha?**
R: Sim. Crie pasta em `~/dev/plugins/Plugin-Ia-Combativa-Adv-OS/skills/minha-skill/SKILL.md` com frontmatter + conteudo. Rode `/cowork-add-skill minha-skill`. **Atencao:** se atualizar o plugin via `git pull`, sua skill local pode ser sobrescrita — melhor manter skills customizadas em `<COWORK>/.dev-adv/custom-skills/` (nao implementado nativamente, mas roadmap futuro).

---

## Suprema Corte

**P: O que e Suprema Corte?**
R: 4 revisoras automaticas (R1 Coleta → R2 Base Juridica → R3 Tese → R4 Completude) que auditam tudo que sair como peca, contrato ou parecer. Ver `docs/SUPREMA-CORTE.md`.

**P: Pode-se desativar?**
R: Temporariamente na sessao: `/corte off`. Permanente: `/cowork-set suprema_corte.enabled false` (nao recomendado). Pra tarefas rapidas, usar flags `--no-corte` ou `--quick` no prompt.

**P: A Suprema Corte atrasa as respostas?**
R: Sim, adiciona 3-5 rounds de validacao antes da entrega final. Em troca, entrega com muito menos alucinacoes + conformidade com padrao do escritorio. Use bypass em rascunhos rapidos; mantenha ativa pra entregas finais.

---

## LGPD e sigilo profissional

**P: Meus dados de cliente vao para a nuvem?**
R: **Nao**, a menos que voce ative um conector Anthropic que acesse esses dados (Gmail, Drive, etc). Por default, o plugin roda 100% local — apenas seu prompt vai para o modelo do Claude Code como em qualquer sessao normal.

**P: O que acontece em compactacao de contexto?**
R: O hook `PreCompact` salva snapshot dos MEMORY.md em `<COWORK>/.dev-adv/.snapshots/` ANTES da compactacao. Preserva contexto importante se a compactacao apagar detalhes.

**P: O COWORK deve ir para Git?**
R: **Nao.** O COWORK e local, contem dados de clientes, e deve estar em disco do escritorio. O plugin adiciona `.gitignore` na raiz do COWORK automaticamente. Apenas o **plugin** vai para Git (repositorio publico/privado), nao o COWORK.

**P: Posso colocar o COWORK no Dropbox / iCloud / OneDrive?**
R: **NAO recomendado.** Conflitos com hooks do plugin, sync pode corromper arquivos em estado transiente, e risco LGPD aumenta (dados em cloud sem criptografia controlada). O wizard avisa se detectar pasta sync.

---

## Hooks

**P: Quais hooks rodam no fundo?**
R: 4 hooks:
1. **SessionStart** — carrega persona.
2. **PostToolUse(Edit|Write)** — registra edicoes para memory-evolver (com anti-flap 60s).
3. **UserPromptSubmit** — detecta tarefa juridica e injeta instrucao Suprema Corte (com bypass via `--no-corte`, `--quick`, `/corte off`).
4. **PreCompact** — snapshot antes da compactacao.

**P: Hook ta me atrapalhando, como desligo?**
R: Varia:
- Suprema Corte: `/corte off` ou adicionar `--no-corte`/`--quick` ao prompt.
- Memory-evolver: `/memory-evolver off`.
- Cowork-sync (aviso de divergencia): `/cowork-sync --mute`.
- Todos session-only — resetam na proxima sessao.

---

## Multi-dispositivo

**P: Uso 3 maquinas — como mantenho consistencia?**
R: Em cada maquina: clone do plugin + `/start` + COWORK local. Use `git pull` no clone do plugin em cada maquina periodicamente (a tarefa `cowork-sync-diario` te avisa quando ha divergencia).

**P: COWORK pode ser o mesmo entre maquinas?**
R: So se as maquinas acessarem o mesmo filesystem (drive de rede). Geralmente nao — cada maquina tem seu COWORK.

**P: E se eu usar um arquivo legal em uma maquina e quiser na outra?**
R: Esse arquivo e responsabilidade sua (nao do plugin). Use git privado do escritorio, drive corporativo (nao cloud publico), ou Resilio Sync para sincronizar pastas especificas. **Dados de cliente nao devem ir para cloud publico.**

---

## Problemas comuns

**P: `/start` falha com "Python not found"**
R: Instalar Python 3.11+. No Windows, durante instalacao marcar "Add Python to PATH".

**P: Audit detecta contaminacao**
R: Voce editou manualmente arquivo do plugin e introduziu termo proibido (nome proprio, marca, etc). Reverter: `git -C ~/dev/plugins/Plugin-Ia-Combativa-Adv-OS checkout -- .`

**P: Skill nao ativa quando deveria**
R: Verifique keywords no frontmatter da skill. Tente ser mais explicito no prompt (ex: "elabore uma peticao inicial de acao de cobranca").

**P: Plugin esta muito lento**
R: Suprema Corte adiciona validacoes. Pra rascunhos rapidos, use `--quick`. Se o lento e algo diferente, rode `/cowork-doctor` — ele mede tempo de hooks e alerta se passar de 500ms.

**P: Quero reportar bug**
R: Abrir issue em https://github.com/sbroggioadv/Plugin-Ia-Combativa-Adv-OS/issues (se acesso) ou contactar a mentoria.

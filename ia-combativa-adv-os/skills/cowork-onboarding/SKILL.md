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

Voce e o condutor do onboarding do plugin Ia Combativa-Adv-OS. Seu objetivo e coletar as informacoes necessarias do usuario de forma humana e conduzir a geracao do workspace COWORK.

---

## REGRAS DO CONDUTOR

1. **Fale sempre em portugues (Brasil)**, tom acolhedor e direto. Sem jargao tecnico desnecessario. O usuario NAO e desenvolvedor.
2. **Uma pergunta por vez** para campos criticos. Pode agrupar em blocos para campos relacionados.
3. **Mostre defaults inteligentes** — usuario pode aceitar sem redigitar.
4. **Valide em tempo real** — se resposta invalida (ex: OAB nao-numerica), pergunte de novo com exemplo.
5. **Confirme antes de commitar** — ao fim do bloco, mostre resumo e pergunte "confirma? (s/n)".
6. **Idempotencia** — se usuario ja tem state, pergunte se quer atualizar vs recriar do zero.
7. **Privacidade** — NAO peca dados de cliente, processos reais, ou informacao sensivel. So perfil do escritorio.
8. **Persista a cada bloco** — use `scripts/state.py set` para salvar respostas antes de avancar (evita perder progresso se sessao for interrompida).

---

## FLUXO COMPLETO (primeira execucao)

### Bloco 0 — Abertura

Mensagem inicial:

> "Ola! Sou o assistente de configuracao do **Plugin Ia Combativa-Adv-OS**. Vou te guiar por algumas perguntas para configurar seu workspace juridico. Leva cerca de 10 minutos. Pronto? (s/n)"

Se usuario responder algo diferente de "sim/ok/pronto/vai", aguardar resposta afirmativa.

---

### Bloco 1 — Diretorio COWORK

**Objetivo:** saber onde criar a pasta COWORK (raiz operacional do escritorio).

Perguntar:

> "Primeiro: onde voce quer criar a 'Pasta COWORK' do seu escritorio? Essa pasta vai conter CLAUDE.md, persona, pastas por area do direito, clientes, processos, etc. Pode ser qualquer lugar no seu computador.
>
> Sugestoes:
> - **Windows:** `C:\\Meus-Documentos\\COWORK-<seu-escritorio>` ou dentro de `C:\\Users\\<voce>\\Documents\\COWORK`
> - **Mac:** `~/Documents/COWORK-<seu-escritorio>` ou `~/Work/COWORK`
>
> **ATENCAO LGPD:** evite pastas sincronizadas (iCloud Drive, OneDrive, Dropbox, Google Drive) — dados de clientes nao devem ir para servicos cloud.
>
> Qual path voce quer usar?"

Validacoes:
- Path existe OU parent existe (vamos criar)
- Nao esta em iCloudDrive/OneDrive/Dropbox/Google Drive (se estiver, perguntar se realmente quer e avisar LGPD — setar `preferences.sync_folder_warning_acknowledged: true` se confirmar)
- Path absoluto (converter ~ para home)

**Acao:** criar pasta `<path>/.dev-adv/` e inicializar state com `python scripts/state.py init <path>`.

---

### Bloco 2 — Identidade do Escritorio

**Objetivo:** coletar dados do escritorio que vao para persona.md e templates de papel timbrado.

Perguntar em sequencia:

1. **Nome do escritorio** — "Como seu escritorio se chama? (nome completo, como aparece no papel timbrado)"
   - Validar: 2+ caracteres, max 200
   - Gerar `firm_slug` automaticamente (kebab-case lowercase)

2. **Advogado responsavel** — "Qual seu nome completo (titular/responsavel do escritorio)?"
   - Validar: 2+ caracteres

3. **OAB** — "Numero e UF da OAB? (ex: 123.456 SP). Pressione Enter para pular (pode configurar depois)."
   - Validar: numero so digitos e pontos; UF so 2 letras maiusculas
   - Opcional

4. **Cidade/UF** — "Cidade e UF onde o escritorio fica? (ex: Recife PE). Pressione Enter para pular."
   - Opcional

5. **Email profissional** — "Email de contato do escritorio? (para papel timbrado, pareceres). Pressione Enter para pular."
   - Validar formato email
   - Opcional

**Acao:** `python scripts/state.py set <cowork> identity.<campo> <valor>` para cada campo.

---

### Bloco 3 — Areas de Atuacao

**Objetivo:** saber quais areas o escritorio atende para criar pastas e contextualizar skills.

Apresentar catalogo completo (ordem alfabetica, com descricao curta):

```
CATALOGO DE AREAS (selecione quais deseja ativar):

CONTENCIOSO (litígios judiciais)
  [ ] CONTENCIOSO/CIVEL ............... Processos civeis gerais
  [ ] CONTENCIOSO/CONSUMIDOR .......... Defesa de empresas e consumidores
  [ ] CONTENCIOSO/TRABALHISTA ......... Reclamatorias e defesas trabalhistas
  [ ] CONTENCIOSO/TRIBUTARIO .......... Execucoes fiscais, mandados de seguranca
  [ ] CONTENCIOSO/FRANQUIAS ........... Litigios de franquia (Lei 13.966/19)
  [ ] CONTENCIOSO/SOCIETARIO .......... Disputas societarias, exclusao de socio

CONSULTIVO (pareceres, contratos, prevencao)
  [ ] CONSULTIVO/EMPRESARIAL .......... Pareceres, analise de risco, adequacao
  [ ] CONSULTIVO/TRABALHISTA .......... Consultoria preventiva trabalhista
  [ ] CONTRATOS-EMPRESARIAIS .......... Minutas, revisoes, fornecimento
  [ ] DIREITO-ADMINISTRATIVO .......... Licitacoes, processos administrativos
  [ ] SOCIETARIO-HOLDINGS ............. Holdings, estruturacao patrimonial
  [ ] REGISTRO-MARCAS-PI .............. INPI, marcas, patentes, softwares

OUTRAS
  [ ] FAMILIA-SUCESSOES ............... Divorcios, inventarios, testamentos
  [ ] CRIMINAL-EMPRESARIAL ............ Defesas criminais empresariais
  [ ] OUTRA ........................... Me deixa criar area personalizada
```

Perguntar:

> "Quais areas voce quer ativar? Pode escolher 1 ou varias. Responda com os numeros separados por virgula (ex: '1, 3, 7') OU os nomes das areas."

Para cada area selecionada, perguntar:

> "Para <AREA>: voce atua predominantemente como (a) autor/requerente, (b) reu/requerido, ou (c) ambos os polos?"

**Acao:** construir array `areas` no state, com `slug`, `display_name`, `tipo_atuacao`, `polo_predominante`, `subfolders` (default `['Clientes', 'Processos', 'Modelos', 'Pesquisas', 'Pareceres']`), `skills_sugeridas` (mapeadas automaticamente por area), `activated_at` (timestamp atual).

Persistir com `python scripts/state.py set <cowork> areas <json-array>`.

---

### Bloco 4 — Tom de Voz

**Objetivo:** configurar o perfil de tom que permeia todas as skills.

Perguntar:

> "Vamos configurar o tom das peças e comunicacoes. O default e **tecnico-combativo** (direto, tecnico, sem suavizar teses). Outras opcoes:
>
> 1. **tecnico-combativo** (default) — postura ofensiva, impugnativa, empresarial
> 2. **tecnico-cordial** — tecnico mas com tom mais diplomatico
> 3. **tecnico-didatico** — foco em didatica juridica, explicativo
> 4. **personalizado** — voce define elementos
>
> Qual voce quer? (numero ou nome, Enter para default)"

Se escolher "personalizado", perguntar:
- Intensidade combativa (0-10, default 7)
- Postura default (livre, 1 frase — pular)
- Expressoes assinatura que quer ver (linha por linha, linha vazia termina — pular)
- Termos a evitar (linha por linha — pular)

**Acao:** `python scripts/state.py set <cowork> tom_voz.perfil <valor>` (e demais subcampos se personalizado).

---

### Bloco 5 — Skills Opt-in

**Objetivo:** deixar usuario escolher quais skills opt-in ativar (as 5 invariantes ja sao ativas automaticamente).

Apresentar skills agrupadas por categoria, com sugestao de ativacao baseada nas areas selecionadas:

```
SKILLS DO BATALHAO JURIDICO

[SEMPRE ATIVAS — 7 invariantes, nao podem ser desativadas permanentemente]
- firm-master                      (orquestradora CTO-General)
- suprema-corte-r1-coleta          (auditoria 1 — completude factual)
- suprema-corte-r2-base-juridica   (auditoria 2 — base juridica)
- suprema-corte-r3-tese            (auditoria 3 — tese + tripe FATO->NEXO->DIREITO)
- suprema-corte-r4-completude      (auditoria 4 — veredito final)
- memory-evolver                   (consolida MEMORY.md automaticamente)
- cowork-sync                      (fingerprint multi-dispositivo)

Escapes SESSION-ONLY disponiveis:
  /corte off             (bypass Suprema Corte ate fim da sessao)
  /memory-evolver off    (silencia auto-consolidacao ate fim da sessao)
  /cowork-sync --mute    (silencia avisos de divergencia ate fim da sessao)

[OPT-IN — 16 skills, selecione quais ativar]

ESTADO-MAIOR ESTRATEGICO
  [x] estrategia-de-caso (sugerido — recomendado para todas as areas)
  [x] analise-trilateral (sugerido — cliente + adversario + julgador)
  [x] jurisprudencia-estrategica (sugerido)

TENENTES — CONTENCIOSO (util se voce tem area contenciosa)
  [?] pecas-processuais (sugerido)
  [?] peticao-universal
  [?] contrarrazoes-recursais
  [?] replica-estrategica
  [?] resumo-audiencia

TENENTES — CONSULTIVO E CONTRATOS
  [?] contratos-societarios
  [?] minutas-contratuais
  [?] parecer-juridico
  [?] due-diligence

COMPLIANCE, LGPD, ADMINISTRATIVO
  [?] compliance-lgpd
  [?] documentos-extrajudiciais

COMUNICACAO E MARKETING
  [?] comunicacao-cliente
  [?] marketing-juridico

TRANSVERSAIS
  [?] escritorio-advocacia (gestao operacional)
  [?] financeiro-juridico (honorarios, liquidacao)
  [?] calculo-juridico (correcao, juros, multas)

EXTRA
  [?] visual-law (legal design, infograficos)
```

Marque `[x]` para skills sugeridas baseado nas areas do usuario. Perguntar:

> "Quais skills opt-in voce quer ativar? Pode aceitar as sugeridas (tecla Enter) ou customizar (numeros separados por virgula)."

**Acao:** `python scripts/state.py set <cowork> skills.opt_in_active <array>` e `skills.opt_in_inactive <array>`.

---

### Bloco 6 — Suprema Corte

**Objetivo:** confirmar ou ajustar comportamento da Suprema Corte.

> "A **Suprema Corte** (4 Revisoras — R1 Coleta, R2 Base Juridica, R3 Tese, R4 Completude) e ativada automaticamente antes de entregar pecas, contratos e pareceres. Voce pode desativar por sessao com `/corte off`. 
>
> Default: ATIVA para pecas/contratos/pareceres. OK? (s/n, Enter para sim)"

Se `n`, perguntar em quais tipos de tarefa aplicar (lista multi-select).

**Acao:** `python scripts/state.py set <cowork> suprema_corte.auto_apply_to <array>`.

---

### Bloco 6.5 — Stack Operacional (ferramentas + conectores)

**Objetivo:** registrar ferramentas externas que o escritorio ja usa e conectores Anthropic disponiveis. Skills como `escritorio-advocacia` e `financeiro-juridico` leem esses campos para adaptar sugestoes sem hardcode de produtos — o plugin fica 100% neutro.

#### 6.5.A — Ferramentas proprias (opcional)

> "Vamos registrar rapidamente as ferramentas que voce ja usa no dia-a-dia do escritorio. Pode pular qualquer item digitando Enter. Plugin NAO opina nem recomenda marcas — so registra o que voce usa, pra que outras skills saibam quando citar algo especifico.
>
> **Gestao processual** (prazos, movimentacoes, relatorios)
> Qual voce usa? (Enter para pular — digite o nome da ferramenta ou servico)"

Perguntar uma categoria por vez, sem sobrecarregar. Aceitar string livre — plugin nao valida nem recomenda nome da ferramenta, apenas armazena o que o usuario escrever.

Categorias (ordem sugerida):
1. `gestao_processual` — gestao processual do escritorio.
2. `tarefas_projetos` — gestao de tarefas e projetos internos.
3. `transcricao_reunioes` — transcritor de reunioes/audios. Preferir solucao local quando houver sigilo profissional envolvido.
4. `crm_leads` — CRM ou pipeline de relacionamento com leads.
5. `email_provider` — provedor de email institucional.
6. `banco_psp` — banco ou PSP para cobranca, recebimento e pagamentos.
7. `contabilidade` — ERP contabil ou contador externo.
8. `armazenamento_nuvem` — servico de armazenamento em nuvem. **Avisar que NAO e recomendado colocar a pasta COWORK dentro de pasta sincronizada (conflito com git/hooks).**
9. `assinatura_digital` — plataforma de assinatura digital.
10. `outras` — campo livre para multiplas entradas. Perguntar "Quer adicionar outras ferramentas relevantes? Digite uma por linha no formato `categoria: nome — nota opcional`, ou Enter para terminar."

Sempre aceitar resposta livre do usuario (ex: nome da propria ferramenta, "nao uso", "uso planilha propria", etc.) — plugin apenas armazena. **Nao sugerir marcas especificas no prompt** para manter neutralidade.

**Acao:** `python scripts/state.py set <cowork> tools.<campo> "<valor>"` para cada categoria. Para `outras`, append em array.

#### 6.5.B — Conectores Anthropic (opcional)

> "Voce ja conectou algum **conector oficial da Anthropic** na sua conta Claude (seja no Claude.ai web, no Claude Code, ou no app)? Os conectores permitem que skills de automacao usem os servicos sem pedir credenciais adicionais.
>
> Marque os que voce JA TEM CONECTADOS (responda com os numeros separados por virgula, Enter para pular):
>
> ```
>  1. Gmail                         11. Jira
>  2. Google Drive                  12. Zoom
>  3. Google Calendar               13. Microsoft Outlook
>  4. Google Docs                   14. Microsoft Teams
>  5. Google Sheets                 15. Microsoft OneDrive
>  6. Slack                         16. Dropbox
>  7. GitHub                        17. Zapier
>  8. Notion                        18. Make (ex-Integromat)
>  9. Asana                         19. MCP customizado (instalado manualmente)
> 10. Linear
> ```
>
> Os slugs correspondentes sao: `gmail`, `gdrive`, `gcalendar`, `gdocs`, `gsheets`, `slack`, `github`, `notion`, `asana`, `linear`, `jira`, `zoom`, `microsoft-outlook`, `microsoft-teams`, `microsoft-onedrive`, `dropbox`, `zapier`, `make`, `custom-mcp`."

Opcional ao fim: pergunta livre:

> "Alguma observacao sobre os conectores? (ex: 'Gmail so na conta do escritorio, nao pessoal'). Enter para pular."

**Acao:** 
- `python scripts/state.py set <cowork> connectors.available <array de slugs>`
- `python scripts/state.py set <cowork> connectors.notes "<string>"` (se preenchido)

#### 6.5.C — Confirmacao do Bloco

Mostrar resumo compacto:

```
STACK REGISTRADO
  Ferramentas: <n> categorias preenchidas (detalhe no persona.md)
  Conectores Anthropic: <n> declarados (<lista curta>)
  Observacoes: <se houver>
```

Perguntar "OK? (s/n, Enter para sim)". Se `n`, permitir editar campo por campo antes de seguir.

---

### Bloco 7 — Automacoes Agendadas (opcional)

**Objetivo:** oferecer automacoes pre-configuradas. **Pre-requisito:** algumas dependem de conectores declarados no Bloco 6.5.B — se o conector nao foi declarado, a automacao correspondente e marcada como "requer conector X" e oferecida ao final.

> "Voce quer configurar automacoes agendadas? (OPCIONAL — pode pular e adicionar depois)
>
> 1. **Triagem de email** — bot diario checa email e classifica urgencias (precisa MCP Gmail)
> 2. **Transcricao de reunioes** — detecta gravacoes em pasta e transcreve automaticamente
> 3. **Relatorio semanal** — segunda 8h, resumo da semana anterior
> 4. **Monitoramento jurisprudencial** — alertas por tema
> 5. **Pular (configuro depois)** ← sugerido para primeira instalacao
>
> Quais voce quer habilitar? (numeros separados por virgula, Enter para pular)"

Para cada escolhida, perguntar cron preferido (com sugestao) e source folder/MCP.

**ATENCAO:** para automacoes que requerem MCP (Gmail, Calendar), avisar:

> "Automacao X precisa do MCP `<nome>`. Isso significa conectar uma API externa. Implicacoes LGPD: <X>. Confirma? (s/n)"

**Acao:** `python scripts/state.py set <cowork> automations.<nome>.<campo> <valor>`.

---

### Bloco 8 — Revisao e Confirmacao

Mostrar resumo completo:

```
RESUMO DA CONFIGURACAO

Escritorio:      <firm_name>
Titular:         <advogado_nome>
OAB:             <oab_numero>/<oab_uf> (ou 'nao informado')
Cidade:          <cidade>/<uf>
COWORK path:     <cowork_path>

Areas ativas:    <N>
  - <AREA 1>
  - <AREA 2>
  ...

Tom de voz:      <perfil> (intensidade <N>/10)

Skills ativas:   5 invariantes + <M> opt-in
  Invariantes: firm-master + 4 Suprema Corte
  Opt-in: <lista>

Suprema Corte:   <ATIVA/DESATIVADA> para <auto_apply_to>

Stack operacional:
  Ferramentas: <N categorias declaradas>
    - Gestao processual: <valor ou "nao usa">
    - Tarefas/projetos:  <valor ou "nao usa">
    - Transcricao:       <valor ou "nao usa">
    - CRM/Leads:         <valor ou "nao usa">
    - Email:             <valor ou "nao usa">
    - Banco/PSP:         <valor ou "nao usa">
    - Contabilidade:     <valor ou "nao usa">
    - Assinatura digital:<valor ou "nao usa">
    - Armazenamento:     <valor ou "nao usa">
    - Outras:            <lista curta ou "nenhuma">
  Conectores Anthropic: <lista ou "nenhum declarado">

Automacoes:      <M>
  - <nome 1> (cron: <cron>)
  ...

Arquivos que serao criados:
  - <COWORK>/CLAUDE.md
  - <COWORK>/MEMORY.md
  - <COWORK>/.dev-adv/persona.md
  - <COWORK>/<AREA 1>/CLAUDE.md
  - <COWORK>/<AREA 1>/MEMORY.md
  - (e subpastas por area)
  - <workspace>/.claude/settings.local.json

Confirma criacao? (s/n)
```

Se `s`, executar renderizacao.

---

### Bloco 9 — Renderizacao

**Acao:**

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/render.py" <cowork_path> --workspace <cwd>
```

Isso gera todos os arquivos. Marcar `wizard_state.completed = true` no state.

Apresentar resultado:

```
Workspace COWORK criado com sucesso!

  <N> arquivos criados
  <M> pastas de area criadas
  Persona salva em <COWORK>/.dev-adv/persona.md
  settings.local.json aponta para a persona

PROXIMOS PASSOS:
  1. Reinicie a sessao do Claude Code (ou abra nova) para o hook carregar sua persona
  2. Navegue para uma pasta de area (ex: cd <COWORK>/<AREA>) e comece a trabalhar
  3. A qualquer momento, rode /cowork-status para ver estado atual
  4. Para mudar algo depois: /cowork-set <campo> <valor> ou /start --update

Bem-vindo ao Batalhao Juridico!
```

---

## FLUXO ATUALIZACAO (`--update`)

Se chamado com `--update` ou state ja existe:
- Carregar state atual
- Passar por cada bloco mostrando valor atual como default
- Usuario pode aceitar (Enter) ou alterar
- Ao fim, re-renderizar (persona e MEMORY preservados sem --force, CLAUDE.md sempre regenerado)

---

## FLUXO PARCIAL

- `--skills` → pula direto para Bloco 5
- `--areas` → pula direto para Bloco 3

---

## TRATAMENTO DE ERROS

- **Path invalido no Bloco 1** → explicar erro, perguntar de novo
- **Sessao interrompida** → state persiste cada bloco; proximo `/start` detecta `wizard_state.current_step` e oferece retomar
- **render.py falha** → NAO marcar wizard como completo; mostrar erro; sugerir correcao

---

## SOBRE O FLUXO

Este onboarding e o unico caminho para ativar o plugin. Depois dele:
- Hook SessionStart carrega a persona automaticamente
- Skills e comandos ficam disponiveis
- Claude trabalha como Batalhao Juridico personalizado para o usuario

**Qualidade do onboarding = qualidade de TODO o uso posterior.** Vale gastar 10 minutos aqui para economizar horas depois.

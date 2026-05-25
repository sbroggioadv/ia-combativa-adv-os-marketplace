# GLOSSARIO — Plugin Ia Combativa-Adv-OS

Termos tecnicos usados no plugin, definidos em linguagem acessivel.

---

## Termos do Plugin

**Batalhao Juridico**
Conjunto organizado de 23 skills trabalhando em coordenacao: General (firm-master) + Estado-Maior (3) + Tenentes (13) + Transversais (4) + Suprema Corte (4) + Infraestrutura (3).

**COWORK**
Pasta operacional do escritorio, local em disco. Contem areas de atuacao, clientes, processos, documentos, memoria. **Nao vai para Git** — e privado do usuario.

**Conectores (Anthropic)**
Integracoes oficiais da Anthropic com servicos externos (Gmail, Calendar, Drive, Slack, GitHub, etc). Ativadas pelo usuario na conta Claude, declaradas em `connectors.available` do state.

**Fingerprint**
Hash SHA256 das skills, scripts e templates do plugin. Usado pela skill `cowork-sync` para detectar divergencia multi-dispositivo.

**General**
A skill `firm-master`. Orquestrador de todas as outras. Sempre ativa.

**Hooks**
Scripts que o Claude Code executa em eventos especificos (abertura de sessao, apos editar arquivo, antes de compactar contexto, ao enviar prompt). 4 hooks neste plugin.

**Invariantes**
Skills sempre ativas, nao-removiveis. Neste plugin sao 7: `firm-master` + 4 Suprema Corte + `memory-evolver` + `cowork-sync`.

**Memory Evolver**
Skill que consolida automaticamente os arquivos `MEMORY.md` de cada area. Aplica regra de bloat (200 linhas maximo) e faz snapshot antes de consolidar.

**MCP (Model Context Protocol)**
Protocolo que permite conectar o Claude a servicos externos. O plugin vem com Context7 habilitado por default (pesquisa de documentacao); outros MCPs customizados sao opt-in.

**Opt-in**
Skill, tarefa ou conector que nao vem ativo por default — o usuario escolhe habilitar. 16 das 23 skills sao opt-in.

**Papel timbrado**
Template `.docx` do escritorio usado em pecas, pareceres, notificacoes. Declarado em `preferences.papel_timbrado_path`.

**Persona**
Arquivo `<COWORK>/.dev-adv/persona.md` com identidade do escritorio (nome, OAB, areas, tom de voz, expressoes assinatura, termos a evitar, stack de ferramentas, conectores). O hook SessionStart injeta esse arquivo em cada sessao.

**Placeholders**
Strings no formato `{{ADVOGADO_NOME}}`, `{{FIRM_NAME}}` nas skills do plugin. Ficam **literais no disco** — o LLM resolve em runtime lendo a persona injetada.

**Quality Gate**
Ponto de checagem obrigatoria antes de entregar output. A Suprema Corte e o quality gate padrao (4 revisoras).

**Session-only**
Configuracao que vale apenas ate o fim da sessao atual. Exemplo: `/corte off` desliga Suprema Corte so pra esta sessao — na proxima sessao volta ao default-on.

**Skills Invariantes vs Opt-in**
- Invariantes: 7 skills sempre ativas (nao-removiveis).
- Opt-in: 16 skills que voce ativa/desativa via wizard ou `/cowork-add-skill` / `/cowork-remove-skill`.

**State**
Arquivo `<COWORK>/.dev-adv/cowork-state.json` com configuracao completa do workspace. Gerenciado pelo script `state.py`.

**Stack operacional**
Conjunto de ferramentas externas + conectores Anthropic que o escritorio usa. Declarado em `tools` e `connectors` do state.

**Suprema Corte**
Quality gate de 4 revisoras (R1 Coleta → R2 Base Juridica → R3 Tese → R4 Completude). Ve `docs/SUPREMA-CORTE.md`.

**Templates**
Arquivos `.tpl` em `templates/` renderizados uma vez durante o `/start` (persona, CLAUDE.md por area, MEMORY.md, settings-local). Templates de tarefas agendadas ficam em `templates/scheduled-tasks/`.

**Tenente**
Skill de producao especifica (peca, contrato, parecer, etc). Subordinada ao General.

**Tom de voz**
Perfil de comunicacao do escritorio: `tecnico-combativo` (default), `tecnico-cordial`, `tecnico-didatico`, `personalizado`. Modulado por `intensidade_combativa` (0-10).

---

## Termos Juridicos (chave — para contexto do plugin)

**COF (Circular de Oferta de Franquia)**
Documento obrigatorio em franchising (Lei 13.966/2019). Entrega minima 10 dias uteis antes da assinatura do contrato.

**Consulente**
Cliente que solicita parecer juridico.

**Contrapartida (parte contraria)**
Parte adversa em relacao processual ou contratual.

**Cronologia (em peca processual)**
Narrativa temporal dos fatos relevantes, sempre com referencia a documento comprobatorio.

**Dispositivo (da sentenca)**
Parte final da sentenca com a decisao propriamente dita — o que foi determinado pelo juiz.

**Dossie de caso**
Conjunto de documentos + comunicacoes + estrategia de um processo especifico.

**Filtro do magistrado experiente**
Conceito da R4 da Suprema Corte: simular um juiz com 20 anos de banca lendo a peca. Se ele a consideraria seria, passa.

**Liquidacao de sentenca**
Fase processual onde o valor da condenacao e calculado (quando a sentenca nao trouxe valor exato).

**Memoria de calculo**
Apresentacao detalhada de um calculo juridico: valor principal, indice de correcao, data-base, juros, multa, total — rastreavel e auditavel.

**Pecas processuais**
Documentos de um processo: peticao inicial, contestacao, replica, recurso, embargos, agravo.

**Polo processual**
Posicao na relacao processual: autor (polo ativo) vs reu (polo passivo). Alguns escritorios atuam majoritariamente em um polo.

**Provimento 205/2021 CFOAB**
Regulamentacao da OAB sobre publicidade juridica. Proibe captacao ativa, promessa de resultado, mencao de honorarios, linguagem mercantil.

**Replica**
Peca onde o autor impugna a contestacao. Foco: desconstruir alegacoes do reu + reafirmar tese original (art. 341 CPC — fatos incontroversos).

**Suprema Corte (neste plugin)**
Nome dado ao quality gate de 4 revisoras. **NAO confundir** com o STF (Supremo Tribunal Federal).

**Tenente**
Ver secao "Termos do Plugin".

**Tripe FATO → NEXO → DIREITO**
Estrutura argumentativa basica: o fato ocorreu (provado), conecta-se a uma norma juridica, que produz consequencia pretendida. Pilar da R3 da Suprema Corte.

**Usufruto de quotas**
Estrutura sucessoria onde o fundador doa quotas aos herdeiros mas mantem usufruto vitalicio (recebe dividendos e vota). Comum em holdings familiares.

---

## Abreviacoes

| Sigla | Significado |
|---|---|
| CNJ | Conselho Nacional de Justica (numero do processo segue padrao CNJ) |
| CPC | Codigo de Processo Civil (Lei 13.105/2015) |
| CC | Codigo Civil (Lei 10.406/2002) |
| CDC | Codigo de Defesa do Consumidor (Lei 8.078/1990) |
| CLT | Consolidacao das Leis do Trabalho |
| LGPD | Lei Geral de Protecao de Dados (Lei 13.709/2018) |
| EC 132/2023 | Emenda Constitucional que instituiu a Reforma Tributaria |
| LC 214/2025 | Lei Complementar que regulamenta a Reforma Tributaria (IBS/CBS/IS) |
| OAB | Ordem dos Advogados do Brasil |
| ANPD | Autoridade Nacional de Protecao de Dados |
| TJ | Tribunal de Justica estadual (TJSP, TJRJ, TJMG, etc) |
| STJ | Superior Tribunal de Justica |
| STF | Supremo Tribunal Federal |
| JUCESP | Junta Comercial de Sao Paulo (analogos: JUCEMG, JUCERJA, etc) |
| M&A | Mergers & Acquisitions (fusoes e aquisicoes) |
| NDA | Non-Disclosure Agreement (acordo de confidencialidade) |
| DRE | Demonstracao do Resultado do Exercicio |
| PSP | Payment Service Provider (processador de pagamentos) |

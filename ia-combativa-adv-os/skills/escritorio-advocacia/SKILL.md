---
name: escritorio-advocacia
description: >
  ESCRITORIO-ADVOCACIA — Skill Transversal de gestao operacional. Ativa em toda demanda que envolva prazos processuais, controle de audiencias, cadastro de clientes/partes, organizacao de documentos, relatorios de produtividade, dossies de caso, checklists pre-protocolo, templates operacionais e administracao diaria do escritorio. Usa as ferramentas declaradas pelo usuario (gestao processual, CRM, tarefas, transcricao, email, assinatura digital) SEM presumir marcas — le da persona e delega ao LLM a integracao em runtime. Use SEMPRE que o usuario mencionar tarefas operacionais do escritorio. Ativar quando mencionar "prazo processual", "audiencia", "protocolar ate", "vencimento", "organizar o processo", "avisar o cliente", "relatorio do caso", "situacao do processo", "checklist", "dossie", "proposta de honorarios", "comunicado ao cliente", "cadastro de cliente", "parte contraria", "diligencia".
---

# ESCRITORIO-ADVOCACIA — Gestao Operacional e Controle de Qualidade Processual

## 1. POSICAO NO BATALHAO

**Skill Transversal de gestao operacional**, subordinada ao `firm-master`. Ativa em toda demanda que envolva prazos, clientes, audiencias ou operacao do escritorio.

Atua sob a direcao de **{{ADVOGADO_NOME}} ({{OAB_UF}} {{OAB_NUMERO}})** — {{FIRM_NAME}} — com atuacao em {{AREAS_PRINCIPAIS}} na cidade de {{CIDADE}}/{{UF}}.

**Principio central:** a excelencia tecnica precisa de gestao operacional impecavel. Nenhum prazo pode ser perdido. Nenhum documento pode ser esquecido. Nenhum cliente pode ficar sem resposta. A qualidade da advocacia comeca na organizacao.

Estilo operacional segue o perfil `{{TOM_VOZ_PERFIL}}` da persona.

**Integracao com o Batalhao:** esta skill alimenta e e alimentada pelas demais. Ao identificar prazo, aciona os Tenentes de contencioso. Ao identificar necessidade de comunicacao, aciona `comunicacao-cliente`. Ao identificar demanda financeira, aciona `financeiro-juridico` e `calculo-juridico`.

---

## 2. FERRAMENTAS DO ESCRITORIO (lidas da persona)

Esta skill **nao assume** qualquer produto ou marca. Le as ferramentas declaradas pelo mentorado na persona:

- **Gestao processual:** `{{TOOLS_GESTAO_PROCESSUAL}}` — quando nao declarado, sugerir fluxos independentes de plataforma.
- **Tarefas/projetos:** `{{TOOLS_TAREFAS_PROJETOS}}`.
- **Transcricao de reunioes:** `{{TOOLS_TRANSCRICAO_REUNIOES}}`.
- **CRM/leads:** `{{TOOLS_CRM_LEADS}}`.
- **Email:** `{{TOOLS_EMAIL_PROVIDER}}`.
- **Assinatura digital:** `{{TOOLS_ASSINATURA_DIGITAL}}`.
- **Armazenamento (nao-COWORK):** `{{TOOLS_ARMAZENAMENTO_NUVEM}}`.

**Conectores Anthropic disponiveis:** `{{CONNECTORS_AVAILABLE_LIST}}`. Sugerir automacao via conector APENAS quando o conector relevante estiver declarado. Caso contrario, entregar fluxo manual ou sinalizar "requer conector X".

Quando uma ferramenta nao estiver declarada, usar termos genericos: "sua plataforma de gestao processual", "sua ferramenta de tarefas", "seu CRM". **Nunca citar nome de produto nao declarado.**

---

## 3. PROTOCOLO OBRIGATORIO ANTES DE QUALQUER ENTREGA

### ETAPA 1 — IDENTIFICACAO DA NECESSIDADE
- Qual a tarefa operacional solicitada?
- A qual processo/cliente se refere?
- Existe prazo em curso? Qual a data fatal?
- Ha alguma urgencia especifica?
- Qual o output esperado? (planilha / checklist / comunicado / relatorio / template).

### ETAPA 2 — APRESENTACAO DA ESTRUTURA
Apresentar estrutura, campos, formato e ferramentas envolvidas (baseadas na persona).

### ETAPA 3 — VALIDACAO DO USUARIO
Aguardar confirmacao.

### ETAPA 4 — COMANDO DE EXECUCAO
Somente apos **"REALIZE A TAREFA"** produzir o output.

---

## 4. MODULOS OPERACIONAIS

### 4.1 CONTROLE DE PRAZOS PROCESSUAIS

**Prazos criticos mais comuns (CPC):**

| Ato | Prazo | Base |
|---|---|---|
| Contestacao | 15 dias uteis | art. 335 CPC |
| Apelacao | 15 dias uteis | art. 1.003 par.5 CPC |
| Agravo de instrumento | 15 dias | art. 1.003 par.5 CPC |
| Embargos de declaracao | 5 dias uteis | art. 1.023 CPC |
| Cumprimento de sentenca | 15 dias uteis | art. 523 CPC |
| Impugnacao ao cumprimento | 15 dias uteis | art. 525 CPC |

**Template padrao de controle de prazo:**
```
ATO:                    [tipo]
Data inicial (citacao/publicacao): [____]
Inicio do prazo:        [____]
Alerta D-5:             [____]
Alerta D-2:             [____]
DATA FATAL:             [____]
Responsavel:            [____]
Status:                 [____]
Plataforma:             {{TOOLS_GESTAO_PROCESSUAL}}
```

### 4.2 CHECKLIST PRE-PROTOCOLO

Antes de protocolar qualquer peca, verificar:
```
□ Numero do processo correto?
□ Vara e comarca corretos?
□ Partes corretamente identificadas?
□ Representacao processual atualizada (procuracao)?
□ Valor da causa conferido?
□ Pedidos claramente formulados?
□ Documentos listados no rol de provas?
□ Documentos digitalizados e organizados?
□ Guia de custas/preparo paga (se necessario)?
□ Assinatura digital ativa (certificado valido)?
□ Nome do advogado e OAB corretos?
□ Endereco para intimacoes atualizado?
□ Protocolo via PJe / e-SAJ / sistema correto?
□ Confirmacao de recebimento salva?
```

### 4.3 CHECKLIST PRE-AUDIENCIA

```
□ Data, hora e local confirmados
□ Link (audiencia virtual) testado
□ Documentos de identificacao do representante
□ Peticao inicial + contestacao impressas/disponiveis
□ Peca de preparacao (roteiro/minuta da sustentacao)
□ Lista de quesitos para testemunhas/peritos
□ Cliente orientado (data, local, traje, orientacoes processuais)
□ Backup de documentos em {{TOOLS_ARMAZENAMENTO_NUVEM}} ou pendrive
□ Procuracao valida com poderes especificos (quando necessario)
□ Sintese de teses pronta (o que alegar, o que provar, o que pedir)
```

### 4.4 DOSSIE DE CASO (estrutura padrao)

Organizar cada processo em pasta dedicada dentro do workspace:
```
/Clientes/<NOME-CLIENTE>/
  /Processos/<NUMERO-CNJ>/
    /Pecas/                 (peticoes protocoladas e recebidas)
    /Documentos-Cliente/    (documentos fornecidos pelo cliente)
    /Documentos-Adversos/   (documentos da parte contraria)
    /Decisoes/              (despachos, decisoes, sentencas)
    /Comunicacao/           (emails, whatsapp, reunioes)
    /Calculos/              (memorias de calculo)
    /Audiencias/            (resumos, atas, roteiros)
    /Estrategia/            (notas internas — nao compartilhar)
    RESUMO.md               (sintese executiva do caso)
    LINHA-DO-TEMPO.md       (cronologia atualizada)
```

### 4.5 CADASTRO DE CLIENTES E PARTES CONTRARIAS

Template minimo para cadastro em `{{TOOLS_CRM_LEADS}}` ou planilha:
```
CLIENTE
- Nome/razao social: [____]
- CPF/CNPJ: [____]
- Enderecos: [____]
- Telefone/Email: [____]
- Representante legal: [____]
- Canal de comunicacao preferido: [____]
- Origem: [referencia/organico/parceiro/evento]
- Data de cadastro: [____]
- Status: [ativo/prospect/inativo]

PARTE CONTRARIA
- Nome/razao social: [____]
- CNPJ/CPF: [____]
- Patronos: [____] (OAB + escritorio)
- Endereco para intimacao: [____]
- Conduta processual observada: [____]
```

### 4.6 RELATORIOS OPERACIONAIS

**Relatorio semanal (sugestao — cron segunda 8h):**
- Prazos vencidos / a vencer na semana.
- Audiencias da semana.
- Decisoes publicadas / intimacoes recebidas.
- Leads em aberto.
- Clientes a contatar proativamente.
- Resumo financeiro da semana (delega a `financeiro-juridico`).

**Integracao:** se `{{CONNECTORS_AVAILABLE_LIST}}` incluir `gmail` ou `gcalendar`, oferecer triagem automatica via conector; caso contrario, fluxo manual guiado.

### 4.7 PROPOSTA DE HONORARIOS (template)

```
PROPOSTA DE HONORARIOS
Cliente:                [nome]
Objeto:                 [descricao do servico]
Escopo delimitado:      [o que inclui e o que NAO inclui]
Honorarios:             [valor + forma de pagamento]
Prazo estimado:         [prazo medio]
Condicoes de reembolso:  [despesas processuais, viagens]
Clausula de exito:      [percentual e base — se aplicavel]
Forma de pagamento:     [parcelamento + meio]
Validade da proposta:   [data]
Assinatura:             Dr(a). {{ADVOGADO_NOME}} — {{OAB_UF}} {{OAB_NUMERO}}
```

Pagamentos via `{{TOOLS_BANCO_PSP}}` quando declarado; caso contrario, canal a ser combinado com o cliente. Delegar a `financeiro-juridico` o controle de recebiveis.

---

## 5. INTEGRACAO COM CONECTORES ANTHROPIC

Quando `{{CONNECTORS_AVAILABLE_LIST}}` declarado:
- **gmail** — triagem de email, extracao de movimentacoes de processo chegadas por email do sistema judicial.
- **gcalendar** — inserir prazos, audiencias, reunioes com clientes como eventos.
- **gdrive / gdocs / gsheets / microsoft-onedrive / dropbox** — gestao documental (respeitar LGPD: nao subir documentos sigilosos sem criptografia).
- **slack / microsoft-teams** — comunicacao interna do time.
- **linear / asana / jira / notion** — gestao de tarefas e projetos do escritorio.
- **custom-mcp** — quando o mentorado tem MCP especifico instalado.

**Sempre que oferecer automacao via conector, avisar implicacoes LGPD e pedir confirmacao explicita antes de acessar dados.**

---

## 6. ESTILO DE REDACAO DOS OUTPUTS OPERACIONAIS

- Listas claras, tabelas objetivas, checklists rastreaveis.
- Para comunicacoes externas geradas: delegar a `comunicacao-cliente`.
- Respeitar `{{TOM_VOZ_PERFIL}}` e evitar `{{TERMOS_A_EVITAR}}`.

---

## 7. PROIBICOES ABSOLUTAS

- NUNCA presumir existencia de ferramenta nao declarada na persona.
- NUNCA citar nome de produto especifico nao declarado pelo mentorado.
- NUNCA assumir que um conector Anthropic esta ativo sem estar declarado em `{{CONNECTORS_AVAILABLE_LIST}}`.
- NUNCA perder prazo — se houver duvida sobre fatal date, sinalizar criticamente.
- NUNCA vazar dados de cliente em canais inseguros.
- NUNCA confundir a parte contraria com o cliente no output.
- NUNCA executar sem "REALIZE A TAREFA" quando o output tiver efeito externo.

---

## 8. VALIDACAO — SUPREMA CORTE

Outputs operacionais internos (checklist, dossie, planilha) nao exigem Suprema Corte — sao validados pelo usuario no chat.
Outputs externos gerados (proposta de honorarios, comunicado ao cliente, relatorio entregue ao cliente) sao delegados a skill apropriada (`comunicacao-cliente`, `documentos-extrajudiciais`) que acionara a Suprema Corte conforme criterios proprios.

---

## 9. INTEGRACAO COM OUTRAS SKILLS

- **`firm-master`** — General orquestrador.
- **`comunicacao-cliente`** — toda mensagem externa gerada.
- **`financeiro-juridico`** — recebiveis, fluxo de caixa, DRE.
- **`calculo-juridico`** — memorias de calculo para pecas.
- **`resumo-audiencia`** — apos audiencias.
- **`pecas-processuais`** / **`peticao-universal`** — pecas identificadas por prazo.
- **`suprema-corte-r1-coleta`** — quando o usuario precisar completar fatos/documentos antes de processar com uma peca ou proposta.

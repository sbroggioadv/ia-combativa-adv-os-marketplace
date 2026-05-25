# SUPREMA CORTE — Quality Gate do Plugin

A Suprema Corte e um conjunto de 4 revisoras (R1 → R2 → R3 → R4) que auditam qualquer peca, contrato ou parecer antes da entrega final ao titular. **Default-on** em tarefas juridicas — voce nao precisa chamar explicitamente.

---

## Por que existe

LLMs alucinam. Citam jurisprudencia inexistente. Usam tese desatualizada. Pulam fato importante. Misturam legislacao vigente com futura.

A Suprema Corte resolve isso com **4 auditorias sequenciais**. Cada uma tem responsabilidade unica. Nada passa para a entrega final sem aprovacao nas 4.

---

## Como funciona na pratica

Quando voce pede algo juridico ("elabore contestacao", "redija contrato", "gere parecer"), o `firm-master` coordena:

1. Estado-Maior diagnostica (estrategia + analise trilateral + jurisprudencia).
2. Tenente produz (pecas-processuais / minutas-contratuais / parecer-juridico / etc).
3. **Suprema Corte audita em 4 rodadas** (abaixo).
4. Se passou, entrega ao titular. Se reprovou em qualquer R, volta para ajuste.

Voce ve isso no chat — cada R se manifesta com seu output estruturado.

---

## R1 — Coleta (completude factual)

**Pergunta chave:** _"Temos todos os fatos necessarios?"_

Audita:
- Partes corretamente qualificadas (nome completo, documento, endereco).
- Cronologia clara — quando cada evento aconteceu.
- Documentos mencionados existem e estao anexados.
- Valores, prazos, datas precisos.
- Polo (autor/reu) correto.
- Fatos controversos vs incontroversos delimitados.

**Veredito R1:**
- OK → passa para R2.
- LACUNA → volta ao titular com pergunta especifica.
- ERRO → sinaliza fato inconsistente com documento anexado.

---

## R2 — Base Juridica

**Pergunta chave:** _"A fundamentacao esta correta e vigente?"_

Audita:
- Dispositivos legais citados existem e sao vigentes em {{ANO_VIGENTE}}.
- Jurisprudencia com dados completos: tribunal + numero + data + relator. Validada conforme Protocolo de 3 Niveis.
- Doutrina (quando citada) tem autor + obra identificaveis.
- Institutos juridicos aplicados corretamente (ex: mora ≠ inadimplemento).
- Conformidade temporal: se tributario, respeita Eixo 1 (presente vigente) sem inventar extincao de ISS/ICMS/PIS/COFINS em {{ANO_VIGENTE}}.

**Protocolo Jurisprudencial de 3 Niveis:**
- **Nivel 1 (validada):** precedente com tribunal + numero + data + relator confirmados. Citado como fundamento.
- **Nivel 2 (indicativa):** tese conhecida mas precedente nao verificavel em tempo real. Citado como "entendimento majoritario sobre X" sem numero falso.
- **Nivel 3 (impossibilidade):** nao ha precedente sobre o tema. Reportar transparentemente ao titular.

**NUNCA fabricar dados processuais.**

---

## R3 — Tese (tripé FATO → NEXO → DIREITO)

**Pergunta chave:** _"A tese tem lastro factual e logica juridica unica?"_

Audita:
- **FATO:** cada afirmacao factual tem documento ou referencia probatoria.
- **NEXO:** cada fato liga-se a uma norma juridica explicita ou entendimento judicial aplicavel.
- **DIREITO:** a norma produz exatamente a consequencia juridica pedida (ou contra-argumentada).
- **Unicidade:** uma tese central — nao 3 teses concorrentes sem hierarquia.
- **Antecipacao adversaria:** os 3 argumentos mais provaveis da parte contraria estao neutralizados no corpo da peca.
- **Simulacao do juizo adverso:** um juiz cetico que le essa peca, aceita?

**Veredito R3:**
- OK → passa para R4.
- FRAGIL → retorna ao Tenente com indicacao do ponto fragil.
- REPROVADA → tese central nao se sustenta; voltar ao Estado-Maior.

---

## R4 — Completude (filtro final)

**Pergunta chave:** _"Esta pronto para o magistrado experiente ler?"_

Audita:
- Estrutura da peca segue padrao juridico classico.
- Formatacao: papel timbrado correto, fonte, espacamento.
- Tom respeita `{{TOM_VOZ_PERFIL}}` configurado na persona.
- Uso de `{{EXPRESSOES_ASSINATURA}}` do escritorio.
- Ausencia de `{{TERMOS_A_EVITAR}}` declarados pelo titular.
- **Filtro do magistrado experiente:** um juiz com 20 anos de banca le isso e pensa "peca seria, tecnica, respeitosa"? Ou "peca amadora, tom inadequado, falta fundamentacao"?

**Veredito consolidado:**
- **APROVADO** → entrega ao titular.
- **APROVADO COM RESSALVAS** → entrega com nota de ajustes sugeridos.
- **REPROVADO** → volta com motivos especificos.

---

## Bypass — quando NAO usar Suprema Corte

Nao faz sentido rodar 4 rodadas de auditoria para:
- Rascunho rapido que voce mesmo vai revisar.
- Resposta curta de WhatsApp ao cliente.
- Simulacao exploratoria ("me mostra como ficaria X").
- Ajuste cosmetico em peca ja aprovada.

### 3 formas de bypass

1. **Session-only (recomendado):** `/corte off` no inicio da sessao. Vale ate fechar o Claude Code.
2. **Por prompt (ad-hoc):** adicionar `--no-corte` ou `--quick` no final do seu pedido. Ex:
   - "Elabore uma minuta de NDA simples --quick"
   - "Me mostra como ficaria a peca de contestacao --no-corte"
3. **Permanente (nao recomendado):** `/cowork-set suprema_corte.enabled false`. So faca se voce sabe o que esta fazendo.

**Importante:** o hook `UserPromptSubmit` detecta o bypass e informa no output que a peca saira sem validacao. Zero surpresa.

---

## Configuracao avancada

### Tipos de tarefa submetidos automaticamente

Por default, Suprema Corte roda em:
- `pecas` (peticoes, recursos, contestacoes).
- `contratos` (minutas, acordos, instrumentos).
- `pareceres` (opinioes formais, legal opinions).

Pra ajustar, edite `state.suprema_corte.auto_apply_to`:
```bash
/cowork-set suprema_corte.auto_apply_to '["pecas","contratos","pareceres","comunicacao-cliente"]'
```

Opcoes suportadas: `pecas`, `contratos`, `pareceres`, `comunicacao-cliente`, `tudo`.

### Threshold de bypass automatico

Tarefas com output esperado abaixo de N palavras recebem sugestao de bypass automatico:
```bash
/cowork-set suprema_corte.bypass_threshold_words 300
```

Default: 200. `0` = nunca sugerir bypass.

---

## Erros comuns

**"A Suprema Corte esta me travando — eu so queria uma resposta rapida."**
→ Use `--quick` ou `/corte off`. A Suprema Corte existe para entregas finais, nao para exploracao.

**"R4 reprovou 3 vezes seguidas a mesma peca."**
→ R4 audita contra o padrao do escritorio (`{{TOM_VOZ_PERFIL}}` + expressoes + termos proibidos). Revise a persona (`<COWORK>/.dev-adv/persona.md`). Talvez o tom configurado nao combine com o estilo que voce usa agora.

**"R2 cita precedente que eu nao consigo validar no tribunal."**
→ E bom sinal — significa que o Protocolo Jurisprudencial funcionou e marcou o precedente como "Nivel 2 (indicativa)" ou reportou Nivel 3. Nunca cite precedente nivel 3 como se fosse comprovado.

**"Demora muito."**
→ Suprema Corte real roda em ~3-5 min por peca complexa. Se demora mais, rode `/cowork-doctor` — hooks lentos sao detectaveis.

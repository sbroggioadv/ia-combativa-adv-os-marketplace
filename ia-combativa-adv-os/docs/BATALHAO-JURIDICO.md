# BATALHAO JURIDICO — Arquitetura do Plugin

O plugin organiza as skills em uma **metafora militar** para deixar claro como elas se relacionam. Nenhuma skill trabalha sozinha — todas respondem ao General e passam pela Suprema Corte antes da entrega final.

---

## Organograma

```
                         FIRM-MASTER (General CTO)
                                 |
        ┌────────────────────────┼────────────────────────┐
        |                        |                        |
   ESTADO-MAIOR               TENENTES               TRANSVERSAIS
 (inteligencia)           (producao)           (apoio operacional)
        |                        |                        |
  ┌─────┼─────┐          ┌───────┼───────┐         ┌──────┼──────┐
  estrategia            contencioso    consultivo    escritorio     financeiro
  analise               + marketing    + extrajud.   + calculo      + comunicacao
  jurisprudencia                                     + visual-law

                    SUPREMA CORTE (quality gate)
              R1 Coleta → R2 Base → R3 Tese → R4 Completude
                                 |
                        ENTREGA AO TITULAR

                   INFRAESTRUTURA (invisivel)
      memory-evolver • cowork-sync • cowork-onboarding
```

---

## General — `firm-master`

**Funcao:** orquestrador. Toda tarefa juridica passa primeiro por ele.

**O que faz:**
1. Recebe o pedido do titular.
2. Identifica qual Tenente ativar (peca, contrato, parecer, comunicacao, etc).
3. Antes de delegar, aciona o Estado-Maior para diagnostico estrategico.
4. Apos producao pelo Tenente, aciona a Suprema Corte para auditoria.
5. Entrega o output final com veredito consolidado.

**Invariante.** Sempre carregado.

---

## Estado-Maior (3 skills — inteligencia estrategica)

### `estrategia-de-caso`
Define linha de atuacao (reativa / ofensiva / mista), tese central, pontos fortes, vulneraveis, cenarios favoravel/neutro/adverso.

### `analise-trilateral`
4 perspectivas simultaneas: cliente (o que ele precisa), adversario (o que argumentara), magistrado (como decidira), sintese estrategica (o que faremos).

### `jurisprudencia-estrategica`
Pesquisa + aplicacao cirurgica. Protocolo anti-alucinacao: validar cada precedente com **tribunal + numero + data + relator**. 3 niveis: validada / indicativa / impossibilidade.

---

## Tenentes — Contencioso (5 skills)

### `pecas-processuais`
Motor principal — peticao inicial, contestacao, recursos, tutelas, embargos. Estrutura combativa configuravel.

### `peticao-universal`
Peticoes simples — requerimentos, manifestacoes, intercorrentes.

### `contrarrazoes-recursais`
Blindagem de decisoes favoraveis + desmonte de recursos adversos.

### `replica-estrategica`
Desconstrucao cirurgica da contestacao (art. 341 CPC — fatos incontroversos).

### `resumo-audiencia`
Ata estruturada + analise estrategica pos-audiencia.

---

## Tenentes — Consultivo / Contratos (5 skills)

### `contratos-societarios`
Contratos sociais (LTDA/SLU/S/A), holdings, acordos de socios, COF (Lei 13.966/2019), M&A.

### `minutas-contratuais`
Contratos B2B entre partes — prestacao, fornecimento, parceria, NDAs, distratos. Semaforo VERDE/AMARELO/VERMELHO em revisoes.

### `parecer-juridico`
Estrutura formal — ementa, fundamentacao hierarquizada, analise do caso, conclusao categorica, recomendacao pratica.

### `due-diligence`
Auditoria pre-contratual / M&A — societaria, fiscal, contenciosa, contratual, regulatoria, imobiliaria.

### `contrato-social-holding`
Especialista em holdings — 4 celulas patrimoniais + clausulas de blindagem (incomunicabilidade, impenhorabilidade, inalienabilidade, golden share, tag along).

---

## Tenentes — Extrajudicial / Compliance / Comunicacao / Marketing (4 skills)

### `documentos-extrajudiciais`
Notificacoes, cartas de cobranca, interpelacoes, rescisoes, distratos, termos de acordo, confissoes de divida. Consciencia probatoria futura.

### `compliance-lgpd`
Mapeamento de dados, RIPD, politica de privacidade, termos de uso, resposta a incidente ANPD.

### `comunicacao-cliente`
Email, WhatsApp, cartas, cobrancas, atualizacoes processuais. 10 destinatarios, 8 formatos por canal. Conformidade Prov. 205/2021 CFOAB.

### `marketing-juridico`
7 formatos (carrossel, reels, thread LinkedIn, legenda, stories, artigo, podcast). OAB-compliant. Opt-in (nem todo escritorio faz marketing).

---

## Transversais (3 skills)

### `escritorio-advocacia`
Gestao operacional — prazos, audiencias, dossie, cadastro, relatorios, proposta de honorarios. Le ferramentas declaradas em `tools` (zero hardcode de marcas).

### `financeiro-juridico`
Fluxo de caixa, DRE, recebiveis, rateio entre socios, comparativo tributario do escritorio. Complementar a `calculo-juridico` (processual).

### `calculo-juridico`
Calculos vinculados a processos — trabalhistas, civil, previdenciario, tributario. Memoria de calculo auditavel.

### `visual-law`
Quadro resumo, timeline, mapa de provas, tabelas comparativas. Complementa peca densa, nao substitui.

---

## Suprema Corte (4 revisoras — quality gate)

Toda peca, contrato ou parecer passa por 4 revisoras antes de chegar ao titular:

### R1 — `suprema-corte-r1-coleta`
Audita **completude factual**. Pergunta: falta informacao? fatos incontroversos claros? cronologia precisa? partes qualificadas?

### R2 — `suprema-corte-r2-base-juridica`
Audita **legislacao vigente + jurisprudencia validada + doutrina**. Protocolo anti-alucinacao: cada citacao valida ou marcada como "indicativa".

### R3 — `suprema-corte-r3-tese`
Audita **tripe FATO → NEXO → DIREITO**. A tese tem fato comprovado? Nexo logico para a norma? Unicidade (uma tese central, nao multiplas)?

### R4 — `suprema-corte-r4-completude`
Audita **padrao do escritorio + estrutura + formatacao + filtro do magistrado experiente**. Emite **veredito consolidado:** APROVADO / APROVADO COM RESSALVAS / REPROVADO.

### Bypass
- `/corte off` — session-only.
- Flags no prompt: `--no-corte`, `--quick`, `--no-suprema`.
- Permanente (nao recomendado): `/cowork-set suprema_corte.enabled false`.

---

## Infraestrutura (invisivel mas essencial)

### `cowork-onboarding`
Conduz o wizard `/start`. So aparece na primeira instalacao ou em atualizacao.

### `memory-evolver`
Consolida automaticamente `MEMORY.md` de cada area aplicando regra de bloat (200 linhas maximo). Acionada pelo hook `PostToolUse(Edit|Write)` + manualmente via `/cowork-doctor --memory-gc` ou `/memory-evolver gc`.

### `cowork-sync`
Fingerprint SHA256 das skills/scripts/templates. Detecta divergencia entre maquinas do mesmo mentorado. Nunca puxa git automaticamente — acao manual.

---

## Fluxo tipico de uma tarefa complexa

**Cenario:** titular pede "Elabore uma peticao inicial para acao de despejo."

1. **UserPromptSubmit hook** detecta keyword "peticao" → injeta instrucao Suprema Corte.
2. **firm-master** recebe, confirma que e tarefa de peca processual.
3. **firm-master** aciona **Estado-Maior**:
   - `estrategia-de-caso` mapeia tese (despejo por falta de pagamento? por denuncia vazia? por cumprimento irregular?).
   - `analise-trilateral` avalia 4 perspectivas.
   - `jurisprudencia-estrategica` busca precedentes.
4. **firm-master** aciona **Tenente `pecas-processuais`**:
   - Aplica protocolo 4-etapas (questionamento → estrutura → validacao → "REALIZE A TAREFA").
   - Produz peca em formato do escritorio com papel timbrado.
5. **firm-master** aciona **Suprema Corte R1 → R2 → R3 → R4** sequencialmente.
6. Se R4 aprovou, entrega ao titular.
7. **Hook PostToolUse** detecta que o titular editou o output → registra em pending para memory-evolver consolidar nos MEMORY.md da area correspondente.

Tempo tipico: 3-7 minutos (depende da complexidade e se usuario pulou protocolo com `--quick`).

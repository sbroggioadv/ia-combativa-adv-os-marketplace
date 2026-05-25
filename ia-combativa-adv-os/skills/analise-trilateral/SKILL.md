---
name: analise-trilateral
description: >
  ANALISE-TRILATERAL — Inteligencia multi-perspectiva em 4 fases. Skill do Estado-Maior do Batalhao Juridico. Executa analise do caso simultaneamente sob 3 perspectivas (advogado do cliente, advogado adversario, magistrado imparcial) + sintese estrategica. Visao 360 graus para teste de resistencia da tese antes de producao documental. Use SEMPRE em caso complexo antes de peca/contrato/parecer. Ativar quando mencionar "analise trilateral", "visao 360", "perspectiva do juiz", "como o adversario vai reagir", "teste de resistencia da tese", "multi-agente", "analise completa do caso".
---

# ANALISE-TRILATERAL — Inteligencia Multi-Perspectiva

## 1. POSICAO NO BATALHAO

Skill do **Estado-Maior Estrategico**, subordinada ao `firm-master`. Tecnica multi-agente: assume 3 perspectivas diferentes em sequencia para teste de resistencia de teses.

**Funcao:** Simular as 3 perspectivas reais do processo (advogado aliado, adversario, magistrado) para produzir analise mais robusta do que qualquer perspectiva isolada. Resultado alimenta os Tenentes de producao com inteligencia tatica testada.

Opera sob perfil `{{TOM_VOZ_PERFIL}}` configurado.

---

## 2. PROTOCOLO DE 4 FASES — OBRIGATORIO

As 4 fases sao **sequenciais e invariaveis**. Nao pular, nao reordenar.

---

## 3. FASE 1 — PERSPECTIVA DO ALIADO (Advogado do Cliente)

Assuma o papel de advogado senior do MESMO LADO do cliente. Objetivo: **FORTALECER** a posicao.

### 3.1 MELHORES ARGUMENTOS
5 argumentos mais fortes, em ordem de impacto.

### 3.2 PROVAS FAVORAVEIS
- Documentais (contratos, atas, comprovantes)
- Testemunhais (depoimentos possiveis)
- Periciais (laudos tecnicos cabiveis)

### 3.3 JURISPRUDENCIA A FAVOR
Hierarquizada:
- **Vinculante** (sumulas vinculantes, repercussao geral, repetitivos)
- **Orientadora** (jurisprudencia dominante)
- **Reforco** (decisoes pontuais alinhadas)

Aplicar Protocolo Jurisprudencial de 3 niveis (ver skill `jurisprudencia-estrategica`).

### 3.4 ESTRATEGIA OFENSIVA
Como atacar os pontos fracos da parte adversa.

### 3.5 PONTOS A EXPLORAR
Fatos ou circunstancias subutilizados que podem virar trunfo.

### 3.6 RECOMENDACOES
Acoes concretas para maximizar chances de exito.

**Tom nesta fase:** `{{TOM_VOZ_PERFIL}}` — combativo se perfil combativo, diplomatico firme se cordial, explicativo se didatico.

---

## 4. FASE 2 — PERSPECTIVA DA PARTE CONTRARIA (Advogado Adversario)

Assuma o papel de advogado da PARTE CONTRARIA. Objetivo: **DESTRUIR** os argumentos do cliente.

### 4.1 FRAGILIDADES
Onde a tese do cliente e mais vulneravel.

### 4.2 CONTRA-ARGUMENTOS
5 melhores argumentos de defesa, fundamentados em lei e jurisprudencia.

### 4.3 PROVAS CONTRA
Fatos ou documentos que enfraquecem a posicao do cliente.

### 4.4 JURISPRUDENCIA CONTRARIA
Precedentes que favorecem a defesa / contra o cliente.

### 4.5 PRELIMINARES POSSIVEIS
Questoes processuais que poderiam barrar o caso (incompetencia, ilegitimidade, inepcia, prescricao).

### 4.6 ESTRATEGIA DE DEFESA
Como desconstruir cada argumento do cliente, ponto a ponto.

### 4.7 RECONVENCAO
Possibilidade e contornos de contra-ataque via reconvencao.

**Tom nesta fase:** agressivo e tecnico. **Encontrar TODAS as fraquezas.** Se esta fase nao for honesta, toda a analise fica inutil.

---

## 5. FASE 3 — PERSPECTIVA DO MAGISTRADO (Juiz Imparcial)

Assuma o papel de MAGISTRADO julgador. Objetivo: **DECIDIR** com base na lei, provas e jurisprudencia. **Sem vies.**

### 5.1 FATOS INCONTROVERSOS
O que ambas as partes concordam (nao vai precisar de prova).

### 5.2 PONTOS CONTROVERTIDOS
Questoes que dependem de prova para serem decididas.

### 5.3 PESO DAS PROVAS (tabela)

| Ponto Controvertido | Prova do Autor | Peso | Prova do Reu | Peso | Tendencia |
|---|---|---|---|---|---|

### 5.4 ENQUADRAMENTO JURIDICO
Legislacao aplicavel vigente em `{{ANO_VIGENTE}}` e interpretacao dominante.

### 5.5 JURISPRUDENCIA DETERMINANTE
Precedentes vinculantes que fixam o entendimento.

### 5.6 TENDENCIA DE JULGAMENTO
Resultado mais provavel com base no conjunto de provas e lei aplicavel.

### 5.7 O QUE MUDARIA O JULGAMENTO
O que cada parte precisaria provar para reverter a tendencia atual.

### 5.8 ESTIMATIVA (tabela)

| Cenario | Probabilidade | Fundamentacao |
|---|---|---|
| Procedencia total | | |
| Procedencia parcial | | |
| Improcedencia | | |

**Tom nesta fase:** **imparcial, tecnico, fundamentado.** **Sem vies.** Se esta fase contaminar vies favoravel ao cliente, a analise perde valor.

---

## 6. FASE 4 — SINTESE ESTRATEGICA

Com as 3 perspectivas completas, consolidar:

### 6.1 DIAGNOSTICO CONSOLIDADO

- **Pontos fortes confirmados** (Aliado + Magistrado concordam — verdadeiros trunfos)
- **Vulnerabilidades reais** (Contraria + Magistrado concordam — riscos confirmados)
- **Pontos controversos** (3 perspectivas divergem — exigem decisao estrategica)

### 6.2 MAPA DE PROVAS CRITICAS

| Ponto | Status da Prova | Impacto se Provado | Impacto se Nao Provado | Acao |
|---|---|---|---|---|

### 6.3 RECOMENDACAO FINAL

- **Probabilidade de exito ajustada** (mais realista que a Fase 1 original)
- **Acoes ANTES de ajuizar/formalizar** (obter provas, reforcar fatos, descartar teses fracas)
- **Argumentos a priorizar** (confirmados pelo teste trilateral)
- **Argumentos a abandonar** (fragilizados pela Fase 2 ou 3)
- **Alternativas ao litigio** (quando risco alto — acordo, mediacao, arbitragem)

---

## 7. PROIBICOES ABSOLUTAS

- NUNCA pular fases — as 4 sao obrigatorias e sequenciais
- NUNCA fabricar jurisprudencia em qualquer perspectiva (aplicar Protocolo de 3 niveis)
- NUNCA contaminar a perspectiva do Magistrado com vies favoravel ao cliente (se fizer isso, esta fase vira placebo)
- NUNCA omitir vulnerabilidades identificadas na Fase 2 (se a Fase 2 e honesta, a sintese fica util)
- NUNCA terminar sem a Fase 4 (sintese e o que transforma 3 analises em decisao)

---

## 8. INTEGRACAO COM OUTRAS SKILLS DO ESTADO-MAIOR

Esta skill e chamada **depois de `estrategia-de-caso`** (que definiu a tese inicial) e **antes de `jurisprudencia-estrategica`** (que vai validar os precedentes em cada perspectiva).

Ordem fixa do Estado-Maior: **`estrategia-de-caso` → `analise-trilateral` → `jurisprudencia-estrategica` → Tenente**.

---

## 9. VALIDACAO — SUPREMA CORTE

A analise trilateral alimenta os Tenentes de producao. A Suprema Corte (R1-R4) verifica na peca final se a estrategia derivada da trilateral foi corretamente implementada — especialmente:

- **R3 (Tese)** verifica se a tese resistiu aos 3 testes
- **R3 (Antecipacao adversaria)** verifica se argumentos da Fase 2 foram neutralizados na peca

---

*analise-trilateral — Estado-Maior. Aguardando o caso para teste de 4 fases.*

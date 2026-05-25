---
name: cowork-sync
description: >
  COWORK-SYNC — Skill de infraestrutura para sincronizacao multi-dispositivo. Mantem um fingerprint SHA256 + tamanho de cada SKILL.md instalada do plugin em `<COWORK>/.dev-adv/AUTO-DEPLOY.md`. Ao rodar (via `/cowork-status`, `/cowork-doctor`, hook SessionStart silencioso, ou comando explicito), compara o fingerprint local com o do plugin e alerta se houver divergencia — sinalizando que outra maquina do mesmo mentorado pode ter atualizado o plugin (via `git pull`). Diferente do padrao AUTO-DEPLOY do plugin-fonte do Mentor (que rebuilda .zip): aqui o auto-deploy e `git pull` no repositorio do plugin — a skill apenas detecta divergencia. Use quando o usuario pedir "verificar versao do plugin", "sincronizar entre maquinas", "qual a ultima versao", "cowork-sync", "status do plugin", ou quando o hook SessionStart detectar divergencia automaticamente.
---

# COWORK-SYNC — Fingerprint Multi-dispositivo

## 1. POSICAO NO BATALHAO

**Skill de infraestrutura**, subordinada ao `firm-master`. Garante consistencia do plugin entre as 2-4 maquinas que um mesmo mentorado tipicamente utiliza (ex: desktop do escritorio + notebook em casa + mac de viagem).

**Principio central:** o plugin e um repositorio git. `git pull` e o auto-deploy. Esta skill apenas **detecta divergencia** entre o fingerprint atual das skills instaladas e o fingerprint registrado pela ultima operacao bem-sucedida de `/start` ou `/cowork-sync --refresh`.

---

## 2. DIFERENCA VS AUTO-DEPLOY DO PLUGIN-FONTE

O plugin-fonte (escritorio-modelo READ-ONLY, fora deste plugin) usa arquivo `.plugin` (zip) como unidade de distribuicao, e `AUTO-DEPLOY.md` instrui rebuild do zip quando a fonte muda.

Neste plugin (`Plugin-Ia-Combativa-Adv-OS`):
- Fonte e **repositorio git publico (privado ao time) hospedado no GitHub**.
- Update e via `git pull` no clone local do plugin.
- `AUTO-DEPLOY.md` apenas **registra snapshot** das skills no momento do ultimo `/start` — serve de baseline para comparacao posterior.
- Skill nao rebuilda nada — apenas detecta e sugere acao manual ao mentorado.

---

## 3. ARQUIVO CANONICO — `<COWORK>/.dev-adv/AUTO-DEPLOY.md`

Estrutura:

```markdown
# AUTO-DEPLOY — Fingerprint do Plugin

> Snapshot das 21 skills instaladas no momento da ultima operacao bem-sucedida.
> Gerado automaticamente pelo plugin. NAO editar manualmente.

**Plugin versao:** 0.1.0-alpha.6
**Gerado em:** 2026-04-17T14:25:00Z
**Maquina:** <hostname>
**Sistema:** <win/mac/linux>

## Fingerprint das Skills

| Skill | SHA256 (8 chars) | Bytes |
|---|---|---|
| firm-master | `abc12345` | 11024 |
| suprema-corte-r1-coleta | `def67890` | 4321 |
| ... | ... | ... |

## Scripts

| Script | SHA256 (8 chars) | Bytes |
|---|---|---|
| state.py | `...` | ... |
| render.py | `...` | ... |
| ... | ... | ... |

## Templates

| Template | SHA256 (8 chars) | Bytes |
|---|---|---|
| persona.md.tpl | `...` | ... |
| ... | ... | ... |
```

---

## 4. FLUXO — DETECCAO DE DIVERGENCIA

### 4.1 Acionamento (4 gatilhos)

1. **Hook SessionStart silencioso** — compara fingerprint atual com o AUTO-DEPLOY.md. Se divergente, imprime aviso curto no console de inicio de sessao:
   ```
   [cowork-sync] Divergencia detectada em 3 skills. Rode /cowork-sync para detalhes.
   ```
2. **Comando `/cowork-status`** — mostra divergencia detalhada como parte do status geral.
3. **Comando `/cowork-doctor`** — detecta divergencia como um dos 15+ checks.
4. **Comando explicito `/cowork-sync`** — forca verificacao + oferece acao.

### 4.2 Diagnose

A skill:
1. Le `<COWORK>/.dev-adv/AUTO-DEPLOY.md` (baseline).
2. Calcula fingerprint atual de todas as skills/scripts/templates do plugin instalado.
3. Compara linha a linha.
4. Classifica divergencias:
   - **ADICIONADA:** skill nova no plugin que nao estava no baseline → provavelmente update do plugin.
   - **REMOVIDA:** skill que estava no baseline e sumiu → incomum; pode ser erro de instalacao.
   - **MODIFICADA:** SHA256 diferente → update de conteudo.

### 4.3 Acao proposta ao usuario

```
COWORK-SYNC — Divergencia detectada

Plugin instalado em: <path>
Baseline registrado: 2026-04-15T10:00Z
Agora:               2026-04-17T14:25Z

Skills modificadas:  3
  - firm-master (baseline abc12345 vs agora xyz98765)
  - suprema-corte-r1-coleta (...)
  - ...

Skills adicionadas:  2
  - memory-evolver (nova no plugin)
  - cowork-sync (nova no plugin)

Diagnostico provavel: plugin foi atualizado via `git pull` em outra maquina
(ou nesta mesma sessao anterior). Baseline esta desatualizado.

Acoes:
  [1] Aceitar o plugin atual como novo baseline (refresh AUTO-DEPLOY.md).
  [2] Inspecionar diff antes de aceitar (abrir cada skill).
  [3] Reverter via `git checkout <commit>` no repo do plugin.
  [4] Nao fazer nada agora.

Qual acao? (1/2/3/4)
```

### 4.4 Refresh (acao 1)

Regenera `<COWORK>/.dev-adv/AUTO-DEPLOY.md` com fingerprint atual. Resultado: divergencia zerada.

---

## 5. MULTI-DISPOSITIVO — CENARIO TIPICO

Mentorado tem:
- Desktop escritorio (Windows) — plugin clone em `C:\dev\plugins\ia-combativa-adv-os\`.
- Notebook casa (Windows) — mesmo clone em path equivalente.
- Mac de viagem — clone em `~/dev/plugins/ia-combativa-adv-os/`.

Cada maquina mantem seu proprio `<COWORK>/.dev-adv/AUTO-DEPLOY.md` — o COWORK e local, nao sincronizado entre maquinas (dados de cliente nao devem ir para cloud).

Update tipico do plugin:
1. Mentorado roda `git pull` no clone do desktop.
2. Skill detecta divergencia no proximo SessionStart do desktop; mentorado aceita (refresh baseline).
3. Uma semana depois, mentorado liga o notebook de casa.
4. SessionStart no notebook detecta divergencia — AUTO-DEPLOY.md do notebook esta desatualizado.
5. Aviso sugere `git pull` no clone do notebook + `/cowork-sync --refresh`.

**A skill nao puxa git automaticamente** — acao manual do usuario e preferida (controle + auditoria).

---

## 6. SCRIPT HELPER — `scripts/fingerprint.py`

A skill usa o script helper `scripts/fingerprint.py` para calcular fingerprints.

Interface:
```bash
# Gerar fingerprint atual e imprimir (modo relatorio)
python scripts/fingerprint.py --plugin-root <path> --out -

# Atualizar AUTO-DEPLOY.md no COWORK (refresh baseline)
python scripts/fingerprint.py --plugin-root <path> --cowork <cowork-path> --update-auto-deploy

# Comparar baseline com estado atual
python scripts/fingerprint.py --plugin-root <path> --cowork <cowork-path> --diff
```

Saida de `--diff` em JSON:
```json
{
  "baseline_generated_at": "2026-04-15T10:00Z",
  "current_at": "2026-04-17T14:25Z",
  "modified": [{"item": "firm-master", "type": "skill", "baseline_sha": "abc12345", "current_sha": "xyz98765"}],
  "added": [{"item": "memory-evolver", "type": "skill", "current_sha": "..."}],
  "removed": []
}
```

---

## 7. PROIBICOES

- NUNCA executar `git pull` ou `git checkout` automaticamente — acao manual do usuario.
- NUNCA sobrescrever AUTO-DEPLOY.md sem confirmacao quando ha divergencia (exceto em refresh explicito).
- NUNCA falhar em SessionStart se AUTO-DEPLOY.md ausente — apenas gerar silenciosamente como novo baseline.
- NUNCA acessar ou enviar dados do COWORK a repositorios git externos.

---

## 8. INTEGRACAO

- **`firm-master`** — orquestrador.
- **Hook `SessionStart`** — verificacao silenciosa na entrada de sessao.
- **Command `/cowork-status`** — mostra resumo de divergencia.
- **Command `/cowork-doctor`** — inclui check de sync nos 15+ testes.
- **Command `/cowork-sync`** — comando explicito com 4 acoes (accept/diff/revert/skip).
- **Script `scripts/fingerprint.py`** — helper que calcula e compara.
- **`cowork-onboarding` (`/start`)** — gera AUTO-DEPLOY.md inicial no primeiro setup.

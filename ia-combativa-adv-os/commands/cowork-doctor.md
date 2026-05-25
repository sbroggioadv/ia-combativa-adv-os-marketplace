---
description: Diagnostica e (opcionalmente) auto-repara problemas comuns do workspace COWORK. Suporta --fix, --memory-gc, --verbose.
allowed-tools: Bash, Read, Edit, Write
---

Voce foi acionado pelo comando `/cowork-doctor`. Execute o diagnostico completo do workspace COWORK ativo e opcionalmente aplique reparos automaticos.

## FLAGS SUPORTADAS

- `--fix` — aplica correcoes automaticas quando possivel.
- `--memory-gc` — aplica regra de bloat em todos os MEMORY.md via skill `memory-evolver`.
- `--verbose` — mostra detalhes de cada check.
- (sem flag) — so diagnostica, reporta status.

## PROTOCOLO

### 1. Localizar COWORK

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/find-cowork.py"
```

Se nao encontrar:
> "Nenhum workspace COWORK configurado neste diretorio. Rode `/start` para configurar."

Se encontrar, guardar como `$COWORK`.

### 2. Executar 15+ checks

Rodar cada check abaixo e classificar como **OK / WARN / FAIL**. Em modo `--fix`, tentar reparar FAILs com solucao determinista.

#### Checks de estrutura
1. **state.json valido** — `python scripts/state.py validate "$COWORK"` → OK/FAIL (com detalhe dos erros).
2. **persona.md existe** em `<COWORK>/.dev-adv/persona.md` — OK/FAIL (fix: `python scripts/render.py "$COWORK" --only persona.md`).
3. **persona aponta para COWORK correto** — conferir `persona_path` no state vs arquivo real.
4. **CLAUDE.md raiz do COWORK** existe — OK/WARN (fix: render).
5. **.gitignore do COWORK** existe e inclui `.dev-adv/.snapshots/`, `.dev-adv/.backup/`, `.dev-adv/.hook-state.json` — OK/WARN (fix: adicionar linhas).
6. **areas do state x pastas reais** — cada area em `state.areas[]` tem pasta em disco? cada pasta tem area no state? — OK/WARN (fix: sugere `/cowork-add-area` ou `/cowork-remove-area`).
7. **Por area: CLAUDE.md + MEMORY.md existem** — OK/WARN (fix: render).

#### Checks de skills
8. **Skills invariantes presentes** (firm-master + 4 Suprema Corte) — listar arquivos em `${CLAUDE_PLUGIN_ROOT}/skills/` e conferir.
9. **Skills opt-in declaradas existem no disco** — para cada skill em `state.skills.opt_in_active`, ver se `${CLAUDE_PLUGIN_ROOT}/skills/<slug>/SKILL.md` existe.

#### Checks de settings
10. **`.claude/settings.local.json` aponta COWORK_PERSONA** para persona deste workspace — OK/WARN (fix: render settings-local.json.tpl).
11. **Env var COWORK_PATH** (opcional) — se definida, bate com `$COWORK`? — INFO.

#### Checks de sincronizacao (delegar a skill `cowork-sync`)
12. **AUTO-DEPLOY.md existe** em `<COWORK>/.dev-adv/AUTO-DEPLOY.md` — OK/WARN (fix: rodar `python scripts/fingerprint.py --plugin-root "${CLAUDE_PLUGIN_ROOT}" --cowork "$COWORK" --update-auto-deploy`).
13. **Fingerprint divergente?** — rodar `python scripts/fingerprint.py --plugin-root "${CLAUDE_PLUGIN_ROOT}" --cowork "$COWORK" --diff` e reportar contagem de added/modified/removed. Em `--fix` NAO atualizar sozinho — apenas sugerir `/cowork-sync`.

#### Checks de seguranca e LGPD
14. **COWORK NAO esta em pasta sincronizada** (iCloud, OneDrive, Dropbox, Google Drive, Box) — verificar path e WARN se detectar padrao de sync folder. Nao ha fix automatico — apenas orientacao.
15. **Permissoes** — `<COWORK>/.dev-adv/` nao deve estar com permissao mundialmente legivel em sistemas Unix. Em Win, apenas informativo.

#### Checks de memoria (se `--memory-gc`)
16. **MEMORY.md de cada area < 200 linhas** — acionar skill `memory-evolver` para cada area que exceder threshold.
17. **Snapshots antigos** em `.snapshots/` > 20 arquivos → auto-prune para 20 mais recentes.

### 3. Report final

Imprimir tabela compacta:

```
COWORK-DOCTOR — <COWORK path>

[OK]   01. state.json valido
[OK]   02. persona.md existe
[WARN] 03. .gitignore sem entrada para .backup/
         (fix automatico aplicado)
[FAIL] 06. area "CONTENCIOSO-CIVEL" no state sem pasta correspondente
         (sugerido: /cowork-remove-area contencioso-civel OU criar pasta manualmente)
[INFO] 11. COWORK_PATH env nao definido
...

Resumo: 13 OK / 1 WARN / 1 FAIL / 2 INFO.
Acoes automaticas aplicadas: 1 (em modo --fix).
Pendente de acao manual: 1 FAIL.
```

Em modo padrao (sem `--fix`), listar o comando exato que o usuario pode rodar para corrigir cada WARN/FAIL.

### 4. Integracao com outras skills

- Divergencia de fingerprint → sugerir rodar `/cowork-sync`.
- Necessidade de consolidar memorias → oferecer `--memory-gc`.
- Problema de renderizacao → sugerir `/cowork-update`.

## PROIBICOES

- NUNCA deletar arquivo do usuario sem confirmacao explicita.
- NUNCA escrever fora do COWORK ativo.
- NUNCA rodar `git` no plugin ou no COWORK automaticamente.
- NUNCA executar `--fix` se houver WARN que envolva mudanca potencialmente destrutiva (ex: remover area com pasta de clientes).

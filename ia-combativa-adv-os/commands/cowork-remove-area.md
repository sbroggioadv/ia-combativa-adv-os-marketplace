---
description: Remove uma area do workspace state (preserva pasta fisica - usuario deleta manualmente se quiser).
allowed-tools: Bash, Read
argument-hint: <slug-area>
---

Voce foi acionado pelo comando `/cowork-remove-area`. Desativa uma area do state.

Argumento: `$ARGUMENTS`

## REGRA IMPORTANTE

Este comando **apenas desativa** a area no state. A pasta fisica `<COWORK>/<SLUG>/` com seus arquivos **NAO e deletada** — preservamos dados do usuario (clientes, processos, modelos) por seguranca.

Se o usuario quiser tambem deletar os arquivos, deve faze-lo manualmente ou pedir explicitamente com warning.

## PROTOCOLO

### 1. Localizar COWORK

```bash
COWORK=$(python "${CLAUDE_PLUGIN_ROOT}/scripts/find-cowork.py")
```

### 2. Verificar se area existe

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/state.py" show "$COWORK"
```

Se `<SLUG>` nao esta em `areas[]`, informar:

> "Area <SLUG> nao esta ativa neste workspace. Veja areas ativas com `/cowork-status`."

### 3. Confirmar com o usuario

Mostrar:

```
Voce quer desativar a area '<SLUG>' do state?

A pasta fisica $COWORK/<SLUG>/ NAO sera deletada (preservamos seus dados).
A area pode ser reativada depois com /cowork-add-area <SLUG>.

Confirma? (s/n)
```

Aguardar confirmacao.

### 4. Remover do state

Via Python inline:

```bash
python -c "
import json, sys
from datetime import datetime, timezone

with open('$COWORK/.dev-adv/cowork-state.json') as f:
    st = json.load(f)

before = len(st['areas'])
st['areas'] = [a for a in st['areas'] if a['slug'] != '<SLUG>']
after = len(st['areas'])

if before == after:
    print('Area nao encontrada'); sys.exit(1)

st['updated_at'] = datetime.now(timezone.utc).isoformat()

sys.path.insert(0, '${CLAUDE_PLUGIN_ROOT}/scripts')
import state as s
errs = s.validate(st)
if errs:
    print('Erro validacao:', errs); sys.exit(1)
s.save('$COWORK', st)
"
```

### 5. Informar

```
Area <SLUG> desativada do state.

Pasta $COWORK/<SLUG>/ preservada (dados intactos).
Para reativar: /cowork-add-area <SLUG>
Para deletar pasta fisica: delete manualmente no explorador de arquivos.
```

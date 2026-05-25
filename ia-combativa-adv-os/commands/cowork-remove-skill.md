---
description: Desativa uma skill opt-in (move para opt_in_inactive para re-oferecer depois).
allowed-tools: Bash, Read
argument-hint: <nome-skill>
---

Voce foi acionado pelo comando `/cowork-remove-skill`. Desativa uma skill opt-in.

Argumento: `$ARGUMENTS`

## REGRA CRITICA

**Skills invariantes NAO podem ser removidas.** Se o usuario tentar remover `firm-master` ou qualquer `suprema-corte-*`, **recusar**.

## PROTOCOLO

### 1. Localizar COWORK

```bash
COWORK=$(python "${CLAUDE_PLUGIN_ROOT}/scripts/find-cowork.py")
```

### 2. Validar skill

Verificar no state:

- Se nome esta em `skills.invariants` -> recusar: "Skill <nome> e invariante (sempre ativa). Nao pode ser removida. Se quer desligar Suprema Corte temporariamente, use `/corte off`."
- Se nome nao esta em `skills.opt_in_active` -> informar: "Skill <nome> nao esta ativa atualmente."

### 3. Mover para `opt_in_inactive`

```bash
python -c "
import json, sys
from datetime import datetime, timezone

with open('$COWORK/.dev-adv/cowork-state.json') as f:
    st = json.load(f)

name = '<NOME_SKILL>'

if name in st['skills']['invariants']:
    print(f'ERRO: {name} e invariante. Nao pode ser removida.'); sys.exit(1)

if name not in st['skills']['opt_in_active']:
    print(f'{name} nao esta ativa.'); sys.exit(0)

st['skills']['opt_in_active'].remove(name)
if name not in st['skills']['opt_in_inactive']:
    st['skills']['opt_in_inactive'].append(name)
st['updated_at'] = datetime.now(timezone.utc).isoformat()

sys.path.insert(0, '${CLAUDE_PLUGIN_ROOT}/scripts')
import state as s
errs = s.validate(st)
if errs: print('ERRO:', errs); sys.exit(1)
s.save('$COWORK', st)
print(f'Skill {name} desativada (movida para opt_in_inactive).')
"
```

### 4. Informar

```
Skill <NOME> desativada.

Para reativar depois: /cowork-add-skill <NOME>

Nota: a skill permanece no plugin instalado, apenas nao sera acionada automaticamente pelo Claude Code nesta COWORK.
```

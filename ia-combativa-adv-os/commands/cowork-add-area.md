---
description: Adiciona uma nova area de atuacao ao workspace (cria pasta + CLAUDE.md + MEMORY.md + subpastas).
allowed-tools: Bash, Read, Write
argument-hint: <slug-area> [tipo_atuacao] [polo]
---

Voce foi acionado pelo comando `/cowork-add-area`. Adiciona uma area nova ao workspace.

Argumento: `$ARGUMENTS`

## CATALOGO DE AREAS RECONHECIDAS

```
CONTENCIOSO/CIVEL              Contencioso civel geral
CONTENCIOSO/CONSUMIDOR         Consumidor (defesa empresas / afastamento CDC)
CONTENCIOSO/TRABALHISTA        Reclamatorias e defesas trabalhistas
CONTENCIOSO/TRIBUTARIO         Execucoes fiscais, MS tributarios
CONTENCIOSO/FRANQUIAS          Litigios de franquia (Lei 13.966/19)
CONTENCIOSO/SOCIETARIO         Disputas societarias
CONSULTIVO/EMPRESARIAL         Pareceres, analise de risco, adequacao
CONSULTIVO/TRABALHISTA         Consultoria trabalhista preventiva
CONTRATOS-EMPRESARIAIS         Minutas, revisoes, fornecimento
DIREITO-ADMINISTRATIVO         Licitacoes, processos administrativos
SOCIETARIO-HOLDINGS            Holdings, estruturacao patrimonial
REGISTRO-MARCAS-PI             INPI, marcas, patentes, softwares
FAMILIA-SUCESSOES              Divorcios, inventarios, testamentos
CRIMINAL-EMPRESARIAL           Defesas criminais empresariais
```

Slugs fora do catalogo sao aceitos mas devem seguir convencao: CAIXA-ALTA com hifens ou barras (ex: `MEU-DIREITO-CUSTOMIZADO` ou `AREA/SUB`).

## PROTOCOLO

### 1. Parsear argumento

Formato: `<slug> [tipo_atuacao] [polo]`

- `<slug>` obrigatorio (catalogo acima ou custom)
- `[tipo_atuacao]` opcional: `contencioso` | `consultivo` | `misto` (default: `misto`)
- `[polo]` opcional: `autor` | `reu` | `ambos` | `null` (default: `null`)

Se slug for de contencioso (catalogo), default `tipo_atuacao=contencioso`. Idem consultivo. Se misto por natureza (ex: SOCIETARIO-HOLDINGS), default `misto`.

### 2. Localizar COWORK

```bash
COWORK=$(python "${CLAUDE_PLUGIN_ROOT}/scripts/find-cowork.py")
```

### 3. Ler state e verificar se area ja existe

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/state.py" show "$COWORK"
```

Se a area com mesmo slug ja existe em `areas[]`, informar:

> "Area <SLUG> ja esta ativa neste workspace. Use /cowork-status para ver detalhes."

### 4. Perguntar detalhes faltantes

Se `tipo_atuacao` nao fornecido e nao ha default obvio, perguntar.
Se `polo` nao fornecido, perguntar: "Voce atua predominantemente como (a) autor/requerente, (b) reu/requerido, ou (c) ambos? (Enter para pular)"

### 5. Sugerir skills opt-in correlatas

Baseado no slug, sugerir skills (se estao inativas):

- Conteciosas -> `pecas-processuais`, `peticao-universal`, `contrarrazoes-recursais`, `replica-estrategica`, `resumo-audiencia`
- Consultivas -> `parecer-juridico`, `due-diligence`, `minutas-contratuais`
- Contratos -> `contratos-societarios`, `minutas-contratuais`
- Holdings -> `contrato-social-holding`, `due-diligence`
- LGPD/Compliance -> `compliance-lgpd`

> "Sugestao: para essa area, skills uteis seriam X, Y, Z. Quer ativar alguma agora?"

Se usuario confirmar, chamar `/cowork-add-skill <nome>` para cada uma.

### 6. Adicionar area ao state

Construir objeto area:

```json
{
  "slug": "<SLUG>",
  "display_name": "<Nome amigavel>",
  "tipo_atuacao": "<tipo>",
  "polo_predominante": "<polo>",
  "subfolders": ["Clientes", "Processos", "Modelos", "Pesquisas", "Pareceres"],
  "skills_sugeridas": ["<lista>"],
  "activated_at": "<timestamp UTC ISO8601>"
}
```

Aplicar via state.py — como ele nao tem comando direto para "append em array", usar fluxo:

```bash
# 1. Ler areas atuais
CURRENT=$(python -c "import json; print(json.dumps(json.load(open('$COWORK/.dev-adv/cowork-state.json'))['areas']))")

# 2. Adicionar nova area ao array (via Python inline)
python -c "
import json
from datetime import datetime, timezone

with open('$COWORK/.dev-adv/cowork-state.json') as f:
    st = json.load(f)

new_area = {
  'slug': '<SLUG>',
  'display_name': '<NAME>',
  'tipo_atuacao': '<TIPO>',
  'polo_predominante': '<POLO_OR_NONE>',
  'subfolders': ['Clientes','Processos','Modelos','Pesquisas','Pareceres'],
  'skills_sugeridas': [],
  'activated_at': datetime.now(timezone.utc).isoformat()
}
st['areas'].append(new_area)

import sys
sys.path.insert(0, '${CLAUDE_PLUGIN_ROOT}/scripts')
import state as s
errs = s.validate(st)
if errs:
    print('ERRO:', errs); exit(1)
s.save('${CLAUDE_PLUGIN_ROOT_PLACEHOLDER}')  # na verdade usar path do cowork
"
```

Na pratica, como Bash-with-Python inline fica verboso, crie `scripts/add-area.py` para essa operacao e chame ele. Se ainda nao existir, faca a operacao via Python inline mesmo, seguindo o padrao acima.

### 7. Re-renderizar

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/render.py" "$COWORK" --only areas
```

Isso cria pasta `$COWORK/<SLUG>/` com CLAUDE.md + MEMORY.md + subpastas.

### 8. Confirmar

```
Area <SLUG> adicionada ao workspace.

Pasta criada: $COWORK/<SLUG>/
  CLAUDE.md        (contextualiza a area)
  MEMORY.md        (memoria especifica da area)
  Clientes/
  Processos/
  Modelos/
  Pesquisas/
  Pareceres/

Tipo de atuacao: <tipo>
Polo predominante: <polo>

Skills sugeridas para essa area: <lista>
  (ative com /cowork-add-skill <nome>)
```

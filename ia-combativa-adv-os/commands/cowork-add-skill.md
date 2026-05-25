---
description: Ativa uma skill opt-in do Batalhao Juridico.
allowed-tools: Bash, Read
argument-hint: <nome-skill>
---

Voce foi acionado pelo comando `/cowork-add-skill`. Ativa uma skill opt-in.

Argumento: `$ARGUMENTS`

## CATALOGO DE SKILLS OPT-IN DISPONIVEIS

```
ESTADO-MAIOR ESTRATEGICO
  estrategia-de-caso           define tese e linha de atuacao
  analise-trilateral           cliente + adversario + julgador
  jurisprudencia-estrategica   fundamentacao jurisprudencial

TENENTES CONTENCIOSO
  pecas-processuais            peticoes, contestacoes, recursos
  peticao-universal            estrutura universal qualquer area
  contrarrazoes-recursais      impugnacao de recursos adversos
  replica-estrategica          replica a contestacao
  resumo-audiencia             ata e resumo pos-audiencia

TENENTES CONSULTIVO/CONTRATOS
  contratos-societarios        contratos sociais, holdings, COF
  minutas-contratuais          redacao contratual empresarial
  parecer-juridico             pareceres tecnicos formais
  due-diligence                M&A, analise pre-contratual
  contrato-social-holding      holdings especificamente

COMPLIANCE / LGPD / ADMINISTRATIVO
  compliance-lgpd              LGPD, adequacao regulatoria
  documentos-extrajudiciais    notificacoes, interpelacoes

COMUNICACAO E MARKETING
  comunicacao-cliente          WhatsApp, email, comunicacao formal
  marketing-juridico           posicionamento institucional

TRANSVERSAIS
  escritorio-advocacia         gestao operacional (prazos, clientes)
  financeiro-juridico          honorarios, liquidacao, DRE
  calculo-juridico             correcao, juros, multas

EXTRA
  visual-law                   legal design, infograficos
```

Skills **invariantes** (sempre ativas, nao removiveis):
- `firm-master`
- `suprema-corte-r1-coleta`
- `suprema-corte-r2-base-juridica`
- `suprema-corte-r3-tese`
- `suprema-corte-r4-completude`

Ativar qualquer uma dessas via este comando **nao faz nada** (ja sao invariantes).

## PROTOCOLO

### 1. Localizar COWORK

```bash
COWORK=$(python "${CLAUDE_PLUGIN_ROOT}/scripts/find-cowork.py")
```

### 2. Validar nome da skill

Se nao esta no catalogo, informar e mostrar lista de disponiveis.

Se esta em `invariants`, informar que ja e sempre ativa.

### 3. Adicionar a `opt_in_active`

```bash
python -c "
import json, sys
from datetime import datetime, timezone

with open('$COWORK/.dev-adv/cowork-state.json') as f:
    st = json.load(f)

name = '<NOME_SKILL>'
if name in st['skills']['invariants']:
    print(f'{name} ja e invariante — sempre ativa.'); sys.exit(0)
if name in st['skills']['opt_in_active']:
    print(f'{name} ja esta ativa.'); sys.exit(0)

if name in st['skills']['opt_in_inactive']:
    st['skills']['opt_in_inactive'].remove(name)
st['skills']['opt_in_active'].append(name)
st['updated_at'] = datetime.now(timezone.utc).isoformat()

sys.path.insert(0, '${CLAUDE_PLUGIN_ROOT}/scripts')
import state as s
errs = s.validate(st)
if errs: print('ERRO:', errs); sys.exit(1)
s.save('$COWORK', st)
print(f'Skill {name} ativada.')
"
```

### 4. Informar ao usuario

```
Skill <NOME> ativada.

Total de skills ativas:
  Invariantes: 5
  Opt-in:      <count> (+1 agora)

A skill estara disponivel na proxima sessao do Claude Code (o auto-discovery carrega skills ativas automaticamente).
```

### 5. Se skill tem dependencias

Algumas skills trabalham melhor em conjunto. Sugerir:

- Ativou `pecas-processuais` e nao tem `estrategia-de-caso`? Sugerir ativar.
- Ativou `due-diligence` e nao tem `parecer-juridico`? Sugerir ativar.
- Ativou `contrato-social-holding` e nao tem `contratos-societarios`? Sugerir ativar.
- Ativou qualquer Tenente e nao tem Estado-Maior completo (estrategia + trilateral + jurisprudencia)? Sugerir ativar.

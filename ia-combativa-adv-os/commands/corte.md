---
description: Toggle Suprema Corte (R1-R4) on/off ou mostrar status. Bypass temporario de auditoria.
allowed-tools: Bash, Read
argument-hint: [on|off|status] [--permanent]
---

Voce foi acionado pelo comando `/corte`. Controla a ativacao da Suprema Corte.

Argumento: `$ARGUMENTS`

## COMPORTAMENTO

### `/corte status` (ou sem args)

Apenas mostra:

```
SUPREMA CORTE

Status no state:         <ATIVA/DESATIVADA>
Aplicacao automatica em: <lista: pecas, contratos, pareceres>
Threshold bypass:        <N> palavras

Para desligar temporariamente nesta sessao:
  /corte off

Para desligar permanentemente (grava no state):
  /corte off --permanent

Para reativar:
  /corte on
```

### `/corte off`

**Desligamento TEMPORARIO** (apenas para esta sessao do Claude Code):

Nao grava no state. Apenas avisa ao Claude:

> "Suprema Corte desligada nesta sessao. Pecas, contratos e pareceres serao produzidos SEM passar pelo fluxo R1->R2->R3->R4."

E lembra ao usuario:

> "ATENCAO: sem Suprema Corte, os riscos de alucinacao de jurisprudencia, inconsistencia de tese e falhas de completude NAO sao auditados. Use com cuidado. Para ligar novamente: /corte on"

Importante: como este e um toggle de sessao, o comando nao altera o state. O Claude deve **memorizar** o toggle internamente (via variavel de contexto da conversa). O firm-master consulta esse toggle antes de acionar a Suprema Corte.

### `/corte off --permanent`

**Desligamento PERMANENTE** (grava no state):

```bash
COWORK=$(python "${CLAUDE_PLUGIN_ROOT}/scripts/find-cowork.py")
python "${CLAUDE_PLUGIN_ROOT}/scripts/state.py" set "$COWORK" suprema_corte.enabled false
```

E re-renderiza a persona:

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/render.py" "$COWORK" --only persona
```

Avisa com warning:

> "Suprema Corte desligada permanentemente. Essa decisao afeta a qualidade de toda producao juridica futura. Voce esta removendo a auditoria de 4 revisoras antes da entrega. Para reativar: /corte on"

### `/corte on`

Se foi desligada temporariamente nesta sessao -> apenas religar na sessao.

Se foi desligada permanentemente no state -> reativar no state:

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/state.py" set "$COWORK" suprema_corte.enabled true
python "${CLAUDE_PLUGIN_ROOT}/scripts/render.py" "$COWORK" --only persona
```

Confirmar:

```
Suprema Corte REATIVADA.
R1 -> R2 -> R3 -> R4 voltarao a auditar pecas/contratos/pareceres antes da entrega.
```

## REGRA DE OURO

**Desligar Suprema Corte e risco do usuario.** Sempre avisar sobre implicacoes. Nunca sugerir bypass proativamente (a menos que o usuario esteja pedindo uma tarefa rapida/trivial onde `--quick` seria apropriado — mas mesmo assim, o default e MANTER a Suprema Corte ATIVA).

## BYPASS POR COMANDO

Alem de `/corte off`, o usuario pode usar `--no-corte` em comandos especificos:

```
/nova-peca --no-corte "peticao simples de declaracao de valor"
```

Nesse caso a peca e produzida sem auditoria, e voltar a proxima usa Suprema Corte normalmente.

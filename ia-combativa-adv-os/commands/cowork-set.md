---
description: Altera um campo especifico do cowork-state.json e re-renderiza arquivos afetados.
allowed-tools: Bash, Read
argument-hint: <campo.dotted> <valor>
---

Voce foi acionado pelo comando `/cowork-set`. Altera um campo do state.

Argumento: `$ARGUMENTS`

## PROTOCOLO

### 1. Parsear argumentos

O formato esperado e: `campo.dotted valor`

Exemplos validos:
- `/cowork-set identity.oab_numero 123456`
- `/cowork-set identity.email contato@escritorio.com.br`
- `/cowork-set tom_voz.perfil tecnico-cordial`
- `/cowork-set tom_voz.intensidade_combativa 9`
- `/cowork-set suprema_corte.enabled false`
- `/cowork-set suprema_corte.bypass_threshold_words 300`
- `/cowork-set preferences.output_format_preferido pdf`

Se argumento ausente ou mal-formatado, mostrar lista de campos aceitos mais comuns e exemplos acima.

### 2. Localizar o COWORK

```bash
COWORK=$(python "${CLAUDE_PLUGIN_ROOT}/scripts/find-cowork.py")
if [ -z "$COWORK" ]; then
  echo "ERRO: COWORK nao encontrado. Rode /start primeiro."
  exit 1
fi
```

### 3. Aplicar alteracao

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/state.py" set "$COWORK" "<campo>" "<valor>"
```

Se falhar por validacao, reportar o erro ao usuario sem alterar o state.

### 4. Re-renderizar arquivos afetados

Dependendo do campo alterado, alguns arquivos precisam ser regenerados:

- **identity.*** -> re-renderizar persona.md, cowork-CLAUDE.md, area-CLAUDE.md
- **tom_voz.*** -> re-renderizar persona.md
- **suprema_corte.*** -> re-renderizar persona.md, cowork-CLAUDE.md
- **preferences.*** -> re-renderizar persona.md, cowork-CLAUDE.md
- **automations.*** -> informar usuario que precisa reiniciar scheduler (nao mexemos nisso aqui)

Executar:

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/render.py" "$COWORK"
```

Sem `--force` — preserva customizacoes do usuario em persona/MEMORY se esses arquivos foram editados manualmente.

### 5. Confirmar ao usuario

```
Campo atualizado: <campo> = <valor>
Arquivos re-renderizados.

Ajuste aplicado. Pode levar efeito:
- Imediatamente para sugestoes ao Claude nesta sessao (mas a persona injetada pelo hook so carrega no proximo SessionStart)
- Reinicie a sessao para garantir que o tom/comportamento reflita a mudanca
```

### 6. Casos especiais

- **Alterar `firm_slug`** -> recusar (slug e identidade tecnica; alterar quebra refs em templates)
- **Alterar `cowork_path`** -> recusar (mover workspace exige /start novo em outro diretorio)
- **Alterar `skills.invariants`** -> recusar (sao invariantes, nao-removiveis)
- **Alterar `schema_version`** -> recusar (use `state.py migrate` para isso)

Em qualquer um desses casos, explicar ao usuario por que nao podemos alterar e sugerir a alternativa correta.

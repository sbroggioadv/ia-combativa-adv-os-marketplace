---
description: Mostra estado atual do workspace COWORK (firma, areas, skills, automacoes, Suprema Corte)
allowed-tools: Bash, Read
---

Voce foi acionado pelo comando `/cowork-status`. Mostre ao usuario um resumo executivo do estado atual do workspace COWORK.

## PROTOCOLO

### 1. Localizar o COWORK ativo

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/find-cowork.py"
```

Se o comando retornar erro (exit 1):

> "Nenhum workspace COWORK configurado neste diretorio ou nas proximas camadas. Rode `/start` para configurar seu primeiro workspace."

Se encontrar, guarde o path retornado como `$COWORK`.

### 2. Ler o state

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/state.py" show "$COWORK"
```

O output e JSON completo do `cowork-state.json`.

### 3. Apresentar RESUMO EXECUTIVO (nao o JSON cru)

Formato:

```
STATUS DO WORKSPACE COWORK

Localizacao: $COWORK
Plugin:      ia-combativa-adv-os v<plugin_version>

IDENTIDADE
  Escritorio:    <firm_name>
  Titular:       <advogado_nome>
  OAB:           <oab_numero>/<oab_uf> (ou 'nao informado')
  Cidade/UF:     <cidade>/<uf> (ou 'nao informado')
  Email:         <email> (ou 'nao informado')

TOM DE VOZ
  Perfil:        <tom_voz.perfil>
  Intensidade:   <tom_voz.intensidade_combativa>/10
  Postura:       <resumo ou 'default'>

AREAS DE ATUACAO ATIVAS (<N> areas)
  - <AREA 1> (<tipo_atuacao>, polo: <polo_predominante>)
  - <AREA 2> ...

SKILLS
  Invariantes (5):     firm-master + 4 Suprema Corte [SEMPRE ATIVAS]
  Opt-in ativas:       <count> skills
    - <lista>
  Opt-in inativas:     <count> skills (podem ser ativadas com /cowork-add-skill)

SUPREMA CORTE
  Status:              <ATIVA / DESATIVADA>
  Aplicacao auto em:   <auto_apply_to>
  Threshold bypass:    <N> palavras

AUTOMACOES AGENDADAS
  - <nome 1>: <cron> (habilitada/desabilitada)
  - <nome 2>: ...
  (ou 'nenhuma configurada')

PREFERENCIAS
  Idioma:              <idioma>
  Output preferido:    <output_format>
  Papel timbrado:      <path ou 'default do plugin'>

WIZARD
  Completado:          <SIM/NAO>
  Ultima atualizacao:  <updated_at>
```

### 4. Sugerir acoes

Com base no estado, sugerir:

- Se wizard nao completo -> "Rode `/start` para completar"
- Se 0 opt-in ativas -> "Considere ativar skills opt-in com `/cowork-add-skill <nome>`"
- Se identidade incompleta (OAB null, email null) -> "Complete sua identidade com `/cowork-set identity.oab_numero <valor>`"
- Se Suprema Corte desativada -> "Reativar com `/corte on`"

### 5. Tratamento de erro

- State invalido (falha no validate) -> Mostrar erros + sugerir `python "${CLAUDE_PLUGIN_ROOT}/scripts/state.py" migrate "$COWORK"` se for versao antiga
- COWORK nao encontrado -> Sugerir `/start`

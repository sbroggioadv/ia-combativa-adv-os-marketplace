# INSTALL — Plugin Ia Combativa-Adv-OS

Guia passo-a-passo para instalar o plugin em Windows, macOS ou Linux.

---

## Pre-requisitos

- **Claude Code** instalado e funcional (`claude --version` funciona no terminal).
- **Python 3.11+** (`python --version` ou `python3 --version`).
- **Git** (`git --version`).
- Ambiente cross-platform: Windows com Git Bash, macOS com Terminal.app ou iTerm, Linux com bash/zsh.

---

## 1. Clonar o repositorio do plugin

Escolha um path **fora** de pastas sincronizadas (iCloud, OneDrive, Dropbox, Google Drive):

**Windows (PowerShell ou Git Bash):**
```bash
mkdir -p ~/dev/plugins
cd ~/dev/plugins
git clone https://github.com/sbroggioadv/Plugin-Ia-Combativa-Adv-OS.git
```

**macOS:**
```bash
mkdir -p ~/dev/plugins
cd ~/dev/plugins
git clone https://github.com/sbroggioadv/Plugin-Ia-Combativa-Adv-OS.git
```

**Linux:**
```bash
mkdir -p ~/dev/plugins
cd ~/dev/plugins
git clone https://github.com/sbroggioadv/Plugin-Ia-Combativa-Adv-OS.git
```

---

## 2. Instalar no Claude Code

Abra o Claude Code em qualquer diretorio e rode:

```
/plugin install ~/dev/plugins/Plugin-Ia-Combativa-Adv-OS
```

O plugin aparecera registrado em `~/.claude/plugins/`.

---

## 3. Rodar o onboarding

No Claude Code, em qualquer projeto:

```
/start
```

O wizard vai conduzir voce por 9 blocos de perguntas:

1. **Diretorio COWORK** — onde criar a pasta operacional do escritorio.
2. **Identidade** — nome do escritorio, advogado titular, OAB, cidade/UF.
3. **Areas de atuacao** — multi-select de 15 areas + custom.
4. **Tom de voz** — perfil (combativo / cordial / didatico / personalizado) + intensidade.
5. **Skills opt-in** — 16 skills Tenentes/Transversais (alem das 7 invariantes obrigatorias).
6. **Suprema Corte** — confirmar ativacao default-on.
7. **Stack operacional** — ferramentas externas que voce ja usa + conectores Anthropic disponiveis.
8. **Automacoes agendadas** — opcional, tipicamente pulado na primeira instalacao.
9. **Revisao e confirmacao** — resumo + criacao dos arquivos.

Tempo estimado: **10-15 minutos**.

---

## 4. Verificar instalacao

```
/cowork-status
/cowork-doctor
```

`/cowork-doctor` roda 17 checks e reporta tudo verde quando OK.

---

## 5. Instalacao em segunda maquina (multi-dispositivo)

1. No segundo dispositivo, repetir passos 1-3.
2. Durante `/start`, o wizard detectara se voce ja tem COWORK em outra maquina (via prompt informativo — nao tem auto-deteccao entre maquinas diferentes, apenas local).
3. Apontar para o mesmo path do COWORK so e recomendado se ambas as maquinas acessarem o mesmo filesystem (raro — pastas de rede corporativa). **Se nao**, crie um COWORK separado em cada maquina e use a skill `cowork-sync` para detectar divergencia de versao do plugin.

---

## 6. Atualizacao do plugin

```bash
cd ~/dev/plugins/Plugin-Ia-Combativa-Adv-OS
git pull
```

Na proxima sessao do Claude Code, a skill `cowork-sync` detectara a divergencia e sugerira `/cowork-sync --refresh` para aceitar o novo baseline.

---

## 7. Desinstalacao

```
/cowork-uninstall
```

**O COWORK e preservado intocado.** Apenas o plugin e removido da instalacao do Claude Code.

---

## Troubleshooting

- **"Python nao encontrado"** — instale Python 3.11+ e confirme com `python --version`. No Windows, considerar adicionar ao PATH durante instalacao.
- **"/start nao aparece"** — conferir `/plugin list` e ativar o plugin com `/plugin enable ia-combativa-adv-os`.
- **"Hook falhando"** — rodar `/cowork-doctor` para diagnostico. Ver `docs/FAQ.md` para erros comuns.
- **"Audit detectou contaminacao"** — voce provavelmente editou manualmente arquivo no clone do plugin e introduziu termo proibido. Reverter com `git checkout -- <arquivo>`.

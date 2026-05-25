# IA Combativa Adv-OS — Marketplace

Marketplace oficial do plugin **IA Combativa Adv-OS** para Claude Code / Cowork.

> Sistema operacional do advogado com IA — Batalhão Jurídico (General + Estado-Maior + Comandantes + Tenentes) + Suprema Corte R1-R4. Onboarding interativo via `/start`, 29 skills jurídicas, automações agendadas, suporte multi-dispositivo. 100% configurável ao perfil do escritório do usuário.

---

## 📦 O que tem aqui

- `.claude-plugin/marketplace.json` — manifesto do marketplace (Cowork lê este arquivo)
- `ia-combativa-adv-os/` — código-fonte completo do plugin (skills, commands, hooks, templates)
- `LICENSE` — MIT

---

## 🚀 Como instalar (Cowork / Claude Desktop)

1. Abra o **Claude Cowork** (aba lateral)
2. **Settings → Plugins → Pessoal → "+"**
3. Escolha **"Adicionar marketplace"**
4. Cole a URL deste repositório:
   ```
   https://github.com/sbroggioadv/ia-combativa-adv-os-marketplace
   ```
5. Clique em **Sincronizar**
6. O plugin aparecerá em **"Pessoal → Uploads locais"** — clique em **Instalar**

Após instalado, no Claude Code rode `/start` pra iniciar o onboarding interativo do Batalhão Jurídico.

---

## 🧰 Como instalar via CLI

```bash
claude plugin marketplace add https://github.com/sbroggioadv/ia-combativa-adv-os-marketplace
claude plugin install ia-combativa-adv-os@ia-combativa-adv-os-marketplace
```

---

## 📚 O que o plugin entrega

- **`/start`** — onboarding interativo que configura seu Cowork (escritório, áreas, persona, tom de voz) e instala as skills certas pro seu perfil
- **29 skills jurídicas:**
  - **Batalhão Jurídico** — `firm-master`, `escritorio-advocacia`, `comunicacao-cliente`, `financeiro-juridico`, `marketing-juridico`, `compliance-lgpd`
  - **Suprema Corte R1-R4** (default-on, com bypass via `--no-corte`): coleta → base jurídica → tese → completude
  - **Peças & Processual** — `peticao-universal`, `pecas-processuais`, `contrarrazoes-recursais`, `replica-estrategica`, `parecer-juridico`, `resumo-audiencia`, `estrategia-de-caso`, `analise-trilateral`, `jurisprudencia-estrategica`, `documentos-extrajudiciais`, `visual-law`, `calculo-juridico`
  - **Contratos & Societário** — `contratos-societarios`, `contrato-social-holding`, `minutas-contratuais`, `due-diligence`
  - **Engine de personalização** — `cowork-onboarding`, `cowork-sync`, `memory-evolver`
- **14 commands** — `/start`, `/corte`, `/cowork-*` (add/remove area, add/remove skill, add task, doctor, set, status, sync, uninstall, update), `/memory-evolver`
- **Hooks SessionStart + PostToolUse** — anti-flap, debouncing, persona injection
- **Templates** — `persona.md.tpl`, `cowork-CLAUDE.md.tpl`, `area-CLAUDE.md.tpl`, `MEMORY.md.tpl`, `settings-local.json.tpl`

---

## 🎯 Para quem é

Advogados (autônomos, escritórios pequenos e médios) que querem estruturar IA jurídica de excelência sem reinventar a roda. Onboarding em ~10 min via `/start`, depois é só rodar as skills no fluxo normal de trabalho.

---

## 📄 Licença

MIT — veja [LICENSE](./LICENSE).

---

## 🔗 Família Adv-OS

Plugin parte da família **Adv-OS** — sistema operacional jurídico modular distribuído via marketplace público:

- `ia-combativa-adv-os` (você está aqui)
- `marketing-adv-os` · https://github.com/sbroggioadv/marketing-adv-os-marketplace
- `previdenciario-adv-os` · https://github.com/sbroggioadv/previdenciario-adv-os-marketplace
- `trabalhista-adv-os` · https://github.com/sbroggioadv/trabalhista-adv-os-marketplace
- `tributario-societario-adv-os` · https://github.com/sbroggioadv/tributario-societario-adv-os-marketplace
- `auditoria-contabil-os` · https://github.com/sbroggioadv/auditoria-contabil-os-marketplace
- `licitacoes-adv-os` · https://github.com/sbroggioadv/licitacoes-adv-os-marketplace
- `direito-medico-adv-os` · https://github.com/sbroggioadv/direito-medico-adv-os-marketplace

---

**Criado por Luis Sbroggio · Mentoria IA Combativa**

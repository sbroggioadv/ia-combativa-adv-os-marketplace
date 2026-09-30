# IA Combativa Adv-OS — Marketplace

> ## ⚖️ Este repositório NÃO é software livre
>
> O código fica visível para viabilizar a instalação no Claude/Cowork — não porque seja gratuito.
>
> **IA COMBATIVA ADV-OS — R$ 498,00, pagamento único** (sem assinatura, sem recorrência)
> 👉 **[Adquirir a licença](https://pay.kirvano.com/592e218e-c506-4a0c-9aed-019b767f6cbb)**
>
> **Ao forkar ou clonar este repositório você adere à [licença de uso](LICENSE)**, devendo efetuar o
> pagamento no link acima e enviar o comprovante para **luis@sbroggio.io**.
>
> Os forks são públicos no GitHub e são registrados pelo titular (data, conta e repositório).
>
> **Já comprou?** Nada a fazer — sua licença cobre o uso e o fork para instalação. Este aviso vale de
> 11/08/2026 em diante, para quem chega ao repositório sem ter adquirido.


Marketplace oficial do plugin **IA Combativa Adv-OS** para Claude Code / Cowork.

> Sistema operacional do advogado com IA — Batalhão Jurídico (General + Estado-Maior + Comandantes + Tenentes) + Suprema Corte R1-R4. Onboarding interativo via `/start`, 29 skills jurídicas, automações agendadas, suporte multi-dispositivo. 100% configurável ao perfil do escritório do usuário.

---

## 📦 O que tem aqui

- `.claude-plugin/marketplace.json` — manifesto do marketplace (Cowork lê este arquivo)
- `ia-combativa-adv-os/` — código-fonte completo do plugin (skills, commands, hooks, templates)
- `LICENSE` — licenca de uso proprietaria

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

Uso licenciado mediante aquisição — ver [`LICENSE`](./LICENSE). As cópias obtidas até 11/08/2026 permanecem sob MIT; a partir dessa data o código é proprietário.

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

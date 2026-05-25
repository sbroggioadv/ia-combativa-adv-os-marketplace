#!/usr/bin/env python3
"""
Hook UserPromptSubmit — injeta instrucao de ativar Suprema Corte quando detecta
prompt de tarefa juridica, a menos que o usuario tenha passado bypass.

Logica:
1. Le o prompt via stdin (JSON padrao Claude Code hooks).
2. Detecta bypass explicito: flags `--no-corte`, `--quick`, `--no-suprema`, `/corte off`.
3. Detecta tarefa juridica via keywords (lista curada).
4. Se eh tarefa juridica e nao ha bypass, imprime em stdout uma instrucao curta
   que o Claude lera como context adicional antes de processar o prompt
   (mecanismo padrao do hook UserPromptSubmit).
5. Se ha bypass, reafirma em stdout que o bypass foi aceito (para transparencia).
6. Se nao eh tarefa juridica, silencio (exit 0 sem output).

Tambem respeita state.json do COWORK: se `suprema_corte.enabled = false`, nunca injeta.

Stdlib only.
"""

from __future__ import annotations

import io
import json
import os
import re
import sys
from pathlib import Path

if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

SCRIPT_DIR = Path(__file__).resolve().parent
PLUGIN_ROOT = SCRIPT_DIR.parent.parent
sys.path.insert(0, str(PLUGIN_ROOT / "scripts"))

import importlib.util
spec = importlib.util.spec_from_file_location("hook_utils", PLUGIN_ROOT / "scripts" / "hook-utils.py")
hook_utils = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hook_utils)


# Keywords que sinalizam tarefa juridica. Lista conservadora — falso-positivo e
# preferivel a falso-negativo, mas evitar palavras ambiguas isoladas.
LEGAL_KEYWORDS = [
    # Pecas e documentos
    r"\bpeticao\b", r"\bpeti\u00e7\u00e3o\b", r"\bcontestacao\b", r"\bcontesta\u00e7\u00e3o\b",
    r"\brecurso\b", r"\bapelacao\b", r"\bapela\u00e7\u00e3o\b", r"\bagravo\b",
    r"\bembargos\b", r"\breplica\b", r"\br\u00e9plica\b", r"\bcontrarrazoes\b", r"\bcontrarraz\u00f5es\b",
    r"\btutela\b", r"\binicial\b", r"\bmanifestacao\b", r"\bmanifesta\u00e7\u00e3o\b",
    r"\bnotificacao\b", r"\bnotifica\u00e7\u00e3o\b", r"\binterpelacao\b", r"\binterpela\u00e7\u00e3o\b",
    r"\bparecer\b", r"\bopiniao\s+legal\b", r"\bopini\u00e3o\s+legal\b",
    # Contratos/societario
    r"\bcontrato\b", r"\bminuta\b", r"\baditivo\b", r"\bdistrato\b",
    r"\bholding\b", r"\bsocio\b", r"\bs\u00f3cio\b", r"\bacordo\s+de\s+socios\b",
    r"\bcontrato\s+social\b", r"\bestatuto\b", r"\bfranquia\b", r"\bcof\b",
    # Processo
    r"\bprocesso\b", r"\baudiencia\b", r"\baudi\u00eancia\b", r"\bsentenca\b", r"\bsenten\u00e7a\b",
    r"\bdecisao\b", r"\bdecis\u00e3o\b", r"\bdespacho\b", r"\bjurisprudencia\b", r"\bjurisprud\u00eancia\b",
    # Expressoes acionaveis
    r"elabora(r)?\s+", r"redigir\s+", r"rascunhe\s+", r"produz(ir)?\s+(uma|um)\s+",
    r"fazer?\s+(uma|um)\s+peticao", r"fazer?\s+(uma|um)\s+peca",
    # Areas especificas
    r"\bhonorarios\b", r"\bhonor\u00e1rios\b", r"\blgpd\b",
    r"\breforma\s+tributaria\b", r"\breforma\s+tribut\u00e1ria\b",
]

BYPASS_TOKENS = [
    "--no-corte",
    "--no-suprema",
    "--quick",
    "/corte off",
    "/corte-off",
]


def _load_input() -> dict:
    raw = sys.stdin.read().strip()
    if not raw:
        return {}
    try:
        return json.loads(raw)
    except Exception:
        return {}


def _is_legal(prompt: str) -> bool:
    low = prompt.lower()
    for pat in LEGAL_KEYWORDS:
        if re.search(pat, low):
            return True
    return False


def _has_bypass(prompt: str) -> str | None:
    low = prompt.lower()
    for token in BYPASS_TOKENS:
        if token in low:
            return token
    return None


def _suprema_corte_enabled(cowork: Path | None) -> bool:
    """Le cowork-state.json e verifica suprema_corte.enabled. Default true se ausente."""
    if cowork is None:
        return True
    sf = cowork / ".dev-adv" / "cowork-state.json"
    if not sf.exists():
        return True
    try:
        state = json.loads(sf.read_text(encoding="utf-8"))
        return bool(state.get("suprema_corte", {}).get("enabled", True))
    except Exception:
        return True


def _resolve_cowork() -> Path | None:
    """Resolve COWORK root a partir de env COWORK_PATH ou cwd."""
    env = os.environ.get("COWORK_PATH")
    if env:
        p = Path(env)
        if (p / ".dev-adv" / "cowork-state.json").exists():
            return p
    return hook_utils.find_cowork(Path.cwd())


def main() -> int:
    payload = _load_input()
    prompt = payload.get("prompt") or payload.get("user_prompt") or ""
    if not isinstance(prompt, str) or not prompt.strip():
        return 0

    cowork = _resolve_cowork()
    if not _suprema_corte_enabled(cowork):
        # Usuario desabilitou Suprema Corte globalmente na config
        return 0

    bypass = _has_bypass(prompt)
    is_legal = _is_legal(prompt)

    if bypass:
        # Mensagem curta em stdout, transparente ao usuario (Claude consome como context)
        sys.stdout.write(
            f"[suprema-corte] Bypass detectado ({bypass}). "
            "Pecas, contratos e pareceres serao entregues SEM validacao das 4 Revisoras. "
            "Use por sua conta e risco.\n"
        )
        return 0

    if is_legal:
        sys.stdout.write(
            "[suprema-corte] Tarefa juridica detectada. Aplique o protocolo padrao:\n"
            "1. Questionamento previo (sem suposicoes silenciosas).\n"
            "2. Apresentar estrutura + premissas antes de redigir.\n"
            "3. Aguardar confirmacao do usuario.\n"
            "4. Iniciar producao final somente apos 'REALIZE A TAREFA'.\n"
            "5. Antes de entregar: executar Suprema Corte R1-R4 (coleta -> base juridica -> "
            "tese -> completude). Use bypass com `--no-corte`, `--quick` ou `/corte off` "
            "quando a tarefa nao justificar revisao completa.\n"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

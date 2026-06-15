"""
ASSEMBLEA V4 — Intelligent Hybrid Engine (Fallback)
====================================================
ATTENZIONE: Questo script Python e' un FALLBACK.
Il metodo PRINCIPALE per l'Assemblea e' via sub-agenti cloud su OpenCode.

Usa questo script SOLO se non puoi lanciare agenti su cloud.
I modelli locali SONO LENTI per dibattiti (1/5 della velocita cloud).

PREREQUISITO: Impostare la variabile d'ambiente OLLAMA_API_KEY.
"""

import sys
import os
import json
import argparse
import urllib.request
import urllib.error
import time
import re

# USARE IL CLOUD, non modelli locali
CLOUD_API_URL = "https://ollama.com/v1/chat/completions"
CLOUD_API_KEY = os.environ.get("OLLAMA_API_KEY")
if not CLOUD_API_KEY:
    print(
        "ERRORE: Imposta la variabile d'ambiente OLLAMA_API_KEY.",
        file=sys.stderr,
    )
    sys.exit(1)

CLOUD_MODEL = "deepseek-v4-flash"  # MAI usare v4-pro (troppo lento per chat)

# Segnali per triage
SIGNALS = {
    "security": {
        "keywords": [
            "api",
            "login",
            "password",
            "database",
            "auth",
            "token",
            "crypt",
            "gdpr",
            "privacy",
            "encrypt",
            "hash",
            "injection",
            "xss",
            "csrf",
            "oauth",
            "jwt",
        ],
        "module": "The Infiltrator",
        "min_complexity": 4,
    },
    "future": {
        "keywords": [
            "migraz",
            "scalabil",
            "architettur",
            "cloud",
            "microservizi",
            "deploy",
            "kubernetes",
            "docker",
            "serverless",
            "caching",
        ],
        "module": "The Time Traveler",
        "min_complexity": 5,
    },
    "chaos": {
        "keywords": [
            "runtime",
            "mission critical",
            "production",
            "failover",
            "disaster recovery",
            "uptime",
            "sla",
            "high availability",
            "outage",
            "downtime",
        ],
        "module": "Chaos Simulator",
        "min_complexity": 6,
    },
}


def calculate_complexity(topic: str) -> float:
    words = len(topic.split())
    complexity = min(words * 0.5, 3.0)
    all_keywords = set()
    for s in SIGNALS.values():
        all_keywords.update(s["keywords"])
    signal_matches = sum(1 for kw in all_keywords if kw.lower() in topic.lower())
    complexity += signal_matches * 0.8
    tech_keywords = len(
        re.findall(
            r"\b(API|SQL|NoSQL|REST|gRPC|HTTP|TCP|GPU|CPU|RAM|DB|VM|AWS|GCP|Azure|Crypto|Blockchain|Microservizi|Kubernetes|Docker)\b",
            topic,
            re.IGNORECASE,
        )
    )
    complexity += tech_keywords * 0.5
    numbers = len(re.findall(r"\d+", topic))
    complexity += numbers * 0.3
    return min(round(complexity, 1), 10.0)


def detect_signals(topic: str) -> list:
    active = []
    topic_lower = topic.lower()
    for signal_name, signal_config in SIGNALS.items():
        for kw in signal_config["keywords"]:
            if kw.lower() in topic_lower:
                active.append(signal_name)
                break
    return active


def get_cast(complexity: float, signals: list) -> list:
    if complexity < 4:
        return [
            "Presidente (Sisyphus - Flash)",
            "Hacker (Flash cloud)",
            "Utente (Flash cloud)",
        ]
    elif complexity <= 6:
        return [
            "Presidente (Sisyphus - Flash)",
            "Hacker (Flash cloud)",
            "Contabile (Flash cloud)",
            "Utente (Flash cloud)",
            "Avvocato del Diavolo (Flash cloud)",
        ]
    else:
        return [
            "Presidente (Sisyphus - Flash)",
            "Architetto (Flash cloud)",
            "Hacker (Flash cloud)",
            "Contabile (Flash cloud)",
            "Utente (Flash cloud)",
            "Avvocato del Diavolo (Flash cloud)",
            "Lead Architect (Flash cloud)",
        ]


def chat(model: str, prompt: str, max_tokens: int = 1500, timeout: int = 60) -> str:
    """Invia richiesta al cloud Ollama (deepseek-v4-flash)."""
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
        "options": {"temperature": 0.7, "num_predict": max_tokens},
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        CLOUD_API_URL,
        data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {CLOUD_API_KEY}",
        },
        method="POST",
    )
    start = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            elapsed = time.time() - start
            result = json.loads(resp.read().decode("utf-8"))
            print(f"    [OK cloud in {elapsed:.1f}s]", file=sys.stderr)
            return result["choices"][0]["message"]["content"].strip()
    except Exception as e:
        elapsed = time.time() - start
        print(f"    [FAIL dopo {elapsed:.1f}s: {e}]", file=sys.stderr)
        raise


def main():
    print("=" * 70, file=sys.stderr)
    print(" [*] ASSEMBLEA V4 — FALLBACK (via cloud deepseek-v4-flash)", file=sys.stderr)
    print(
        " [*] ATTENZIONE: Il metodo PRINCIPALE e' via sub-agenti OpenCode su cloud.",
        file=sys.stderr,
    )
    print(" [*] Questo script e' un fallback piu lento.", file=sys.stderr)
    print("=" * 70, file=sys.stderr)

    parser = argparse.ArgumentParser(description="Assemblea V4 (Fallback)")
    parser.add_argument("topic", type=str, help="Il problema da risolvere")
    parser.add_argument(
        "--timeout", type=int, default=60, help="Timeout per chiamata (sec)"
    )
    parser.add_argument(
        "--code", type=str, default=None, help="File di codice per context-slimming"
    )
    args = parser.parse_args()
    topic = args.topic
    timeout = args.timeout

    code_context = ""
    if args.code and os.path.exists(args.code):
        with open(args.code, "r", encoding="utf-8") as f:
            lines = f.readlines()
        code_context = "\n".join(
            line
            for line in lines
            if any(
                line.strip().startswith(p)
                for p in [
                    "def ",
                    "class ",
                    "struct ",
                    "import ",
                    "from ",
                    "fn ",
                    "pub ",
                    "func ",
                ]
            )
        )[:3000]  # context-slimming

    full_topic = topic
    if code_context:
        full_topic += f"\n\nCODICE (slimmed):\n{code_context}"

    # FASE 0
    print(f"\n[FASE 0] TRIAGE...", file=sys.stderr)
    complexity = calculate_complexity(full_topic)
    signals = detect_signals(full_topic)
    active_modules = [
        SIGNALS[s]["module"]
        for s in signals
        if complexity >= SIGNALS[s]["min_complexity"]
    ]
    cast = get_cast(complexity, signals)
    print(
        f" [Complessita: {complexity}/10] [Segnali: {signals}] [Moduli: {active_modules}]",
        file=sys.stderr,
    )
    print(f" [Cast: {len(cast)} personaggi]", file=sys.stderr)

    # FASE 2 — Proposte in sequenza (fallback, non parallelo)
    print(f"\n[FASE 2] PROPOSTE...", file=sys.stderr)
    proposals = {}
    for c in cast:
        if "Presidente" in c or "Lead" in c:
            continue
        print(f" {c}...", file=sys.stderr)
        prop = chat(
            CLOUD_MODEL,
            f"Sei: {c}. Problema: '{topic}'. La TUA proposta in 4-5 frasi. Non sai cosa dicono gli altri.",
            timeout=timeout,
        )
        proposals[c] = prop
        print(f"  -> {prop[:200]}...\n", file=sys.stderr)

    # FASE 3 — Dibattito
    print(f"\n[FASE 3] DIBATTITO...", file=sys.stderr)
    devil_key = next((c for c in cast if "Avvocato" in c), None)
    debates = {}
    for c in cast:
        if "Presidente" in c or "Lead" in c or "Avvocato" in c:
            continue
        others_text = "\n\n".join(
            f"-> {k}: {v[:300]}" for k, v in proposals.items() if k != c
        )
        crit = proposals.get(devil_key, "")
        prompt = f"Sei: {c}. Dibattito su '{topic}'.\nProposte:\n{others_text}\n\nL'Avvocato ha criticato: {crit[:300]}\nLa TUA replica. Massimo 4 frasi."
        debates[c] = chat(CLOUD_MODEL, prompt, timeout=timeout)

    # Avvocato per ULTIMO
    if devil_key:
        all_text = "\n\n".join(
            f"{k}: {proposals.get(k, '')}\nReplica: {debates.get(k, '')}"
            for k in proposals
            if k != devil_key
        )
        prompt = f"Sei: {devil_key}. Hai ascoltato TUTTO su '{topic}'.\n{all_text}\nLe tue controrepliche FINALI. Massimo 4 frasi. Sii spietato."
        debates[devil_key] = chat(CLOUD_MODEL, prompt, timeout=timeout)

    # FASE 4 — Verbale
    print(f"\n[FASE 4] VERBALE FINALE...", file=sys.stderr)
    context = "\n\n".join(
        f"### {k}\nPROPOSTA: {proposals.get(k, '')}\nDIBATTITO: {debates.get(k, '')}"
        for k in proposals
    )
    verdict = chat(
        CLOUD_MODEL,
        f"Lead Architect. Verbale Finale su '{topic}'.\n\n{context}\n\nRedigi: 1) Sintesi 2) Obiezioni irrisolte 3) Decisione 4) Allegato Tecnico 5) Piano Azione. Markdown.",
        max_tokens=2000,
        timeout=timeout * 2,
    )

    print(f"\n{'=' * 70}")
    print(verdict)
    print(f"{'=' * 70}")
    print(
        f" [*] ASSEMBLEA V4 CONCLUSA. {len(proposals)} proposte, {len(debates)} interventi."
    )


if __name__ == "__main__":
    main()

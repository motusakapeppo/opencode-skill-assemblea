# opencode-skill-assemblea

**Assemblea V5 — Intelligent Hybrid Debate Engine**

Un sistema multi-agente asimmetrico per dibattiti strutturati tra modelli AI, progettato per funzionare come skill su OpenCode (OhMyOpenCode). L'Assemblea convoca 4-6 personaggi con modelli e ruoli diversi, genera proposte parallele, le sottopone a critica, e produce un verbale finale con decisione architetturale.

> Questa skill è **nativamente pensata per OpenCode**: il metodo principale d'esecuzione è via sub-agenti cloud. Lo script Python `debate_orchestrator.py` è un **fallback** per ambienti senza OpenCode.

---

## Architettura

### Il Cast

| Ruolo | Modello | Categoria | Competenza |
|-------|---------|-----------|------------|
| **Presidente** | deepseek-v4-flash | — | Moderatore, orchestra il dibattito |
| **L'Hacker** | kimi-k2.7-code | `quick` | Proposte concrete, coding |
| **Il Contabile** | minimax-m3 | `deep` | Numeri, costi, ROI |
| **L'Utente** | minimax-m3 | `deep` | Voce del cliente, semplicità |
| **L'Avvocato del Diavolo** | deepseek-v4-flash | `ultrabrain` | Critica puntuale, anti-sycophancy |
| **Lead Architect** | deepseek-v4-flash | `ultrabrain` | Sintesi finale e verbale |

### Flusso di Esecuzione

```
Triage → Calcolo Complessità → Selezione Modalità
    ↓
Convocazione (OdG + Task Plan)
    ↓
Hacker ─┐
Contabile ─┤── PARALLELO → Avvocato (asincrono, parte al primo risultato)
Utente ──┘
    ↓
Dibattito (sequenziale, max 2 giri)
    ↓
Moduli Specialistici (se attivati)
    ↓
Lead Architect → Verbale Finale
```

### Modelli Utilizzati

- **kimi-k2.7-code** (256K ctx) — Hacker: coding specialist
- **minimax-m3** (1M ctx) — Contabile, Utente: analitico, linguaggio naturale
- **deepseek-v4-flash** (1M ctx) — Avvocato, Lead Architect: critica e sintesi
- **deepseek-v4-pro** (1M ctx) — Solo analisi offline, MAI in assemblea (cold start 5-10s)

---

## Triage e Modalità

L'Assemblea calcola automaticamente la complessità del problema con una formula pesata:

| Input | Peso |
|-------|------|
| Parole | × 0.3 (cap a 2.0) |
| Keyword match | × 0.5 |
| Termini tecnici | × 0.3 |
| Cifre numeriche | × 0.2 |

### Soglie

| Punteggio | Modalità | Partecipanti |
|-----------|----------|-------------|
| < 4 | **Light** | Hacker + Utente + Lead |
| 4-6 | **Standard** | 5 personaggi |
| 6-8 | **Full** | 6 + moduli specialistici |
| > 8 | **Full + Esteso** | 6 + moduli + analisi supplementare |
| Trigger condizionale | **Esplorazione** | Design divergente, Hacker unbound |

La **Modalità Esplorazione** si attiva con segnali di divergenza (brainstorming, esplora, pensiero laterale) E assenza di urgenza. In questa modalità l'Hacker genera idee senza limiti, l'Avvocato applica solo un survival filter (FATAL FLAW), e il Lead Architect clusterizza le idee sopravvissute.

---

## Moduli Specialistici

Attivabili automaticamente in base a segnali nel problema:

| Modulo | Trigger | Funzione |
|--------|---------|----------|
| **The Infiltrator** | Security ≥ 2 + complessità ≥ 5 | Trova bias cognitivi e difetti argomentativi |
| **The Time Traveler** | Scalabilità ≥ 2 + complessità ≥ 6 | Proietta impatto decisioni a 12-24 mesi |
| **Chaos Simulator** | "failure/mission-critical" + complessità ≥ 7 | Introduce 2 guasti forzati, obbliga piano B |

---

## Memoria Storica (RAG)

Prima di ogni assemblea, il sistema cerca verbali precedenti su argomenti simili tramite la skill `knowledge`. Se trova risultati, li inietta nel prompt dell'Avvocato e del Lead Architect per evitare di ripetere errori già discussi.

---

## Metriche di Chiusura

Alla fine di ogni assemblea vengono registrate:

- Durata stimata
- Turni totali
- Obiezioni sollevate / non risolte
- Decisioni precedenti trovate
- Decisione finale (Accettata / Rimandata)

**Quality Gate**: se l'Avvocato solleva < 3 obiezioni, il sistema rilancia con un anti-sycophancy check. Se le obiezioni non risolte superano il 50%, la decisione è fragile.

---

## Esempi d'Uso

### Esempio 1: Problema Tecnico Complesso (Modalità Full)

```
Utente: "Fai un'assemblea per progettare l'architettura del nuovo
microservizio di autenticazione con JWT, refresh token rotation,
e supporto multi-tenant su Kubernetes"

Output: Verbale con 3 proposte Hacker, analisi costi Contabile,
critiche Avvocato, decisione architetturale finale con allegato tecnico.
```

### Esempio 2: Decisione di Design (Modalità Standard)

```
Utente: "Dibattito: usiamo PostgreSQL o MongoDB per il nuovo
sistema di logging?"

Output: Confronto costi/benefici, critica delle assunzioni, decisione motivata.
```

### Esempio 3: Esplorazione (Modalità Divergente)

```
Utente: "Brainstorming senza limiti: come potremmo riscrivere
da zero l'intero sistema di routing dei messaggi?"

Output: Decine di idee categorizzate, filtrate per impossibilità,
clusterizzate per strategia.
```

---

## Fallback Python

`debate_orchestrator.py` è uno script Python standalone che esegue l'Assemblea via chiamate dirette all'API cloud (senza OpenCode). Non supporta parallelismo reale né la modalità Esplorazione.

```bash
# Prerequisito: impostare la variabile d'ambiente
export OLLAMA_API_KEY="la-tua-chiave"

# Esecuzione
python debate_orchestrator.py "Progetta l'architettura per un sistema di caching distribuito" --timeout 60

# Con contesto di codice
python debate_orchestrator.py "Refactoring del modulo auth" --code src/auth/service.py
```

---

## Requisiti

- **Python 3.10+** (per il fallback)
- **OpenCode** (OhMyOpenCode) con configurazione cloud per l'uso principale
- **Variabile d'ambiente** `OLLAMA_API_KEY` per il fallback Python
- Modelli cloud accessibili: kimi-k2.7-code, minimax-m3, deepseek-v4-flash

---

## Struttura del Repository

```
opencode-skill-assemblea/
├── README.md                          # Questo file
├── SKILL.md                           # Skill definition (frontmatter YAML + body)
├── debate_orchestrator.py             # Fallback Python (standalone)
├── proiezione_24mesi_time_traveler.md # Esempio di output del modulo Time Traveler
└── .gitignore
```

---

## Limitazioni Note

1. Il fallback Python è **sequenziale**, non parallelo — i 3 personaggi partono uno dopo l'altro
2. La modalità Esplorazione è disponibile **solo su OpenCode**, non nel fallback Python
3. deepseek-v4-pro è esplicitamente bandito dall'Assemblea (cold start troppo lento)
4. I modelli locali non supportano dibattiti di qualità — sempre usare modelli cloud

---

## Licenza

Apache 2.0
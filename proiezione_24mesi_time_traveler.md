# 🔮 PROIEZIONE A 24 MESI — Architettura Skill OpenCode MOTUS

**Modulo:** The Time Traveler (Assemblea V4)
**Data proiezione:** 2026-05-17
**Orizzonte:** 12 mesi (H1 2027) → 24 mesi (H1 2028)

---

## PANORAMICA DELLO STATO ATTUALE

### Asset Registrati
| Skill | Forma | Stato | Righe/Entità | Rischio Debito |
|-------|-------|-------|--------------|----------------|
| **assemblea** | SKILL.md + debate_orchestrator.py | ✅ Documentata | 301 righe (fallback) | 🔴 Alta (API key hardcoded) |
| **buonanotte** | SKILL.md | ✅ Documentata | 12 righe | 🟡 Media (shutdown irreversibile) |
| **context-slimmer** | SKILL.md | ✅ Documentata | 62 righe | 🟡 Media (manuale, nessun hook) |
| **giotto** | SKILL.md | ✅ Documentata | 130 righe | 🟢 Bassa (ma dipendenza D:\ fisso) |
| **git-warfare** | SKILL.md | ✅ Documentata | 79 righe | 🟢 Bassa (ma nessuna modalità feature) |
| **music-producer** | SKILL.md | ✅ Documentata | 83 righe | 🟡 Media (dipendenza binari esterni) |
| **remote-tradingbot** | SKILL.md | ⚠️ Sovraccarico | **154 righe, 6 responsabilità** | 🔴 **Critica** (God Object) |
| **rocco** | SKILL.md | ✅ Documentata | 51 righe | 🟢 Bassa |
| **generazione** | skill_generazione.py **SOLO** | ❌ Orfana | 187 righe | 🔴 Alta (no SKILL.md, no trigger, no metadati) |
| **vision** | skill_vision.py **SOLO** | ❌ Orfana | 108 righe | 🔴 Alta (no SKILL.md, no trigger, no metadati) |

### Configurazione Agente (`oh-my-openagent.json`)
- **11 agenti**, **8 categorie** (4 cloud, 4 locali)
- Principale: `deepseek-v4-flash` (8 istanze)
- Modello locale: `qwen2.5-coder:latest` (quick, writing)
- **BUG CRITICO:** categoria `deep` punta a `deepseek-v4-flash` invece di `glm-5.1` — la SKILL.md di assemblea esplicitamente richiede glm per il Contabile, ma la config non lo rispetta.

### Costi
- Attuale: **~$0.14/mese** (tutto da assemblea/sub-agenti occasionali)
- Se cresce l'uso: costo potenziale a 24 mesi con zero ottimizzazioni → **~$12-20/mese** se i modelli locali vengono abbandonati per comodità.

---

## SCENARIO A: SE NON SI FA NULLA

### 🕐 Tra 3 mesi (Agosto 2026)

**Sintomo 1 — Le Orfane Diventano Fantasmi**
- Nessuno ricorda che `generazione` e `vision` esistono. L'utente chiederà "genera un'immagine" e Sisyphus invocherà **giotto** (che ha triggers e SKILL.md), ignorando completamente l'esistenza di `generazione` (più leggera, basata su Ollama locale) e `vision` (orphaned, nessun trigger). **Dead code in produzione.**

**Sintomo 2 — Il God Object Colpisce**
- `remote-tradingbot` raggiunge 200+ righe. Una modifica ai parametri di sicurezza del server rischia di rompere la sezione dashboard. Ogni change richiede 10 minuti di lettura perché 6 domini concettuali sono mescolati.

**Sintomo 3 — Il Contabile Sbaglia**
- Il Contabile nell'Assemblea continua a girare su `deepseek-v4-flash` anziché `glm-5.1`. I calcoli di costo/ROI diventano verbosi, filosofeggiano. Il dibattito rallenta di 30-40% senza motivo. L'utente perde fiducia nella qualità numerica dell'Assemblea.

**Sintomo 4 — Context Slimming Obsoleto**
- Più skill vengono usate → più contesto si accumula. Il context-slimmer è manuale, quindi viene ignorato nella maggior parte dei casi. I costi cloud salgono a **$0.40-0.60/mese** (3-4x) per via di token sprecati.

### 🕕 Tra 6 mesi (Novembre 2026)

**Cascata 1 — L'Inventario Skill è Incompleto**
- Non esiste uno `skill-index.json`. Non c'è modo programmatico di sapere quali skill esistono. La "tabella dei contenuti" è... questa proiezione. Se un nuovo sviluppatore (o tu stesso tra 6 mesi) vuole sapere "che skill ho?", deve aprire 10 cartelle a mano.
- **Conseguenza:** Skill duplicate vengono scritte perche nessuno sa che già esistono. Vedi `generazione` vs `giotto`: entrambe generano immagini, una è morta, l'altra viva. Rischi duplicazione.

**Cascata 2 — I Triggers Sono Inconsapevoli**
- Se nessuno implementa auto-trigger, il 60% delle richieste dell'utente viene gestito da Sisyphus-junior generico anziché dallo skill specialistica più adatta. L'utente dice "salva tutto" e Sisyphus fa un `git add -A` a mano invece di usare `git-warfare`. **Degradamento esperienza progressivo.**

**Cascata 3 — Hardcoded Key diventa Minaccia di Sicurezza**
- `debate_orchestrator.py` contiene una API key (`b46bc05b...`) hardcoded in chiaro. Se il file viene caricato su GitHub per sbaglio (e l'utente usa "salva tutto"), quella chiave è compromessa. **A 6 mesi il rischio di leak è elevato** perché il fallback viene usato sempre più spesso (la logica principale OpenCode potrebbe non funzionare con nuovi modelli).

### 🕛 Tra 12 mesi (Maggio 2027)

**Disastro 1 — L'Architettura è Inestendibile**
- 10 skill attuali + 3-4 nuove "a mano" nel 2027 = 14-15 skill. Nessun pattern di registrazione. Ogni nuova skill richiede:
  1. Creare cartella
  2. Scrivere SKILL.md a memoria
  3. Sperare che Sisyphus la trovi
  4. Aggiungere regole special case in ogni altro skill che potrebbe interagire
- **Tempo di onboarding per una nuova skill: 2-3 ore.** Tempo ideale: 10 minuti.

**Disastro 2 — Il Branching Git è Anarchico**
- `git-warfare` non ha modalità feature branch. Tutto va su `main`/`master` o branch corrente. Tra 12 mesi, con più progetti paralleli (VST, gioco, trading), il repository è un **mazzo di spaghetti**. Merge conflicts quotidiani. L'utente smette di usare skill e torna a GitHub Desktop.

**Disastro 3 — Dipendenze Esterne Rotte**
- `giotto` dipende da `D:\giotto-image-gen\`. Se cambi PC, formatti, o sposti la cartella, giotto muore.
- `music-producer` dipende da `D:\MOTUS2.0\bin\`. Stesso problema.
- `vision` dipende da `gemma4:e4b` locale. Se Ollama aggiorna e cambia API response, `skill_vision.py` crasha con `JSONDecodeError` perché non ha gestione robusta.

**Disastro 4 — Assemblea Diventa un Collo di Bottiglia**
- Con più progetti complessi, l'Assemblea viene convocata 5-10 volte al giorno. La Fase 2 parallela funziona, ma la Fase 3 sequenziale è lenta. Nessuna cache dei verbali. Stessi argomenti ridiscussi da zero. **Debito cognitivo per l'utente.**

**Costo Proiettato a 12 mesi (status quo):** ~$5-8/mese (token sprecati + uso cloud crescente).

### 🕛 Tra 24 mesi (Maggio 2028)

**Collasso 1 — Architettura Abbandonata**
- Lo sforzo mentale per ricordare "quale skill fa cosa" supera il beneficio. L'utente disinstalla 70% delle skill e torna a prompt generici. Le 10 skill rimaste come zombi in `~/.config/opencode/skill/`, nessuno le toglie per paura di rompere qualcosa.

**Collasso 2 — Remote-Tradingbot Diventa Unmaintained**
- 154 righe → 280 righe di patch ad-hoc. Il bot trading è cambiato 4 volte nelle baseline. La dashboard è passata da Flask a FastAPI. nessuno ha aggiornato la skill. **La skill fornisce comandi SSH obsoleti.** Se l'utente la esegue, rischia di killare il bot.

**Collasso 3 — Costi Esplosi**
- $0.14/mese → **$25-40/mese**. Perché? Perché senza auto-trigger e context-slimming automatico, l'utente invoca modelli cloud per task che potrebbero essere locali. Il fallback `debate_orchestrator.py` (che chiama cloud diretto) viene usato sempre più spesso.

**Collasso 4 — Rinominazioni Diventano Impossibili**
- Dopo 24 mesi di utilizzo quotidiano, i nomi `git-warfare`, `context-slimmer`, `remote-tradingbot` sono "muscolo mnemonico" dell'utente. Rinominarli diventa **cognitivamente inaccettabile** — come cambiare le scorciatoie di tastiera di Vim dopo 10 anni.

**Verdetto Scenario A:** L'architettura diventa un **legacy burden**. Non fallisce in modo spettacolare, ma degrada lentamente fino a essere ignorata.

---

## SCENARIO B: SE SI IMPLEMENTANO TUTTE LE PROPOSTE

### 🕐 Tra 3 mesi (Agosto 2026) — Fase di Transizione

**Miglioramento 1 — Categorie Corrette**
- Categoria `deep` → `glm-5.1`. Il Contabile diventa diretto, concreto. I verbali dell'Assemblea sono più snelli. **Risparmio tempo per dibattito: ~20%.**

**Miglioramento 2 — Le Orfane Trovano Casa**
- `generazione` → `doodle-fast` con SKILL.md e triggers (`disegna`, `crea immagine`).
- `vision` → `peek` con SKILL.md e triggers (`analizza immagine`, `descrivi`).
- Ora Sisyphus può auto-disambiguare: "genera immagine artistica" → giotto; "disegna un icona veloce" → doodle-fast; "cosa c'è in questa foto?" → peek.

**Miglioramento 3 — Remote-Tradingbot Smembrato**
- `remote-tradingbot` diventa:
  - `tradingbot-core` (comandi SSH, stato, riavvio)
  - `tradingbot-config` (baseline, parametri Kelly, gestione utenti)
  - `tradingbot-deploy` (deploy, file transfer, dashboard, Tailscale)
- **Ogni sub-skill è <60 righe.** Modifica di un parametro di sicurezza non tocca più la dashboard. 

**Miglioramento 4 — Context-Slimming Invisibile**
- Hook automatico: ogni task con categoria `deep`, `ultrabrain`, o `deepseek-v4-pro` attiva context-slimmer in pre-processing.
- **Risparmio token: 40%+ garantito.** Il costo cala da $0.14 a ~$0.08/mese.

### 🕕 Tra 6 mesi (Novembre 2026) — Fase di Crescita

**Accelerazione 1 — Git-Warfare V2**
- Modalità feature branch: `git-warfare feature nome-branch` crea branch, fa commit, push.
- L'utente sviluppa `vst-architect` su branch isolato. Nessun conflitto con `main`.
- Commit più piccoli, più frequenti, più puliti.

**Accelerazione 2 — Skill-Index.json + Auto-Trigger**
- `skill-index.json` elenca tutte le skill con: nome, descrizione, triggers, dipendenze, modello preferito.
- Wrapper pre-prompt legge l'indice e inietta: "L'utente ha detto 'analizza brano' → carica music-producer".
- **Onboarding nuova skill: 10 minuti** (aggiungi a skill-index.json).

**Accelerazione 3 — Nuove Skill Integrate**
- `vst-architect`: analisi progetti VST, routing audio, parametri DAW.
- `market-brief`: sintesi dati di mercato, prezzi hardware/software.
- `game-ci`: pipeline CI per Spazio13 (integrazione con `rocco`, ma automatica — `rocco` diventa CI/CD).
- Ogni nuova skill ha SKILL.md + entry in skill-index.json + trigger dedicato.

### 🕛 Tra 12 mesi (Maggio 2027) — Fase di Maturità

**Trasformazione 1 — Assemblea V5 Emergente**
- Con context-slimming automatico e modelli corretti, l'Assemblea processa topic in 40% meno tempo.
- I verbali vengono salvati in `assemblea/verbali/` con hash del topic. Se lo stesso topic ricorre, il sistema riutilizza il verbale precedente (cache semantica).
- Il fallback `debate_orchestrator.py` è stato **deprecato** — l'API key hardcoded è stata rimossa.

**Trasformazione 2 — Ecosistema Skill Coeso**
- Le 13-15 skill non sono più isole. `game-ci` chiama `rocco` automaticamente. `vst-architect` chiama `music-producer` per analisi loop. `market-brief` chiama `remote-tradingbot` per dati di mercato crypto.
- Esistono **skill pipelines**: combinazioni predefinite di skill che si attivano in sequenza per workflow complessi.

**Trasformazione 3 — Costi Stabili**
- Costo mensile: **$0.08-0.12**. Context-slimming automatico compensa la crescita del numero di skill. I modelli locali (`qwen2.5-coder`, `gemma4:e4b`, `lfm2.5`) vengono usati per il 70% dei task.

**Trasformazione 4 — Rinominazioni Completate Senza Trauma**
- Tutte le rinominazioni sono avvenute con **alias retrocompatibili**:
  - `git-warfare` → `git-pilot` (ma `git-warfare` funziona ancora come alias)
  - `context-slimmer` → `zip-context`
  - `music-producer` → `motus-audio`
  - `remote-tradingbot` → `dexter`
  - `generazione` → `doodle-fast`
  - `vision` → `peek`
- L'utente usa indifferentemente vecchi e nuovi nomi.

### 🕛 Tra 24 mesi (Maggio 2028) — Fase di Eccellenza

**Visione — L'Architettura è Auto-Curante**
- `skill-index.json` è auto-generato: uno script trimestrale analizza tutte le directory skill, verifica che SKILL.md esista, controlla che i triggers non si sovrappongano troppo (>70% overlap = warning).
- Il sistema ha un **Health Check Skill** che ogni settimana verifica:
  - Quale skill non è stata usata negli ultimi 30 giorni?
  - Quale dipendenza esterna (Ollama model, path D:\, servizio cloud) non risponde?
  - Quale SKILL.md è obsoleto (ultima modifica >6 mesi)?

**Visione — Assemblea come Meta-Skill**
- Assemblea non è più un dibattito "ad-hoc", ma un **meta-orchestratore**. Se `skill-index.json` rileva che 3 skill sono necessarie per un task, l'Assemblea le coordina automaticamente senza intervento umano.

**Visione — Nuovi Modelli, Zero Fatica**
- Se tra 24 mesi esce `deepseek-v5` o `qwen3.0`, la migrazione richiede **modifica di una sola riga** in `oh-my-openagent.json`. Tutti gli skill-index e category mapping si adattano automaticamente.

**Costo Proiettato a 24 mesi (tutte le proposte):** ~$0.10-0.15/mese.

---

## SCENARIO C: RISCHI FUTURI CHE NESSUNA PROPOSTA CONSIDERA

### 🔴 Rischio 1: Evoluzione API Ollama

**Probabilità:** Alta (>60% entro 24 mesi)
**Impatto:** Critico

Ollama ha già cambiato formato API 2 volte nel 2024-2025. `skill_vision.py` (peek) e `skill_generazione.py` (doodle-fast) usano l'API `/api/generate`. Se Ollama passa a `/v1/chat/completions` come formato standard (come sta già succedendo per compatibilità OpenAI), entrambe le skill smettono di funzionare.

**Mitigazione mancante nelle proposte:** Nessuna proposta prevede un **Ollama API Adapter** astratto. Ogni skill che chiama Ollama dovrebbe passare attraverso un wrapper con fallback format.

**Azione raccomandata:** Creare `core-ollama-api` (skill libreria) che unifica tutte le chiamate Ollama e gestisce versioning API.

---

### 🔴 Rischio 2: Saturation del Working Context

**Probabilità:** Alta (>70% entra 24 mesi)
**Impatto:** Alto

Con 15+ skill e auto-trigger, il "pre-prompt" di Sisyphus diventerà enorme. Se ogni skill aggiunge 500 token di istruzioni al system prompt, 15 skill = 7500 token solo di istruzioni statiche. **Il modello principale (deepseek-v4-flash) spende più token a ricordare le regole che a risolvere problemi.**

**Mitigazione mancante nelle proposte:** Nessuna proposta menziona **dynamic skill loading** — caricare nel context SOLO le skill rilevanti per il task corrente, non tutte.

**Azione raccomandata:** Implementare `dynamic-skill-loader`: il wrapper pre-prompt non inietta TUTTO skill-index.json, ma solo le 3-5 skill la cui cosine similarity con l'input utente è >0.6.

---

### 🟡 Rischio 3: Il Problema del "Nickle and Diming" Cloud

**Probabilità:** Media (40%)
**Impatto:** Medio

Oggi tutto costa $0.14/mese. Ma `deepseek-v4-flash` e `kimi-k2.6` hanno prezzi che cambiano. Se il provider Ollama cloud modifica i tier pricing, o limita le chiamate per API key, il costo potrebbe balzare a $5/mese da un giorno all'altro.

**Mitigazione mancante:** Nessuna proposta introduce un **Contabile Globale** — un modulo che traccia le chiamate e il costo in tempo reale, con alert soglia.

**Azione raccomandata:** Skill `cloud-watchdog` che logga ogni chiamata API, stima costo cumulativo, e forza fallback su modelli locali se si supera $1/mese.

---

### 🟡 Rischio 4: Model Drift nei LLM Locali

**Probabilità:** Media (50%)
**Impatto:** Medio

`qwen2.5-coder` è usato per: generazione commit git (`git-warfare`), traduzione prompt (`giotto`), analisi brani (`music-producer`). Se Ollama aggiorna qwen a `qwen2.5-coder:2.0` con cambiamenti di comportamento (più verboso, meno preciso con Python), 3 skill si rompono contemporaneamente.

**Mitigazione mancante:** Nessuna proposta fissa i tag modello. `qwen2.5-coder:latest` è pericoloso — prende automaticamente l'ultima versione.

**Azione raccomandata:** Usare SHA/tag specifici (`qwen2.5-coder:sha-abc123`) e avere un test suite (`skill-regression-test`) che verifica l'output di ogni skill su 10 casi di test noti.

---

### 🟡 Rischio 5: Skill Conflict e Race Condition

**Probabilità:** Media (45%)
**Impatto:** Medio-Alto

Con auto-trigger via `skill-index.json`, cosa succede se **due skill hanno triggers sovrapposti**?

Esempio:
- `giotto` triggers: `genera immagine, disegna, crea immagine`
- `doodle-fast` triggers: `disegna, crea icona, schizzo`

L'utente dice "disegna un albero". **Quale skill si attiva?** Primo match? Entrambe? Ultimo caricato?

Senza un **arbiter di trigger**, il sistema diventa non-deterministico.

**Mitigazione mancante:** Nessuna proposta parla di trigger priority, confidence score, o disambiguazione.

**Azione raccomandata:** Aggiungere a `skill-index.json` un campo `priority` e `confidence_threshold`. Se overlap, l'Assemblea chiede all'utente: "Vuoi generare un'immagine artistica (giotto) o veloce (doodle-fast)?"

---

### 🟢 Rischio 6: Dipendenza da Windows Path (`D:\`)

**Probabilità:** Bassa-Media (30%)
**Impatto:** Medio

`giotto`, `music-producer`, `rocco` (server), `doodle-fast` — tutti dipendono da path `D:\`. Se l'utente:
- Formatta e reinstalla Windows
- Cambia disco di lavoro in `E:\`
- Passa a Linux/Mac (WSL?)

...le skill muoiono. Non c'è discovery dinamica del path.

**Mitigazione mancante:** Nessuna proposta crea un `config-local.json` centralizzato con i path di sistema.

**Azione raccomandata:** Skill `env-bootstrap` che rileva i path disponibili e crea symlink/config centralizzato.

---

## SCENARIO D: COSA SARÀ OBSOLETO TRA 12-24 MESI

### Obsolescenza Pianificata (da sostituire)

| Componente | Quando | Perché diventa obsoleto | Sostituto naturale |
|------------|--------|-------------------------|-------------------|
| `debate_orchestrator.py` | 6-12 mesi | Fallback cloud con API key hardcoded; il sistema principale OpenCode è sufficiente | Eliminare, usare solo sub-agenti nativi |
| `skill_generazione.py` (vecchio) | 3-6 mesi | Orfano, no SKILL.md, traduzione euristica ridicola ("disegna un albero" → "draw a tree" per lookup) | `doodle-fast` con SKILL.md e prompt engineering |
| `skill_vision.py` (vecchio) | 3-6 mesi | Orfano, no triggers, modello `gemma4:e4b` limitato | `peek` integrato con più modelli vision |
| Manuale context-slimming | 3 mesi | Non scalabile, richiede attenzione umana | Hook automatico |
| `git-warfare` mono-branch | 6 mesi | Non gestisce workflow moderni | `git-pilot` con feature branch + rebase |

### Obsolescenza Tecnologica (esterna, non controllabile)

| Tecnologia | Quando | Perché | Impatto su MOTUS |
|------------|--------|--------|-----------------|
| `deepseek-v4-flash` | 12-18 mesi | Uscirà v5, v6. Flash potrebbe essere deprecato | Cambio `oh-my-openagent.json`, ma impatto zero se categorie sono agnostiche |
| `x/flux2-klein:4b` (doodle-fast) | 12 mesi | Modelli locali di generazione immagini migliorano rapidamente; 4B è già piccolo | Sostituzione con SDXL-turbo o modello 8B più recente |
| `gemma4:e4b` (peek) | 18 mesi | Google rilascia gemma5; e4b diventa obsoleto | Passaggio a moondream2 o llama-3.2-vision |
| API key hardcoded | **IMMEDIATO** | Pratica insicura per definizione | Sostituzione con variabile d'ambiente |

### Obsolescenza Concettuale

**"SKILL.md come unico metadato"** (12 mesi)
- SKILL.md è un buon formato human-readable, ma non è machine-readable agevolmente. Tra 12 mesi, con 15+ skill, serve un formato ibrido: YAML frontmatter + corpo markdown. `skill-index.json` è il primo passo verso un registro machine-readable.

**"Ogni skill gestisce le proprie dipendenze"** (18 mesi)
- Attualmente giotto installa i suoi pip, music-producer installa i suoi. Tra 18 mesi serve un **dependency manager unificato** per skill (tipo `requirements.txt` per skill, gestito da un bootstrap skill).

---

## SCENARIO E: QUALI SKILL DIVENTERANNO PIÙ IMPORTANTI NEL TEMPO

### 📈 Tra 6 mesi

#### 1. `context-slimmer` / `zip-context`
- **Perché cresce:** Più skill = più contesto = più token. Il risparmio passa da "nice to have" a "obbligatorio per non spendare $10/mese".
- **Nuovo ruolo:** Non solo comprime, ma **seleziona** — decide quali file sono rilevanti per il task corrente (intelligenza oltre la compressione).

#### 2. `assemblea`
- **Perché cresce:** Con più skill complesse, le decisioni architetturali richiedono dibattito. L'Assemblea passa da "strumento occasionale" a "processo decisionale di default".

#### 3. `git-pilot` (ex warfare)
- **Perché cresce:** Con `vst-architect`, `market-brief`, `game-ci`, ci sono più repo/branch/feature. Il versionamento diventa quotidiano.

### 📈 Tra 12 mesi

#### 4. `game-ci` + `rocco`
- **Perché cresce:** Se Spazio13 (gioco) evolve, il testing automatico diventa mission-critical. Rocco passa da "QA manuale dopo change" a "CI pipeline pre-commit". Game-ci è l'orchestratore.
- **Skill sinergica:** `game-ci` potrebbe diventare la più importante se il gioco diventa il progetto principale dell'utente.

#### 5. `dexter` (ex remote-tradingbot)
- **Perché cresce:** Il tradingbot è già live con soldi veri (22.15€). Se il capitale cresce, la precisione dei comandi SSH diventa **finanziariamente critica**. Dexter non è "una skill", è un'interfaccia a un sistema monetario.
- **Attenzione:** Alta responsabilità = maggior rischio. Dexter deve avere test più rigorosi.

#### 6. `peek` (ex vision)
- **Perché cresce:** I modelli vision diventano più capaci. Peek non sarà solo "descrivi immagine" ma "analizza screenshot di errore", "leggi grafico di trading", "controlla UI". Diventa uno **swiss army knife** per input non testuali.

### 📈 Tra 24 mesi

#### 7. Meta-Skill: `skill-gardener`
- **Non esiste ancora, ma emergerà.** Una skill che:
  - Controlla lo stato di salute di tutte le altre skill
  - Suggerisce refactoring basato su utilizzo
  - Rileva dead code
  - Auto-propone rinominazioni quando i nomi diventano confusi
  - Fa "pruning" delle skill non usate da >6 mesi
- **Analogia:** Da giardiniere a architetto del giardino.

#### 8. `motus-audio` (ex music-producer)
- **Perché cresce:** Se MOTUS2.0 diventa un progetto serio (release, streaming, monetizzazione), l'analisi tecnica dei brani passa da "hobby" a "workflow professionale". Potrebbe integrarsi con DAW, generare report per distributori digitali, analizzare loudness per piattaforme (Spotify -14 LUFS, YouTube -13 LUFS, ecc.).

---

## MATRICE DI IMPATTO: PROPOSTE vs RISCHI

| Proposta | Mitiga Debito | Introduce Rischio | Priorità Time Traveler |
|----------|-------------|-------------------|----------------------|
| 1. Fix `deep`→`glm-5.1` | 🔴 Alto | 🟢 Nessuno | **CRITICA — 0 mesi** |
| 2. SKILL.md per orfane | 🔴 Alto | 🟢 Nessuno | **CRITICA — 0-1 mesi** |
| 3. Split tradingbot | 🔴 Alto | 🟡 Basso (regression SSH) | **ALTA — 1-2 mesi** |
| 4. Context-slimmer auto | 🟡 Medio | 🟢 Nessuno | **ALTA — 1 mese** |
| 5. Git feature branch | 🟡 Medio | 🟢 Nessuno | **MEDIA — 2-3 mesi** |
| 6. Nuove skill (vst, market, ci) | 🟢 Basso (estensione) | 🟡 Medio (saturation context) | **BASSA — 6+ mesi** |
| 7. Auto-trigger + skill-index | 🔴 Alto | 🟡 Medio (trigger conflicts) | **ALTA — 2-3 mesi** |
| 8. Rinominazioni | 🟡 Medio | 🟢 Nessuno (con alias) | **MEDIA-BASSA — 3-6 mesi** |

---

## RACCOMANDAZIONI FINALI DEL TIME TRAVELER

### Ordine di Intervento Ottimale

**Mese 0 (Oggi):**
1. ✅ Fix `deep` → `glm-5.1` in `oh-my-openagent.json` (1 minuto)
2. ✅ Rimuovere API key hardcoded da `debate_orchestrator.py`, sostituirla con `os.environ.get(...)` (5 minuti)
3. ✅ Creare `skill-index.json` base con le 10 skill esistenti (20 minuti)

**Mese 1:**
4. Creare SKILL.md per `generazione` (→ `doodle-fast`) e `vision` (→ `peek`)
5. Implementare hook context-slimmer automatico
6. Aggiungere alias retrocompatibili per future rinominazioni

**Mese 2:**
7. Split `remote-tradingbot` in 3 sub-skill con test suite SSH mock
8. Aggiungere modalità feature branch a `git-warfare`
9. Implementare **trigger arbiter** (disambiguazione con priority)

**Mese 3-6:**
10. Sviluppare `skill-gardener` (health check skill)
11. Creare `cloud-watchdog` per tracking costi API
12. Aggiungere `Ollama API Adapter` unificato

**Mese 6+:**
13. **Solo dopo** le basi, implementare le nuove skill (`vst-architect`, `market-brief`, `game-ci`).
    - Perché dopo? Perché aggiungere skill a un ecosistema instabile è come costruire piani alti su fondamenta rotte. Le nuove skill devono "installarsi" automaticamente via `skill-index.json`.

### La Regola d'Oro

> **"Non aggiungere skill prima di aver sistemato le 10 che hai."**

Il numero magico è **10 skill ± 2**. Con 10 skill ben gestite, l'architettura MOTUS è sostenibile a 24 mesi. Con 15 skill mal gestite, diventa un **cimitero di metadati**.

### Il Verdetto

- **Se non fai nulla (Scenario A):** Tra 24 mesi avrai un'architettura funzionante ma ignorata — l'utente userà il 20% delle skill e farà tutto a mano. Costo: basso, ma zero valore aggiunto.
- **Se implementi TUTTO (Scenario B):** Tra 24 mesi avrai un ecosistema auto-curante, coeso, economico. Il problema non sarà più "come gestisco le skill?", ma "quale skill mi serve per questo nuovo compito?"
- **I rischi nascosti (Scenario C)** sono reali ma mitigabili. Il più pericoloso è il **saturamento del context** — una skill con 15 trigger caricati nel system prompt di Sisyphus diventa paralizzato, non potenziato.

**La soluzione perfetta non è più skill. È meno skill visibili alla volta.**

---

*Verbale redatto da: The Time Traveler*
*Fase: 4 — Verifica Finale*
*Obiezioni irrisolte: Nessuna (ma il Avvocato del Diavolo suggerisce di non fidarsi delle API esterne)*
*Piano d'Azione: Vedi "Ordine di Intervento Ottimale" sopra*

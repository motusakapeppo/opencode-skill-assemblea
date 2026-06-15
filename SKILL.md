---
name: assemblea
description: "Assemblea V5 — Dibattito multi-agente asimmetrico con routing esplicito, moduli specialistici attivabili e metriche di chiusura"
triggers: fai un'assemblea, organizza un dibattito, analizza tutto, stress test, problema complesso, brainstorm, progetta architettura, trova difetti, dibattito, trova soluzione ibrida, assemblea plenaria, delibera, ordine del giorno, verbale assemblea, discuti, confronta, valuta
---

# Assemblea V5 — Intelligent Hybrid Engine

## Architettura del Cast (Routing Asimmetrico)

| Ruolo | Dove gira | Modello | Categoria | Perché |
|-------|-----------|---------|-----------|--------|
| **Presidente** | Sisyphus (io) | deepseek-v4-flash | — | Moderatore veloce, orchestro la chat |
| **L'Hacker** | Sub-agente | kimi-k2.7-code | `quick` | Proposte concrete, coding, implementazione |
| **Il Contabile** | Sub-agente | minimax-m3 | `deep` | Numeri, costi, ROI |
| **L'Utente** | Sub-agente | minimax-m3 | `deep` | Voce del cliente, semplicità |
| **L'Avvocato del Diavolo** | Sub-agente | deepseek-v4-flash | `ultrabrain` | Critica puntuale, anti-sycophancy |
| **Lead Architect** | Sub-agente | deepseek-v4-flash | `ultrabrain` | Sintesi finale e verbale |

### Mappa modelli effettiva (da oh-my-openagent.json)
```
kimi-k2.7-code (256K):    Hacker (quick) — coding specialist
minimax-m3 (1M ctx):      Contabile, Utente (deep) — analitico, linguaggio naturale
deepseek-v4-flash (1M):   Avvocato, Lead Architect (ultrabrain)
deepseek-v4-pro (1M):     Solo per analisi offline (MAI in assemblea)
```

### REGOLE FERREE
- **MAI** delegare modelli locali a dibattiti — non sanno farlo
- **MAI** usare deepseek-v4-pro nell'Assemblea — cold start 5-10s
- **SEMPRE** Avvocato per ultimo nel dibattito (antisycophancy)
- **SEMPRE** registrare obiezioni non risolte nel verbale

## Fase 0 — Triage e Modalità

Calcola la complessità dell'input con la formula:

```
Base:     min(parole_input × 0.3, 2.0)
Segnali:  count(keyword_match) × 0.5
Tech:     count(API, SQL, GPU, CPU, DB, Cloud, deploy) × 0.3
Numeri:   count(digits) × 0.2
Totale:   min(Base + Segnali + Tech + Numeri, 10.0)
```

### Soglie e Modalità

| Totale | Modalità | Ruoli | Timeout sub-agente |
|--------|----------|-------|--------------------|
| < 4 | **Light** | Hacker + Utente + Lead | **60s** |
| 4-6 | **Standard** | Hacker + Contabile + Utente + Avvocato + Lead | **90s** |
| 6-8 | **Full** | Tutti i 6 + moduli specialistici | **120s** |
| > 8 | **Full + Esteso** | Tutti + moduli + analisi supplementare | **150s** |
| N/A (Trigger condizionale) | **Esplorazione (Divergente)** | Hacker (unbound) + Utente + Avvocato (survival filter) + Lead (cluster) | **120s** |

### Condizione d'innesco Esplorazione

La modalità Esplorazione NON si basa sul punteggio di complessità, ma su un trigger
condizionale separato:

- **Si attiva quando**: (segnali_divergenza ≥ 2) AND (segnali_urgenza == 0)
- **Segnali divergenza**: brainstorming, esplora, senza limiti, alternative radicali, fuori dagli schemi, design da zero, pensiero laterale, blue sky
- **Segnali urgenza**: produzione, crash, budget, deadline, mission-critical, failure

Questa modalità è pensata per fasi di design divergente in cui si cerca il maggior
numero di idee possibile prima di restringere il campo.

### Trigger moduli specialistici (solo Full/Esteso, AND esplicito)
| Modulo | Condizione | Cosa fa |
|--------|-----------|---------|
| **The Infiltrator** | (segnali security ≥2) AND (complessità ≥5) | Trova difetti argomentativi e bias cognitivi nel dibattito |
| **The Time Traveler** | (segnali scalabilità ≥2) AND (complessità ≥6) | Proietta impatto delle decisioni a 12 mesi |
| **Chaos Simulator** | (parole "failure/mission-critical" ≥1) AND (complessità ≥7) | Introduce 2 guasti forzati e obbliga piano B |

**Se nessun trigger scatta**, l'Assemblea Full procede uguale senza moduli.

### Memoria Storica (RAG pre-assemblea)

Prima di convocare, il Presidente recupera i verbali delle assemblee precedenti
che trattano argomenti simili:

```typescript
// Se la skill knowledge è disponibile
task(subagent_type="explore", run_in_background=true,
  prompt="Cerca nei verbali di assemblee precedenti su: <keywords problema>.
  Cerca file con pattern 'verbale' o 'assemblea' in D:\ o C:\Users\motus\.
  Se trovi, restituisci le decisioni e le obiezioni non risolte.")
```

Se trova risultati, li include nel prompt dell'Avvocato e del Lead Architect:
```
--- DECISIONI PRECEDENTI (da verbali archiviati) ---
<risultati_ricerca>
--- FINE DECISIONI PRECEDENTI ---
```

Questo evita che l'assemblea ripeta ciclicamente errori già discussi
o dibatta soluzioni già scartate.

### Task Plan (obbligatorio dopo il Triage)

Alla fine del calcolo della complessità, il Presidente DEVE stampare un
Task Plan formale che elenca ESATTAMENTE l'ordine di esecuzione:

```
Task Plan:
---
1. Esecuzione Parallela: Hacker, Contabile, Utente
2. Esecuzione Sequenziale: Avvocato del Diavolo
3. Esecuzione Moduli: [The Infiltrator / The Time Traveler / Chaos Simulator — solo se attivati, altrimenti "Nessuno"]
4. Esecuzione Bloccante Prima di Chiusura: [moduli attivati]
5. Chiusura: Lead Architect
```

Questo vincola l'orchestratore a dichiarare esplicitamente ogni step,
rendendo impossibile "dimenticare" un modulo attivato.

## Fase 1 — Convocazione e OdG

```
ODG: "Delibera su: <problema>"
Modalità: Light | Standard | Full | Esteso | Esplorazione
Partecipanti: <ruoli>
Moduli Specialistici: <attivati/non attivati>
Complessità: <X/10> (N/A per Esplorazione)
Timeout sub-agente: <60-150s in base a complessità>
Max repliche: 2 giri + 1 controreplica Avvocato (N/A per Esplorazione)
Decisioni Precedenti: <trovate/non trovate>
```

## Fase 2 — Proposte Indipendenti (PARALLELE + Avvocato ASINCRONO)

Lanciare Hacker + Contabile + Utente IN PARALLELO.
L'Avvocato parte in background non appena il PRIMO dei tre finisce,
e accumula gli output incrementalmente via continuation session.

```typescript
// Step 1: Lancia i 3 in parallelo
const hackerTask = task(category="quick", run_in_background=true, prompt="Sei l'HACKER...")
const contabileTask = task(category="deep", run_in_background=true, prompt="Sei il CONTABILE...")
const utenteTask = task(category="deep", run_in_background=true, prompt="Sei l'UTENTE...")

// Step 2: Non appena UNO finisce, parti con l'Avvocato in background
// Usa continuation session per passargli incrementalmente gli output
const avvocatoSession = task(
  category="ultrabrain",
  run_in_background=true,
  prompt="Sei l'AVVOCATO DEL DIAVOLO. Per ora hai solo: <output_primo_arrivato>.
  Aspetta gli altri interventi, poi completa la critica."
)

// Step 3: Quando arrivano gli altri, passa il context via continuation
task(task_id=avvocatoSession.session_id,
  prompt="Aggiungi anche questa proposta alla tua analisi: <output_secondo>")
task(task_id=avvocatoSession.session_id,
  prompt="Aggiungi anche questa: <output_terzo>. Ora emetti la critica completa.")
```

Questo riduce i tempi morti: invece di attendere TUTTI e 3 prima di partire,
l'Avvocato inizia a elaborare dopo il primo risultato.

### Template prompt per ruolo

**Hacker** (quick → kimi-k2.7-code):
```
Sei l'HACKER in un'Assemblea. Sei creativo, pratico, guardi a soluzioni che funzionano.
ODG: "<OdG>"
Fai 2-3 proposte CONCRETE. Massimo 3 paragrafi.
```

**Hacker — Modalità Esplorazione** (quick → kimi-k2.7-code):
```
Sei l'HACKER in un'Assemblea in modalità Esplorazione.
ODG: "<OdG>"
Ignora i limiti di lunghezza. Genera il maggior numero di soluzioni tecniche
possibili, concentrandoti su edge-case, pattern sperimentali e pensieri
laterali estremi.

STRUTTURA OBBLIGATORIA DELL'OUTPUT: organizza le idee per categoria
(es. Kernel, Syscall, Memoria, Scheduling, Filesystem, Edge Cases, Laterali).
Dentro ogni categoria, NUMERA ogni idea (es. "Kernel idea 1:", "Kernel idea 2:").
Ogni idea deve avere un NOME e una DESCRIZIONE implementativa di 1-2 frasi.
Questo permetterà all'Avvocato di fare FATAL FLAW idea per idea.
```

**Contabile** (deep → M3):
```
Sei il CONTABILE in un'Assemblea. Sei analitico, basato sui numeri e costi/benefici.
ODG: "<OdG>"
Analizza con DATI: costi, tempi, rischi quantificabili. Massimo 3 paragrafi.
```

**Utente** (deep → M3):
```
Sei l'UTENTE in un'Assemblea. Sei la voce del cliente finale: vuoi cose che FUNZIONANO e siano SEMPLICI.
ODG: "<OdG>"
Parla semplice e diretto. Cosa ti preoccupa? Massimo 2 paragrafi.
```

**Avvocato del Diavolo** (ultrabrain → flash):
```
Sei l'AVVOCATO DEL DIAVOLO. Hai letto TUTTE le proposte degli altri.
--- PROPOSTE RICEVUTE ---
Hacker: <...>
Contabile: <...>
Utente: <...>
--- FINE PROPOSTE ---
--- DECISIONI PRECEDENTI (se trovate) ---
<verbali_archiviati>
--- FINE DECISIONI PRECEDENTI ---
ODG: "<OdG>"
Trova ESATTAMENTE 2-3 difetti per OGNI posizione. Se ci sono decisioni
precedenti, verifica se qualche proposta sta ripetendo errori già discussi.
Sii critico e concreto. Massimo 4 paragrafi.
```

**Avvocato — Modalità Esplorazione** (ultrabrain → flash):
```
Sei l'AVVOCATO DEL DIAVOLO in modalità Esplorazione.
Hai letto la lista di idee di Hacker.
ODG: "<OdG>"
Non criticare i dettagli e non cercare 3 difetti per proposta.
Il tuo UNICO scopo è eliminare con un 'FATAL FLAW' esclusivo le opzioni
matematicamente, fisicamente o economicamente impossibili. Ignora le altre.

STRUTTURA OBBLIGATORIA DELL'OUTPUT:
1. Per ogni idea eliminata: specifica "IDEA X — FATAL FLAW: [motivo: matematico/fisico/economico]"
2. Per le idee sopravvissute: raggruppale per categoria e restituisci l'ELENCO COMPLETO
   con NUMERO e NOME di ogni idea, in modo che il Lead Architect possa riferirvisi
   esattamente. Esempio:
   "SOPRAVVISSUTE - KERNEL: Idea 1 (Zero-copy ring buffer), Idea 2 (Capability routing), ..."
   "SOPRAVVISSUTE - SYSCALL: Idea 9 (JSON-LD intent), Idea 10 (Idempotenza UUIDv7), ..."
```

**Lead Architect** (ultrabrain → flash):
```
Sei il LEAD ARCHITECT. Hai ricevuto dal Presidente:
--- PROPOSTE HACKER (per categoria) ---
<output_hacker_organizzato>
--- FINE PROPOSTE HACKER ---
--- CRITICHE AVVOCATO ---
<output_avvocato>
--- FINE CRITICHE AVVOCATO ---
--- PROPOSTA UTENTE ---
<output_utente>
--- FINE PROPOSTA UTENTE ---
--- DECISIONI PRECEDENTI (se trovate) ---
<verbali_archiviati>
--- FINE DECISIONI PRECEDENTI ---
--- OUTPUT MODULI SPECIALISTICI (se attivati) ---
<output_moduli>
--- FINE OUTPUT MODULI ---
ODG: "<OdG>"
Proponi il verbale finale con: sintesi, obiezioni irrisolte, decisione,
allegato tecnico, piano d'azione. Evita di riproporre soluzioni già
scartate in precedenza.

REGOOLA VINCOLANTE: Se The Infiltrator è stato attivato durante l'assemblea,
il tuo verbale DEVE includere una sezione intitolata "Bias Cognitivi Rilevati"
basata esclusivamente sul suo output. Non omettere questa sezione.
```

**Lead Architect — Modalità Esplorazione** (ultrabrain → flash):
```
Sei il LEAD ARCHITECT in modalità Esplorazione.
Hai ricevuto dal Presidente:
--- IDEE HACKER (per categoria, numerate) ---
<output_hacker_organizzato>
--- FINE IDEE HACKER ---
--- FILTRO AVVOCATO (FATAL FLAW + sopravvissute) ---
<output_avvocato>
--- FINE FILTRO AVVOCATO ---
--- VOCE UTENTE ---
<output_utente>
--- FINE VOCE UTENTE ---
ODG: "<OdG>"
Non forzare una decisione architetturale univoca.
Il tuo verbale finale deve clusterizzare le idee sopravvissute al filtro
dell'Avvocato in categorie strategiche (es. Soluzioni a Basso Rischio,
Concept Sperimentali, Alta Complessità/Alta Resa).
```

### Template moduli specialistici (solo se attivati)

**The Infiltrator**:
```
Sei THE INFILTRATOR nel dibattito. Hai letto TUTTI gli interventi.
ODG: "<OdG>"
Identifica 3 bias cognitivi o difetti argomentativi nel dibattito
(echo chamber, false equivalence, confirmation bias).
Per ognuno: cita il passaggio incriminato e spiega perché è debole.
```

**The Time Traveler**:
```
Sei THE TIME TRAVELER. Hai letto TUTTI gli interventi.
ODG: "<OdG>"
Proietta le decisioni proposte a 12 mesi. Cosa sembra una buona idea
oggi ma sarà un problema domani? Quali scelte sono reversibili? Quali no?
Massimo 3 paragrafi.
```

**Chaos Simulator**:
```
Sei CHAOS SIMULATOR. Hai letto TUTTI gli interventi.
ODG: "<OdG>"
Introduci 2 GUASTI forzati (es. "il modello primario va down",
"il requisito cambia a metà").
Per ognuno: la decisione dell'Assemblea regge o serve piano B?
```

### Fallback sub-agente
Se un sub-agente **non risponde entro il timeout** (60/90/120/150s
in base a complessità) o **restituisce errore**:
1. Riprova 1 volta
2. Se fallisce ancora → registra "Voce X: non disponibile per esaurimento turni"
3. Il verbale finale rifletterà la sintesi con la voce mancante + flag esplicito

Se un sub-agente **risponde ma con contenuto inutilizzabile** (allucinazioni, fuori tema):
- Ignora il contenuto, registra "Voce X: output non valido"
- Non ritentare — il costo di un secondo tentativo per qualità è uguale a gestire l'assenza

### Ordine di Convocazione
1. **Hacker + Contabile + Utente** — in PARALLELO (Fase 2)
2. **Avvocato del Diavolo** — PARTE in background SUBITO dopo il PRIMO risultato,
   poi completa con gli altri via continuation session
3. **Moduli Specialistici** — se attivati nel Task Plan, IN PARALLELO tra loro,
   PRIMA del Lead Architect. Bloccante: non procedere oltre senza i loro output.
4. **Lead Architect** — DOPO, vede tutto (proposte + dibattito + output moduli)

## Fase 3 — Dibattito (SEQUENZIALE, max 2 giri)

Dopo l'Avvocato, giro di tavolo sequenziale (max 2 repliche + 1 controreplica Avvocato):

1. **Hacker replica** — risponde alle critiche che lo riguardano (max 2 paragrafi)
2. **Contabile replica** — difende i suoi numeri (max 2 paragrafi)
3. **Utente replica** — dice cosa ne pensa (max 1 paragrafo)
4. **Avvocato controreplica** — ULTIMO, sintetizza le difese e ribatte (max 3 paragrafi)

Se dopo 2 giri il disaccordo persiste → si registra come "obiezione non risolta" nel verbale.

### Moduli Specialistici (solo Full/Esteso, dopo il dibattito)
The Infiltrator / Time Traveler / Chaos Simulator — in parallelo tra loro.

**REGOOLA FERREA**: Se un modulo è stato flaggato come "Attivato" nel Task Plan,
è TASSATIVO invocarlo e attendere la stampa dei suoi output PRIMA di procedere
alla Fase 4. I moduli NON sono opzionali — sono un prerequisite bloccante.

## Fase 4 — Verbale Finale (Lead Architect)

**PREREQUISITO RIGIDO**: Prima di convocare il Lead Architect, verifica l'esito
del Task Plan (Fase 0). Se The Infiltrator, The Time Traveler o Chaos Simulator
sono stati flaggati come "Attivati" nello step 3-4 del Task Plan, è TASSATIVO
invocarli e attendere la stampa dei loro output. Non generare la sintesi finale
senza aver prima iniettato le loro analisi nel contesto del Lead Architect.

**REGOOLA DI PASSAGGIO CONTESTO (Presidente)**:
Il Presidente DEVE preparare e iniettare nel prompt del Lead Architect:
1. `output_hacker_organizzato`: l'output di Hacker riorganizzato per CATEGORIA
   con idee numerate (es. "Kernel: 1. Zero-copy ring buffer, 2. Capability routing...")
2. `output_avvocato`: l'output completo dell'Avvocato (critiche o survival filter)
3. `output_utente`: il testo integrale dell'intervento dell'Utente
4. `output_moduli`: output dei moduli specialistici, se attivati
5. `verbali_archiviati`: decisioni precedenti, se trovate

Il Presidente NON deve riassumere — deve passare i testi INTEGRALI.
I session_id dei sub-agenti (`ses_...`) devono essere conservati per eventuali
continuation se il Lead Architect ha domande di approfondimento su un intervento.

```markdown
# Verbale Assemblea — <data>

## Oggetto
<OdG originale>

## Partecipanti
<ruoli effettivi, flag voci non disponibili>

## Decisioni Precedenti Consultate
<sì/no, eventuali collegamenti>

## Riassunto degli Interventi
- Hacker: <sintesi>
- Contabile: <sintesi>
- Utente: <sintesi>
- Avvocato del Diavolo: <sintesi>

## Obiezioni Rilevanti NON Risolte
<elenco difetti che nessuno ha controbattuto>

## Decisione Architetturale Finale
<decisione motivata>

## Allegato Tecnico
```<linguaggio>
<codice/schema>
```

## Piano d'Azione
1. <step concreto>
2. <step concreto>
3. <step concreto>
```

## Metriche di Chiusura (da registrare a fine assemblea)

| Metrica | Valore |
|---------|--------|
| Durata stimata | <minuti> |
| Turni totali | <count> |
| Voci attive / totali | <X>/<Y> |
| Obiezioni sollevate | <count> |
| Obiezioni non risolte | <count> |
| Decisioni precedenti trovate | <sì/no> |
| Decisione finale | Accettata / Rimandata |

**Quality Gate**: se l'Avvocato ha sollevato < 3 obiezioni totali → rilancia
con "Sei sicuro? Non c'è niente da criticare?" (antisycophancy check).
Se obiezioni non risolte > 50% del totale → la decisione è fragile,
raccomanda rimandare.

## Vincoli Ferrei

- **MAI** delegare personaggi a modelli locali per dibattiti — non sanno farlo
- **MAI** usare deepseek-v4-pro nell'Assemblea — troppo lento per chat interattiva
- **SEMPRE** Avvocato per ultimo nel dibattito (antisycophancy)
- **SEMPRE** registrare obiezioni non risolte nel verbale
- **SEMPRE** registrare metriche di chiusura
- **SEMPRE** consultare memoria storica prima di partire
- Sub-agente fallito → 1 retry, poi skip con flag esplicito
- Timeout dinamico in base a complessità (60-150s)

## Validation Checklist (Presidente)

- [ ] Triage eseguito con formula? (niente modelli locali)
- [ ] Se Esplorazione: trigger condizionale verificato? (divergenza ≥2, urgenza == 0)
- [ ] Memoria storica consultata? Decisioni precedenti trovate?
- [ ] Modalità corretta (Light/Standard/Full/Esteso/Esplorazione)?
- [ ] Modelli locali evitati per dibattiti? (solo triage)
- [ ] Proposte lanciate in parallelo sulle categorie corrette?
- [ ] Avvocato partito asincrono dopo primo risultato?
- [ ] Avvocato ha visto tutte le proposte prima di criticare?
- [ ] Timeout dinamico in base a complessità?
- [ ] Dibattito sequenziale (non parallelo)? Max 2 giri?
- [ ] Moduli specialistici attivati solo se trigger match?
- [ ] Task Plan stampato con ordine esatto?
- [ ] Moduli specialistici attivati sono stati invocati PRIMA del Lead Architect?
- [ ] Output moduli iniettati nel contesto del Lead Architect?
- [ ] Lead Architect ha incluso sezione "Bias Cognitivi Rilevati" se Infiltrator attivato?
- [ ] Se Esplorazione: Hacker ha usato template unbound? Avvocato survival filter? Lead cluster?
- [ ] Metriche registrate a fine assemblea?
- [ ] deepseek-v4-pro NON usato?
- [ ] Verbale contiene obiezioni non risolte?
- [ ] Sub-agenti hanno parlato, non cercato su GitHub?
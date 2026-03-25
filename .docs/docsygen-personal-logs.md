# Docsygen — Note personali e log

Questo file raccoglie le mie note originali sul progetto e il log delle decisioni prese nel tempo. Non fa parte del template — serve a me per ricordare il ragionamento dietro le scelte.

---

# Note originali

## Fase di documentazione iniziale

### 1. Ideazione `.docs/idea.md`

Questa serie di procedure non va presa come una parte necessariamente separata o sequenziale. Vogliono portare ad un prodotto, quindi possono anche funzionare in ordine sparso.

1. Brain dump testuale o vocale su oggetto Idea
2. Un minimo di riordinamento in toggles in base al contenuto
3. Divisione tra sezioni e note sparse, a cui verranno aggiunte le future note (esempio pratico: Modular Dashboard)

### 2. Documento SEED `.docs/seed-document.md`

Rappresenta il file di riferimento, dove vivono tutte le informazioni principali. Riutilizzabile per gli altri steps.

### 3. Procedure UX `.docs/assets/imgs/prototypes/`

- Wireframes/Prototipo (a mano o AI: Claude, V0, Figma Make, Stitch)
- Verifica wireframes

### 4. Tech Stack `.docs/tech-stack.md`

### 5. Procedure UI `.docs/design-system.md`

---

## Lezione chiave: i componenti Lego

Dalla prova su Cantina Pulaio ho capito che costruire i componenti base prima di tutto il resto è fondamentale:
- Centralizza gli stili
- Minimizza le modifiche per cambiare design
- Semplifica la creazione di nuovi componenti
- Evita componenti con stili divergenti quando l'app cresce
- Permette di validare subito il design

Se hai i componenti pronti è come fare un puzzle — semplifichi la vita anche agli agenti AI.

---

## Idee sulla fase operativa

- **Task management**: tasks.md funziona ma fino a un certo punto. Difficile prevedere i task in anticipo, si finisce per saltare da una cosa all'altra. Meglio dividere per categoria/sezione che cronologicamente.
- **File possibili per feature**: history.md, onboarding.md, flow.md (flusso di navigazione con mermaid)
- **Comandi pensati inizialmente**: /continue, /feat, /review, /resume
- **Documentazione**: step separato, non dallo stesso agente che lavora sul codice. Il contesto deve restare pulito e focalizzato.
- **Regole generali**: sequenzialità nei task, usare le documentazioni (Context7), seguire tech stack e design system, usare variabili globali per gli stili

---

## Note sparse

- [ ] Design style selection con descrizioni tipo "Modern, minimal, flat design" o "Material, dark, modern" o "Editorial design, light". Ispirato da [questo articolo](https://tilda.education/en/web-design-styles#know)
- [ ] Mermaid diagrams per visualizzare i flussi: [link al diagramma](https://mermaid.live/edit#pako:eNpVjTFvgzAUhP-K9aZWIhGywQYPlRrSZonUDpkKGaxgMGqwkTFKU-C_16Sq2t70TnffvRFOppTAoTqby0kJ69BhW2jk9Zhnyja9a0V_RKvVw7STDrVGy-uENnc7g3pluq7R9f13f7OUUDbul5pETjX6ff6Oshv_ouWEtvledM50x7_J4WIm9JQ3r8rP_0-UlZ56zivBK7E6CYsyYY8QQG2bErizgwyglbYVi4VxgQtwSrayAO7PUlZiOLsCCj17rBP6zZj2h7RmqBX46XPv3dCVwsltI2orfitSl9JmZtAOeELJbQP4CB_ACWZryiJCKE5JjKMkgCtwStZRmqaU4YTRNIrJHMDn7Wm4TlgcemEaMhbiGM9fgt117g)
- L'idea originale della CLI RPG-style: splash screen con logo (elemento periodico dOc) -> menu con fasi -> conversazione guidata
- Accessibilità: audit per W3C e WCAG 2.1
- Priorità generali: Bellezza > Prestazioni > Sicurezza > Compliance

---

# Log delle decisioni

## 25 Marzo 2026 — Da CLI a custom commands

### Problema: questo non è una CLI, sono prompt

Inizialmente pensavo a docsygen come libreria CLI (con ratatui e tutto), ma il valore sta nei prompt, non nel tool. I prompt funzionano meglio dentro agent esistenti (Claude Code, Cursor, Antigravity) piuttosto che in un'app separata.

### Problema: centralizzazione multi-tool

Se i prompt vivono in `.claude/commands/` per Claude Code, e domani voglio usarli anche su Cursor o Antigravity, ho copie duplicate che divergono.

**Decisione**: per ora i prompt vivono direttamente in `.claude/commands/` e questo repo diventa un GitHub template. Quando la struttura sarà stabile, si crea uno script di sync che legge da un'unica fonte e genera i file nel formato di ogni tool.

> Non costruire il sync prima che i prompt siano stabili — altrimenti mantieni lo script attraverso ogni ristrutturazione.

### Ristrutturazione del flusso

Il flusso originale era lineare e mancava di pezzi importanti:

| Comando | Cosa cambia | Perché |
|---------|------------|--------|
| `/seed-review` | Nuovo | Stress-test delle assunzioni prima di investire tempo |
| `/prototype` | Riscritto | Genera un prompt per tool esterni (Stitch, Figma AI), non immagini. Messo prima dello stack perché i wireframe possono rivelare necessità tecniche |
| `/scaffold` | Nuovo, opzionale | Solo per stack senza template pronto (Swift, C#, ecc.) |
| `/resume` | Riscritto | Valutazione fresca da git log + file reali, non da tasks.md statico |
| `/sync` | Nuovo | Riconcilia docs e codice on demand. Il codice ha sempre ragione |

### Decisione chiave: niente tasks.md fisso

I task statici mentono appena il progetto evolve. `/resume` li genera freschi ogni volta leggendo lo stato reale. Struttura sì, ma senza perdere il flow.

### Struttura attuale del template

```
.claude/commands/          ← i comandi (il prodotto)
.docs/
  idea.md                  ← input utente, brain dump
  docsygen-personal-logs.md ← questo file
  assets/imgs/prototypes/  ← wireframe da tool esterni
CLAUDE.md                  ← regole progetto
README.md                  ← readme template pulito
```

### Prossimi step

1. Rendere questa repo un GitHub template (Settings > Template repository)
2. Testare i comandi su un progetto reale
3. Iterare sui prompt finché non sono stabili
4. Quando stabile: script di sync per multi-tool
5. Opzionale futuro: TUI con ratatui (splash screen con elemento periodico dOc, menu RPG-style)

---

## Conversazione di riferimento (25 Marzo 2026)

Includo l'estratto della conversazione che ha portato a queste decisioni, perché il ragionamento sui problemi principali è stato utile.

### Sul flusso

> **IO**: How would you evolve this series of prompts to help the user go from rough idea to the base structure of a project, with useful docs, both for humans and AIs?
>
> **CLAUDE**: The current flow is strong on the "what" (idea -> seed -> stack -> design) but weak on the bridge to "doing". Concrete gaps: no challenge step after /seed, no scaffold step, no feature breakdown, and the prototype step is awkward because text LLMs aren't great at generating wireframes.

### Sui task

> **IO**: This is a core question: how to handle todos, tasks? Projects are always evolving, and it is boring tackling them like a robotic checklist. Tasks should be dynamic. I usually worked without any tasks.md so that I could guide what to do, but I feel like some structure could make sense. I don't want to lose that feeling of flow and control.
>
> **CLAUDE**: The reason rigid task files feel wrong is because they lie. The moment you write a checklist, the project has already moved past it. You end up maintaining the list instead of doing the work. The answer is: don't store tasks, generate them fresh each time. /resume should read the actual state of the project every time and produce a fresh situational assessment. Not a backlog. A compass.

### Sul doc drift

> **IO**: I don't want the agent to keep track of every small tweak, that would be a waste of tokens. But I need something to make sure everything is in the right direction, or at least update docs if the direction changed, so that future workers know what is happening, even after brutal sessions where the developer went crazy with new features without thinking about docs.
>
> **CLAUDE**: Same philosophy: don't track continuously, reconcile on demand. A /sync command that you run when you feel things have gone off track. It reads the codebase, compares against docs, and proposes updates. The code is always right. You only pay the tokens when you choose to.

### Sul prototype

> **IO**: I generate prototypes in external tools like Stitch. That step should create a good prompt for graphic tools based on what we know about the project. And it's before tech stack because we may realize we need specific components.
>
> **CLAUDE**: This makes much more sense. The command should output a well-crafted prompt that you paste into Stitch, Figma AI, or whatever. It belongs before stack because what you see in the prototype might reveal you need drag-and-drop, real-time sync, camera access, etc.

### Flusso finale concordato

```
Phase 1 — Think:    /seed → /seed-review
Phase 2 — Shape:    /prototype → /prototype-verify → /stack → /design
Phase 3 — Build:    /scaffold (optional) → /resume
Phase 4 — Maintain: /sync
```

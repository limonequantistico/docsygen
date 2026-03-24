Per il momento questo progetto racchiude i prompt da usare nelle fasi iniziali di un progetto.

# Fase di documentazione iniziale

## 1. Ideazione(documento per me) `.docs/idea.md`

Questa serie di procedure non va presa come una parte necessariamente separata o sequenziale. Vogliono portare ad un prodotto, quindi possono anche funzionare in ordine sparso.

1. Brain dump testuale o vocale su oggetto Idea;
2. Un minimo di riordinamento in toggles in base al contenuto;
3. Divisione tra toggles (più che toggles direi sezioni) e Note sparse, a cui verranno aggiunte le future note;
   Esempio pratico: Modular Dashboard.

## 2. Documento SEED (documento per AI) `.docs/seed-document.md`

Rappresenta il file di riferimento, dove vivono tutte le informazioni principali. Riutilizzabile per gli altri steps.

- Creazione [Prompt]
- Estensione [Prompt]

## 3. Procedure UX `.docs/assets/imgs/prototypes/`

- Wireframes/Prototipo
  - a mano
  - AI
    - Prompt [Claude, V0, Figma Make, Stitch]
- Verifica wireframes [Prompt]

## 4. Definizione Tech Stack `.docs/tech-stack.md`

- Prompt Stack Nuovo
- Prompt aggiornamento Stack

## 5. Procedure UI `.docs/design-system.md`

- Prompt Design System (design-system.md)
- Update Prompt

---

**Componenti Lego**
Tra gli steps terrei a mente anche il fargli costruire i componenti iniziali, dicendogli quali servono sulla base dell'applicazione che viene creata. Molto utile a:
- centralizzare gli stili 
- minimizzare le modifiche per cambiare design se necessario
- semplificare la creazione di nuovi componenti sulla base di quelli esistenti
- evitare di perdersi componenti qua e là che abbiano stile diverso, quando l'app si ingrandisce è facile che l'AI si perda il modo in cui deve fare una determinata cosa
- vedere da subito se il design che pensa l'AI sia di tuo gradimento

Questa è la cosa credo fondamentale che ho capito dalla prova su Cantina Pulaio, che mi ha forse fatto perdere tanto tempo e tokens, perché se hai i componenti pronti è un po' come fare un puzzle, un lego, e semplifichi anche la vita agli agenti.

---

# Fase operativa

Non so bene come impostarla, ma l'idea è di avere una cartella per ogni funzionalità, con all'interno tutto quello che serve, non so ancora bene quali file includere.

## File

Possibili file:
- tasks.md sembra funzionare discretamente al momento, per quanto sia abbastanza difficile capire in anticipo quali sono i task da fare, mi è capitato di fare cose saltando qua e la e a quel punto boh quanto serva. Più che cronologicamente ed in fasi forse dividerei le cose in base alla loro categoria o sezione.
- history.md 
- onboarding.md (per chi deve capirci qualcosa sulla feature, per rivisitare)
- Tra l'altro stavo anche pensando al fatto che potrei riutilizzare, ora che l'AI ha un senso, quella fase in cui descrivevo in maniera più dettagliata le pagine che dovevano comporre un'app e le varie funzionalità che dovevano avere. Non necessariamente andando sul troppo specifico, ma potrebbe aver senso quantomeno fargli fare un grafico del flusso di navigazione tra le varie pagine e le varie funzionalità. Ed il tutto potrebbe andare a finire in un file tipo `flow.md` o qualcosa del genere.

---

## Comandi

Potrei impostare comandi come (per questa roba vedo bene i mermaid diagrams):
- /continue -> check tasks.md -> check latest features docs
- /feat -> create new feature branch -> check tech-stack.md -> check constitution.md -> 
- /review -> check constitution.md -> check tech-stack.md -> check features docs -> 
- /resume (o qualcosa di simile, per capire a che punto stavi e farti spiegare cosa è stato fatto e che altro c'è da fare come prossima cosa)

Roba di questo tipo. Non necessariamente deve essere un file, ma potrebbe far comodo per tenerli d'occhio. Ma più realisticamente almeno all'inizio sarebbero workflows interni ad Antigravity. Se poi dovesse funzionare la struttura potrei anche pensare di farci un tool da console apposito. Potrei anche farlo a prescindere insomma, vediamo.

Ah che poi i comandi sarebbero i prompts, non ricordavo di aver creato una cartella per questo.

---

## Documentazione

Forse mi servirebbe un file per spiegargli come documentare le varie feature man mano che le aggiungiamo.

Comunque ogni funzionalità diventerà una cartella con all'interno tutto quello che serve, non so ancora bene quali file includere.

- La sequenzialità sembra andare quasi sempre meglio, i singoli task funzionano meglio delle fasi intere. L'ho già scritto da qualche altra parte, ma non so se qua.
- Ricordagli di Context7 e di usare in generale le documentazioni, di non starsi a inventare cose a caso.
- Ricordagli di seguire il tech stack e il design system, di usare le variabili globali per gli stili come il `themes.ts` con tamagui.
- Tieni a mente che puoi anche definire le rules ed i workflows, globali o per il workspace, qua su antigravity.
- Delega docs a tool esterno, non sprecare potenza di calcolo e tempo mentre lavori
- Ricorda dei tests

## Gestione

- **Gestione git**: almeno l'inizializzazione di una repo per velocizzare i primi steps, poi per i singoli commit forse rimarrei anche sui manuali per ora, vediamo.
- **Gestione task/todos**: 
- **Gestione feature**:  
- **Gestione test**:  
- **Gestione documentazione**: lo terrei uno step separato, non da far gestire allo stesso agente, almeno in termini di documentazione delle singole features, il contesto deve essere il più possibile pulito e focalizzato sul task da svolgere. Una documentazione base comunque può avere senso, tipo qualche mermaid diagram o simile
- **Gestione design system**:  
- **Wiring dei file da controllare prima di eseguire una qualsiasi richiesta**:  

## Note

- [ ] Provare a scrivere flusso della libreria
- [ ] Valutare se ci sono flussi interessanti da integrare nella fase di documentazione interna: [Mermaid](https://mermaid.live/edit#pako:eNpVjTFvgzAUhP-K9aZWIhGywQYPlRrSZonUDpkKGaxgMGqwkTFKU-C_16Sq2t70TnffvRFOppTAoTqby0kJ69BhW2jk9Zhnyja9a0V_RKvVw7STDrVGy-uENnc7g3pluq7R9f13f7OUUDbul5pETjX6ff6Oshv_ouWEtvledM50x7_J4WIm9JQ3r8rP_0-UlZ56zivBK7E6CYsyYY8QQG2bErizgwyglbYVi4VxgQtwSrayAO7PUlZiOLsCCj17rBP6zZj2h7RmqBX46XPv3dCVwsltI2orfitSl9JmZtAOeELJbQP4CB_ACWZryiJCKE5JjKMkgCtwStZRmqaU4YTRNIrJHMDn7Wm4TlgcemEaMhbiGM9fgt117g)
- [ ] Fare una descrizione più sequenziale di quello che deve fare la libreria, tipo "Questa libreria serve per implementare lo spec-driven development, in modo tale che l'AI possa capire meglio cosa fare e come farlo, e l'utente riesca ad orientarsi facilmente in cosa si sta facendo, come ecc"
- [ ] Posso sia renderla una libreria da subito che usare workflows e rules per simulare la libreria. In ogni caso ci sarà un lavoro iterativo per capire come farla funzionare al meglio. Quindi forse per ora conviene impostare tutto su Antigravity.
- [ ] Potrei forse gestire prima le fasi, per solo dopo fargli creare i task delle singole fasi, per poi affrontare i task individualmente. Potrei anche indicargli più o meno le dimensioni dei task, in modo da evitare che vada troppo avanti a caso.
- [ ] Init project con i file iniziali su cui scrivere ed init della repo github
- [ ] Design style selection. With style description like "Modern, minimal, flat design: for products where minimalism and simplicity are key" or "Material, dark, modern: for products where a more traditional and refined look is desired" or "Editorial design, light" for editorial experiences. Inspired by [This article](https://tilda.education/en/web-design-styles#know)



Può diventare una semplice app CLI stile conversazione a risposta multipla degli RPG, in cui ti guida all'inizializzazione di un progetto tramite la documentazione e ti aiuta a tenere la documentazione aggiornata.

Quindi provando a ricapitolare, il flusso potrebbe essere:

First screen con logo -> 
Init, update o refactor project docs -> 
idea.md per iniziare, init git ecc. -> 
creazione seed ->
UX ->
Tech stack ->
UI ->
Components e variabili globali ->
parte operativa (todos, tasks) ->
test

Per ora questa è la struttura che mi immagino, in versione conversazione con numeretti come su Cursor a volte o come detto come negli RPG.

- Deve essere semplice e richiedere pochi tokens il cambiare stile grafico.
- Do an accessibility and contrast audit for w3c and wcag 2.1 standards.

- Bellezza
- Prestazioni
  - Ottimizzazione
- Sicurezza
- Compliance (tasse, regole varie)

- Anche la fase di ideazione è importante, quando non sei sicuro che direzione dare al progetto magari.

- Sarebbe interessante se potesse leggere tutte le ultime modifiche fatte, sia dalle chat che dai commit
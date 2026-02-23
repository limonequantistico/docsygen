# 1. Ideazione(documento per me) {[X] Done}

Questa serie di procedure non va presa come una parte necessariamente separata o sequenziale. Vogliono portare ad un prodotto, quindi possono anche funzionare in ordine sparso.
1. Brain dump testuale o vocale su oggetto Idea;
2. Un minimo di riordinamento in toggles in base al contenuto;
3. Divisione tra toggles e Note sparse, a cui verranno aggiunte le future note;
Esempio pratico: Modular Dashboard.

Il riordinamento è troppo dipendente dal tipo di idea per poter fare procedure più strutturate. Rischia di essere una perdita di tempo continua. Questa procedura mira a semplificare e rendere più efficace questa fase.
Questo documento serve a me, per orientarmi su quello che voglio che il progetto faccia.
Qua potrebbe avere senso creare una cartella sul desktop ed aprirla con l'IDE, e far generare il tutto agli agenti già lì dentro.

---

# 2. Documento SEED (documento per AI) `seed-document.md` {[X] Done}

Rappresenta il file di riferimento, dove vivono tutte le informazioni principali. Riutilizzabile per gli altri steps.
- ## Creazione [Prompt]
    ```markdown
        I have some scattered notes about a project idea. Create a SHORT summary document in markdown format (max 2-3 pages) following this structure:
        
        **# [Project Name]** *(if not provided, suggest 3)*
        
        **## Vision** *(3-4 lines)*
        What this project solves and why it exists.
        
        **## User Personas** *(2-3 essential profiles representing the main user groups)*
        For each persona: name, age, job, context, main pain point, what they're looking for, hobbies, demographics.
        
        **## Core Features** *(5-7 points max)*
        Only the fundamental features, numbered by priority.
        
        **## Non-Goals**
        What this project will NOT do or is NOT (to clarify the scope).
        
        **## High-level Concept**
        Draw an analogy with one or more existing products (e.g. YouTube = Flickr for videos)
        
        **## Existing Alternatives**
        What are the top 3 competitors? How is this problem solved today?
        
        **## Unique Value Proposition**
        A direct, simple, and clear message explaining why this project is different from what's currently available, and why it's worth paying attention to.
        
        **## Short Storybrand Brandscript**
        A brief brandscript describing the core parts of the brand according to Donald Miller's model.
        
        ---
        
        **RULES:**
        - Be concise: each section max 5-6 lines
        - Use clear language, avoid jargon where possible
        - If information is missing, put \[TBD\] instead of making things up
        - Don't repeat information
        - No need to pad the text if there's no content worth adding (if there are only 2 features, there's no need to write 7)
        - Use Context7 for any needed deeper research.
        
        **Output:** `seed-document.md`
        
        **RAW NOTES:**
        *[paste your audio/written notes here]*
    ```
    
- ## Estensione [Prompt]
    ```markdown
        I have my project seed document and new notes to integrate.

        TASK:
        1. Read the current document
        2. Integrate the new thoughts into the appropriate sections
        3. Keep the existing structure (don't add new sections randomly)
        4. If something contradicts the current document, propose the change but
        flag it with [CONFLICT] so I can decide

        AT THE END, provide a short "Changelog" summarizing:
        - What was added
        - What changed compared to before
        - Any conflicts/decisions to be made

        Use Context7 for any needed deeper research.
        ---
        CURRENT SEED DOCUMENT:

        NEW NOTES:
        [paste new ideas/notes]
    ```

---

# 3.  Procedure UX `prototypes/` {[X] Done}

- ## Wireframes/Prototipo
    - a mano
    - AI
        - Prompt [Claude, V0, Figma Make, Stitch]
            ```markdown
                Create a prototype based on the defined structure.
        
                REQUIREMENTS:
                - Focus on core user flows and information architecture
                - Include realistic placeholder content
                
                STYLE: Propose a visual style and color palette that fits the project's vision. Be creative to inspire the design direction.
                SEED DOC ATTACHED.
            ```
- ## Verifica wireframes [Prompt]
    ```markdown
        I'm attaching wireframes of the project's main screens.

        ANALYZE:
        1. Is the information hierarchy clear?
        2. Is the flow between screens logical?
        3. Are there standard UI patterns I could use? (e.g. card layout, tab navigation)
        4. Add, only if you deem it necessary, any advice you think is useful

        REFERENCE SEED DOCUMENT: 

        WIREFRAMES:
        [photos/scans of sketches]
    ```

---

# 4.  Definizione Tech Stack `tech-stack.md` {[X] Done}

- ## Prompt Stack Nuovo
    ```markdown
        You are helping me define the technical stack for a new project.
    
        [Inserisci qui tecnologie se hai già deciso qualcosa]
        I plan to use these technologies. Feel free to choose a different tool if necessary, but motivate your suggestion:
        - State management: zustand
        - Animations: framer motion
        - 
        
        **Context:**
        Read the attached `seed-document.md` to understand:
        - Project goals and scope
        - Target users and their context (mobile/desktop, tech savviness, etc.)
        - Key features and functionality requirements
        - Scale expectations (MVP vs production-ready)
        - Timeline and team size
        
        **Your task:**
        Create a `tech-stack.md` file that documents all technical decisions for this project.
        
        **Guidelines:**
        1. **Recommend appropriate technologies** based on:
        - Project requirements from seed doc
        - Modern best practices (2025-2026)
        - Developer experience and productivity
        - My stated preferences (if any)
        
        2. **Be specific:**
        - Include version numbers where relevant
        - Specify exact packages/libraries, not just categories
        - Example: "shadcn/ui + Radix UI primitives" not just "component library"
        
        3. **Justify key choices:**
        - Why this framework over alternatives?
        - Why this styling approach?
        - How does it serve the project goals?
        
        4. **Consider the full stack:**
        - Don't assume frontend-only unless seed doc specifies
        - Think about auth, database, deployment if needed
        - Consider development workflow (local dev, testing, CI/CD)
        
        5. **Keep it practical:**
        - Focus on what we need now, not every possible tool
        - Prefer established, well-documented technologies
        - Consider my skill level and learning curve
        - Highlight any significant risks or vendor lock-in with these choices
        
        6. **Include documentation links:**
        - Official docs for each major technology
        - This will be a reference during development
        
        **Output:**
        A complete `tech-stack.md` file following the structure provided. Explain your choices, don't just list options.
        
        Use Context7 for any needed deeper research.
    ```
- ## Prompt aggiornamento Stack
    ```markdown
        You are helping me document the technical stack for a new project.
    
        **Context:**
        - Read the attached `seed-document.md` and `tech-stack.md`
        - I plan to update my tech stack with these technologies: [list your preferred technologies]
        
        **Your task:**
        Update `tech-stack.md` by creating a new one that documents my chosen stack and:
        1. Fills in any missing pieces I haven't specified
        2. Suggests complementary tools (testing, deployment, etc.)
        3. Ensures all choices work well together
        4. Adds version numbers and documentation links
        5. Highlights any potential conflicts or issues
        
        Follow the standard tech-stack.md structure and be specific about packages and versions.
        
        Use Context7 for any needed deeper research.
    ```

---

# 5.  Procedure UI `design-system.md` {[ ] Done}

- ## Prompt Design System (design-system.md)
    ```markdown
        You are helping me define a design system for a new project. 
        
        **Context:**
        - Read the attached `seed-document.md` to understand the project vision, target users, and key features
        - Review the prototype screenshots in the /docs/prototypes/ folder, if present, to extract visual patterns and UX
        - Check `tech-stack.md`, if present, to understand technical constraints
        * If using Tailwind → reference Tailwind tokens and classes
        * If using shadcn/ui → base components on shadcn defaults
        * If using a specific component library → align with its design patterns
        * Match the styling approach specified in the tech stack
        
        **Your task:**
        Create a `design-system.md` file that serves as a living reference for building this app. The design system should be:
        1. **Practical** - focused on components and patterns we'll actually use
        2. **Specific** - concrete values (hex codes, px values, component variants)
        3. **Aligned** - coherent with the project vision and prototypes
        4. **Flexible** - easy to evolve as the project develops
        
        **Structure to follow:**
        1. Visual Foundation (colors, typography, spacing, shadows, borders)
           - Include suggested design tokens/CSS variables (e.g., `--color-primary`) for easy implementation
        2. Core Components (identify 5-8 key components from the seed doc and prototypes)
        3. Layout Patterns (common page structures we'll need)
        4. Interaction & Motion (basic transition/animation guidelines)
        5. Accessibility Checklist
        6. References (links to other docs and prototypes)
        7. Design Style (Glassmorphism, Neomorphism etc.)
        
        **Guidelines:**
        - Don't extract color palettes and typography from the prototypes if not necessary for your vision of the project, the design system should be based more on the user personas and the seed document's specs
        - If the tech stack uses a component library (e.g., shadcn/ui, MUI), reference it and define only customizations
        - Be opinionated but justify choices based on the project needs
        - Include practical examples for each component
        - Keep it concise - this should be scannable and actionable
        
        **Output:**
        A complete `design-system.md` file.
        
        Use Context7 for any needed deeper research.
    ```
- ## Update Prompt
    ```markdown
        Update the design-system.md based on:
        - New components we've built in [specific files]
        - Design decisions we made during implementation
        - New patterns that emerged
        Keep consistency with existing choices, document only what changed and why.
        
        Use Context7 for any needed deeper research.
    ```

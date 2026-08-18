---
name: seed
description: Create the seed document from raw notes in .docs/idea.md, or integrate new notes into an existing seed. Use only when the user explicitly asks to create or update the seed or runs /seed.
---

I have notes about a project idea. Turn them into a structured seed document that serves as the single reference point for this project — both for me and for any AI that works on it.

**Custom instructions:** If the user included extra instructions when invoking this skill, treat them as overriding or extending the guidance below.

**Read:**

- **Raw notes:** `.docs/idea.md`. If the file is empty or missing, check if the user included notes in this prompt. If neither exists, ask — don't invent. If notes are too scattered or difficult to understand, ask for clarifications - don't invent.
- **An interview in this conversation:** if a `/grill-me` or `/grill-with-docs` session ran earlier, treat what it resolved as raw notes — that's the whole point of starting a project by talking rather than writing. Combine it with `.docs/idea.md` when both exist.
- **Existing seed:** `.docs/seed.md`. If it already exists, this run is an **update** — read it first and follow "Updating an existing seed" below instead of regenerating it.

---

**Output file:** `.docs/seed.md`

**Structure:**

**# [Project Name]** _(if not provided, use the name of the folder and suggest 3 other options with brief reasoning)_

**## Vision**
What this project solves, who it's for, and why it matters. 3-4 lines max.

**## One-liner**
A single sentence someone could use to explain this project to a friend. Think "X for Y" or a plain description.

**## Target Users**
2-3 user profiles. For each, include only what's useful for making decisions:

- Who they are (role, context, age range, digital comfort level)
- Their main frustration with current solutions
- What they expect from this project

Skip demographics, hobbies, and anything that doesn't inform design or feature decisions.

**## Core Features**
The fundamental features, numbered by priority. Maximum 7, but don't pad — if there are 3, list 3.

**## Non-Goals**
What this project is NOT and will NOT do. This is as important as features for keeping scope honest.

**## Existing Alternatives**
Top 2-3 competitors or current solutions. For each: what they do well and where they fall short. This directly informs why this project should exist.

---

**Updating an existing seed:**

When `.docs/seed.md` is already there, integrate the new notes into it — don't regenerate it from scratch.

- Put each note in the section where it belongs and preserve the current structure. Don't add sections unless the new notes clearly require one.
- Don't just append. If integrating a note makes a section too long, tighten the existing text rather than growing it — unless the longer version is genuinely more useful.
- Flag contradictions with **[CONFLICT]** and briefly explain both sides so I can decide. Flag anything the new notes make obsolete or wrong with **[CHANGED]**, saying what was there before.
- If the new notes suggest a significant pivot (different target users, different core problem), say so explicitly **before** making changes. A pivot is a conversation, not a silent edit.

Then report back: what was added and where, what changed compared to before, any [CONFLICT] or [CHANGED] items that need my decision, and any [TBD] items the new information can now fill.

This is for integrating new _ideas_. If instead the _code_ has diverged from the seed, use `/drift` to reconcile docs with reality.

---

**RULES:**

- Be concise: each section max 5-6 lines
- Skip sections that don't apply (small projects don't need all of them)
- Use clear language, avoid jargon
- If information is missing, put [TBD] — never make things up
- Don't pad. 2 features means 2 features, not 7.
- This document will be read by AI agents as context before every task. Write it so that an LLM reading it understands the project's direction, scope, and constraints without needing anything else. Other commands refer to this whole document as **project context** (not a single heading).
- If the raw notes are too vague to produce a useful seed (less than ~3 concrete ideas), don't force it. Instead, list what you understood and ask targeted questions to fill the gaps.

**Logging:** On success, append to `.docs/changelog.md` per `.docs/changelog-spec.md`: `- YYYY-MM-DD HH:mm ran /seed — [brief description of what was produced, added, or changed]`.

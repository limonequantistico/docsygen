I have some scattered notes about a project idea. Transform them into a structured seed document that serves as the single reference point for this project — both for me and for any AI that works on it.

**Custom instructions from user:** $ARGUMENTS

**Read raw notes from:** `.docs/idea.md`
If the file is empty or missing, check if the user included notes in this prompt. If neither exists, ask — don't invent.

---

**Output file:** `.docs/seed-document.md`

**Structure:**

**# [Project Name]** _(if not provided, use the name of the folder and suggest 3 other options with brief reasoning)_

**## Vision**
What this project solves, who it's for, and why it matters. 3-4 lines max.

**## One-liner**
A single sentence someone could use to explain this project to a friend. Think "X for Y" or a plain description.

**## Target Users**
2-3 user profiles. For each, include only what's useful for making decisions:
- Who they are (role, context)
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

**RULES:**

- Be concise: each section max 5-6 lines
- Skip sections that don't apply (small projects don't need all of them)
- Use clear language, avoid jargon
- If information is missing, put [TBD] — never make things up
- Don't pad. 2 features means 2 features, not 7.
- This document will be read by AI agents as context before every task. Write it so that an LLM reading it understands the project's direction, scope, and constraints without needing anything else.
- If the raw notes are too vague to produce a useful seed (less than ~3 concrete ideas), don't force it. Instead, list what you understood and ask targeted questions to fill the gaps.

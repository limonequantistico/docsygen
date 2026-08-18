---
name: design-system
description: Define the project's design system (visual tokens and decisions) in .docs/design-system.md through a guided interview — proposing options and letting the user choose before anything is written. Use only when the user explicitly asks to define the design system or runs /design-system.
---

You are helping define the design system for this project: the aesthetic direction and the visual tokens that follow from it.

**This is a conversation, not a generation task.** A design system invented in one shot is a guess dressed as a decision — it looks finished, so it never gets challenged, and every screen built on it inherits the guess. Your job is to surface the real choices, propose options with trade-offs, and let the user pick. **Write nothing to disk until the decisions are made.**

**Custom instructions:** If the user included extra instructions when invoking this skill, treat them as overriding or extending the guidance below.

**Read first (silently):**

- `.docs/seed.md` — vision, target users, key features. The users decide most of this: a tool for professionals under time pressure wants different defaults than a consumer app competing on delight.
- `.docs/assets/imgs/prototypes/` — if wireframes exist, extract UX patterns and structure (ignore their visual style, they're structural references only)
- `.docs/assets/imgs/references/` — reference screenshots from other apps, if the user has collected any. These are the strongest signal available: a handful of screens someone liked says more about the direction than any amount of describing it. If the folder is empty, run **Step 0** below before interviewing. Treat references as inspiration to react to, never as templates to copy.
- `.docs/tech-stack.md` — a component library already in the stack constrains what's realistic

---

## Step 0 — Get references, if there are none

Skip this entirely when `.docs/assets/imgs/references/` already has screenshots, or when the seed makes the direction obvious.

Otherwise: don't start the interview blind. Asking someone to choose an aesthetic from written descriptions is asking them to imagine four things they've never seen. Two or three screens they actually like collapses that into a decision, and it makes every later question sharper.

**Do the curation work yourself — don't just name galleries.** From the seed's product type and users, produce a short, specific shortlist:

- **Named products worth studying**, and *why each one* — apps solving a similar problem, or with a similar interaction shape, for a similar audience. This is the part the user can't easily search for, and the part worth spending effort on. Three or four, each with a one-line reason.
- **The right gallery for this product type**, not a generic list — [Mobbin](https://mobbin.com/) for real mobile and web app flows, [Dribbble](https://dribbble.com/) for visual direction (aspirational, often impractical), [21st.dev](https://21st.dev/community/components) for component-level patterns, [Land-book](https://land-book.com/) for marketing and landing pages, and the platform's own guidance (Apple HIG, Material) when convention matters more than distinctiveness.
- **What to look for**, given this project — density and information hierarchy for a data-heavy tool, warmth and motion for a consumer app, restraint and legibility for something used daily under pressure.

Then ask the user to drop a few screenshots into `.docs/assets/imgs/references/` and say when they're ready. If they'd rather skip it, proceed with the interview — just note the direction is being chosen from description alone.

---

## Step 1 — Ask, one decision at a time

Work through the decisions below in order, because each one narrows the next. **Ask one question per turn** and wait for the answer — don't dump the whole questionnaire at once.

For every question:

- Offer **3-4 concrete named options**, not open prompts. "What kind of typography do you want?" is a bad question. "Geometric sans (Inter, Manrope) — neutral and modern; Humanist sans (Source Sans, Lato) — warmer, better at long text; Serif display + sans body — editorial, more distinctive; Monospace accents — technical, developer-facing" is a good one.
- Give each option a **one-line consequence**: what it makes easy, what it costs, who it suits.
- **Recommend one** and say why, grounded in the seed's users — never a neutral menu.
- Let the user pick an option, combine them, or reject them all and give you their own direction.

If a structured multiple-choice question tool is available, use it. Otherwise present the options as a short numbered list and ask the user to reply with a number.

**The decisions, in order:**

1. **Aesthetic direction** — the one that governs everything else. Offer named directions with real character (e.g. "Modern minimal", "Editorial", "Warm and tactile", "Dense and utilitarian"), each tied to how the seed's users would react to it.
2. **Color strategy** — before specific hex values: is this monochrome with one accent, a two-color brand pairing, or a fuller palette? Light-first, dark-first, or both from the start? Ask about existing brand colors before inventing any.
3. **Typography** — pairing strategy first, then scale. One family or two? How much size contrast between heading and body?
4. **Density and shape** — how much breathing room, and how round. These two carry most of a UI's personality and are cheap to decide early: tight vs. generous spacing, sharp vs. soft vs. pill radii.
5. **Depth and motion** — flat, bordered, or shadowed? Motion as functional-only or expressive? Keep this small; unused tokens are noise.

Skip a question when the seed or the references already answer it — say what you inferred and confirm in one line rather than asking from scratch. Don't stretch this past five or six exchanges; if the user says "you decide", make the call, state it, and move on.

## Step 2 — Show the direction before committing

Once the decisions are made, present a compact summary: the direction in a sentence, the palette with hex values, the type pairing and scale, spacing base, radii, and elevation. Concrete values, so the user is approving a real thing rather than adjectives.

Ask for confirmation, and expect changes — one or two rounds of "make the accent warmer, tighten the spacing" is normal and cheap here. It's expensive after fifty components exist.

## Step 3 — Write the file

Only after confirmation, write `.docs/design-system.md` — a tech-agnostic reference a designer could read fluently. No code, no framework specifics.

1. **Design Style**
   - The aesthetic direction, named
   - Why it fits these users and this project — carry over the reasoning from the interview, so the *why* survives
2. **Visual Foundation**
   - **Colors**: primary, secondary, accent, neutrals, semantic (success, error, warning). Hex codes.
   - **Typography**: font families, size scale, weights, line heights
   - **Spacing**: base unit and scale (e.g. 4px grid: 4, 8, 12, 16, 24, 32, 48)
   - **Shadows, borders, radii**: defined values per elevation level
3. **Interaction & Motion**
   - Transition durations and easing for common interactions
   - Keep it minimal — only what will actually be used
4. **Accessibility Checklist**
   - Contrast ratios, focus states, keyboard navigation, screen reader considerations, based on WCAG 2.1
   - Verify the chosen palette actually clears contrast targets. If a brand color fails against its intended background, say so now and propose a corrected pair — this is the cheapest moment to catch it.

**If `.docs/design-system.md` already exists**, this is a revision, not a rewrite. Read it, ask what should change, and confirm before overwriting — components already depend on these values.

**RULES:**

- Nothing gets written before the user has chosen. A file that appears unasked-for is a decision made on their behalf.
- Be opinionated. A recommendation with a reason is useful; a neutral list of options is work handed back to the user.
- Be specific: hex codes, px values, font names — not vague descriptions.
- Don't over-build. Only the tokens the project will actually use; every unused scale step is future confusion.
- Keep the file concise and scannable. It's a working reference, not a design essay.
- No code, no framework references, no implementation details. That's `/setup`'s job.

**After completing, ask the user** if they're happy with the result. Suggest `/scaffold` as the next step to validate or create the project structure, followed by `/setup` to translate these tokens into code.

**Logging:** On success, append to `.docs/changelog.md` per `.docs/changelog-spec.md`: `- YYYY-MM-DD HH:mm ran /design-system — [brief description of the design direction chosen]`.

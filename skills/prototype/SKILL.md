---
name: prototype
description: Generate a paste-ready prompt for external design tools (Claude Design, Stitch, Figma AI, V0) to create screens and prototypes. Use only when the user explicitly asks to prototype or runs /prototype.
---

Generate a detailed prompt that the user can paste into an external design tool — [Claude Design](https://claude.ai/design), Google Stitch, Figma AI, V0, or similar — to create screens and prototypes.

**Custom instructions:** If the user included extra instructions when invoking this skill, treat them as overriding or extending the guidance below.

**Read:**

- `.docs/seed.md` — the project context the screens have to serve
- `.docs/design-system.md` — if it exists, the direction is already settled and the prompt should carry it (see below)
- `.docs/assets/imgs/references/` — reference screenshots, if the user has collected any
- `.docs/prototype-notes.md` — feedback from a previous prototype round, if it exists

**Your task:**

Design tools generate **one screen at a time** — paste a whole-app brief into Stitch or V0 and you get one screen plus a lot of ignored context. So the output is not one prompt: it's a **shared context block plus a self-contained prompt per screen**, each ready to paste on its own.

### Pick the screens first

Derive the screen list from the seed, show it to the user numbered by priority, and ask **which screens to write prompts for**. Default to the core flow — usually three or four screens — rather than every screen the app will eventually have. Writing twelve prompts nobody pastes is waste, and the later ones are better written once you've seen how the first came out.

### Then write each prompt

Every per-screen prompt must stand alone, because it gets pasted into a fresh session with no memory of the others. Each one repeats the shared context, then adds only that screen's specifics:

**Shared context** (identical in every prompt, kept tight — this is overhead paid once per paste):

1. **App type and platform** — Web app, mobile app, desktop, or responsive. Infer from the **project context** (the seed document as a whole: vision, users, features, constraints — not a single section by that name) or ask if unclear.
2. **App overview** — One paragraph: what it does, who it's for, and the core problem it solves.
3. **UX constraints** — Requirements from the seed that affect layout: accessibility needs, mobile-first, offline support, specific interaction patterns (drag-and-drop, real-time updates, etc.).
4. **Visual direction** — **only if `.docs/design-system.md` exists.** Today's design tools generate styled screens, not grey-box wireframes, so they will invent an aesthetic whether or not you give them one. Give them yours: the named direction, the palette with hex codes, the type pairing, spacing base, and radii. Keep it to a compact block — you're constraining the tool, not pasting the whole document.

**Per-screen specifics** (the part that changes):

5. **This screen's purpose** — one line: what the user came here to do.
6. **Where it sits in the flow** — one line naming the screens immediately before and after, so the tool gets navigation and entry/exit right without needing the full screen list.
7. **Key elements, realistic placeholder content, and available actions** — real-looking copy, not `Lorem ipsum` or `[Title]`. Placeholder text that reads like the actual product is the single biggest quality difference in generated screens.
8. **States** — empty, loading, and error, where they matter for this screen. Most tools skip these unless asked.

**RULES:**

- Structure and flow are the priority. Visual direction is a constraint you pass through, not something to invent here — if `.docs/design-system.md` doesn't exist yet, say so and suggest `/design-system` first, since the tool's output is far more usable when it isn't guessing the aesthetic.
- Keep it practical — only screens the MVP needs. If the seed lists 7 features, the prototype doesn't need all 7 — focus on the core flow.
- Use clear, well-structured formatting. The user will paste this into a design tool and may need to adapt it slightly for the specific tool.
- If the seed is too vague to define screens confidently (e.g., core features are [TBD], no clear primary user), say what's missing and suggest running `/seed` or `/seed-review` first.
- If the user specifies which design tool they're using, adapt the prompt style to work best with that tool. [Claude Design](https://claude.ai/design) runs its own guided questionnaire and visual taste-tests before generating, so give it the structure and constraints and let it drive the visual exploration; prompt-only tools need the visual direction spelled out in the prompt itself.

**Output file:** Write everything to `.docs/prototype-prompt.md` (overwrite each run): a short header naming the shared context, then one `##` section per chosen screen, each containing its complete self-contained prompt **in its own fenced code block** so it can be copied in one click. Don't make the user assemble anything.

**Deprioritize onboarding and generic login screens** unless the seed marks auth or onboarding as core MVP (e.g. B2B SSO, compliance, paid signup). If auth is core, treat those as screens like any other.

**After generating the prompt, remind the user:**

- Paste one screen, look at what comes back, then adjust the next prompt before pasting it. These tools rarely nail the first attempt, and the second prompt is much better written with the first result in front of you. Re-run `/prototype` any time to regenerate for more screens.
- Once you have screens you like, drop them in `.docs/assets/imgs/prototypes/` — they inform `/stack` and `/setup`, and are worth re-reading when revising `/design-system`.
- Screens from these tools are **references, not specifications**. They're worth keeping for their structure and flow; don't treat their visual choices as decisions — `.docs/design-system.md` is where those live.

**Logging:** On success, append to `.docs/changelog.md` per `.docs/changelog-spec.md`: `- YYYY-MM-DD HH:mm ran /prototype — [brief description of what was generated]`.

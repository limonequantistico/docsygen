---
name: prototype
description: Generate a paste-ready prompt for external design tools (Stitch, Figma AI, V0) to create wireframes. Use only when the user explicitly asks to prototype or runs /prototype.
---

Generate a detailed prompt that the user can paste into an external design tool (Google Stitch, Figma AI, V0, or similar) to create wireframes/prototypes.

**Custom instructions:** If the user included extra instructions when invoking this skill, treat them as overriding or extending the guidance below.

**Read:** `.docs/seed.md`
Also check if `.docs/prototype-notes.md` exists with feedback from a previous prototype round.

**Your task:**
Create a ready-to-paste prompt that includes:

1. **App type and platform** — Web app, mobile app, desktop, or responsive. Infer from the **project context** (the seed document as a whole: vision, users, features, constraints — not a single section by that name) or ask if unclear.
2. **App overview** — One paragraph: what it does, who it's for, and the core problem it solves.
3. **Screen list** — Every screen the MVP needs, with a one-line description of its purpose. Don't include screens for features marked as non-goals.
4. **Core user flows** — The main paths the user walks. **Deprioritize onboarding and generic login screens** unless the seed marks **auth or onboarding as core MVP** (e.g. B2B SSO, compliance, paid signup). If auth is core, include those flows explicitly. Number by priority — most important first.
5. **Per-screen details** — For each screen: key elements, realistic placeholder content, and available actions.
6. **UX constraints** — Requirements from the seed that affect layout: accessibility needs, mobile-first, offline support, specific interaction patterns (drag-and-drop, real-time updates, etc.).

**RULES:**

- Focus purely on UX and structure, not visual style — that comes later in `/design`
- Keep it practical — only screens the MVP needs. If the seed lists 7 features, the prototype doesn't need all 7 — focus on the core flow.
- Use clear, well-structured formatting. The user will paste this into a design tool and may need to adapt it slightly for the specific tool.
- If the seed is too vague to define screens confidently (e.g., core features are [TBD], no clear primary user), say what's missing and suggest running `/seed-update` or `/seed-review` first.
- If the user specifies which design tool they're using, adapt the prompt style to work best with that tool.

**Output file:** Write the complete ready-to-paste prompt to `.docs/prototype-prompt.md` (overwrite the file each run).

**After generating the prompt, remind the user:**

- For UI inspiration, browse [Mobbin](https://mobbin.com/discover/apps/ios/latest), [Dribbble](https://dribbble.com/), or [21st.dev](https://21st.dev/community/components) for reference designs for similar interfaces to insert in `.docs/assets/imgs/references`. Remember that UI is great at reproducing UI elements (at least single components), not that great at creating them from scratch.
- Once you have the wireframes, drop them in `.docs/assets/imgs/prototypes/` — they inform `/stack`, `/design`, and `/setup`.

**Logging:** On success, append to `.docs/changelog.md` per `.docs/changelog-spec.md`: `- YYYY-MM-DD HH:mm ran /prototype — [brief description of what was generated]`.

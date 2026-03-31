Generate a detailed prompt that the user can paste into an external design tool (Google Stitch, Figma AI, V0, or similar) to create wireframes/prototypes.

**Custom instructions from user:** $ARGUMENTS

**Read:** `.docs/seed.md`
Also check if `.docs/prototype-notes.md` exists with feedback from a previous prototype round.

**Your task:**
Create a ready-to-paste prompt that includes:

1. **App type and platform** — Web app, mobile app, desktop, or responsive. Extract this from the seed's Project Context or ask if unclear.
2. **App overview** — One paragraph: what it does, who it's for, and the core problem it solves.
3. **Screen list** — Every screen the MVP needs, with a one-line description of its purpose. Don't include screens for features marked as non-goals.
4. **Core user flows** — The main paths the user is going to walk, omit onboarding and auth in this phase since they are obvious and always similar. Number them by priority — the most important flow first.
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
- For UI inspiration, check tools like **Mobbin**, **Dribbble**, and **Behance** to find reference designs for similar interfaces to insert in `.docs/assets/imgs/references`.
- Once you have the wireframes, drop them in `.docs/assets/imgs/prototypes/` and you can use `/prototype-verify` to analyze them.

**Logging:** When this command completes successfully, append a dated entry to `.docs/changelog.md`: `- YYYY-MM-DD HH:mm ran /prototype — [brief description of what was generated]`. Create the file if it doesn't exist.
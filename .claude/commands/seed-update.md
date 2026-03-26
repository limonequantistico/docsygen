I have new thoughts to integrate into my seed document.

**Custom instructions from user:** $ARGUMENTS

**Read:**
- Current seed: `.docs/seed-document.md`
- New notes: check `.docs/idea.md` for new additions, or the rest of this prompt. If neither has content, ask — don't guess.

**Your task:**

1. Read the current seed document carefully
2. Integrate the new notes into the appropriate existing sections
3. Preserve the current structure — don't add new sections unless the new notes clearly require one
4. If something contradicts the current document, flag it with **[CONFLICT]** and briefly explain both sides so I can decide

**At the end, provide a Changelog:**
- What was added (and where)
- What changed compared to before
- Any [CONFLICT] items that need my decision
- Any [TBD] items that could now be filled based on the new information
- If new notes make an existing section obsolete or wrong, flag it with **[CHANGED]** and tell me what was there before

**RULES:**
- The seed document's purpose is to be the single reference for both humans and AI agents. Keep it concise and decision-useful.
- Don't bloat sections — if integrating a note makes a section too long, tighten the existing text rather than just appending. Unless a longer text is actually more useful.
- If the new notes suggest a significant pivot (different target users, different core problem), say so explicitly before making changes. A pivot is a conversation, not a silent edit.

**Note:** This command is for integrating your new ideas. If instead the *code* has diverged from the seed, use `/sync` to reconcile docs with reality.

**Logging:** When this command completes successfully, append a dated entry to `.docs/archive/archive.md`: `- YYYY-MM-DD ran /seed-update — [brief description of what was added or changed]`. Create the file if it doesn't exist.

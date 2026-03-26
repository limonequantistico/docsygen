You are reviewing a seed document to stress-test it before the user invests time in prototypes and tech decisions.

**Custom instructions from user:** $ARGUMENTS

**Read:** `.docs/seed-document.md`

**Your task:**
Analyze the seed document critically. Go through each point:

1. **Scope check** — Given the Project Context (team size, timeline, stage), is this realistic? If time was halved, what would you cut first? If Project Context is missing or marked [TBD], flag this — you can't assess scope without it.

2. **Riskiest assumption** — What's the one thing that, if wrong, makes the whole project collapse? Every project has one. Name it clearly.

3. **Missing pieces** — Are there obvious gaps that will block the next steps? (e.g., needs auth but doesn't mention it, targets mobile but no offline strategy, no clear primary user)

4. **Audience clarity** — Are the target users specific enough to make real design and feature decisions? "Tech-savvy professionals" describes half the internet — that's not useful.

5. **Differentiation** — If alternatives are listed, is the difference actually clear and meaningful? If no alternatives exist (personal tool, internal project, niche use case), skip this and say so.

6. **[TBD] audit** — List any [TBD] items and flag which ones are blockers for the next phases (prototype, stack, design) vs. which can wait.

**RULES:**
- Be direct and honest, not encouraging. The point is to find weaknesses before they become expensive.
- Each point should be 2-3 lines max. This is a quick stress-test, not a report.
- End with a clear recommendation:
  - **Proceed** → seed is solid enough, suggest `/prototype` as the next step
  - **Revise** → specific sections need work first (list them), suggest `/seed-update`
  - **Rethink** → fundamentals are shaky, suggest going back to `/seed` with better input

Always ask the user if they agree with the recommendation before suggesting the next command. Never chain commands automatically.

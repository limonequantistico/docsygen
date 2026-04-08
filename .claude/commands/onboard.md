You are producing or refreshing **onboarding documentation** so another developer can work on this repository without tribal knowledge.

**Custom instructions from user:** $ARGUMENTS

**Read:**

- `.docs/seed.md` — what the product is (short orientation)
- `.docs/tech-stack.md` — tools, versions, key commands
- `README.md` — what exists today
- Repo: `package.json` scripts, `Makefile`, Docker files, CI workflow, `.nvmrc` / toolchain files

**Your task:**

Update or create concise onboarding content. Prefer improving **README.md** sections unless the user asks for `CONTRIBUTING.md` or `.docs/onboarding.md`.

Cover only what applies:

1. **Prerequisites** — Runtime versions, package manager, optional CLI tools.
2. **First run** — Clone, install, env file from example, database/setup migrations if any, command to start dev.
3. **Project map** — Where features, UI, API, tests, and docs live (high level).
4. **Conventions** — Branching, commits, lint/test before PR, how design tokens and the design system doc relate to code.
5. **Common tasks** — Run tests, typecheck, build, storybook/showcase if present.
6. **Where to ask** — Point to backlog, seed, or team channel if mentioned in docs.

**RULES:**

- Do not invent scripts that do not exist; read `package.json` / CI / Makefile first.
- Keep README accurate: replace placeholder “Project Name” / generic text only if you have seed content to substitute.
- After edits, the README should answer “how do I run this?” in under two minutes of reading.

**Logging:** On success, append to `.docs/changelog.md` per `.docs/changelog-spec.md`: `- YYYY-MM-DD HH:mm ran /onboard — [brief summary]`.

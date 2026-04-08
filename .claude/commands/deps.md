You are updating **dependencies** to current **latest stable** releases in line with this project’s tech choices.

**Custom instructions from user:** $ARGUMENTS

**Read:**

- `.docs/tech-stack.md` — canonical packages and tools; do not add unrelated ecosystems
- Lockfiles and manifest(s): `package.json`, `pnpm-lock.yaml`, `package-lock.json`, `yarn.lock`, `Cargo.toml`, `pyproject.toml`, `go.mod`, etc.

**Your task:**

1. **Scope** — Decide which manifests to update based on the stack (e.g. root app only, or monorepo packages). If unclear, ask once.

2. **Resolve versions** — For each direct dependency, determine the **latest stable** version (not nightly, not deprecated). Use Context7 MCP or official registries/docs when versions are uncertain.

3. **Plan** — Present a concise table or list: package → current → target → note if major/breaking. Flag high-risk upgrades (major semver, known migrations).

4. **Apply** — After the user approves, run the appropriate package-manager update commands (`pnpm up`, `npm update`, `cargo update`, etc.) and fix straightforward breakage.

5. **Docs** — Update `.docs/tech-stack.md` so listed versions and packages match reality.

**RULES:**

- Do not add packages that are not justified by the seed or stack without explicit user approval.
- If a major upgrade needs a migration guide, summarize steps and link or cite official migration notes — do not guess API changes.
- Ask before running install/update commands if project rules require it.

**Logging:** On success, append to `.docs/changelog.md` per `.docs/changelog-spec.md`: `- YYYY-MM-DD HH:mm ran /deps — [brief summary]`.

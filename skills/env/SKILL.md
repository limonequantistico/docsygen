---
name: env
description: Audit environment variables, secrets hygiene, and production readiness. Use only when the user explicitly asks for an env or secrets review or runs /env.
---

You are auditing **environment configuration**: variables, secrets, and production readiness — the layer where mistakes cause outages or leaks.

**Custom instructions:** If the user included extra instructions when invoking this skill, treat them as overriding or extending the guidance below.

**Read (as applicable):**

- `.docs/seed.md` — deployment assumptions (SaaS, self-hosted, mobile, etc.)
- `.docs/tech-stack.md` — hosting, frameworks, and declared services
- Repo: `.env.example`, `.env.local.example`, `docker-compose`, deployment configs, CI secrets references, config loaders

**Your task:**

1. **Inventory** — List required env vars by area (app, database, auth, third-party APIs). Mark which are **secret** vs **non-secret config**.

2. **Documentation** — Check whether every required variable is documented in a safe template (e.g. `.env.example` with placeholder values, no real secrets). Flag missing or stale entries.

3. **Secrets hygiene** — Scan for common mistakes: keys in repo, logged secrets, client-exposed server keys, default passwords in production paths. **Do not repeat real secret values** in your output — redact.

4. **Environments** — Clarify dev vs staging vs prod expectations: which vars differ, what should never be enabled in prod (debug flags, mock auth).

5. **Production checklist** — Short actionable list: rotation, least-privilege API keys, CORS/origin config if relevant, HTTPS-only cookies if relevant — only what applies to this stack.

**RULES:**

- If you find a likely secret in the codebase, tell the user to **rotate** it and remove it from history if committed; do not paste the value.
- If the project has no env story yet, propose a minimal convention consistent with the stack.

**Logging:** On success, append to `.docs/changelog.md` per `.docs/changelog-spec.md`: `- YYYY-MM-DD HH:mm ran /env — [brief summary]`.

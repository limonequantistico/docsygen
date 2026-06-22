---
name: performance
description: Review performance and observability — bottlenecks, logging, metrics. Use only when the user explicitly asks for a performance or observability review or runs /performance.
---

You are reviewing **performance and observability**: how the app behaves under load, how failures surface, and whether operators can debug production issues.

**Custom instructions:** If the user included extra instructions when invoking this skill, treat them as overriding or extending the guidance below.

**Read (as applicable):**

- `.docs/seed.md` — latency-sensitive flows, scale expectations, SLAs if any
- `.docs/tech-stack.md` — framework, hosting, suggested monitoring tools
- Code: hot paths (DB queries, N+1 patterns, large payloads), caching, background jobs, API routes, client bundles
- Existing logging, metrics, tracing, error reporting (Sentry, OpenTelemetry, APM, etc.)

**Your task:**

1. **Performance** — Identify likely bottlenecks in the **current** implementation (not hypothetical). Prefer concrete references (file + pattern): missing indexes, unbounded queries, sync work on request thread, heavy client JS, missing pagination, etc.

2. **Baselines** — Suggest what to measure (p95 latency, error rate, job queue depth) and where — only what fits this stack.

3. **Logging** — Are errors and key events logged with enough context (request id, user id if appropriate) without logging secrets? Is log level usage sensible?

4. **Tracing & metrics** — Gaps: no structured errors, no health check, no uptime probe, no dashboards. Recommend minimal additions aligned with the tech stack.

5. **Prioritized actions** — Short list: highest impact first, each item actionable in one sitting.

**RULES:**

- Do not recommend a new vendor or library unless the user asks or the stack already allows it; otherwise flag once for user decision.
- Focus on shipped code paths, not future features.

**Logging:** On success, append to `.docs/changelog.md` per `.docs/changelog-spec.md`: `- YYYY-MM-DD HH:mm ran /performance — [brief summary]`.

---
name: logs
description: Establish or audit application logging — what gets recorded, at what level, with what context — shaped to the project's architecture and existing stack. Use only when the user explicitly asks about logging or runs /logs.
---

You are establishing or auditing **application logging** — what the running system records about itself so a problem can be diagnosed after the fact.

Most logging is bad in a specific way: too much of what the code is *doing* (which you already know, you wrote it) and too little of what actually *happened* to a given piece of work. The goal here is fewer, richer, queryable records — not more lines.

**Custom instructions:** If the user included extra instructions when invoking this skill, treat them as overriding or extending the guidance below.

**Read:**

- `.docs/tech-stack.md` — what's already available; **stay inside it** unless the user approves an addition
- `.docs/logging.md` — if it exists, this project already has a logging contract; audit against it rather than inventing a new one
- `.docs/seed.md` — what the product does, so "important operation" means something concrete
- The code: entry points, error handling, existing log calls, and any env/config that sets log levels or destinations

---

## Step 1 — Establish the shape of the project

Logging means different things in different architectures. Work out which of these applies before proposing anything — a checklist written for HTTP services is worse than useless on a mobile app.

- **Request/response service** (API, web backend) — the unit of work is a request. One rich record per request per service.
- **Jobs, workers, pipelines** — the unit is a job or stage. A single end-of-run record may never fire, so emit at each meaningful stage boundary, each carrying the context accumulated so far.
- **Mobile app** — there's no request to anchor to. What matters is crash and non-fatal error reporting, a breadcrumb trail leading up to a failure, lifecycle and network outcomes, and offline buffering. Volume and battery are real constraints; PII rules are stricter.
- **Frontend web** — unhandled errors and rejections, failed network calls, and a breadcrumb trail. `console.log` is not logging. Beware volume and beware shipping user data to a third party.
- **CLI / desktop** — logs are local and the user is the one who reads them. What matters is a verbosity flag, a predictable log file location, and an easy way for a user to hand you the log when reporting a bug.
- **Library** — usually shouldn't log at all. Surface errors to the caller; at most, expose a hook the host application can wire to its own logger.

If the project is more than one of these (an app plus its backend), say so and treat them separately — they'll need different answers.

## Step 2 — Establish the current state, then pick the mode

**No logging standard yet** — propose one. Assess what's already in `.docs/tech-stack.md` and in the code:

- If a destination already exists (an error reporter, a hosted log service, the platform's own facility, plain files), build on it. Don't propose a second one.
- If nothing exists, present **two or three realistic options with a recommendation**, sized to the project. A solo project often needs nothing more than structured local logs plus a crash reporter; proposing a full observability pipeline for it is a mistake.
- Adding a dependency or a vendor is a **question, not a step**. Ask before touching the stack.

**Logging already exists** — audit it against Step 3 and report gaps. Don't rewrite every call site: name the paths where better logging would actually have saved you (auth, payments, external API calls, background jobs, anything that has already burned you), and fix those first.

Either way, the output is a proposal the user approves before you change code.

## Step 3 — The standard to design or audit against

**Record outcomes, not narration.** Six lines saying "entering payment processing", "validating card", "calling Stripe" tell you nothing in production. One record per unit of work, carrying everything, tells you everything. Step-by-step tracing is legitimate at DEBUG level, off by default — just don't make it the baseline.

**Structure over prose.** Key-value fields, not interpolated sentences. `{"event": "payment.failed", "error_type": "card_declined", "amount_cents": 4999}` can be filtered and grouped; `"Payment failed for user abc123 - card_declined ($49.99)"` can only be grepped, badly.

**Accumulate, then emit once.** Build the record up as the work proceeds and emit at the end. Make sure a crash still flushes what was collected — a `finally` block or a global handler — or the failures you most need to see are exactly the ones you lose.

**Carry business context, not just technical context.** Status codes and durations are necessary and insufficient. Add the *who* (user or account id, tier, org), *what* (order, transaction, feature flag variant), *where* (service, version, environment), and *how much* (amount, count, retries). This is the difference between "errors spiked" and "errors spiked for trial users on the new checkout path".

**Use levels honestly.** ERROR means someone must act — if nobody ever acts on it, it isn't an error, it's noise that trains you to ignore the channel. WARN is unexpected but survived. INFO is a normal milestone worth recording. DEBUG is off in production.

**Scalars only.** Strings, numbers, booleans. Never attach a whole object, a query result, or an API response — that's how you blow up cost and leak data at the same time.

**Never log:** secrets and tokens; full request or response bodies; PII beyond what debugging genuinely needs (hash or tokenize identifiers where regulation demands it); high-frequency health checks and liveness probes. `/env` owns the secrets-hygiene scan — flag anything you spot and defer the sweep to it.

**Treat field names as a contract.** Once anything queries `duration_ms`, renaming it or changing its type breaks dashboards and alerts silently. Changes get communicated and deprecated, like any other API.

**Control volume deliberately.** At low traffic, log everything. As traffic grows, sample — keeping 100% of errors, slow outliers, and flagged accounts — rather than lowering the level and losing the signal entirely.

**Logs are not analytics events.** Logs are what the *system* did (a timeout, a retry, a failed charge). Events are what the *user* did (signed up, clicked, purchased). If product-analytics events are being used to track system failures, or log lines to track user behaviour, say so — they belong in different places.

## Step 4 — Write it down

A logging standard nobody can look up decays within weeks. Record the agreed contract in **`.docs/logging.md`**: the destination and library, the fields every record carries, the level convention, what must never be logged, and how to add a new field. Create the file if it's missing; update it if this pass changed the contract. Keep it to a page.

## Step 5 — Report

- **Project shape and current state** — two or three lines.
- **The proposed or audited contract** — the fields every record carries, with an example record from *this* project's domain, not a generic checkout.
- **Gaps, ordered by what would actually cost you at 2am** — a payment path with no error context outranks an inconsistent level somewhere quiet.
- **Concrete changes**, applied only on approval.

**RULES:**

- Don't introduce a logging library, vendor, or SDK that isn't in `.docs/tech-stack.md` without asking. Present options and let the user choose — the point is a standard that fits this project, not a favourite tool.
- Don't propose an observability stack a solo project will never operate. Match the ambition to the blast radius.
- Don't rewrite every log call in one pass. Fix the paths that matter, establish the pattern, leave the rest.
- Be specific. "Add more context to errors" is not actionable; "the checkout handler logs `e.message` only — add order id, amount, provider, and retry count" is.
- If the project genuinely needs almost no logging (a static site, a small library), say so and stop. Not every project needs this.

**Logging:** On success, append to `.docs/changelog.md` per `.docs/changelog-spec.md`: `- YYYY-MM-DD HH:mm ran /logs — [brief summary of what was proposed, audited, or changed]`.

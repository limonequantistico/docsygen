---
name: test
description: Define or improve automated testing strategy and critical-path coverage. Use only when the user explicitly asks about testing strategy or runs /test.
---

You are defining or improving **automated testing** for this project — strategy, critical-path coverage, and practical guardrails against flaky tests.

**Custom instructions:** If the user included extra instructions when invoking this skill, treat them as overriding or extending the guidance below.

**Read (as applicable):**

- `.docs/seed.md` — what must not break for the product to be viable
- `.docs/tech-stack.md` — test runners, frameworks, and conventions already chosen
- Existing test directories, config (`vitest`, `jest`, `pytest`, `cargo test`, etc.), and CI workflow files if present

**Your task:**

1. **Strategy** — Given the stack and scope, name the test layers that matter (unit, integration, e2e). Say what to test at each layer and what to avoid duplicating across layers.

2. **Critical path** — List the smallest set of tests that would catch regressions in the core user journeys or APIs described in the seed. Order by risk, not by file layout.

3. **Conventions** — Match this repo: file naming, where tests live, how mocks/fixtures are organized, and how the project runs tests locally and in CI.

4. **Flakiness & speed** — Call out patterns that cause flaky tests (real timers, shared global state, unordered async, network without hermetic stubs) and how this codebase should avoid them. Note anything that should be marked slow or run only in CI.

5. **Gaps** — If important areas have no tests, list them with suggested first tests (describe file + behavior), not vague advice.

**RULES:**

- Do not introduce a new test framework unless the user explicitly allows it and it fits the tech stack doc.
- Prefer extending existing test utilities over new parallel helpers.
- If there is no test setup yet, propose a minimal first step consistent with `.docs/tech-stack.md` and ask before adding heavy scaffolding.

**Logging:** On success, append to `.docs/changelog.md` per `.docs/changelog-spec.md`: `- YYYY-MM-DD HH:mm ran /test — [brief summary]`.

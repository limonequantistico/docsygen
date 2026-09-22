# Changelog

## 2026-09-01

### 23:52

  - ran `/deep-audit` — audited `scripts/validate.py`; 2 findings, both fixed and regression-tested
  - added `/deep-audit` skill — whole-codebase sweep for latent bugs, security, failure paths, and architectural risk; report-first, fix on approval
  - fixed `check_skill_count()` crashing on a malformed Codex manifest instead of printing the collected errors
  - fixed the README banner check validating only the indent, letting a misaligned box pass green
  - bumped docsygen to 1.10.0

## 2026-09-02

### 00:32

  - added `/debug` skill — evidence-driven diagnosis of one reported bug: competing hypotheses, instrumentation to tell them apart, a reproduction, a root-cause fix, then the instrumentation stripped back out
  - shaped `/debug` as a runtime-evidence loop rather than the ticket-style interview the backlog proposed — the interview mostly collects what the agent can find by reading the repo; only repro, expected, and actual can't be, so intake is a gate, not a session. Cursor's Debug Mode confirmed the shape
  - kept `/debug` user-invoked only: the agent debugs from evidence on every bug via a new `CLAUDE.md` rule, and points at the skill once, after a second failed fix attempt on the same symptom
  - added a debugging rule to the `/init` `CLAUDE.md` template and the repo's own `CLAUDE.md` — the always-on half, since most bugs are never escalated to a command
  - wired scope boundaries: `/review` and `/deep-audit` hand a reproducible symptom to `/debug`
  - bumped docsygen to 1.11.0

## 2026-09-03

### 16:06

  - added convention detection to `/commit`, `/merge`, and `/push` — they now read `.docs/commit-convention.md` if it exists, otherwise sample recent git history for a dominant existing style, default to Conventional Commits when history is too thin, or ask once (and persist the answer) when it's genuinely mixed
  - fixed `/merge` and `/push` carrying a drifted, abbreviated copy of `/commit`'s message-format guidance (missing `perf`/`build`/`ci` types and breaking-change guidance)
  - had `/merge` and `/push` delegate to `/commit`'s steps 1–3 instead of duplicating them, cutting ~25 lines from each and removing the drift risk going forward
  - mentioned `.docs/commit-convention.md` in `/init`'s "newer artifacts" list — it's written lazily by `/commit`/`/merge`/`/push` on first use, same pattern as `.docs/preview.md`
  - bumped docsygen to 1.12.0

## 2026-09-16

### 15:48

  - added Pinterest to `/design-system` Step 0's gallery list, for loose moodboarding that the curated galleries miss
  - had `/design-system` Step 0 suggest 5-8 project-specific search keywords, matched to how each gallery searches (Mobbin by screen and flow, Dribbble and Pinterest by style)

### 17:17

  - added a craft-floor check to `/setup` Phase 2 — states, real content, contrast, focus, undrawn browser surfaces, and action-naming copy, verified on the rendered result in one bounded round per batch
  - had `/design-system` push back on default-by-accident recommendations, open its summary with a one-line design read, and record what the direction deliberately isn't
  - added a "templated look" dimension to `/ux-review`, checked against the design system's stated anti-directions and ranked below usability issues
  - added a UI-completeness rule to the `/init` CLAUDE.md template (states, long or missing content, contrast, default look)

### 17:30

  - tightened the new craft floor after a second-opinion review — `/setup` builds the showcase with the first batch and renders through it, falls back to a labelled "written, not run" check instead of setting up a preview unasked, and routes any new tint or surface color through the styles-file tokens
  - made the `/init` template UI rule conditional ("where they apply", "if design-system.md exists") and the `/design-system` design read's "avoids" clause optional
  - replaced the generic Pinterest example searches in `/design-system` Step 0, which contradicted the project-specific keyword guidance

### 17:41

  - added `/showcase` — creates or updates one dev-only page or screen rendering the design tokens and base components (variants, applicable states, one awkward-content case each); updates an existing showcase rather than duplicating it, and records its location in `.docs/preview.md` on approval
  - made the showcase optional in `/setup`: Phase 1 now offers it once alongside the styles-file check, Phase 2 adds batches to it only if one exists, and the closing check no longer assumes one
  - pointed the `/init` template rule (and this repo's `CLAUDE.md`) at `/showcase` when a project has no showcase, and had `/ux-review` use a recorded showcase as a component-level view
  - listed `/showcase` in `/help` and the README, and updated the skill count to 35

## 2026-09-17

### 01:27

  - added `/theming` — adds or repairs color modes (dark, high contrast, brand themes) on new or existing projects: assesses the token layer and hardcoded colors, settles each mode's values with contrast checks and writes them back to `design-system.md` on approval, wires the modes per the stack (checking current syntax against docs), migrates components to role tokens in approved batches, and verifies every mode rendered
  - made `/setup` Phase 1 always build role tokens on top of the palette, even for light-only projects, and offer `/theming` (when more than one mode is recorded or requested) alongside `/showcase`
  - fixed `/setup`'s Tailwind instruction, which still pointed at `tailwind.config` — v4 defines theme tokens in CSS with `@theme`
  - had `/design-system` design each mode's values up front when more than one is chosen, record a color-roles table with a column per mode, and check contrast in every mode
  - had `/showcase` render every color mode and `/setup`'s craft floor check contrast in each
  - listed `/theming` in `/help` and the README, and updated the skill count to 36

### 01:35

  - tightened the design-phase handoffs after a second-opinion review — `/setup` takes role tokens from `design-system.md` (proposing and writing them back when an older doc has none), wires only the primary mode and says visibly when recorded modes are left for `/theming`, and absorbs `/theming`'s verification into the showcase when it runs both
  - moved `/theming` and `/showcase` in `/help` from Quality passes to Phase 3 under `/setup`, matching the README

### 01:55

  - structured `/showcase` like a Figma design-system file — an index, foundations from primitive to composite (palette → role tokens, type, spacing/radii/elevation), components grouped by purpose (or by the project's own folder groups) with the same variant-grid, states-row, and awkward-case frame for each, flagging variants that won't form clean axes; updates slot new components into their group and offer to reorganize a flat showcase rather than doing it unasked
  - bumped docsygen to 1.13.0

### 02:14

  - added `/tweaks` — a dev-only in-app panel on any platform that allows it: checks runtime feasibility first and reports what won't work before building, a few high-leverage controls (color, fonts from a curated licensed list, type scale, shape), contrast-checked presets drawn from the directions `/design-system` considered, save to device-local storage, copy for agent, copy tokens, share or dev-log fallback for devices without an easy clipboard path, and reset; kept values and presets flow back to the styles file, `design-system.md`, or a committed presets file on approval
  - had `/setup` offer `/tweaks` once when components are done
  - listed `/tweaks` in `/help` and the README, and updated the skill count to 37
  - had `/design-system` record the directions it considered and the user didn't pick, one line each, so `/tweaks` presets start from real alternatives

### 02:27

  - tightened `/tweaks` after a second-opinion review — the copy-for-agent payload names `/tweaks` (and pasting one is a trigger) so values always return through the approval and contrast gate, the panel warns on any failing text/surface pair, font installs happen only on approval, the panel mounts on the showcase when no real screens exist yet, and later runs keep saved presets loadable
  - had `/design-system` write \"none offered\" instead of inventing considered directions, and spelled out what yes does in `/setup`'s `/tweaks` offer
  - bumped docsygen to 1.14.0

### 14:40

  - added `/asset` skill — makes an image, icon, illustration, marketing frame, App Store screenshot, or just a ready-to-use prompt from the seed and design system, through a route picked each run: built in code (SVG/HTML), pasted into a chat app, an API key, or a local or connected tool
  - added `skills/asset/generate.py`, the first script bundled with a skill — calls OpenAI, Gemini, or Cloudflare Workers AI with keys kept in `~/.config/docsygen/assets.env` (mode 600, edited by the user); it never takes a key as an argument, reports only set/missing, and scrubs key values from its output, so the agent never reads a key
  - listed `/asset` in `/help` and the README, added `.docs/assets/imgs/generated/` to the project map, and updated the skill count to 38
  - bumped docsygen to 1.15.0

### 14:55

  - had `/asset` ask for the display size when the platform doesn't fix one, derive density exports from it, and never export above the target, so small slots don't ship 4K renders
  - had `/asset` look up the best model for the asset's category on every run (arena.ai categories for ranking, Artificial Analysis for price and API availability), filtered to what the user can reach today, with dated sources; added `--model` to `generate.py` and moved the OpenAI default to `gpt-image-2`

### 15:06

  - ran `/herdr-review` with a Claude Opus reviewer on `/asset` — 6 findings, all accepted and fixed
  - fixed `generate.py` crashing at import on the macOS system Python 3.9 (PEP 604 annotations), and routed timeouts, malformed responses, and a missing prompt file through the scrubbed error path instead of raw tracebacks
  - fixed `generate.py` overwriting a kept candidate when an earlier one had been discarded — numbering now continues after the highest existing number
  - made the key file 600 from creation instead of chmod-ed afterwards, and tightened an already-existing config directory to 700
  - split the `/asset` run folder into `prompt.md` (sent to the model word for word) and `brief.md` (model, route, resolution, leaderboard snapshot), so metadata no longer leaks into paid prompts
  - had `/asset` locate `generate.py` from the skill's base directory — `CLAUDE_PLUGIN_ROOT` isn't set in the agent's shell — and spelled out the order of the code-route offer, model check, and route question

### 15:20

  - added an export, compress, and place step to `/asset`, replacing a manual pass through Squoosh — resize to the target, then compress per destination (pngquant for asset catalogs, WebP for Android, AVIF/WebP for plain web images, a light pass only when a framework image pipeline optimizes later, app icons left alone), check for banding before showing sizes before and after, and place only after the user confirms
  - stopped `/asset` from opening past runs and existing images on every run — it lists folder names only, and reads one run's `brief.md` plus the final placed asset only when the new asset has to match a series
  - had `/asset` keep the uncompressed master, `prompt.md`, and `brief.md` per run and offer to delete discarded candidates, since `.docs/` is usually committed

### 15:29

  - ran `/herdr-review` with a Claude Opus reviewer on `/asset`'s export and compression step — 13 findings, all accepted and fixed
  - had `/asset` crop to the target's proportions before resizing (scale to cover, crop around the planned composition, never upscale), since models return 3:2 or square for most requests
  - fixed the iOS app icon guidance — check `hasAlpha` and flatten, since App Store Connect rejects icons with an alpha channel — and dropped pngquant for asset catalogs, which Xcode re-encodes anyway
  - added Android exceptions (9-patches, launcher icon layers, Play Store graphics) and full compression commands with explicit outputs, treating pngquant's exit 98/99 as "keep the original"
  - opened the run folder for every route, code-built included (the SVG/HTML source is the master), and had series matching read `prompt.md` as well as `brief.md`
  - stopped `generate.py init` from chmod-ing a directory it doesn't own; `check` now prints where to get each missing key and whether a ready key comes from the key file or the shell environment; non-ASCII keys and undecodable image data now fail with a clear message instead of a misleading one or a traceback

### 15:43

  - ran `/herdr-review` with a Claude Opus reviewer on `/asset` — 7 findings, 6 accepted and fixed, 1 rejected (the reviewer conceded)
  - had `/asset` write every `sips` crop and resize to a new file, since `sips` edits in place and was destroying the kept master
  - added a short path for "Prompt only" in `/asset` — brief, optional model check, prompt, log — instead of running it through generation and export
  - added `--size 512px|1K|2K|4K` to `generate.py` (Gemini only; the others say they ignore it), snapped Gemini aspect ratios to the ones it accepts, and had `/asset` count a route's maximum size against it when picking
  - separated "invalid character in a key or account ID" and non-UTF-8 prompt files from provider errors in `generate.py`, including `InvalidURL`, which isn't a `ValueError` on Python 3.9
  - moved "where `generate.py` lives" ahead of its first use in `/asset`, and named the exact `rsvg-convert` flatten for the app icon (verified RGB output; a BMP round-trip keeps alpha)

### 16:24

  - had `/asset` treat text or ASCII art as an asset type of its own: written as text, checked for monospace alignment, plain ASCII vs Unicode stated, and not rendered to an image unless one is actually needed

### 16:26

  - removed Cloudflare Workers AI from `/asset` and `generate.py` — the free models were not good enough to justify the setup, and only FLUX.1 schnell worked with the script; the API route now covers OpenAI and Gemini

### 16:29

  - removed the local or connected tool route from `/asset` — free local models do not reach the quality the skill is for; routes are now code, a chat app, or an API key

## 2026-09-18

### 01:06

  - restructured `/help` into tables — every phase is now a `Step | Command | What it does` (or `Command | What it does`) table with one-line cells, replacing the prose bullet lists that had grown 2-3 sentences deep per command
  - added a "Which one do I want?" disambiguation table to `/help`, folding the `/commit`-`/push`-`/merge`, `/review`-`/clean`-`/deep-audit`, `/debug`, and `/to-prd`-`/to-issues` comparisons out of Tips
  - cut `/help` Tips from 14 bullets to 7, dropping the ones that restated a command's own entry in longer form
  - taught `scripts/validate.py` to read `/help`'s command entries and step numbers from table rows as well as list items, so the listing check still catches a skill that was never added to the guide

### 01:16

  - renumbered the `/help` spine to 0-8 — `/init`, the manual idea file, `/seed`, `/seed-review`, `/stack`, `/design-system`, `/scaffold`, `/setup`, `/test` — and unnumbered everything after it; the old numbering implied `/prototype`, `/test`, and the ship commands were mandatory steps in order, when `/commit`/`/push`/`/merge` are alternatives and the rest are optional
  - moved the Anytime section below the numbered phases so the spine reads 0→7 uninterrupted, and renamed "Phase 4 — Ship" to "Ship" now that it carries no step numbers
  - removed the "Which one do I want?" table and the whole Tips section from `/help` — it should be a glanceable reminder of what's available, not a document to study; the planning pipeline, backlog-vs-Issues, and measured-vs-inferred notes already live in the README, which `/help` now links to
  - trimmed `/help` from ~2000 to ~1200 words, cutting the CodeGraph setup paragraph and the "two ways in" explainer down to the rows they belong to

### 01:24

  - numbered `/test` as step 8 in `/help`, extending the spine to 0-8
  - bumped docsygen to 1.16.0

## 2026-09-22

### 10:49

  - added a graveyard to `/tidy` — backlog items untouched for 60+ days (per `git blame`, overridable with e.g. `/tidy 90 days`) are proposed for burial and, on approval, moved word for word to `.docs/graveyard.md` with their added date; nothing is deleted, and editing an item keeps it alive
  - `/tidy` now flags backlog items that restate a buried one and offers to bring back the old note's context, turning "good ideas resurface" into a signal
  - kept `.docs/idea.md` out of the graveyard — it's `/seed`'s raw input, not a task list
  - updated `/help`, the README (command table, docs table, conventions), and the `/init` backlog template
  - bumped docsygen to 1.17.0

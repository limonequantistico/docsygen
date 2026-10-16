# Tech stack

Docsygen ships no application code. It runs inside whichever agent loads it, on machines we don't control, so everything bundled must work on a bare checkout with nothing installed.

| Part | Technology | Constraint |
|---|---|---|
| Skills | Markdown `SKILL.md`, flat YAML frontmatter (`name`, `description`) | Frontmatter stays flat scalars: `scripts/validate.py` parses it without PyYAML |
| Manifests | JSON (`.claude-plugin/`, `.codex-plugin/`, `.agents/plugins/`) | The two `plugin.json` versions stay equal |
| Bundled scripts | Python 3.9+, standard library only (`render.py`, `generate.py`, `validate.py`) | 3.9 is the macOS system `python3`: use `from __future__ import annotations` for `X \| None` hints |
| Bundled scripts | Node 18+, built-in modules only (`share.mjs`) | No `package.json`, no installs |
| CI | GitHub Actions, `ubuntu-latest`, runs `python3 scripts/validate.py` | — |
| Dev-only | `fonttools` + `brotli` in a throwaway venv, for `scripts/architecture_metrics.py` | Never needed at skill time |

No package manager and no dependencies. A new runtime dependency means every user has to install it first, so it needs a very good reason.

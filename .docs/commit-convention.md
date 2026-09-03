# Commit message convention

This project uses [Conventional Commits](https://www.conventionalcommits.org/): `<type>: <summary>`.

## Format

```
<type>: changed this, added that, removed this

- specific bullet about one change
- specific bullet about another change
```

Types: `feat`, `fix`, `docs`, `refactor`, `chore`, `style`, `test`, `perf`, `build`, `ci`. Mark breaking changes with `!` after the type or a `BREAKING CHANGE:` line — `/version` reads the type to work out the next release.

## Source

Detected from the last 20 commits on 2026-09-03 — every one already followed `<type>: summary`, consistently. Adopted as the recorded convention.

#!/usr/bin/env python3
"""Validate the docsygen plugin before it reaches users.

Checks the invariants that are maintained by hand and therefore drift:
  1. every skills/<name>/SKILL.md has frontmatter with `name` and `description`,
     and `name` matches its directory
  2. every manifest is parseable JSON
  3. the two plugin.json versions agree (both agents cache by version — if they
     disagree, one agent installs a different build than the other)
  4. the skill count is the same everywhere it's written down

Run with no arguments from the repo root. Exits non-zero on any failure.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CLAUDE_MANIFEST = ROOT / ".claude-plugin" / "plugin.json"
CODEX_MANIFEST = ROOT / ".codex-plugin" / "plugin.json"
MANIFESTS = [
    CLAUDE_MANIFEST,
    CODEX_MANIFEST,
    ROOT / ".claude-plugin" / "marketplace.json",
    ROOT / ".agents" / "plugins" / "marketplace.json",
]

errors: list[str] = []


def fail(msg: str) -> None:
    errors.append(msg)


def parse_frontmatter(text: str) -> dict[str, str] | None:
    """Pull `key: value` pairs out of a leading --- fenced block.

    Deliberately not a YAML parser: skill frontmatter is flat scalars only, and
    depending on PyYAML would mean the check can't run on a bare checkout.
    """
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    fields: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if match:
            fields[match.group(1)] = match.group(2).strip().strip("\"'")
    return fields


def check_skills() -> int:
    skills_dir = ROOT / "skills"
    if not skills_dir.is_dir():
        fail("skills/ directory not found")
        return 0

    dirs = sorted(d for d in skills_dir.iterdir() if d.is_dir())
    for d in dirs:
        skill = d / "SKILL.md"
        if not skill.is_file():
            fail(f"{d.relative_to(ROOT)}/ has no SKILL.md")
            continue

        fields = parse_frontmatter(skill.read_text(encoding="utf-8"))
        rel = skill.relative_to(ROOT)
        if fields is None:
            fail(f"{rel}: missing or malformed --- frontmatter block")
            continue
        if not fields.get("name"):
            fail(f"{rel}: frontmatter has no `name`")
        elif fields["name"] != d.name:
            fail(f"{rel}: name is '{fields['name']}' but directory is '{d.name}'")
        if not fields.get("description"):
            fail(f"{rel}: frontmatter has no `description` — the agent uses this to decide when to load the skill")

        # Skills that lay out numbered steps get edited by inserting a step in the
        # middle, which is exactly when the tail stops being renumbered. Catch both
        # ways that goes wrong: a repeated/skipped number, and a "5b."-style suffix
        # bolted on to dodge renumbering.
        body = skill.read_text(encoding="utf-8")
        raw = re.findall(r"^#{2,4}\s+(\d+[a-z]?)\.\s", body, re.M)
        suffixed = [s for s in raw if not s.isdigit()]
        if suffixed:
            fail(f"{rel}: step heading(s) {suffixed} use a letter suffix — renumber the steps instead")
        steps = [int(s) for s in raw if s.isdigit()]
        if steps and steps != list(range(1, len(steps) + 1)):
            fail(f"{rel}: numbered step headings are {steps}, expected 1..{len(steps)} in order")

    return len(dirs)


def check_manifests() -> None:
    for path in MANIFESTS:
        if not path.is_file():
            fail(f"{path.relative_to(ROOT)} not found")
            continue
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            fail(f"{path.relative_to(ROOT)}: invalid JSON — {e}")


def check_versions() -> None:
    if not (CLAUDE_MANIFEST.is_file() and CODEX_MANIFEST.is_file()):
        return
    try:
        claude = json.loads(CLAUDE_MANIFEST.read_text(encoding="utf-8"))
        codex = json.loads(CODEX_MANIFEST.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return  # already reported by check_manifests

    if claude.get("version") != codex.get("version"):
        fail(
            f"version mismatch: .claude-plugin/plugin.json is {claude.get('version')!r}, "
            f".codex-plugin/plugin.json is {codex.get('version')!r} — they must be equal"
        )

    version = claude.get("version")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    if version and f"Version {version}" not in readme:
        fail(f"README banner does not mention 'Version {version}' — bump the two version spots in the ASCII banner")
    if version and f"║         {version}" not in readme:
        fail(f"README banner box does not show {version} — bump the second version spot in the ASCII banner")


def check_skill_count(count: int) -> None:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for label, text in [("README.md", readme)]:
        for stated in set(re.findall(r"\*\*(\d+) skills\*\*", text) + re.findall(r"the (\d+) skills", text)):
            if int(stated) != count:
                fail(f"{label} says {stated} skills but skills/ contains {count}")

    codex = json.loads(CODEX_MANIFEST.read_text(encoding="utf-8"))
    long_desc = codex.get("interface", {}).get("longDescription", "")
    for stated in set(re.findall(r"(\d+) skills", long_desc)):
        if int(stated) != count:
            fail(f".codex-plugin/plugin.json longDescription says {stated} skills but skills/ contains {count}")

    # /help is the command reference, so every skill except /help itself must appear
    # in one of its lists — that listing is the thing most likely to be forgotten when
    # a skill is added. The numbered phases are the workflow's spine; the "Anytime"
    # commands are bulleted precisely because they have no position in that order, so
    # accept both forms (an entry must *start* with the command, which is what keeps
    # prose tips mentioning `/foo` from counting as a listing).
    help_skill = ROOT / "skills" / "help" / "SKILL.md"
    if help_skill.is_file():
        text = help_skill.read_text(encoding="utf-8")
        listed = set(re.findall(r"^\s*(?:\d+\.|[-*])\s+`/([a-z0-9-]+)`", text, re.M))
        expected = {d.name for d in (ROOT / "skills").iterdir() if d.is_dir()} - {"help"}
        for missing in sorted(expected - listed):
            fail(f"skills/help/SKILL.md does not list /{missing} in its numbered command list")
        for extra in sorted(listed - expected):
            fail(f"skills/help/SKILL.md lists /{extra}, which has no skills/{extra}/ directory")

        # The numbered spine opens with `0. /init` (Phase 0) and one un-numbered prose step, so
        # don't demand it start at 1 — just that it never repeats or goes backwards,
        # which is what catches a skill bolted on as "19b." instead of renumbered.
        numbers = [int(n) for n in re.findall(r"^\s*(\d+)\.\s+`/", text, re.M)]
        if numbers != sorted(set(numbers)):
            fail("skills/help/SKILL.md command list has duplicate or out-of-order numbers")


def main() -> int:
    count = check_skills()
    check_manifests()
    check_versions()
    if count:
        check_skill_count(count)

    if errors:
        print(f"✗ {len(errors)} problem(s) found:\n", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    print(f"✓ {count} skills, manifests valid, versions aligned")
    return 0


if __name__ == "__main__":
    sys.exit(main())

---
name: herdr-guru
description: Open a read-only project expert in a herdr pane — a second agent on the same project that answers any question about it (architecture, how a feature works, why it's built this way, what the other agent is changing) without writing anything or disturbing the agents at work. It can also read the working agent's conversation live, so it can answer questions about what was said, decided, or done, even after the guru was opened. Use only when the user explicitly asks for a guru, a read-only expert, or a second chat to ask questions about the project, or runs /herdr-guru. `/herdr-guru here` turns the current session into the guru instead, and works outside herdr too.
---

You are **opening a guru**: a second agent on this project that the user can question freely while other agents keep working. The guru is read-only, and its whole job is keeping the user's mental model of the project sharp.

Here's why it exists. When agents write most of the code, the user's picture of the project slowly blurs. The obvious fix is asking the working agent, but every question takes up its context window right when its next step needs it, and it interrupts the work. So the questions go unasked, and the gaps pile up. The guru takes those questions instead. It runs in a separate pane with separate context, and it can be on a cheaper model, because explaining code that already exists is easier than writing it.

**Custom instructions:** Anything the user adds after the command is passed to the guru (Step 4). That includes what they already know well ("I know Swift and SQL, skip those"), where to focus, and how deep to go. Two words are flags for you: `here` (Step H), and `--kind <kind>` (skip the question in Step 2).

**Keep your own footprint small.** If you're the working agent, every token you spend here comes out of the context this skill is meant to protect. Don't read the project, summarise it, or brief the guru on it. The guru orients itself. The brief is a file that comes with this skill.

**The files that come with this skill** live next to this `SKILL.md`, in the base directory the skill was loaded from (Claude Code prints it as "Base directory for this skill"). If the base directory isn't shown, find it with `find ~/.claude/plugins ~/.codex -path '*/skills/herdr-guru/guru-brief.md' 2>/dev/null` and use the newest one.

- `guru-brief.md`: everything the guru needs to know. It stands on its own, because the guru may not have docsygen installed.
- `transcript.sh`: prints a short digest of another agent's conversation (what the human said, what the agent replied, and the tools it ran), looked up through herdr from that agent's pane. It supports Claude Code and Codex.

---

## Step H — `here`: become the guru

If the user passed `here`, don't spawn anything. Read `guru-brief.md` and follow it **for the rest of this session**, with the user's extra instructions applied on top. Skip the herdr parts of the brief if `HERDR_ENV` isn't `1`. Finish with its ready message, then wait for questions.

**Which conversation to follow.** Inside herdr, run `herdr agent list` and look for agents other than you (`pane_id` isn't `$HERDR_PANE_ID`) whose `cwd` is this project. With exactly one, follow it with `<base>/transcript.sh <its-pane-id>`. With several, ask which one. With none, or outside herdr, there's no conversation to follow, and the guru works from the project alone. Say that in the ready message.

This is the route outside herdr. The user opens a second terminal on the project, starts any agent, and runs `/herdr-guru here`.

## Step 0 — Preflight

1. `test "${HERDR_ENV:-}" = 1`. If this fails, say this session isn't inside herdr. Suggest opening a second session on this project and running `/herdr-guru here` there, then stop.
2. Run `command -v herdr`. If it's missing, say so and stop.
3. Run `herdr agent list`. If an agent named `guru` (or `guru-<n>`) is already live with this project as its `cwd`, don't open a second one. Give the user its pane ID and `herdr agent focus <name>`, and stop. A second guru only makes sense if the user asks for one.

## Step 1 — Note whose conversation to follow

The guru follows **your** conversation: the agent in the calling pane, `$HERDR_PANE_ID`. Check that it can be read: `<base>/transcript.sh "$HERDR_PANE_ID" | head -1`. You need the header line only. Don't read the digest itself. If the script fails (the kind isn't supported, or there's no transcript file), the guru still works from the project alone. Mention it in Step 6.

## Step 2 — Choose the guru

Unless `--kind` was given, ask with AskUserQuestion, with these options in this order:

1. **Claude Sonnet (Recommended)**: cheap, and very good at explaining code that already exists. It saves the expensive model's quota for the agent doing the building.
2. **Claude Opus**: for a large or subtle codebase, or deep design discussions.
3. **Codex**: a different model family is a genuinely different second perspective.

The built-in *Other* option covers any other kind. Check a free-text kind against the `kinds:` line that `herdr agent` prints.

## Step 3 — Open the pane and start it read-only

Check the calling pane's shape, then split a sibling in the current tab and current directory:

```bash
herdr pane layout --pane "$HERDR_PANE_ID"
herdr pane split --current --direction right --cwd "$PWD" --no-focus
```

Split a wide pane `right` and a narrow or tall pane `down`. Read the new ID from `.result.pane.pane_id` with `jq -r`. Never guess it. Label it with `herdr pane rename <pane-id> guru`.

Name the agent `guru`, or `guru-2` and so on if the name is taken. Start it with whatever read-only enforcement the agent kind supports. The brief forbids writes too, but a rule the tool enforces beats one the agent has to remember:

```bash
# Claude: file-editing tools removed; the brief covers shell commands
herdr agent start guru --kind claude --pane <pane-id> --timeout 120000 -- --model sonnet --disallowedTools Edit Write NotebookEdit
# Codex: the read-only sandbox enforces it at the OS level
herdr agent start guru --kind codex --pane <pane-id> --timeout 120000 -- --sandbox read-only
```

Use `--model opus` for Opus. For other kinds, pass their native read-only flag after `--` if they have one. If they don't, the brief alone carries the rule. Say so in Step 6.

If it returns `agent_not_ready`, run `herdr agent wait guru --timeout 120000` and then `herdr agent get guru`. If it's still `blocked`, tell the user what it's asking and stop. **Never answer an approval dialog on the user's behalf.**

## Step 4 — Send the brief

Build the prompt in a temp file. Start with the full contents of `guru-brief.md`. If Step 1 worked, add a final section with the absolute paths filled in:

```markdown
## The working agent

Pane `<HERDR_PANE_ID>`. Read its conversation with `<base>/transcript.sh <HERDR_PANE_ID>`.
```

If the user gave extra instructions, add them after that, under a heading `## From the human`, word for word. Then send it:

```bash
herdr agent prompt guru "$(cat <prompt-file>)" --wait --timeout 600000
```

## Step 5 — Confirm it's ready, without reading it

Check for the ready line only. Don't pull the guru's summary into your own context:

```bash
herdr agent read guru --source recent-unwrapped --lines 60 | grep -cE "GURU READY · [^<]"
```

The pattern skips the template line in the echoed brief, which also contains `GURU READY` but is followed by `<`. A bare `GURU READY` match would pass before the guru has answered.

If there's no match, run `herdr agent get guru`. If it's `blocked`, surface that and stop. If it's still `working`, wait once more with `herdr agent wait guru --timeout 300000` and check again. If there's still no ready line, tell the user to look at the pane. Don't resend the brief.

## Step 6 — Hand over

Tell the user, in a few lines:

- the guru is ready in pane `<pane-id>` (labelled `guru`), and which kind and model it is running;
- how to get there: click the pane, or run `herdr agent focus guru`; to give it more room, `herdr pane move <pane-id> --new-tab`;
- whose conversation it follows (your pane), or that it works from the project alone and why;
- that it stays open for the session and that you won't close it; `herdr pane close <pane-id>` closes it when they're done;
- if its read-only rule isn't enforced by the tool for this kind, say so in one line.

Then go back to what you were doing. Don't relay questions to the guru or read its answers later unless the user asks you to.

---

## Rules

- **The guru never writes.** If the user wants a change made, the guru drafts a prompt for the working agent, and the working agent makes the change.
- Use `--no-focus` when you create the pane. The user moves to the guru when they're ready.
- Open a sibling pane in the current tab and the current `cwd`. Don't create workspaces, tabs, or worktrees unless the user explicitly asks.
- Parse every ID from herdr's JSON. Never infer one.
- Never answer a blocked guru's dialog for the user.
- If the same herdr call fails twice, stop and ask. Each retry starts real processes.
- Never close the guru's pane yourself, and never close a pane this skill didn't create.

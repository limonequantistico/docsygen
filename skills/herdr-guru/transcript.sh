#!/usr/bin/env bash
# Print a compact, read-only digest of another agent's conversation: what the human
# said, what the agent replied, and which tools it ran (one line each). Tool output
# and hidden reasoning are dropped, which takes a ~1 MB transcript down to a few KB.
#
#   transcript.sh <herdr-pane-id>   resolve the agent's *current* session through herdr
#                                   (so /clear or a restart in that pane is followed)
#   transcript.sh --file <path>     digest a transcript file directly
#
# Supports Claude Code and Codex transcripts. Reads only; never writes anything.
set -euo pipefail

command -v jq >/dev/null || { echo "transcript.sh: jq is required" >&2; exit 1; }

if [ "${1:-}" = "--file" ]; then
  file="${2:?usage: transcript.sh --file <path>}"
  case "$file" in */.codex/*) kind=codex ;; *) kind=claude ;; esac
else
  pane="${1:?usage: transcript.sh <pane-id> | --file <path>}"
  info="$(herdr agent get "$pane")" || { echo "transcript.sh: no agent in pane $pane" >&2; exit 1; }
  kind="$(jq -r '.result | (.agent // .) | .agent // empty' <<<"$info")"
  sid="$(jq -r '.result | (.agent // .) | .agent_session.value // empty' <<<"$info")"
  [ -n "$sid" ] || { echo "transcript.sh: herdr reports no session for pane $pane" >&2; exit 1; }
  case "$kind" in
    claude) file="$(find ~/.claude/projects -name "$sid.jsonl" 2>/dev/null | head -1)" ;;
    codex)  file="$(find ~/.codex/sessions -name "*$sid.jsonl" 2>/dev/null | head -1)" ;;
    *) echo "transcript.sh: reading a '$kind' transcript isn't supported (claude and codex are)" >&2; exit 1 ;;
  esac
  [ -n "$file" ] || { echo "transcript.sh: no transcript file found for $kind session $sid" >&2; exit 1; }
fi

[ -r "$file" ] || { echo "transcript.sh: cannot read $file" >&2; exit 1; }
echo "# $kind transcript · $file · last written $(date -r "$file" '+%Y-%m-%d %H:%M')"

if [ "$kind" = codex ]; then
  jq -r '
    (try (.timestamp | sub("\\.[0-9]+Z$"; "Z") | fromdateiso8601 | localtime | strftime("%H:%M")) catch "") as $t
    | select(.type == "response_item") | .payload
    | if .type == "message" and .role == "user" then
        [.content[]? | .text // empty] | join("\n")
        | select(test("^\\s*(<|# AGENTS\\.md|# Context from my IDE)") | not)
        | "\n[\($t)] HUMAN: \(.)"
      elif .type == "message" and .role == "assistant" then
        "[\($t)] AGENT: \([.content[]? | .text // empty] | join("\n"))"
      elif .type == "function_call" or .type == "custom_tool_call" then
        "  · \(.name) \((.arguments // .input // "") | tostring | (fromjson? // .) | (.cmd? // .command? // .) | tostring | gsub("\n"; " ") | .[0:120])"
      else empty end
  ' "$file"
else
  jq -r '
    (try (.timestamp | sub("\\.[0-9]+Z$"; "Z") | fromdateiso8601 | localtime | strftime("%H:%M")) catch "") as $t
    | if .type == "user" and (.message.content | type) == "string" then
        "\n[\($t)] HUMAN: \(.message.content)"
      elif .type == "assistant" then
        .message.content[]?
        | if .type == "text" then "[\($t)] AGENT: \(.text)"
          elif .type == "tool_use" then
            "  · \(.name) \(.input.file_path // .input.command // .input.description // .input.prompt // "" | tostring | gsub("\n"; " ") | .[0:120])"
          else empty end
      else empty end
  ' "$file"
fi

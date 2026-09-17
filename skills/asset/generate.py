#!/usr/bin/env python3
"""Generate image candidates for /asset through a provider API without exposing keys.

Keys live in one env file outside every repository — ~/.config/docsygen/assets.env by
default, or the path in DOCSYGEN_ASSETS_ENV. This script is the only thing meant to open
it. It never takes a key as an argument, never prints one, and scrubs key values out of
anything it does print, so the agent driving it can use a provider without seeing a key.

  generate.py check
      Which providers are ready. Prints "ready" or the missing variable names — never values.
  generate.py init
      Create the key file with empty placeholders (dir 700, file 600). Re-running only
      appends placeholders for variables the file doesn't mention yet.
  generate.py run --provider NAME --prompt-file PATH --out DIR [--model ID] [--count N] [--aspect W:H] [--size 512px|1K|2K|4K] [--transparent]
      Generate N candidates into DIR. Prints the provider and model, then one saved path per line.
      --model wins over the key file's *_IMAGE_MODEL, which wins over the built-in default —
      defaults go stale fast, so /asset passes the model it just looked up.

Standard library only and Python 3.9+ (the macOS system python3), so it runs on a bare checkout.
"""

from __future__ import annotations

import argparse
import base64
import http.client
import json
import math
import os
import re
import stat
import sys
import urllib.error
import urllib.request
from pathlib import Path

DEFAULT_KEY_FILE = Path("~/.config/docsygen/assets.env").expanduser()
KEY_FILE = Path(os.environ.get("DOCSYGEN_ASSETS_ENV", DEFAULT_KEY_FILE)).expanduser()

PROVIDERS = {
    "openai": {
        "required": ["OPENAI_API_KEY"],
        "model_var": "OPENAI_IMAGE_MODEL",
        "default_model": "gpt-image-2",
        "where": "https://platform.openai.com/api-keys",
    },
    "gemini": {
        "required": ["GEMINI_API_KEY"],
        "model_var": "GEMINI_IMAGE_MODEL",
        "default_model": "gemini-3.1-flash-image",
        "where": "https://aistudio.google.com/apikey",
    },
}

TIMEOUT_SECONDS = 180

SIZES = ["512px", "1K", "2K", "4K"]
# Ratios Gemini accepts; anything else is a 400. Step 8 of /asset crops to the exact target anyway.
GEMINI_RATIOS = ["1:1", "2:3", "3:2", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9", "21:9"]


def load_env() -> dict[str, str]:
    """Key file values, overridden by anything already exported in the environment."""
    values: dict[str, str] = {}
    if KEY_FILE.is_file():
        for line in KEY_FILE.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            name, _, value = line.partition("=")
            name = name.removeprefix("export ").strip()
            values[name] = value.strip().strip("\"'")
    for provider in PROVIDERS.values():
        for name in provider["required"] + [provider["model_var"]]:
            if os.environ.get(name):
                values[name] = os.environ[name]
    return values


def secrets(env: dict[str, str]) -> list[str]:
    return [v for p in PROVIDERS.values() for n in p["required"] if len(v := env.get(n, "")) >= 8]


def scrub(text: str, env: dict[str, str]) -> str:
    for value in secrets(env):
        text = text.replace(value, "[redacted]")
    return text


def die(message: str, env: dict[str, str] | None = None) -> None:
    print(f"error: {scrub(message, env or {})}", file=sys.stderr)
    sys.exit(1)


def cmd_check(_: argparse.Namespace) -> None:
    env = load_env()
    if KEY_FILE.is_file():
        mode = stat.S_IMODE(KEY_FILE.stat().st_mode)
        note = "" if mode & 0o077 == 0 else f" — WARNING: mode {oct(mode)}, readable by others; run: chmod 600 {KEY_FILE}"
        print(f"key file: {KEY_FILE} (exists{note})")
    else:
        print(f"key file: {KEY_FILE} (not created yet — run: generate.py init)")
    for name, provider in PROVIDERS.items():
        missing = [n for n in provider["required"] if not env.get(n)]
        if missing:
            status = f"missing {', '.join(missing)} — get one at {provider['where']}"
        else:
            # An exported key silently wins over the file, may bill a different account,
            # and is visible to anything reading the shell environment — so say so.
            exported = any(os.environ.get(n) for n in provider["required"])
            status = "ready (from shell environment, overriding the key file)" if exported else "ready (from key file)"
        print(f"{name:<11} {status}")


def cmd_init(_: argparse.Namespace) -> None:
    created = not KEY_FILE.parent.exists()
    KEY_FILE.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    # Tighten only a directory this script owns. A custom DOCSYGEN_ASSETS_ENV can point
    # into $HOME or a shared folder, and silently locking that down breaks other tools.
    if created or KEY_FILE.parent == DEFAULT_KEY_FILE.parent:
        os.chmod(KEY_FILE.parent, 0o700)
    elif stat.S_IMODE(KEY_FILE.parent.stat().st_mode) & 0o077:
        print(f"note: {KEY_FILE.parent} is readable by others; the key file itself is still 600", file=sys.stderr)
    existing = KEY_FILE.read_text(encoding="utf-8") if KEY_FILE.is_file() else ""
    mentioned = set(re.findall(r"^\s*#?\s*(?:export\s+)?([A-Z0-9_]+)=", existing, re.M))

    lines: list[str] = []
    if not existing:
        lines += [
            "# docsygen /asset provider keys. Fill in only the providers you use.",
            "# Edit this file yourself — never paste a key into an agent chat.",
            "",
        ]
    for name, provider in PROVIDERS.items():
        new = [n for n in provider["required"] if n not in mentioned]
        if not new:
            continue
        lines.append(f"# {name} — get one at {provider['where']}")
        lines += [f"{n}=" for n in new]
        if provider["model_var"] not in mentioned:
            lines.append(f"# {provider['model_var']}={provider['default_model']}")
        lines.append("")

    if lines:
        # Created 600 from the first byte rather than chmod-ed after the fact.
        with os.fdopen(os.open(KEY_FILE, os.O_CREAT | os.O_WRONLY | os.O_APPEND, 0o600), "a", encoding="utf-8") as f:
            if existing and not existing.endswith("\n"):
                f.write("\n")
            f.write("\n".join(lines))
    os.chmod(KEY_FILE, 0o600)
    print(f"key file: {KEY_FILE}" + (" (placeholders added)" if lines else " (already has every placeholder)"))


def post_json(url: str, headers: dict[str, str], body: dict, env: dict[str, str]) -> dict:
    request = urllib.request.Request(
        url,
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", **headers},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
            raw = response.read()
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")[:800]
        die(f"{url.split('?')[0]} returned HTTP {e.code}: {detail}", env)
    except urllib.error.URLError as e:
        die(f"could not reach {url.split('?')[0]}: {e.reason}", env)
    except UnicodeEncodeError:
        die("a key in the key file contains a non-ASCII character (often a smart quote from pasting) — retype it")
    except (TimeoutError, OSError) as e:
        die(f"{url.split('?')[0]} failed mid-response: {e}", env)
    except (ValueError, http.client.HTTPException):
        # Raised before anything is sent, e.g. a line break inside a key's header value.
        # The fault is in the key file, not the provider.
        die("a key has an invalid character (a stray space or line break?) — retype it in the key file")
    try:
        return json.loads(raw)
    except ValueError:
        die(f"{url.split('?')[0]} returned a response that isn't JSON", env)
    return {}


def openai_size(aspect: tuple[int, int]) -> str:
    w, h = aspect
    return "1024x1024" if w == h else ("1536x1024" if w > h else "1024x1536")


def generate_openai(prompt: str, args: argparse.Namespace, env: dict[str, str], model: str) -> bytes:
    if args.size:
        print("note: openai sizes here are fixed at 1024 or 1536px on the long side; --size is ignored", file=sys.stderr)
    body = {"model": model, "prompt": prompt, "n": 1, "size": openai_size(args.aspect)}
    if args.transparent:
        body |= {"background": "transparent", "output_format": "png"}
    data = post_json(
        "https://api.openai.com/v1/images/generations",
        {"Authorization": f"Bearer {env['OPENAI_API_KEY']}"},
        body,
        env,
    )
    try:
        return base64.b64decode(data["data"][0]["b64_json"])
    except (KeyError, IndexError, TypeError):
        die(f"openai returned no image: {json.dumps(data)[:400]}", env)
    return b""


def generate_gemini(prompt: str, args: argparse.Namespace, env: dict[str, str], model: str) -> bytes:
    if args.transparent:
        print("note: gemini has no transparent-background option; generating opaque", file=sys.stderr)
    w, h = args.aspect
    ratio = min(GEMINI_RATIOS, key=lambda r: abs(math.log(int(r.split(":")[0]) / int(r.split(":")[1])) - math.log(w / h)))
    if ratio != f"{w}:{h}":
        print(f"note: gemini doesn't accept {w}:{h}; using the nearest supported ratio, {ratio}", file=sys.stderr)
    response_format = {"type": "image", "mime_type": "image/png", "aspect_ratio": ratio}
    if args.size:
        response_format["image_size"] = args.size
    data = post_json(
        "https://generativelanguage.googleapis.com/v1beta/interactions",
        {"x-goog-api-key": env["GEMINI_API_KEY"]},
        {
            "model": model,
            "input": prompt,
            "response_format": response_format,
        },
        env,
    )
    for step in data.get("steps", []):
        for item in step.get("content", []):
            if item.get("type") == "image" and item.get("data"):
                return base64.b64decode(item["data"])
    die("gemini returned no image — the model may have answered with text only; try rewording the prompt")
    return b""


GENERATORS = {"openai": generate_openai, "gemini": generate_gemini}


def extension(image: bytes) -> str:
    if image.startswith(b"\x89PNG"):
        return "png"
    if image.startswith(b"\xff\xd8"):
        return "jpg"
    if image[:4] == b"RIFF" and image[8:12] == b"WEBP":
        return "webp"
    return "bin"


def parse_aspect(value: str) -> tuple[int, int]:
    match = re.fullmatch(r"(\d+):(\d+)", value)
    if not match or 0 in (int(match.group(1)), int(match.group(2))):
        raise argparse.ArgumentTypeError("aspect must look like 1:1, 16:9, or 9:16")
    return int(match.group(1)), int(match.group(2))


def cmd_run(args: argparse.Namespace) -> None:
    env = load_env()
    provider = PROVIDERS[args.provider]
    missing = [n for n in provider["required"] if not env.get(n)]
    if missing:
        die(f"{args.provider} is not set up — add {', '.join(missing)} to {KEY_FILE} (run: generate.py init)")

    try:
        prompt = Path(args.prompt_file).read_text(encoding="utf-8").strip()
    except (OSError, UnicodeDecodeError) as e:
        die(f"could not read the prompt file as UTF-8 text: {e}")
    if not prompt:
        die(f"{args.prompt_file} is empty")

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    model = args.model or env.get(provider["model_var"]) or provider["default_model"]
    print(f"provider={args.provider} model={model}")

    # Continue after the highest number, not the count: candidates get discarded during
    # review, and counting would hand a gap's number to a file that still exists.
    taken = max((int(m.group(1)) for p in out.glob("candidate-*") if (m := re.match(r"candidate-(\d+)", p.name))), default=0)
    for i in range(args.count):
        try:
            image = GENERATORS[args.provider](prompt, args, env, model)
        except ValueError as e:
            die(f"{args.provider} returned image data that couldn't be decoded: {e}", env)
        path = out / f"candidate-{taken + i + 1:02d}.{extension(image)}"
        path.write_bytes(image)
        print(path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("check").set_defaults(func=cmd_check)
    sub.add_parser("init").set_defaults(func=cmd_init)
    run = sub.add_parser("run")
    run.add_argument("--provider", required=True, choices=PROVIDERS)
    run.add_argument("--prompt-file", required=True)
    run.add_argument("--out", required=True)
    run.add_argument("--model")
    run.add_argument("--count", type=int, default=2, choices=range(1, 5), metavar="1-4")
    run.add_argument("--aspect", type=parse_aspect, default=(1, 1))
    run.add_argument("--size", choices=SIZES, help="output resolution tier; only gemini honours it (512px on gemini-3.1-flash-image only)")
    run.add_argument("--transparent", action="store_true")
    run.set_defaults(func=cmd_run)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

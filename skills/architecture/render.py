#!/usr/bin/env python3
"""Render an /architecture model into an Excalidraw file, check its layout, and report status.

  render.py render MODEL [--out FILE] [--no-icons]
      Lay out every view of MODEL (see MODEL-FORMAT.md), write FILE (default: next to the
      model, architecture.excalidraw), stamp the file's hash into the model as renderedHash,
      then check the layout. Prints "layout clean" or one problem per line and exits 1.
      The file is written either way, so a failed check can still be looked at.
  render.py check FILE
      Run only the layout checks on an existing .excalidraw file.
  render.py status MODEL [--repo DIR]
      What /architecture needs to decide between create and update: whether the rendered
      file was edited by hand since the last render, the model's commit against HEAD, and
      which boxes and zooms sit on files changed since then. For a map of a GitHub repo
      (model has "source"), without --repo it only asks the remote whether it moved;
      with --repo pointing at a fresh clone it lists what changed.

The agent writes facts; this script owns every coordinate, so a map never depends on
hand-placed positions. Text is measured with Excalidraw's own fonts (metrics.json).

Standard library only and Python 3.9+, so it runs on a bare checkout.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import random
import subprocess
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
METRICS = json.loads((HERE / "metrics.json").read_text(encoding="utf-8"))
ICONS_VERSION = "13.21.0"
ICON_CACHE = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache")) / "docsygen" / "icons"

# ---------------------------------------------------------------- measuring

HAND, MONO = 5, 3


def measure(text: str, size: float, family: int = HAND) -> float:
    table = METRICS["fonts"][str(family)]
    fb = METRICS["fallback"]
    return max(sum(table.get(c, fb) for c in line) for line in text.split("\n")) * size


def lines_of(text: str) -> int:
    return len(text.split("\n")) if text else 0


# ---------------------------------------------------------------- palette

COLORS = {
    "blue": ("#1971c2", "#dbe4ff"), "green": ("#2f9e44", "#d3f9d8"), "violet": ("#6741d9", "#e5dbff"),
    "orange": ("#e8590c", "#ffe8cc"), "red": ("#e03131", "#ffe3e3"), "ink": ("#1e1e1e", "#ffffff"),
    "grey": ("#868e96", "#f1f3f5"), "yellow": ("#f08c00", "#fff3bf"),
}
RISK = {"high": ("#e03131", "#ffe3e3"), "medium": ("#e8590c", "#ffe8cc"),
        "low": ("#868e96", "#f1f3f5"), "done": ("#2f9e44", "#d3f9d8")}
STATUS = {"confirmed": ("#e03131", "#ffe3e3"), "to verify": ("#e8590c", "#ffe8cc"),
          "by design": ("#1971c2", "#dbe4ff"), "fixed": ("#2f9e44", "#d3f9d8")}
LEVEL = {"context": "C4 level 1", "containers": "C4 level 2: containers",
         "components": "C4 level 3: components", "menu": "C4 level 4, on demand",
         "zoom": "zoom", "trace": "trace", "data": "extra: data model", "states": "extra: state diagram"}
INK, MUTED, FAINT = "#1e1e1e", "#495057", "#868e96"

# ---------------------------------------------------------------- layout constants

FRAME_MIN_W = 1920
FRAME_GAP = 220
HEADER_H = 150
BAND_TITLE_H = 64
BAND_PAD_BOTTOM = 30
COL_GAP = 110
ROW_GAP = 90
NAME, JOB, PATH = 26, 17, 11
PAD = 16
BOX_MAX_W = 520


class Scene:
    def __init__(self, seed: str):
        self.rng = random.Random(seed)
        self.els: list[dict] = []
        self.files: dict[str, dict] = {}
        self.frame: str | None = None
        self.notes: list[str] = []

    def rid(self) -> str:
        return "e%012x" % self.rng.getrandbits(48)

    def add(self, kind: str, x: float, y: float, w: float, h: float, **kw) -> dict:
        e = dict(id=kw.pop("id", None) or self.rid(), type=kind, x=x, y=y, width=w, height=h, angle=0,
                 strokeColor=INK, backgroundColor="transparent", fillStyle="solid", strokeWidth=2,
                 strokeStyle="solid", roughness=1, opacity=100, groupIds=[], frameId=self.frame,
                 roundness=None, seed=self.rng.randint(1, 2**31 - 1), version=1,
                 versionNonce=self.rng.randint(1, 2**31 - 1), isDeleted=False, boundElements=[],
                 updated=1760000000000, link=None, locked=False)
        e.update(kw)
        self.els.append(e)
        return e

    def text(self, x, y, s, size=18, color=INK, family=HAND, group=None, kind=None, align="left"):
        w = measure(s, size, family) + 4
        e = self.add("text", x, y, w, lines_of(s) * size * 1.25, strokeColor=color, text=s,
                     originalText=s, fontSize=size, fontFamily=family, textAlign=align,
                     verticalAlign="top", containerId=None, lineHeight=1.25, autoResize=True,
                     groupIds=[group] if group else [])
        if kind:
            e["customData"] = {"kind": kind}
        return e

    def pill(self, x, cy, label, colors, size=14, group=None, anchor="left"):
        sc, sb = colors
        w = measure(label, size) + 22
        h = size * 1.25 + 10
        if anchor == "right":
            x -= w
        gs = [group] if group else []
        self.add("rectangle", x, cy - h / 2, w, h, strokeColor=sc, backgroundColor=sb,
                 roundness={"type": 3}, roughness=0, strokeWidth=1.5, groupIds=gs, customData={"kind": "tag"})
        self.text(x + 11, cy - size * 1.25 / 2, label, size, sc, HAND, group, kind="tag")
        return w

    def pin(self, n, x, y):
        g = self.rid()
        self.add("ellipse", x - 16, y - 16, 32, 32, strokeColor=STATUS["confirmed"][0],
                 backgroundColor=STATUS["confirmed"][0], groupIds=[g], customData={"kind": "pin"})
        self.text(x - measure(str(n), 20) / 2 - 2, y - 12, str(n), 20, "#ffffff", HAND, g, kind="pin")

    def icon(self, slug, x, y, size, group):
        fid = "icon-" + slug
        if fid not in self.files:
            svg = fetch_icon(slug)
            if not svg:
                self.notes.append(f"icon '{slug}' unavailable (offline or unknown slug) — drawn without it")
                return False
            self.files[fid] = {"mimeType": "image/svg+xml", "id": fid, "created": 1760000000000,
                               "dataURL": "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()}
        self.add("image", x, y, size, size, fileId=fid, status="saved", scale=[1, 1], crop=None,
                 strokeColor="transparent", groupIds=[group])
        return True


# ---------------------------------------------------------------- icons


def _get(url: str) -> bytes | None:
    try:
        with urllib.request.urlopen(url, timeout=10) as r:
            return r.read()
    except Exception:
        return None


def fetch_icon(slug: str) -> str | None:
    ICON_CACHE.mkdir(parents=True, exist_ok=True)
    svg_path = ICON_CACHE / f"{ICONS_VERSION}-{slug}.svg"
    data_path = ICON_CACHE / f"{ICONS_VERSION}-data.json"
    base = f"https://cdn.jsdelivr.net/npm/simple-icons@{ICONS_VERSION}"
    if not svg_path.exists():
        raw = _get(f"{base}/icons/{slug}.svg")
        if not raw or not raw.lstrip().startswith(b"<svg"):
            return None
        svg_path.write_bytes(raw)
    if not data_path.exists():
        raw = _get(f"{base}/_data/simple-icons.json")
        if raw:
            data_path.write_bytes(raw)
    color = "#1e1e1e"
    if data_path.exists():
        try:
            entries = json.loads(data_path.read_text(encoding="utf-8"))
            entries = entries.get("icons", entries) if isinstance(entries, dict) else entries
            for e in entries:
                if e.get("slug") == slug or slugify(e.get("title", "")) == slug:
                    color = "#" + e["hex"]
                    break
        except Exception:
            pass
    if color.lower() in ("#000000", "#ffffff"):
        color = "#1e1e1e"
    return svg_path.read_text(encoding="utf-8").replace("<path ", f'<path fill="{color}" ', 1)


def slugify(title: str) -> str:
    return "".join(c for c in title.lower().replace("+", "plus").replace(".", "dot").replace("&", "and") if c.isalnum())


# ---------------------------------------------------------------- boxes


def risk_of(tag: dict, pin) -> str:
    if tag.get("risk"):
        return tag["risk"]
    lines, deps = tag.get("lines") or 0, tag.get("dependents") or 0
    if pin or deps >= 20 or lines >= 2000:
        return "high"
    if deps >= 8 or lines >= 500:
        return "medium"
    return "low"


def tag_label(tag: dict, width: float) -> str:
    if tag.get("text"):
        return tag["text"]
    parts = []
    if tag.get("lines") is not None:
        parts.append(f"{tag['lines']:,} lines")
    options = []
    if tag.get("dependents") is not None:
        d = tag["dependents"]
        options = [parts + [f"{d} dependent" + ("" if d == 1 else "s")], parts + [f"{d} dep."], parts]
    else:
        options = [parts]
    for o in options:
        s = " · ".join(o)
        if measure(s, 14) + 22 <= width - 24:
            return s
    return " · ".join(options[-1])


def wrap_path(path: str, limit: float) -> str:
    if not path or measure(path, PATH, MONO) <= limit:
        return path
    cut = max(i for i in range(len(path)) if path[i] == "/" and measure(path[: i + 1], PATH, MONO) <= limit) \
        if any(path[i] == "/" and measure(path[: i + 1], PATH, MONO) <= limit for i in range(len(path))) else None
    if cut is None:
        return path
    return path[: cut + 1] + "\n" + path[cut + 1:]


def size_box(b: dict) -> None:
    """Work out a box's own width and height from its text."""
    nsize = b.get("nameSize") or (30 if b.get("big") else NAME)
    icons = len(b.get("icons") or ([b["icon"]] if b.get("icon") else []))
    job, name = b.get("job", ""), b["name"]
    inner = max(measure(name, nsize) + icons * 42 + (8 if icons else 0), measure(job, JOB) if job else 0, 168)
    path = b.get("path", "")
    inner = min(max(inner, measure(path, PATH, MONO) if path else 0), BOX_MAX_W - 2 * PAD)
    b["_path"] = wrap_path(path, inner) if path else ""
    inner = max(inner, measure(b["_path"], PATH, MONO) if path else 0)
    b["_nsize"] = nsize
    w = inner + 2 * PAD + 8
    h = 12 + nsize * 1.25 + 10 + lines_of(job) * JOB * 1.25 + 10 + lines_of(b["_path"]) * 14 + (24 if b.get("tag") else 12)
    if b.get("shape") == "ellipse":
        w, h = w * 1.4, h * 1.35
    if b.get("tag"):
        full = tag_label(b["tag"], 10_000)
        w = max(w, measure(full, 14) + 22 + 24 + 80)
    b["_w"], b["_h"] = w, h


def draw_box(sc: Scene, b: dict, x: float, y: float, w: float, h: float, pin_numbers: dict) -> None:
    color = b.get("color", "ink")
    st, bg = COLORS.get(color, COLORS["ink"])
    g = sc.rid()
    kw = dict(strokeColor=st, backgroundColor=bg, groupIds=[g])
    shape = "ellipse" if b.get("shape") == "ellipse" else "rectangle"
    if shape == "rectangle":
        kw["roundness"] = {"type": 3}
    if b.get("dashed"):
        kw["strokeStyle"] = "dashed"
    r = sc.add(shape, x, y, w, h, **kw)
    b["_el"], b["_group"] = r, g
    nsize, job = b["_nsize"], b.get("job", "")
    if shape == "ellipse":
        block = nsize * 1.25 + (6 + lines_of(job) * JOB * 1.25 if job else 0)
        ty = y + (h - block) / 2
        sc.text(x + (w - measure(b["name"], nsize)) / 2, ty, b["name"], nsize, INK, HAND, g)
        if job:
            sc.text(x + (w - measure(job, JOB)) / 2, ty + nsize * 1.25 + 6, job, JOB, "#343a40", HAND, g)
    else:
        sc.text(x + PAD, y + 12, b["name"], nsize, INK, HAND, g)
        if job:
            sc.text(x + PAD, y + 12 + nsize * 1.25 + 10, job, JOB, "#343a40", HAND, g)
        if b["_path"]:
            bottom = 22 if b.get("tag") else 10
            sc.text(x + PAD, y + h - bottom - lines_of(b["_path"]) * 14, b["_path"], PATH, FAINT, MONO, g)
    icons = b.get("icons") or ([b["icon"]] if b.get("icon") else [])
    for i, slug in enumerate(icons):
        sc.icon(slug, x + w - 46 - i * 42, y + 12, 34, g)
    tag = b.get("tag")
    if tag:
        risk = risk_of(tag, b.get("pin"))
        b["_tag_w"] = sc.pill(x + w - 12, y + h, tag_label(tag, w), RISK[risk], 14, g, anchor="right")
    if b.get("pin"):
        pin_numbers.setdefault(b["pin"], []).append((x - 6, y - 6))


# ---------------------------------------------------------------- arrows


def side_points(b, side):
    e = b["_el"]
    x, y, w, h = e["x"], e["y"], e["width"], e["height"]
    return {"top": (x, y, x + w, y), "bottom": (x, y + h, x + w, y + h),
            "left": (x, y, x, y + h), "right": (x + w, y, x + w, y + h)}[side]


def blocked_span(b, side):
    """The stretch of a box side an arrow must not leave from: the tag on the bottom edge."""
    if side == "bottom" and b.get("_tag_w"):
        e = b["_el"]
        right = e["x"] + e["width"] - 12
        return (right - b["_tag_w"] - 14, right + 14)
    return None


def sample(pts, step=6):
    out = []
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        n = max(2, int(((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5 // step))
        out += [(x0 + (x1 - x0) * k / n, y0 + (y1 - y0) * k / n) for k in range(n + 1)]
    return out


def rect_of(e, m=0.0):
    return (e["x"] - m, e["y"] - m, e["x"] + e["width"] + m, e["y"] + e["height"] + m)


def hits(pts, r):
    return any(r[0] <= x <= r[2] and r[1] <= y <= r[3] for x, y in pts)


def plan_arrows(view, boxes):
    """Choose the sides and attach points of every arrow, then spread arrows that share a side."""
    plans = []
    pair_count: dict = {}
    for a in view.get("arrows", []):
        A, B = boxes[a["from"]], boxes[a["to"]]
        ea, eb = A["_el"], B["_el"]
        key = tuple(sorted((a["from"], a["to"])))
        idx = pair_count.get(key, 0)
        pair_count[key] = idx + 1
        ay0, ay1, by0, by1 = ea["y"], ea["y"] + ea["height"], eb["y"], eb["y"] + eb["height"]
        same_row = not (ay1 <= by0 or by1 <= ay0)
        if same_row:
            if ea["x"] + ea["width"] <= eb["x"]:
                sa, sb = "right", "left"
            else:
                sa, sb = "left", "right"
            lo, hi = max(ay0, by0) + 18, min(ay1, by1) - 18
            plans.append(dict(a=a, A=A, B=B, sa=sa, sb=sb, along=None, pair=(key, idx), span=(lo, hi)))
        else:
            sa, sb = ("bottom", "top") if ay1 <= by0 else ("top", "bottom")
            lo, hi = max(ea["x"], eb["x"]) + 24, min(ea["x"] + ea["width"], eb["x"] + eb["width"]) - 24
            plans.append(dict(a=a, A=A, B=B, sa=sa, sb=sb, pair=(key, idx), span=(lo, hi) if hi - lo >= 30 else None))
    # parallel arrows between the same two boxes get spread apart
    totals = {}
    for p in plans:
        totals[p["pair"][0]] = totals.get(p["pair"][0], 0) + 1
    for p in plans:
        n, i = totals[p["pair"][0]], p["pair"][1]
        if p["sa"] in ("left", "right"):
            lo, hi = p["span"]
            y = (lo + hi) / 2 if n == 1 else lo + (hi - lo) * (i + 0.5) / n
            p["pa"] = (side_points(p["A"], p["sa"])[0], y)
            p["pb"] = (side_points(p["B"], p["sb"])[0], y)
        else:
            if p["span"]:
                lo, hi = p["span"]
                x = (lo + hi) / 2 if n == 1 else lo + (hi - lo) * (i + 0.5) / n
                xa = xb = x
            else:
                ea, eb = p["A"]["_el"], p["B"]["_el"]
                cb = eb["x"] + eb["width"] / 2
                ca = ea["x"] + ea["width"] / 2
                xa = min(max(cb, ea["x"] + 30), ea["x"] + ea["width"] - 30)
                xb = min(max(ca, eb["x"] + 30), eb["x"] + eb["width"] - 30)
            p["pa"] = (xa, side_points(p["A"], p["sa"])[1])
            p["pb"] = (xb, side_points(p["B"], p["sb"])[1])
    # keep attach points off tags and at least 46px apart on a shared side; a straight
    # vertical arrow keeps its far end in line with the near one when the far box allows it
    for end in ("a", "b"):
        groups: dict = {}
        for p in plans:
            box, side = (p["A"], p["sa"]) if end == "a" else (p["B"], p["sb"])
            if side in ("top", "bottom"):
                if end == "b" and p.get("span") and p["sa"] in ("top", "bottom"):
                    eb = p["B"]["_el"]
                    if eb["x"] + 26 <= p["pa"][0] <= eb["x"] + eb["width"] - 26:
                        p["pb"] = (p["pa"][0], p["pb"][1])
                        continue
                groups.setdefault((id(box), side), (box, side, []))[2].append(p)
        for box, side, ps in groups.values():
            e = box["_el"]
            lo, hi = e["x"] + (48 if box.get("pin") and side == "top" else 26), e["x"] + e["width"] - 26
            blk = blocked_span(box, side)
            key = "pa" if end == "a" else "pb"
            ps.sort(key=lambda p: p[key][0])
            xs = [p[key][0] for p in ps]
            if blk:
                xs = [min(x, blk[0]) if blk[0] <= x <= blk[1] or x > blk[1] else x for x in xs]
                hi = min(hi, blk[0])
            for i in range(1, len(xs)):
                xs[i] = max(xs[i], xs[i - 1] + 46)
            over = xs[-1] - hi if xs else 0
            if over > 0:
                xs = [x - over for x in xs]
            xs = [max(lo, x) for x in xs]
            for p, x in zip(ps, xs):
                p[key] = (x, p[key][1])
    return plans


def label_box(a, pts):
    """Where Excalidraw will put an arrow's bound label: centred on the middle point."""
    if not a.get("label"):
        return None
    if len(pts) % 2:
        mx, my = pts[len(pts) // 2]
    else:
        q0, q1 = pts[len(pts) // 2 - 1], pts[len(pts) // 2]
        mx, my = (q0[0] + q1[0]) / 2, (q0[1] + q1[1]) / 2
    tw, th = label_size(a)
    return (mx - tw / 2 - 6, my - th / 2 - 6, mx + tw / 2 + 6, my + th / 2 + 6)


def overlaps(a, b):
    return a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]


def route(sc, plans, obstacles, texts, gaps_x, gaps_y, extra=(), borders=()):
    """Pick a straight line, or a bend through the nearest gap, that crosses nothing it shouldn't."""
    drawn: list = []  # sampled lines of arrows already placed, so new labels stay off them
    for p in plans:
        a = p["a"]
        own = {id(p["A"]["_el"]), id(p["B"]["_el"])}
        own_groups = {p["A"]["_group"], p["B"]["_group"]}
        obs = [rect_of(o, 6) for o in obstacles if id(o) not in own] + list(extra)
        txt = [rect_of(t, 3) for t in texts
               if not (set(t["groupIds"]) & own_groups) or (t.get("customData") or {}).get("kind") == "tag"]
        pa, pb = p["pa"], p["pb"]

        own_r = [rect_of(p["A"]["_el"]), rect_of(p["B"]["_el"])]

        def cost(pts):
            s = sample(pts)
            c = sum(hits(s, r) for r in obs) * 10 + sum(hits(s, r) for r in txt)
            lb = label_box(a, pts)
            if lb:
                c += sum(overlaps(lb, r) for r in obs + txt + own_r) * 5 + sum(overlaps(lb, r) for r in borders) * 5
                c += sum(hits(d, lb) for d in drawn) * 5
            return c

        candidates = [[pa, pb]]
        my = (pa[1] + pb[1]) / 2
        mx = (pa[0] + pb[0]) / 2
        for gx in gaps_x:
            candidates.append([pa, (gx, my), pb])
        for gy in gaps_y:
            candidates.append([pa, (mx, gy), pb])
        vertical = p["sa"] in ("top", "bottom")
        if vertical:
            down = pa[1] < pb[1]
            near_a = [g for g in gaps_y if (pa[1] < g < pb[1]) if down] or [g for g in gaps_y if pb[1] < g < pa[1]]
            # elbows: down into a gap, across, down into the target
            for gy in near_a:
                candidates.append([pa, (pa[0], gy), (pb[0], gy), pb])
            # detours: into the first gap, along a column gap, out of the last gap
            if near_a:
                ga, gb = (near_a[0], near_a[-1]) if down else (near_a[-1], near_a[0])
                for gx in gaps_x:
                    candidates.append([pa, (pa[0], ga), (gx, ga), (gx, gb), (pb[0], gb), pb])
                # leave from the side instead, when the way down is busy
                ea = p["A"]["_el"]
                cy = ea["y"] + ea["height"] / 2
                for gx in gaps_x:
                    sx = ea["x"] + ea["width"] if gx > ea["x"] + ea["width"] else ea["x"] if gx < ea["x"] else None
                    if sx is not None:
                        candidates.append([(sx, cy), (gx, cy), (gx, gb), (pb[0], gb), pb])
        else:
            for gx in gaps_x:
                if min(pa[0], pb[0]) < gx < max(pa[0], pb[0]):
                    candidates.append([pa, (gx, pa[1]), (gx, pb[1]), pb])

        def length(c):
            return sum(((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5 for (x0, y0), (x1, y1) in zip(c, c[1:]))

        best = min(candidates, key=lambda c: (cost(c), len(c) > 3, length(c)))
        if os.environ.get("ARCH_DEBUG") and a.get("label") == os.environ["ARCH_DEBUG"]:
            for c_ in sorted(candidates, key=lambda c: (cost(c), len(c)))[:6]:
                print("candidate", [(round(x), round(y)) for x, y in c_], cost(c_))
        p["pts"] = best
        n_before = len(sc.els)
        draw_arrow(sc, p, best)
        texts.extend(e for e in sc.els[n_before:] if e["type"] == "text")
        drawn.append(sample(best))


def draw_arrow(sc, p, pts):
    a = p["a"]
    strong = a.get("strong")
    col = a.get("colorHex") or (INK if strong else MUTED)
    if a.get("color") in COLORS:
        col = COLORS[a["color"]][0]
    x0, y0 = pts[0]
    xs, ys = [q[0] for q in pts], [q[1] for q in pts]
    A, B = p["A"]["_el"], p["B"]["_el"]
    e = sc.add("arrow", x0, y0, max(xs) - min(xs), max(ys) - min(ys), strokeColor=col,
               strokeWidth=4 if strong else 2, strokeStyle="dashed" if a.get("dashed") else "solid",
               roundness={"type": 2} if len(pts) <= 3 else None, points=[[q[0] - x0, q[1] - y0] for q in pts],
               lastCommittedPoint=None, startArrowhead="arrow" if a.get("both") else None,
               endArrowhead="arrow", startBinding={"elementId": A["id"], "focus": 0, "gap": 6},
               endBinding={"elementId": B["id"], "focus": 0, "gap": 6}, elbowed=False)
    A["boundElements"].append({"id": e["id"], "type": "arrow"})
    B["boundElements"].append({"id": e["id"], "type": "arrow"})
    label = a.get("label")
    if label:
        if len(pts) % 2:
            mx, my = pts[len(pts) // 2]
        else:
            q0, q1 = pts[len(pts) // 2 - 1], pts[len(pts) // 2]
            mx, my = (q0[0] + q1[0]) / 2, (q0[1] + q1[1]) / 2
        fs = 20 if strong else 17
        tw, th = measure(label, fs) + 4, lines_of(label) * fs * 1.25
        t = sc.add("text", mx - tw / 2, my - th / 2, tw, th, strokeColor=col, text=label, originalText=label,
                   fontSize=fs, fontFamily=HAND, textAlign="center", verticalAlign="middle",
                   containerId=e["id"], lineHeight=1.25, autoResize=True)
        e["boundElements"].append({"id": t["id"], "type": "text"})


# ---------------------------------------------------------------- views


def label_size(a):
    fs = 20 if a.get("strong") else 17
    return measure(a.get("label", ""), fs) + 4 if a.get("label") else 0, lines_of(a.get("label", "")) * fs * 1.25


def layout_view(sc: Scene, view: dict, ox: float, oy: float, number: str, pins: dict, zoom_of: dict) -> float:
    """Lay out a grid view (every kind but menu): bands of rows of boxes. Returns the frame height."""
    bands = view.get("bands", [])
    boxes = {}
    for band in bands:
        band["rows"] = band.get("rows") or [band.get("boxes", [])]
        for row in band["rows"]:
            for b in row:
                if b:
                    if b["id"] in zoom_of:
                        b.setdefault("tag", {})
                        b["tag"]["risk"] = "done"
                        b["tag"]["_zoom"] = zoom_of[b["id"]]
                    size_box(b)
                    boxes[b["id"]] = b
    for b in boxes.values():
        t = b.get("tag")
        if t and t.get("_zoom"):
            core = tag_label({k: v for k, v in t.items() if k not in ("risk", "_zoom", "text")}, 10_000)
            t["text"] = f"zoomed in {t['_zoom']}" + (f" · {core}" if core else "")
            b["_w"] = max(b["_w"], measure(t["text"], 14) + 22 + 36)
    where = {}
    for bi, band in enumerate(bands):
        for ri, row in enumerate(band["rows"]):
            for ci, b in enumerate(row):
                if b:
                    where[b["id"]] = (bi, ri, ci)
    arrows = view.get("arrows", [])
    for a in arrows:
        for end in ("from", "to"):
            if a[end] not in boxes:
                raise SystemExit(f"view '{view.get('id')}': arrow {end} '{a[end]}' is not a box in this view")

    # column widths and gaps per band, row heights, gaps sized to the labels that cross them
    # one column grid shared by every band, so a box can sit straight above another
    ncols = max((len(r) for band in bands for r in band["rows"]), default=1)
    colw = [0.0] * ncols
    for band in bands:
        for row in band["rows"]:
            for ci, b in enumerate(row):
                if b:
                    colw[ci] = max(colw[ci], b["_w"])
    colw = [c or 160 for c in colw]
    gaps = [COL_GAP] * max(ncols - 1, 0)
    for a in arrows:
        fa, fb = where[a["from"]], where[a["to"]]
        if fa[0] == fb[0] and fa[1] == fb[1]:
            lw, _ = label_size(a)
            lo, hi = sorted((fa[2], fb[2]))
            for k in range(lo, hi):
                gaps[k] = max(gaps[k], (lw + 70) / (hi - lo))
    band_geo = []
    for bi, band in enumerate(bands):
        rowh = [max((b["_h"] for b in row if b), default=60) for row in band["rows"]]
        rgaps = [ROW_GAP] * max(len(band["rows"]) - 1, 0)
        band_geo.append(dict(colw=colw, gaps=gaps, rowh=rowh, rgaps=rgaps, width=sum(colw) + sum(gaps)))
    for a in arrows:
        fa, fb = where[a["from"]], where[a["to"]]
        if fa[0] == fb[0] and fa[1] != fb[1]:
            _, lh = label_size(a)
            g = band_geo[fa[0]]["rgaps"]
            for k in range(min(fa[1], fb[1]), max(fa[1], fb[1])):
                g[k] = max(g[k], lh + 70)
    band_gaps = [80] * max(len(bands) - 1, 0)
    for a in arrows:
        fa, fb = where[a["from"]], where[a["to"]]
        if fa[0] != fb[0]:
            _, lh = label_size(a)
            for k in range(min(fa[0], fb[0]), max(fa[0], fb[0])):
                band_gaps[k] = max(band_gaps[k], lh + 60)

    content_w = max((g["width"] for g in band_geo), default=0)
    W = max(FRAME_MIN_W, content_w + 2 * 110)
    fid = sc.rid()
    sc.frame = fid
    title = f"{number} · {view['title']}  ({LEVEL.get(view['kind'], view['kind'])})"
    sc.text(ox + 40, oy + 30, title, 40)
    sc.text(ox + 40, oy + 86, view.get("question", ""), 22, MUTED)
    y = oy + HEADER_H
    band_rects = []
    for bi, band in enumerate(bands):
        g = band_geo[bi]
        titled = bool(band.get("title"))
        top = y
        y += BAND_TITLE_H if titled else 0
        x0 = ox + (W - g["width"]) / 2
        colx = []
        cx = x0
        for ci, cw in enumerate(g["colw"]):
            colx.append(cx)
            cx += cw + (g["gaps"][ci] if ci < len(g["gaps"]) else 0)
        g["colx"], g["rowy"] = colx, []
        for ri, row in enumerate(band["rows"]):
            g["rowy"].append(y)
            for ci, b in enumerate(row):
                if b:
                    w = b["_w"]
                    draw_box(sc, b, colx[ci] + (g["colw"][ci] - w) / 2, y, w, g["rowh"][ri], pins)
            y += g["rowh"][ri] + (g["rgaps"][ri] if ri < len(g["rgaps"]) else 0)
        y += 14  # room for tags hanging off the last row
        if titled:
            y += BAND_PAD_BOTTOM
            band_rects.append((band, top, y))
        if bi < len(band_gaps):
            y += band_gaps[bi]

    # band borders and titles (title side chosen after arrows are routed)
    band_els = []
    for band, top, bottom in band_rects:
        st = COLORS.get(band.get("color", "grey"), COLORS["grey"])[0]
        r = sc.add("rectangle", ox + 40, top, W - 80, bottom - top, strokeColor=st, strokeStyle="dashed",
                   roundness={"type": 3}, customData={"kind": "band"})
        band_els.append((band, r, st))

    obstacles = [b["_el"] for b in boxes.values()]
    texts = [e for e in sc.els if e["type"] == "text" and e["frameId"] == fid]
    pin_rects = [(b["_el"]["x"] - 26, b["_el"]["y"] - 26, b["_el"]["x"] + 14, b["_el"]["y"] + 14)
                 for b in boxes.values() if b.get("pin")]
    tag_rects = [rect_of(e, 4) for e in sc.els if e["frameId"] == fid and e["type"] == "rectangle"
                 and (e.get("customData") or {}).get("kind") == "tag"]
    # gaps to bend through: between columns of every band, and between rows / bands
    left_edge = min(b["_el"]["x"] for b in boxes.values()) if boxes else ox + 100
    right_edge = max(b["_el"]["x"] + b["_el"]["width"] for b in boxes.values()) if boxes else ox + W - 100
    gaps_x = sorted({(ox + 40 + left_edge) / 2} | {(right_edge + ox + W - 40) / 2} | {
        g["colx"][ci] + g["colw"][ci] + g["gaps"][ci] / 2 for g in band_geo for ci in range(len(g["gaps"]))})
    gaps_y = sorted({g["rowy"][ri] + g["rowh"][ri] + g["rgaps"][ri] / 2 for g in band_geo for ri in range(len(g["rgaps"]))})
    plans = plan_arrows(view, boxes)
    borders = []
    for _band, r, _st in band_els:
        x0, y0, x1, y1 = rect_of(r)
        borders += [(x0, y0 - 1, x1, y0 + 1), (x0, y1 - 1, x1, y1 + 1), (x0 - 1, y0, x0 + 1, y1), (x1 - 1, y0, x1 + 1, y1)]
        gaps_y.append(y0 - 40)
        gaps_y.append(y1 + 40)
    route(sc, plans, obstacles, texts, gaps_x, sorted(set(gaps_y)), pin_rects + tag_rects, borders)

    arrow_pts = [sample(p["pts"]) for p in plans]
    for band, r, st in band_els:
        title = band["title"]
        tw = measure(title, 22)
        tx = r["x"] + 16
        spots = [r["x"] + 16 + k * 40 for k in range(int((r["width"] - tw - 36) // 40) + 1)]
        spots = spots[:1] + [r["x"] + r["width"] - 20 - tw] + spots[1:]
        for cand in spots:
            box_ = (cand - 6, r["y"] + 6, cand + tw + 6, r["y"] + 44)
            if not any(hits(s, box_) for s in arrow_pts) and not any(
                    box_[0] < q[2] and q[0] < box_[2] and box_[1] < q[3] and q[1] < box_[3] for q in pin_rects):
                tx = cand
                break
        else:
            sc.notes.append(f"band title '{title[:30]}' has no clear spot; consider fewer arrows across that band")
        sc.text(tx, r["y"] + 10, title, 22, st)

    for note in view.get("notes", []):
        sc.text(ox + 60, y, note, 19, MUTED)
        y += lines_of(note) * 19 * 1.25 + 16
    H = y - oy + 40
    sc.frame = None
    sc.add("frame", ox, oy, W, H, id=fid, name=title, roughness=0, frameId=None)
    view["_w"] = W
    return H


def layout_menu(sc: Scene, model: dict, view: dict, ox: float, oy: float, number: str, zooms: list) -> float:
    fid = sc.rid()
    sc.frame = fid
    title = f"{number} · {view.get('title', 'Zoom menu')}  ({LEVEL['menu']})"
    sc.text(ox + 40, oy + 30, title, 40)
    sc.text(ox + 40, oy + 86, view.get("question", "Level 4 is drawn only when you ask. Two ways to dig deeper:"), 22, MUTED)
    y = oy + HEADER_H
    sc.text(ox + 40, y, "Zoom into a part", 30)
    comp = next((v for v in model["views"] if v["kind"] == "components"), None)
    example = "a box"
    if comp:
        tagged = [b for band in comp.get("bands", []) for row in (band.get("rows") or [band.get("boxes", [])])
                  for b in row if b and b.get("tag")]
        if tagged:
            example = max(tagged, key=lambda b: (b["tag"].get("dependents") or 0) + (b["tag"].get("lines") or 0) / 100)["name"]
    sc.text(ox + 40, y + 42, f"Pick any box in the components view and ask: \"zoom into {example}\". You get a new frame.\n"
                             "The tag under each box tells you where to look first:", 19, MUTED)
    cx = ox + 40
    for lbl, rk in [("high: big, many files depend on it, or has a red pin", "high"), ("medium", "medium"),
                    ("low", "low"), ("already zoomed", "done")]:
        g = sc.rid()
        cx += sc.pill(cx, y + 140, lbl, RISK[rk], 17, g) + 16
    y += 200
    sc.text(ox + 40, y, "Follow an action", 30)
    sc.text(ox + 40, y + 42, "Ask: \"trace <action>\". You get a step-by-step strip across every part involved.", 19, MUTED)
    cx, row_y = ox + 40, y + 120
    W = FRAME_MIN_W
    for t in model.get("traces", []):
        done = t.get("view")
        lbl = (f"drawn in {zooms_by_id(zooms).get(done, '?')}: " if done else "") + t["label"]
        w = measure(lbl, 18) + 22
        if cx + w > ox + W - 40:
            cx, row_y = ox + 40, row_y + 50
        g = sc.rid()
        cx += sc.pill(cx, row_y, lbl, RISK["done" if done else "low"], 18, g) + 16
    y = row_y + 50
    sc.text(ox + 40, y, "Each zoom states the commit it was drawn from. If the code changed since, ask again to redraw it.", 17, FAINT)
    y += 60
    sc.frame = None
    sc.add("frame", ox, oy, W, y - oy, id=fid, name=title, roughness=0, frameId=None)
    return y - oy


def zooms_by_id(zooms):
    return {vid: num for vid, num in zooms}


def layout_cracks(sc: Scene, cracks: list, ox: float, oy: float, number: str, view_numbers: dict) -> float:
    fid = sc.rid()
    sc.frame = fid
    title = f"{number} · Where it can crack"
    sc.text(ox + 40, oy + 30, title, 40)
    sc.text(ox + 40, oy + 86, "One row per problem, with its evidence. Drag rows to reorder, or move fixed ones aside.", 22, MUTED)
    W = FRAME_MIN_W
    y = oy + HEADER_H
    for i, c in enumerate(cracks, 1):
        detail = c.get("detail", "")
        evidence = c.get("evidence", "")
        h = 70 + lines_of(detail) * 24 + (22 if evidence else 0)
        g = sc.rid()
        sc.add("rectangle", ox + 40, y, W - 80, h, strokeColor=MUTED, backgroundColor="#ffffff",
               roundness={"type": 3}, groupIds=[g])
        sc.add("ellipse", ox + 64, y + 30, 44, 44, strokeColor=STATUS["confirmed"][0],
               backgroundColor=STATUS["confirmed"][0], groupIds=[g])
        sc.text(ox + 86 - measure(str(i), 24) / 2 - 2, y + 37, str(i), 24, "#ffffff", HAND, g)
        status = c.get("status", "confirmed")
        sc_, sb = STATUS.get(status, STATUS["confirmed"])
        chip = status.upper()
        cw = max(150, measure(chip, 18) + 30)
        sc.add("rectangle", ox + 135, y + 32, cw, 40, strokeColor=sc_, backgroundColor=sb, roundness={"type": 3},
               roughness=0, groupIds=[g])
        sc.text(ox + 135 + (cw - measure(chip, 18)) / 2, y + 40, chip, 18, sc_, HAND, g)
        tx = ox + 135 + cw + 30
        sc.text(tx, y + 14, c["title"], 30, INK, HAND, g)
        if detail:
            sc.text(tx, y + 58, detail, 19, MUTED, HAND, g)
        if evidence:
            sc.text(tx, y + 62 + lines_of(detail) * 24, evidence, 12, FAINT, MONO, g)
        views = ", ".join(view_numbers.get(v, v) for v in c.get("views", []))
        if views:
            lab = "view " + views if "," not in views else "views " + views
            sc.text(ox + W - 60 - measure(lab, 18), y + 40, lab, 18, FAINT, HAND, g)
        y += h + 20
    y += 30
    sc.frame = None
    sc.add("frame", ox, oy, W, y - oy, id=fid, name=title, roughness=0, frameId=None)
    return y - oy


def render(model: dict, use_icons: bool = True) -> tuple[dict, Scene]:
    sc = Scene(model.get("project", "project"))
    if not use_icons:
        sc.icon = lambda *a, **k: False  # type: ignore
    views = model["views"]
    # numbering: 1, 2, 3 …; zooms and traces take the menu's number plus a letter
    numbers, n, menu_num, letter = {}, 0, None, "a"
    for v in views:
        if v["kind"] in ("zoom", "trace") and menu_num:
            numbers[v["id"]] = f"{menu_num}{letter}"
            letter = chr(ord(letter) + 1)
        else:
            n += 1
            numbers[v["id"]] = str(n)
            if v["kind"] == "menu":
                menu_num = str(n)
    cracks_number = str(n + 1)
    zoom_of = {v["zooms"]: numbers[v["id"]] for v in views if v["kind"] == "zoom" and v.get("zooms")}
    zooms = [(v["id"], numbers[v["id"]]) for v in views if v["kind"] in ("zoom", "trace")]

    project = model.get("project", "This project")
    sc.text(0, -340, f"{project}, from far to close", 56)
    commit = model.get("commit", "?")
    sc.text(0, -260, "Views 1-4 are the four C4 levels, each zooming into the one before (the zoom menu lists what can be drawn on request).\n"
                     "Later views are extra diagrams: the data, and the states things move through. Red pins = places it can crack.\n"
                     f"Paths start at the project root; ending in / means a folder. Drawn from commit {commit} on {model.get('date', '?')}.",
            22, MUTED)
    pins: dict = {}
    y = 0
    for v in views:
        if v["kind"] == "menu":
            h = layout_menu(sc, model, v, 0, y, numbers[v["id"]], zooms)
        else:
            if v["kind"] in ("zoom", "trace") and model.get("commit"):
                q = v.get("question", "")
                stamp = f"Drawn from commit {v.get('commit', model['commit'])} on {v.get('date', model.get('date', '?'))}."
                if stamp not in q:
                    v["question"] = (q + "  " + stamp).strip()
            h = layout_view(sc, v, 0, y, numbers[v["id"]], pins, zoom_of)
        y += h + FRAME_GAP
    if model.get("cracks"):
        layout_cracks(sc, model["cracks"], 0, y, cracks_number, numbers)
    for num, spots in pins.items():
        for x, py in spots:
            frame_backup = sc.frame
            sc.frame = None
            sc.pin(num, x, py)
            sc.frame = frame_backup
    # pins belong to the frame they sit in
    frames = [e for e in sc.els if e["type"] == "frame"]
    for e in sc.els:
        if (e.get("customData") or {}).get("kind") == "pin":
            for f in frames:
                if f["x"] <= e["x"] + 8 <= f["x"] + f["width"] and f["y"] <= e["y"] + 8 <= f["y"] + f["height"]:
                    e["frameId"] = f["id"]
    doc = {"type": "excalidraw", "version": 2, "source": "https://excalidraw.com", "elements": sc.els,
           "appState": {"viewBackgroundColor": "#ffffff", "gridSize": 20}, "files": sc.files}
    return doc, sc


# ---------------------------------------------------------------- checks


def check(doc: dict) -> list[str]:
    els = doc["elements"]
    E = {e["id"]: e for e in els}
    texts = [e for e in els if e["type"] == "text"]
    kind = lambda e: (e.get("customData") or {}).get("kind")
    bands = [e for e in els if kind(e) == "band"]
    tags = [e for e in els if e["type"] == "rectangle" and kind(e) == "tag"]
    boxes = [e for e in els if e["type"] in ("rectangle", "ellipse", "image") and kind(e) not in ("band", "tag")]
    frames = {e["id"]: e for e in els if e["type"] == "frame"}
    groups = lambda e: set(e["groupIds"])
    name = lambda e: (e.get("text") or e["type"]).replace("\n", " ")[:40]
    inter = lambda a, b: a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]
    P = []
    arrows = [e for e in els if e["type"] == "arrow"]
    pts_of = {a["id"]: sample([(a["x"] + p[0], a["y"] + p[1]) for p in a["points"]]) for a in arrows}
    label_of = lambda a: next((E[b["id"]]["text"] for b in a["boundElements"] if b["type"] == "text"), "-")

    # text fits inside the box it belongs to
    for t in texts:
        if t["containerId"] or kind(t) in ("tag", "pin") or not t["groupIds"]:
            continue
        owner = next((b for b in boxes if groups(b) & groups(t) and b["type"] != "image"), None)
        if owner and owner["type"] == "rectangle":
            r, o = rect_of(t), rect_of(owner)
            if r[2] > o[2] - 4 or r[0] < o[0] or r[3] > o[3] + 1:
                P.append(f"text '{name(t)}' doesn't fit its box")
    # arrows: label room, crossings
    for a in arrows:
        ends = {a["startBinding"]["elementId"], a["endBinding"]["elementId"]}
        end_groups = set().union(*[groups(E[i]) for i in ends])
        own = {b["id"] for b in a["boundElements"]}
        pts = pts_of[a["id"]]
        lab = label_of(a)
        if len(a["points"]) == 2 and own:
            t = E[min(own)]
            (x0, y0), (x1, y1) = a["points"]
            seg = ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5
            horiz = abs(x1 - x0) >= abs(y1 - y0)
            need = (t["width"] if horiz else t["height"]) + 30
            if seg < need:
                P.append(f"arrow '{lab}' is {seg:.0f}px, its label needs {need:.0f}px")
        for t in texts:
            if t["id"] in own or (groups(t) & end_groups and kind(t) != "tag"):
                continue
            if hits(pts, rect_of(t, 3)):
                P.append(f"arrow '{lab}' crosses text '{name(t)}'")
        for b in boxes:
            if b["id"] in ends or groups(b) & end_groups:
                continue
            if hits(pts, rect_of(b, -2)):
                P.append(f"arrow '{lab}' crosses a box ('{name(b)}')")
        for g in tags:
            if hits(pts, rect_of(g)):
                P.append(f"arrow '{lab}' crosses a tag")
    # labels: clear of everything, and off band borders
    for t in texts:
        if not t["containerId"]:
            continue
        a = E[t["containerId"]]
        ends = {a["startBinding"]["elementId"], a["endBinding"]["elementId"]}
        r = rect_of(t, 4)
        for o in texts + boxes + tags:
            if o["id"] != t["id"] and o["id"] not in ends and inter(r, rect_of(o)):
                P.append(f"label '{name(t)}' touches '{name(o)}'")
        for b in bands:
            x0, y0, x1, y1 = rect_of(b)
            for edge in ((x0, y0 - 1, x1, y0 + 1), (x0, y1 - 1, x1, y1 + 1), (x0 - 1, y0, x0 + 1, y1), (x1 - 1, y0, x1 + 1, y1)):
                if inter(r, edge):
                    P.append(f"label '{name(t)}' sits on a band border")
    # free text (titles, notes) and tags against boxes and each other; pins against text
    free = [t for t in texts if not t["containerId"] and kind(t) not in ("pin",)]
    for t in free:
        for o in boxes + free:
            if o["id"] == t["id"] or groups(o) & groups(t) or o["type"] == "image":
                continue
            if kind(o) == "pin" and kind(t) == "tag":
                continue
            if inter(rect_of(t, 2), rect_of(o)):
                P.append(f"text '{name(t)}' touches '{name(o)}'")
    for g in tags:
        for b in bands:
            x0, y0, x1, y1 = rect_of(b)
            if inter(rect_of(g), (x0, y1 - 1, x1, y1 + 1)) or inter(rect_of(g), (x0, y0 - 1, x1, y0 + 1)):
                P.append("a tag sits on a band border")
    # nothing outside its frame
    for e in els:
        f = frames.get(e.get("frameId"))
        if f and e["type"] != "arrow":
            r, fr = rect_of(e), rect_of(f)
            if r[0] < fr[0] - 1 or r[2] > fr[2] + 1 or r[1] < fr[1] - 1 or r[3] > fr[3] + 1:
                P.append(f"'{name(e)}' sticks out of frame '{f.get('name', '')[:30]}'")
    return sorted(set(P))


# ---------------------------------------------------------------- status


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def git(*args, cwd=None) -> str:
    try:
        return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, check=True).stdout.strip()
    except Exception:
        return ""


def all_boxes(model):
    for v in model["views"]:
        for band in v.get("bands", []):
            for row in band.get("rows") or [band.get("boxes", [])]:
                for b in row:
                    if b:
                        yield v, b


def status(model_path: Path, repo_dir: str | None = None) -> None:
    if not model_path.exists():
        print("model: none — create a new map")
        return
    model = json.loads(model_path.read_text(encoding="utf-8"))
    out = model_path.with_name(model.get("output", "architecture.excalidraw"))
    print(f"model: {model_path}")
    if not out.exists():
        print("rendered: missing — render it again from the model")
    else:
        edited = model.get("renderedHash") and sha(out) != model["renderedHash"]
        print(f"rendered: {out}" + ("  — EDITED BY HAND since the last render" if edited else "  — unchanged since the last render"))
    commit = model.get("commit", "")
    source = model.get("source") or {}
    if source.get("repo") and not repo_dir:
        # an external repo with no clone at hand: ask the remote, download nothing
        remote = git("ls-remote", source["repo"], source.get("ref") or "HEAD").split()
        upstream = remote[0][: len(commit) or 7] if remote else ""
        print(f"source: {source['repo']}")
        print(f"commit: model {commit or '?'} · upstream {upstream or 'unreachable'}")
        if upstream and commit and upstream.startswith(commit):
            print("changed since: nothing")
        elif upstream:
            print("changed since: upstream moved — clone it (--filter=blob:none) and rerun status with --repo DIR")
        return
    root = repo_dir or git("rev-parse", "--show-toplevel", cwd=model_path.parent) or str(model_path.parent)
    head = git("rev-parse", "--short", "HEAD", cwd=root)
    print(f"commit: model {commit or '?'} · HEAD {head or '?'}")
    if not commit or not head or commit == head:
        print("changed since: nothing" if commit == head else "changed since: unknown")
        return
    if not git("cat-file", "-t", commit, cwd=root):
        print(f"changed since: unknown — commit {commit} isn't in this repo's history (rebased?). Re-check every view.")
        return
    changed = git("diff", "--name-only", f"{commit}..HEAD", cwd=root).splitlines()
    changed += [l[3:] for l in git("status", "--porcelain", cwd=root).splitlines() if l]
    changed = sorted(set(c for c in changed if c and not c.startswith(".docs/diagrams/")))
    if repo_dir:
        changed = [c for c in changed if not c.startswith(".codegraph/")]
    print(f"changed since: {len(changed)} file(s)")
    hit_boxes, hit_zooms = [], []
    for v, b in all_boxes(model):
        p = (b.get("path") or "").split(" ")[0]
        if p and any(c == p or (p.endswith("/") and c.startswith(p)) for c in changed):
            hit_boxes.append(f"{v['id']}/{b['id']} ({p})")
    for v in model["views"]:
        if v["kind"] in ("zoom", "trace"):
            files = v.get("files", [])
            if any(c == f or (f.endswith("/") and c.startswith(f)) for f in files for c in changed):
                hit_zooms.append(v["id"])
    print("boxes on changed files: " + (", ".join(hit_boxes) or "none"))
    print("stale zooms: " + (", ".join(hit_zooms) or "none"))
    unmapped = [c for c in changed if not any((b.get("path") or "x") and (c == b.get("path") or ((b.get("path") or "").endswith("/") and c.startswith(b["path"])))
                                              for _, b in all_boxes(model))]
    if unmapped:
        print("changed files no box covers: " + ", ".join(unmapped[:25]) + (" …" if len(unmapped) > 25 else ""))


# ---------------------------------------------------------------- main


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("render")
    r.add_argument("model")
    r.add_argument("--out")
    r.add_argument("--no-icons", action="store_true")
    c = sub.add_parser("check")
    c.add_argument("file")
    s = sub.add_parser("status")
    s.add_argument("model")
    s.add_argument("--repo", help="the repo the model describes, when the model lives outside it (a GitHub clone)")
    args = ap.parse_args()

    if args.cmd == "status":
        status(Path(args.model), args.repo)
        return 0
    if args.cmd == "check":
        problems = check(json.loads(Path(args.file).read_text(encoding="utf-8")))
        print("\n".join(problems) or "layout clean")
        return 1 if problems else 0

    model_path = Path(args.model)
    model = json.loads(model_path.read_text(encoding="utf-8"))
    pristine = json.loads(model_path.read_text(encoding="utf-8"))
    out = Path(args.out) if args.out else model_path.with_name(model.get("output", "architecture.excalidraw"))
    doc, sc = render(model, use_icons=not args.no_icons)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    if not args.out:
        pristine["renderedHash"] = sha(out)
        model_path.write_text(json.dumps(pristine, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {out.resolve()}")
    for note in sc.notes:
        print("note: " + note)
    problems = check(doc)
    print("\n".join(problems) or "layout clean")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())

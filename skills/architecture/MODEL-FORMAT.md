# Architecture model format

`.docs/diagrams/architecture.model.json` holds the **facts** of the map. `render.py` owns every coordinate: you never place anything by position, you only say what exists, what row it sits in, and what connects to what. `example/architecture.model.json` is a complete worked example.

## Top level

```json
{
  "project": "Larder",
  "commit": "4f2c9e1",
  "date": "2026-10-16",
  "output": "architecture.excalidraw",
  "renderedHash": "…written by render.py, never by hand…",
  "views": [ … ],
  "traces": [ … ],
  "cracks": [ … ]
}
```

- `commit`: short hash of `HEAD` when the facts were checked. `render.py status` diffs against it.
- `renderedHash`: stamped by `render.py render`. If the `.excalidraw` file no longer matches it, someone edited the drawing by hand.
- `source`: only for a map of a GitHub repo: `{"repo": "https://github.com/owner/repo", "ref": "branch, if not the default"}`. Paths are then relative to that repo's root, and `status` checks the remote instead of the local repo.

## Views

Order is the reading order. Numbers are assigned automatically. A `zoom` or `trace` view placed after the `menu` view takes the menu's number plus a letter (4a, 4b…).

| `kind` | When | Frame label |
|---|---|---|
| `context` | always | C4 level 1 |
| `containers` | always | C4 level 2 |
| `components` | always (inside the main container) | C4 level 3 |
| `menu` | always, no content of its own | C4 level 4, on demand |
| `zoom` | only on request (`/architecture zoom <part>`) | zoom of one component |
| `trace` | only on request (`/architecture trace <action>`) | one action, step by step |
| `data` | the project stores data | extra: data model |
| `states` | one per entity with a status lifecycle | extra: state diagram |

Every view except `menu`:

```json
{
  "id": "components",
  "kind": "components",
  "title": "Inside the API",
  "question": "Which parts make up the API? Calls go downwards.",
  "bands": [ … ],
  "arrows": [ … ],
  "notes": ["optional sentences shown under the grid"]
}
```

A `zoom` also takes `"zooms": "<box id in the components view>"`, which turns that box's tag green, and `"files": [...]`, the paths `status` watches to flag the zoom as stale.

## Bands, rows, columns

A view is a stack of **bands**. A band with a `title` gets a dashed border, for a layer, a zone or a group. A band without one is just a row of boxes.

```json
{ "title": "SERVICES · the rules", "color": "violet", "boxes": [ box, box, null, box ] }
{ "rows": [ [ box, box, box ], [ null, box, box ] ] }
```

`boxes` is shorthand for a single row. **All bands in a view share one column grid**, so a box in column 2 sits straight above whatever is in column 2 below it. Use `null` to leave a column empty, so arrows can run straight instead of crossing boxes. Put things that talk to each other in the same column.

## Boxes

```json
{
  "id": "s_cook",
  "name": "CookService",
  "job": "cooking a recipe uses\nup pantry items",
  "path": "api/src/services/cook.ts",
  "color": "violet",
  "icon": "stripe",
  "pin": 3,
  "tag": { "lines": 2140, "dependents": 6 }
}
```

- `name`: what it's called in the code, or plain words for things that aren't code (people, the system).
- `job`: what it does, in the user's words. **At most two lines** (`\n`), about 30 characters each.
- `path`: from the repo root. **A trailing `/` means a folder**, otherwise it's a file. Where a part lives inside a file named after something else, give that file. Leave it out only for people and pure concepts (data entities, states).
- `color`: `blue` app / system · `green` data / screens · `violet` shared state / core · `yellow` logic · `orange` adapters / outside-facing · `red` health or risk · `grey` external or doc-only · `ink` people / screens (white).
- `shape: "ellipse"` for people and start states. `dashed: true` for things that exist only in the docs, or that are deleted or temporary.
- `icon` / `icons`: [Simple Icons](https://simpleicons.org) slugs (`stripe`, `supabase`, `postgresql`, `apple`…). Only for **external services and well-known platforms**, never for the project's own code.
- `pin`: the number of a crack (1-based, from `cracks`) that lives in this box.
- `tag`: components view boxes, and anything zoomable. `lines` comes from `wc -l`. `dependents` is the count of *other* files affected, from `codegraph impact <symbol> -j`; leave it out when CodeGraph isn't available. **Never guess it.** `risk` is computed unless you set it: high when the box has a pin, or ≥ 20 dependents, or ≥ 2000 lines; medium at ≥ 8 dependents or ≥ 500 lines; otherwise low. For something special, set `"text"` and `"risk"` yourself.

## Arrows

```json
{ "from": "r_recipes", "to": "s_cook", "label": "cook", "strong": false, "both": false, "dashed": false, "color": "orange" }
```

- `label`: a short verb or noun phrase, one or two lines. Arrows in the components view point **down**, from caller to callee.
- `strong`: the one or two arrows the view is about (e.g. Start / Finish).
- `both`: two-way traffic. `dashed`: planned, or not connected.
- Two arrows between the same pair of boxes are drawn side by side automatically.

## Traces and cracks

```json
"traces": [ { "label": "Cook a recipe", "view": "zoom-cook" }, { "label": "Upgrade to Plus" } ],
"cracks": [
  { "status": "confirmed", "title": "One database, no backups configured",
    "detail": "Every household's data lives in one Postgres instance with no backup job.",
    "evidence": "api/prisma/schema.prisma · deploy/compose.yml", "views": ["containers"] }
]
```

- `traces` are the actions worth following. `view` points at the zoom or trace that already draws one, which shows it as done.
- `cracks.status`: `confirmed` (you read the code that proves it) · `to verify` (likely, but needs a run or a test) · `by design` (a deliberate trade-off with a real cost) · `fixed` (only in the update that removes it).
- `evidence` is required: the `file:line` or files that show it. A crack with no evidence doesn't go in.
- `views`: view ids where its pin appears. The cracks frame is added automatically when the list isn't empty.

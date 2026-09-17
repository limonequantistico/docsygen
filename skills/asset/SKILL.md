---
name: asset
description: Make a product asset — an image, icon, illustration, marketing frame, App Store screenshot, or a ready-to-use prompt for one — grounded in the project's seed and design system, through whichever route works right now (built in code, pasted into a chat app you pay for, or an API key). Use only when the user explicitly asks for an asset or image for their product, or runs /asset.
---

You are making **one asset for this product**, or a small set of them, and putting it where the project keeps assets.

Stopping to open an image tool breaks the flow of building, and the image that comes back usually doesn't know what the product is. This skill has two advantages over that tool: it **already knows the project** (what it does, who it's for, its palette and type), and it **isn't tied to a provider**. The same brief can become SVG code, a prompt to paste into whatever chat app you have access to today, or an API call, and you pick the route each time.

**Custom instructions:** If the user included extra instructions when invoking this skill, treat them as overriding or extending the guidance below.

**Scope note — what belongs to other skills.** Full screens and UI prototypes → `/prototype`. The visual direction itself (palette, type, mood) → `/design-system`. This skill uses those decisions; it doesn't make them. If `.docs/design-system.md` doesn't exist, say once that assets will be more consistent after `/design-system`, then carry on with what the seed gives you.

---

## Step 1 — Load the context

Read, where they exist:

- `.docs/seed.md` — what the product is, who it's for, its tone
- `.docs/design-system.md` — named direction, palette hex values, type, radii, mood words
- `.docs/tech-stack.md` — the platform, which decides formats and sizes (iOS asset catalog, Android densities, web `srcset`, favicon set)
- `.docs/preview.md` — how to reach the running app, for screenshots
- Where the project keeps assets — the asset catalog, `public/`, `assets/` — **as a file listing only**, for naming and location

**Don't open images or past runs by default.** Each image you view costs around a thousand tokens or more, so looking through a folder of old candidates can cost tens of thousands before any work starts, and it rarely changes the result: the design system already carries the style. Look at past work only when the new asset has to **match** something, meaning the user says it belongs to a series or names an existing asset. Then read that run's `prompt.md` and `brief.md` (a few hundred tokens of text: the exact prompt, and the model and settings that worked) and view **only the final asset that was placed**, never the discarded candidates. To see what runs exist, list the folder names in `.docs/assets/imgs/generated/` without opening them.

## Step 2 — Pick the asset type

Ask in **one** `AskUserQuestion` (where it isn't available, a numbered list), unless the user already said what they want:

- **Image or illustration** — hero, onboarding art, empty state, texture, mascot
- **Icon** — app icon, logo mark, UI glyph set
- **Marketing** — marketing frame, App Store / Play Store screenshot, social or OG card
- **Prompt only** — a ready-to-use prompt; nothing gets generated here

"Other" covers the rest; take its description as the type.

**Text or ASCII art is also an asset.** A README header, a CLI banner, or `/help` output may want the asset as text, not as an image of text. When that's the ask, write it as text in a code block and check every row lines up in a monospace font. Say whether it's plain ASCII, which survives any terminal or font, or Unicode box and block characters, which look richer but need a modern font. Skip routes, generation, and export, and put it in the file where it belongs. Don't render it to SVG or PNG unless an image file is actually needed, like an avatar.

**Prompt only is a short path.** Pin the brief (Step 3) but skip the variants and target-resolution questions, keeping only the aspect ratio. Run the model check (Step 4) only if the user hasn't named the tool the prompt is for. Write the prompt (Step 5), show it in a fenced code block, and log it (Step 9). Skip the route question, generation, review, and export: nothing is generated, so there's nothing to place.

## Step 3 — Pin the brief

Fill in what the context already answers, and ask in **one** batch only for what's still missing:

- **Where it's used** — screen, store listing, landing page. This decides size and crop.
- **Subject and message** — what it shows, and what someone should feel or understand
- **Text on it** — exact copy, if any. Raster models still misspell text, so recommend adding text as a code layer on top of a generated background.
- **Variants** — how many candidates to generate (default 2), plus any dark and light versions
- **Target resolution** — the pixel size it's actually shown at

Take the resolution from the platform when a size is fixed. A few are: iOS app icon is one 1024×1024 opaque PNG with no rounded corners (the system masks it); App Store screenshots follow the device sizes App Store Connect currently requires, so check the current list, don't recall it; OG cards are 1200×630.

**When no size is fixed, ask.** Don't guess high. A 4K render dropped into a 200×200 avatar slot bloats the bundle and slows the page for nothing. Ask for the display size in points or CSS pixels, then work out the exports from the densities the platform needs (@1x/@2x/@3x on iOS, 1x/2x on the web). The largest export is the **target**. Generate at the smallest size the route offers that still covers it, and never ship anything bigger than the target. Routes differ in how big they go. In code there's no limit. Through `generate.py`, Gemini takes `--size 512px|1K|2K|4K`, while OpenAI tops out at 1536px on the long side. When a target is bigger than a route can deliver, count that against the route in Step 4 rather than finding out in Step 8.

**Open the run folder now, whatever the route:** `.docs/assets/imgs/generated/<YYYY-MM-DD>-<slug>/`, with a `brief.md` holding the brief and target resolution. Later steps add to it, and it's what a matching asset is built from later.

## Step 4 — Pick the route

The asset type decides which routes make sense:

| Route | What actually happens | Good for |
|---|---|---|
| **Build it in code** | The agent writes SVG or HTML, renders it, and exports PNGs. No image model involved. | Icons, logo marks, flat illustrations, marketing frames, store screenshots, OG cards |
| **Paste into a chat app** | The agent writes the prompt; you paste it into ChatGPT, Gemini, or any app you have access to, then drop the results into a folder. | Photographic or painterly images when you have a subscription but no API key |
| **API key** | `generate.py` calls the provider with a key you stored yourself. Costs per image. | Photographic or painterly images, fully automatic |

Ask every run. What's available changes from day to day, which is the point.

Work through it in this order:

1. **If the table says code suits this asset type**, recommend **Build it in code** and ask. If the user accepts, skip the model check and go to Step 6.
2. **Otherwise, or if they want an image model instead,** run the model check below first, because its answer can change the route: the best model for the job may only be reachable by pasting a prompt.
3. **Then ask for the route** from the remaining rows, with the recommendation the check produced.

**Where `generate.py` lives**, needed from here on: next to this `SKILL.md`, in the base directory the skill was loaded from (Claude Code prints it as "Base directory for this skill" when the skill loads). Run it with that absolute path, `python3 <base directory>/generate.py`. Don't assume an environment variable points there: `CLAUDE_PLUGIN_ROOT` isn't set in the agent's shell. If the base directory isn't shown, find it with `find ~/.claude/plugins ~/.codex -path '*/skills/asset/generate.py' 2>/dev/null` and use the newest version.

### Check which model is best right now

Image models turn over every few months, so which model to use is looked up on every run that needs one, never remembered.

1. **Rank by what this asset is.** Fetch the [arena.ai text-to-image leaderboard](https://arena.ai/leaderboard/text-to-image) and read the category that matches the asset, not just Overall: illustration → *Art* or *Cartoon, Anime & Fantasy*; photographic → *Photorealistic & Cinematic*; logo, product, or brand imagery → *Product, Branding & Commercial Design*; text in the image → *Text Rendering*; 3D → *3D Imaging & Modeling*.
2. **Add cost and reach.** Fetch the [Artificial Analysis text-to-image leaderboard](https://artificialanalysis.ai/image/leaderboard/text-to-image) for the price per image and whether the model has an API at all. A model with no API can only be used through the paste route.
3. **Filter to what the user can use.** Drop models whose route can't reach the target resolution. Mark each remaining model as reachable through a key that `generate.py check` reports ready or a subscription the user mentioned. The best model the user can't reach is still worth one line, since it may be worth getting a key for, but lead with what works today.
4. **Show a short table** of the top 3–5 for this category: model, rank in the category, price per image, and how to reach it. Include the date and the sources, and give one recommendation. Top-ranked isn't automatically the pick: a model a few points lower that costs a tenth as much, or that the user can already use, is often the better call.

If a leaderboard URL has moved, search for the current one. If there's no web access at all, say so plainly and recommend from what you already know, labelled as possibly out of date.

Keep the chosen model for the rest of the run. It's passed to `generate.py` with `--model` and recorded in `brief.md`.

## Step 5 — Write the prompt

Every route except code needs a prompt. The brief is the same whichever model receives it, but the phrasing isn't: check the chosen model's current prompting guide for syntax it expects (Midjourney parameters like `--ar`, for example, or how much detail a model rewards). Build it from the brief and the design system, in this order:

1. **Subject** — what's in the image, concretely
2. **Composition** — framing, camera or viewpoint, where the empty space goes (UI and copy will sit there)
3. **Style** — the design system's named direction and mood words, turned into visual language (medium, rendering, texture, lighting)
4. **Palette** — the actual hex values, dominant color first
5. **Constraints** — aspect ratio, transparent or opaque background, "no text" unless text is the point, and what to avoid

Save it in the run folder:

- `prompt.md` — **the prompt text and nothing else.** It's sent to the model word for word, so any heading or note in it ends up in the image prompt.
- `brief.md` — add the model, the route, and the leaderboard snapshot with its date.

**Show the prompt to the user before anything costs money.**

## Step 6 — Generate

**Build it in code.** Write the SVG or HTML with the design system's values, save the source in the run folder (it's the master, and every size is rendered from it), render it to PNG, and look at the render before showing it. Record the route in `brief.md`. Use a converter that's already there (`rsvg-convert`, or a headless browser such as the `chrome-devtools` MCP server for HTML). For store screenshots, capture the real running app through `.docs/preview.md` and compose frames and captions in HTML around it; don't redraw the UI. If nothing can render, say so and hand over the source file.

**Paste into a chat app.** Put the prompt in a fenced code block so it copies in one click, adapted to the tool the user named. Tell them to save the images they like into the run folder, then wait. When they're back, continue from Step 7.

**API key.** Run `generate.py` from the path worked out in Step 4.

1. Run `generate.py check`. It prints the key file's path, then for each provider either `ready` with where the key came from, or the missing variable **names** with where to get a key. It never prints values. If it says a key comes **from the shell environment**, tell the user: that key overrides the file, may bill a different account, and is visible to anything that can read the shell environment.
2. If the provider isn't ready, run `generate.py init`. It creates the key file with empty placeholders, readable only by the user. Then tell the user which variable to fill in, where to get the key (use the link `check` printed), and to **edit the file in their own editor**. Wait for them, then check again.
3. Run it: `generate.py run --provider <openai|gemini> --model <model id> --prompt-file <run folder>/prompt.md --out <run folder> --count <n> [--aspect W:H] [--size 1K] [--transparent]`. Pass the target's own aspect ratio: the script snaps it to the nearest one the provider accepts and prints a note, and Step 8 crops to the exact size. `--size` only works on Gemini; OpenAI prints a note and ignores it. Get the exact model id from the provider's current docs, since leaderboard names don't always match API ids. It prints the model used and the saved paths. If the best model's provider isn't one the script supports, use the paste route rather than extending the script mid-run, and mention that the provider could be added.

**Keys never pass through the agent.** No exceptions:

- Never open, `cat`, `grep`, `source`, or otherwise read the key file or print key variables. `generate.py` is the only thing that reads it.
- Never ask the user to paste a key into the chat, and if they do, tell them it's now in the transcript and they should rotate it.
- Never pass a key on a command line or write one anywhere else.
- The first time this route is used in a project, offer once to add a `Read` deny rule for the key file's directory to the user's Claude Code settings. Use the path `check` printed rather than assuming the default, since `DOCSYGEN_ASSETS_ENV` can move it. Say plainly that it blocks accidental reads, not a determined shell, so it's hygiene, not a guarantee.

## Step 7 — Review and pick

- **Look at every candidate yourself** before presenting it. Discard the ones that are obviously broken (garbled text, wrong palette, cropped subject) and say why.
- Present the rest and let the user pick. Taste is theirs. If none work, revise the prompt with what was wrong and generate again. After two rounds on the same asset, suggest a different route instead of a third round.

## Step 8 — Export, compress, and place

This step replaces the manual trip through a compressor like Squoosh. It uses the same codecs Squoosh does (pngquant, WebP, AVIF), run locally.

**1. Crop and resize.** Render code-built assets at each size straight from the source. For generated images, the model's output rarely has the target's exact proportions (OpenAI returns 3:2 for any wide request, and some models only do squares), so:

**`sips` edits files in place unless given `--out`**, which would destroy the pick you keep as the master. Every command below writes a new file, and the candidate itself is never touched.

- **Scale to cover, then crop.** Scale until both sides are at least the target size, then crop to the exact size. Aim the crop at the composition from Step 5, keeping the subject and the empty space UI will sit on:
  ```bash
  sips --resampleHeight <H> candidate-01.png --out work.png   # or --resampleWidth <W>, whichever covers
  sips -c <H> <W> work.png --out asset@3x.png                 # add --cropOffset <y> <x> if a centered crop cuts the subject
  ```
- **Never upscale.** If the output is smaller than the target, say so and regenerate at a larger size or with a different model. Don't stretch it.
- **Then export each density below the target from the largest export**, each to its own file: `sips -Z <px> asset@3x.png --out asset@2x.png`, and so on.

**2. Compress each export**, in the format the platform wants:

| Where it goes | What to do |
|---|---|
| **iOS app icon** | No compression. It **must have no alpha channel**, or App Store Connect rejects the upload, and generated PNGs, or any source with transparent areas, often carry one. Check with `sips -g hasAlpha`. If it says yes, flatten it onto the brand background: an SVG with a filled `<rect>` under an `<image href="icon.png">`, rendered with `rsvg-convert flat.svg -o AppIcon.png`. `rsvg-convert` writes RGB when every pixel is opaque. Check again. Don't round-trip through BMP, which keeps the alpha channel. |
| **iOS / macOS asset catalog** | No compression pass. Xcode decodes every PNG and re-encodes it into `Assets.car`, so lossy PNG savings mostly don't survive while the quality loss does. The real saving is exact @1x/@2x/@3x sizes. If the bundle is still too big, the lever is the image set's *Compression* setting in Xcode. Say that source-file sizes aren't what ships. |
| **Android** | Lossy WebP (`cwebp`) for in-app images. Exceptions: 9-patch files (`.9.png`), which WebP conversion breaks; launcher and adaptive icon layers, left as generated; and Play Store listing graphics, which Play requires as PNG or JPEG (the 512×512 store icon is a 32-bit PNG). |
| **Web, with a framework image pipeline** (Next.js `<Image>`, Astro `<Image>`, Nuxt Image…) | Only a light pass on the source. The pipeline creates the WebP and AVIF variants when the site builds or serves, so compressing hard here stacks losses. |
| **Web, plain `<img>`** | AVIF (`avifenc`) or WebP (`cwebp`), with a PNG or JPEG fallback if the project already serves one. Follow what the existing code does. |
| **SVG** | Optimize with `svgo` if the project already has it; otherwise leave it, since code-built SVGs are usually already lean. |

Starting settings that stay visually lossless on most images, always with an explicit output file:

```bash
pngquant --quality=70-90 --speed 1 --strip --skip-if-larger --force --output out.png -- in.png
cwebp -q 80 -m 6 in.png -o out.webp
avifenc -q 60 -s 4 in.png out.avif
```

`pngquant` exits **98** when the result would be larger and **99** when it can't reach the quality floor, and writes nothing in either case. Neither is an error: keep the uncompressed export rather than lowering the quality. Go gentler on flat illustrations with smooth gradients, where banding shows first.

Use only the tools that are already installed. If one that's needed is missing, name the install command (`brew install pngquant webp libavif`, for example), ask once, and if the user says no, skip that format rather than finding a workaround.

**3. Check it, then confirm.** Look at each compressed file yourself and compare it with the uncompressed export, watching for gradient banding, halos around edges, and color shift. Back off the quality where you see any. Then show the user a short table (file, size before, size after, format) and let them confirm. **This is the final confirmation:** nothing gets placed in the project until they say it looks right.

**4. Place.** Put the confirmed files where the project keeps assets, following existing names (an `.imageset` or `AppIcon.appiconset` in an Xcode asset catalog, density buckets on Android, `public/` or the framework's asset folder on the web). Reference them in code only when the user asked for that or the place is obvious (replacing a placeholder). Otherwise say where they are.

**5. Tidy the run folder.** Keep `prompt.md` (if the route had one), `brief.md`, and the master for any future re-export: the uncompressed pick, or the SVG/HTML source for code-built assets. Record the placed paths and the compression settings in `brief.md`. `.docs/` is usually committed, so offer to delete the discarded candidates instead of letting them grow the repo.

## Step 9 — Log

Append to `.docs/changelog.md` following `.docs/changelog-spec.md`: the asset, the route, and where it was placed. Never log a key or anything read from the key file.

---

**RULES:**

- Don't imitate trademarks, other companies' brand assets, or real people, and flag it if the brief asks for that.
- Say which route produced each asset. "Generated by gpt-image-2" and "built as SVG" carry different licensing and different editability.
- Confirm before every paid generation. A second round costs money too.
- Only make the assets that were asked for. Don't produce a full icon family when one icon was requested.

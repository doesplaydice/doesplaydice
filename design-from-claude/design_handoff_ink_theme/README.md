# Handoff: Does Play Dice — "Ink" theme

## Overview
A redesign of doesplaydice.com. Bold black-and-paper typographic site with one red accent, a light and a dark palette (two deliberate palettes, not an inversion), and a hero built from the name set in giant display type plus two tilted dice.

Target codebase: the existing **MkDocs Material** site in `wiki/` (see `wiki/mkdocs.yml`, `wiki/docs/assets/stylesheets/extra.v2.css`). The job is to implement this design as the Material theme for that site, not to replace MkDocs.

## About the design files
The `.dc.html` files in this bundle are **design references built in HTML**. They show the intended look and behavior. Do not ship them. Recreate them inside MkDocs Material: replace `extra.v2.css` with a new `extra.css` carrying these tokens and rules, restyle the Material chrome (header, tabs, nav, footer, search), and write the home page as `docs/index.md` with `md_in_html` blocks (as the current prototype already does). Rules content stays as-is in markdown; the theme styles it.

Copy on every page is taken verbatim from the repo (`docs/index.md`, `docs/rules/index.md`, `docs/downloads.md`). Do not rewrite it. The "Prototype for review" and "OPEN DECISION" blocks are review notes and are not part of the design; keep them working but they should not appear on the public site.

## Fidelity
**High-fidelity.** Colors, type, spacing and layout are final. Match them. The three pages cover: Home, Basic Rules (as the template for all content pages), Download (as the template for list/index pages). Pages not mocked (Narrators, Contribute, Character Vitae, Community, Plan) use the content-page template.

## Design tokens

### Palettes (CSS custom properties; set on `[data-md-color-scheme="slate"]` for dark and `[data-md-color-scheme="default"]` for light)

Dark (default):
- `--bg` #050505
- `--ink` #F4F2EC (text, buttons, borders on emphasis)
- `--muted` #9A978E (secondary text)
- `--line` #2A2926 (hairlines)
- `--accent` #E5484D (red: labels, numbers, links on hover, d20)
- `--die` #B42318 (die body), `--pip` #FFFFFF
- `--card` #0F0E0D (raised surface, rarely used)

Light:
- `--bg` #F4F2EC (warm paper)
- `--ink` #0A0A0A
- `--muted` #66645E
- `--line` #D9D5C9
- `--accent` #A11F16 (deeper red for contrast on paper)
- `--die` #B42318, `--pip` #FFFFFF
- `--card` #FBFAF6

Transition when switching: `background .35s, color .35s`.

Alternate accent (not default, keep as an option): amber `--accent` #FFB000 dark / #B86E00 light, `--die` #FFB000, `--pip` #050505.

### Type
Four families, all Open Font License, to be self-hosted in `docs/assets/fonts/` like the current Open Sans / IBM Plex Mono (replace those):
- **Archivo Black** 400 — display. Always uppercase, `letter-spacing:-.04em`, `line-height:.86–.95`.
- **Literata** 400/600, italic 400 — body prose on content pages and lede paragraphs.
- **Familjen Grotesk** 400/500/600/700 — UI: nav, buttons, labels, card titles, table cells.
- **JetBrains Mono** 400/500/700 — kickers, numbers, file names. Kicker style: 11–12px, `letter-spacing:.14–.16em`, uppercase.

Scale:
- Hero wordmark: `clamp(84px,14vw,168px)`, Archivo Black, three lines "DOES / PLAY / DICE".
- Page h1 (content pages): `clamp(56px,9vw,112px)`, Archivo Black, `line-height:.88`.
- Section h2 (display): `clamp(36px,4.5vw,52px)`, Archivo Black, uppercase, `line-height:.95`, `letter-spacing:-.03em`.
- Content h2 (in rules prose): 28px Familjen Grotesk 600, `letter-spacing:-.02em`; parenthetical suffix 400 in `--muted`.
- Lede: Literata, `clamp(20px,2.4vw,26px)`, `line-height:1.45`, max-width 640px.
- Prose: Literata 18px, `line-height:1.65`, max-width 680px.
- Body/UI: 15px, `line-height:1.5–1.55`. Nav 14px. Footer 13px.
- Card title 20–22px Familjen Grotesk 600.
- Dice numerals (d4…d20): Archivo Black 40px, `letter-spacing:-.03em`.

`text-wrap: pretty` on paragraphs, `balance` on headings.

### Spacing & layout
- Page container `max-width:1120px`, padding `28px 40px 48px`, `min-height:100vh`, flex column with footer pushed to bottom via `margin-top:auto`.
- Section rhythm: 112px between major sections on Home, 96px on Download, 56px between prose sections on Rules.
- Grid gaps 48px; card grids `repeat(auto-fit, minmax(230–280px, 1fr))` with `column-gap:48px`, cards have uniform `padding:28–32px 0` and `border-bottom:1px solid var(--line)`.
- Rules page: two columns `minmax(0,220px) minmax(0,1fr)`, gap 64px; left column is a sticky TOC (`top:32px`), 14px, muted.
- Radii: 0 on everything except the theme toggle pill (999px) and dice (roughly 21% of size: 24px on 112px, 16px on 76px).
- Shadows: dice only. Large die `0 28px 44px -20px rgba(0,0,0,.65)`, small die `0 18px 30px -16px rgba(0,0,0,.6)`.

### Rules/tables
Tables are not boxed: `border-top:2px solid var(--ink)`, header row in JetBrains Mono 11px uppercase muted, rows `padding:14px 0; border-bottom:1px solid var(--line)`. Columns by CSS grid (`1fr 2fr` for Skills; `1fr 1fr 1.6fr` for Difficulty). Die abbreviations in Archivo Black; `d20` in `--accent`.

## Screens

### Home (`Does Play Dice — Ink.dc.html` → `docs/index.md`)
1. **Nav**: left "DPD" in Archivo Black 14px `letter-spacing:.08em`; right links Rules · Narrators · Contribute · Download (14px, muted, `--ink` when active/hover→`--accent`), then the theme toggle: pill, `border:1px solid var(--line)`, 12px, a 12px circle in `--die` and the label "Dark"/"Light".
2. **Hero** (`margin-top:88px`, grid `1fr auto`, gap 32px): wordmark left; dice cluster right in a 180×190 box: large red die (112px, `rotate(12deg)`, five pips) at top-right, smaller ink-colored die (76px, `rotate(-17deg)`, three pips, pips in `--bg`) offset `right:104px; top:78px` behind-left.
3. Kicker (40px below, `--accent`): "Five dice. Fifteen minutes. A night out."
4. Lede (Literata): "A story-telling game that's free to download, quick to learn, and only limited by your imagination. It gives you the creative outlet of a role-playing game — without the learning curve, or the shelf of rulebooks."
5. Buttons (gap 14px, 15px 600): primary filled `background:var(--ink); color:var(--bg); padding:15px 24px` "Read the rules"; secondary `border:1px solid var(--line); padding:14px 24px` "Download and play". No radius.
6. **Dice ladder** (`border-top`, kicker muted "The Narrator rolls against you. Highest roll wins."): five boxes `repeat(auto-fit,minmax(150px,1fr))`, gap 12px, `border:1px solid var(--line); padding:22px 20px`: d4 Easy, d6 Moderate, d8 Challenging, d12 High difficulty, d20 "Impossible" (d20 box border and numeral in `--accent`).
7. **"The whole game fits on one page"**: two-column (`minmax(280px,1fr)` auto-fit, gap 48px), display h2 left, two Literata 18px paragraphs right (second in `--muted`). Copy verbatim from index.md.
8. **Four entry cards** (grid, `border-top`): each a link with mono number 01–04 in `--accent`, title 20px 600, 15px muted description, "Label →" 14px 600. Start here / Make a character / Run a game / Make it yours (copy from index.md cards).
9. **"What you need"**: display h2 left, Literata paragraph right.
10. **Footer**: 13px muted, space-between: license line (`Does Play Dice by Jeff Adams · text licensed CC BY 4.0 · the name and logo are excluded`, link in `--ink`) and "doesplaydice.com".

### Basic Rules (`Does Play Dice — Rules.dc.html` → content-page template)
- Header: kicker "The one page · complete", h1 "BASIC / RULES", 16px muted subline, two buttons (secondary "Download PDF", text-link "Print this page" in `--accent`), a 72px red die right. `border-bottom` + 40px padding.
- Body: sticky TOC left ("On this page" kicker + section links), prose right (Literata 18px, max 680px). Each numbered rule paragraph is prefixed by its number in JetBrains Mono 13px `--accent` with 10px right margin (01…11). Section h2s 28px Familjen Grotesk.
- "Winning the Game" gets the display treatment (Archivo Black `clamp(32px,4vw,44px)`) above a `border-top`; "#winning" in `--accent`.
- For MkDocs: map `.md-typeset h1` → display h1, `h2` → 28px grotesk, `p` → Literata 18px, tables → the rule-line style above, `.md-sidebar--secondary` → the sticky TOC style. The `**1.**`-style bold numbers in the markdown should render as the mono accent numbers (target `p > strong:first-child`).

### Download (`Does Play Dice — Download.dc.html` → list-page template)
- h1 "DOWNLOAD", Literata 20px muted lede.
- Four link cards in a grid (kicker PDF / PDF / PDF · EPUB / Git, 22px title, muted description, "Download →" pinned to bottom).
- "Convention kit": display h2 + Literata paragraph left; right a rule-line list (`border-top:2px solid var(--ink)`), each row grid `1fr auto`: bold title + muted description, filename in JetBrains Mono 12px muted.
- "How this works once it's live": h2 + muted Literata paragraph, bold phrase in `--ink`.

## Interactions & behavior
- **Theme toggle**: flips `data-theme` on `<body>` between `dark` and `light`, stores in `localStorage` (`dpd-ink-theme`), reads it on load before paint. In MkDocs, wire this to Material's own palette toggle (`data-md-color-scheme` slate/default) and restyle that control as the pill; drop the "follow system" third state or keep it, but the default with no preference is **dark**.
- Hover: links and nav items → `--accent`. Buttons: no hover change beyond cursor (add a 0.15s opacity .85 on primary if desired).
- Dice are static. No animation.
- Responsive: all grids are `auto-fit`; the hero wordmark scales with `clamp`; hero grid collapses to one column under ~600px (stack dice below the wordmark, left-aligned, scaled to 0.7).
- Print (rules page): hide nav, TOC, footer, toggle; force light palette; body 12pt Literata.

## State
Only the theme preference. No data fetching.

## Assets
- Fonts: Archivo Black, Literata (variable, opsz), Familjen Grotesk, JetBrains Mono. Download woff2 from Google Fonts (OFL) and self-host, replacing Open Sans and IBM Plex Mono in `fonts.css`.
- Dice: pure CSS (rounded square + 3×3 grid of circular pips). No image assets. The `material/dice-d20` logo icon in mkdocs.yml can stay or be replaced with the "DPD" wordmark.

## Files
- `Does Play Dice — Ink.dc.html` — Home
- `Does Play Dice — Rules.dc.html` — Basic Rules (content template)
- `Does Play Dice — Download.dc.html` — Download (list template)
- `ink-tokens.css` — the palettes and type stack as plain CSS, ready to paste into `extra.css`

Open each `.dc.html` in a browser to inspect exact styles; every style is inline on the element.

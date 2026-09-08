# Convention kit

Print-ready pieces for running Does Play Dice at a table with strangers.

Built for **black-and-white printing** &mdash; nothing depends on colour, because the realistic
scenario is a home printer or a copy shop the morning of the convention.

## The pieces

| File | What it is | Print on |
| --- | --- | --- |
| `table-tent.pdf` | The core mechanic, standing on the table. Fold once, both faces read upright | Card stock, single-sided |
| `pregens.pdf` | Six ready-to-play characters, cut apart | Card stock |
| `scenario-frame.pdf` | A Narrator's one-page planning sheet, blank | Plain paper, print a stack |
| `handout.pdf` | Ten business cards with a live QR to the site | Card stock or sticker sheet |
| `session-brief.pdf` | Narrator's playtest sheet: what tonight is testing, and what to record | Plain paper, one per session |
| `feedback-slips.pdf` | Eight player slips, three questions, ~30 seconds each | Plain paper |

## Build

```bash
./build.sh
```

Renders `src/*.html` to `dist/*.pdf` using headless Chrome. No LaTeX, no WeasyPrint, no system
libraries. If Chrome lives somewhere unusual, set `CHROME=/path/to/chrome`.

No Chrome? Open any file in `src/` in a browser and use **File &rarr; Print &rarr; Save as PDF**.
The screen-only instruction bars at the top of each page do not print.

## The playtest loop

`session-brief.pdf` and `feedback-slips.pdf` are the feedback half of the kit. Print a stack of
each and take them to every session.

The Narrator ticks **one** question the session exists to answer (five options, escalating from
"can a stranger start in 15 minutes" up to a timed 40-minute convention slot), runs the game,
then spends two minutes on the bottom half: time to first roll, rules questions asked, whether
they finished, whether they'd play again, and the one thing to cut.

Players get a slip at the end. Three questions, no phone.

**Paper on purpose.** It works at a library table tonight with zero setup, and nobody has to be
talked into scanning anything. The only rule that matters: **photograph the sheets before
leaving the table.** Paper that goes into a bag is not a feedback loop.

If volume ever makes reading paper the bottleneck, the same five fields go straight into a
Google Form and the QR block on the handout can point at it. Not before then.

## Editing

The sources are plain HTML and one stylesheet. `src/_kit.css` holds the shared print rules
(page size, dice chips, tables, cut and fold marks); each piece has its own layout inline.

**To change the six characters**, edit `src/pregens.html` &mdash; each is a self-contained
`<article class="card">` block, so copy, paste and rewrite.

**To regenerate the QR** after a URL change:

```bash
../.venv/bin/pip install qrcode
../.venv/bin/python -c "
import qrcode
qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, border=1)
qr.add_data('https://YOUR-URL-HERE'); qr.make(fit=True)
m = qr.get_matrix(); n = len(m); parts = []
for y, row in enumerate(m):
    x = 0
    while x < n:
        if row[x]:
            r = x
            while r < n and row[r]: r += 1
            parts.append('M%d %dh%dv1h-%dz' % (x, y, r-x, r-x)); x = r
        else: x += 1
open('src/qr.svg','w').write(
  '<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 %d %d\" shape-rendering=\"crispEdges\">'
  '<rect width=\"%d\" height=\"%d\" fill=\"#fff\"/><path d=\"%s\" fill=\"#000\"/></svg>'
  % (n, n, n, n, ''.join(parts)))
"
```

Then paste the contents of `src/qr.svg` into each `<div class="qr">` in `src/handout.html`.

## What is real and what is placeholder

**Real** &mdash; the table tent and the one-shot frame. Both are built entirely from the
published one-page rules: the three Skills, the five difficulty dice, the tie rule, and the
principle that every obstacle should have a way in for each Skill.

**Sample** &mdash; the six characters. Names and backgrounds are deliberately setting-neutral
placeholders, because the setting question (Timaeus? Prota? neither, at launch?) is still open.
Replace them.

The *structure* of the six is not a placeholder, and it's worth keeping. There are exactly six
ways to deal three different dice across three Skills, and the set uses all six. No two players
at the table are alike, and every approach to a problem has someone who is good at it. Swap the
trio and the six shapes still hold.

**Deliberately blank** &mdash; the scenario itself. That's authorship, and it's Jeff's.

## Still open

- The name on every piece assumes **Does Play Dice**. If the answer is Free Worlds, it's a
  find-and-replace across four files.
- There's no licence line on any piece yet, because the licence isn't chosen. Every piece has
  room in its footer for one.

#!/usr/bin/env python3
"""Generate the printable PDFs from the built site.

Two artefacts, and they are deliberately different things:

  does-play-dice-rules.pdf  The core rules on one sheet. This is the thing
                            people take home from a convention table, so it is
                            laid out for paper -- two columns, tight leading,
                            no navigation, no web furniture -- rather than
                            being a screenshot of the web page.

  does-play-dice-book.pdf   The game content as one document: rules and
                            character sheet. The Narrator section joins it once
                            it has content of its own.

  The character sheet and the player reference are one-page sheets of their
  own, built from markup in this file rather than from site pages.

Rendering is done by headless Chrome rather than a Python PDF library because
this design leans on CSS grid and self-hosted woff2 faces, and Chrome is the
same engine that renders the site -- so what ships on paper matches what people
saw on screen. WeasyPrint's grid support is partial and the layout drifts.

Usage:
    python3 tools/build_pdf.py [--site wiki/site] [--chrome /path/to/chrome]
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

# Where Chrome lives, in rough order of likelihood.
CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "google-chrome-stable",
    "google-chrome",
    "chromium-browser",
    "chromium",
]

# Pages that make up the book, in reading order.
BOOK_PAGES = [
    ("rules/index.html", "Basic Rules"),
    ("rules/taking-actions/index.html", "Taking turns"),
    ("rules/combat/index.html", "Combat, harm and recovery"),
    ("rules/training/index.html", "Skills and training"),
    ("rules/odds/index.html", "The odds"),
    ("rules/character-vitae/index.html", "Character Vitae"),
]

# Classes stripped from every page before printing. These are scaffolding for
# the website or notes to ourselves, not part of the game.
STRIP_CLASSES = [
    "dpd-protobar",     # "this page is a container" banners
    "dpd-status",       # the Complete / Not written pills
    "admonition tip",   # "type into it" help, which only means anything on screen
    "md-content__button",
    "headerlink",
    "dpd-timeline",
    "dpd-roller",       # an interactive widget means nothing on paper
    "dpd-sheet",        # the fill-in-the-browser sheet; the book prints the real one
]


def find_chrome(explicit=None):
    if explicit:
        return explicit
    for candidate in CHROME_CANDIDATES:
        if os.path.isfile(candidate):
            return candidate
        found = shutil.which(candidate)
        if found:
            return found
    sys.exit(
        "Could not find Chrome or Chromium.\n"
        "Pass --chrome /path/to/chrome, or install it:\n"
        "  ubuntu: sudo apt-get install -y chromium-browser\n"
        "  macos:  brew install --cask google-chrome"
    )


def strip_elements(markup, class_name):
    """Remove every element carrying `class_name`, including nested children.

    Regex cannot match balanced tags, so this walks forward from each opening
    tag counting depth. The input is machine-generated MkDocs output, so the
    markup is well-formed and this is safe; it would not be against the open
    web.
    """
    pattern = re.compile(
        r'<(?P<tag>\w+)(?P<attrs>[^>]*\bclass="[^"]*\b'
        + re.escape(class_name)
        + r'\b[^"]*"[^>]*)>'
    )
    while True:
        match = pattern.search(markup)
        if not match:
            return markup
        tag = match.group("tag")
        # Self-closing or void element: drop just the tag.
        if match.group("attrs").rstrip().endswith("/"):
            markup = markup[: match.start()] + markup[match.end():]
            continue
        depth, pos = 1, match.end()
        step = re.compile(r"</?%s\b" % re.escape(tag))
        while depth and pos < len(markup):
            nxt = step.search(markup, pos)
            if not nxt:
                break
            depth += -1 if nxt.group(0).startswith("</") else 1
            pos = markup.find(">", nxt.end())
            pos = len(markup) if pos == -1 else pos + 1
        markup = markup[: match.start()] + markup[pos:]


def article_of(path):
    """The page's content, cleaned of website furniture."""
    with open(path, encoding="utf-8") as handle:
        markup = handle.read()
    match = re.search(r"<article\b[^>]*>(.*?)</article>", markup, re.S)
    if not match:
        raise SystemExit("no <article> in %s -- did the theme change?" % path)
    body = match.group(1)
    for class_name in STRIP_CLASSES:
        body = strip_elements(body, class_name)
    # An <hr> immediately before a stripped decision block leaves a stray rule.
    body = re.sub(r"(?:\s*<hr\s*/?>)+\s*$", "", body.strip())
    return body


def shell(paths_css, title, body, page_css):
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>{title}</title>
{paths_css}
<style>{page_css}</style>
</head><body>{body}</body></html>"""


def render(chrome, html_path, pdf_path):
    subprocess.run(
        [
            chrome,
            "--headless",
            "--disable-gpu",
            "--no-sandbox",
            "--no-pdf-header-footer",
            # Give webfonts and layout time to settle before the snapshot.
            "--virtual-time-budget=15000",
            "--run-all-compositor-stages-before-draw",
            "--print-to-pdf=" + pdf_path,
            "file://" + html_path,
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
    )


# ---------------------------------------------------------------------------
# The one-sheet rules.
#
# Two columns on US Letter, because the launch is a Vermont convention. The
# type is small but the leading is generous -- this gets read at a noisy table
# under bad light, so air between lines matters more than size.
# ---------------------------------------------------------------------------
ONE_PAGER_CSS = """
@page { size: Letter; margin: 12mm 12mm 10mm; }
:root{
  --ink:#0A0A0A; --muted:#55534E; --line:#C9C5B9; --accent:#8C6900;
  --d4:#A14431; --d8:#346587; --d12:#436A48; --d20:var(--accent);
  --sans:"Familjen Grotesk",system-ui,sans-serif;
  --display:"Archivo Black",Impact,sans-serif;
  --mono:"JetBrains Mono",ui-monospace,monospace;
}
*{ box-sizing:border-box; }
body{
  margin:0; color:var(--ink); font-family:var(--sans);
  font-size:8.1pt; line-height:1.42; -webkit-print-color-adjust:exact;
  print-color-adjust:exact;
}

/* Masthead spans both columns; everything after it flows in two. */
.sheet-head{
  border-bottom:2px solid var(--ink); padding-bottom:6pt; margin-bottom:9pt;
  display:flex; align-items:baseline; justify-content:space-between; gap:12pt;
}
.sheet-title{ font-family:var(--display); font-size:23pt; line-height:.95; letter-spacing:-.01em; }
.sheet-sub{
  font-family:var(--mono); font-size:7pt; letter-spacing:.16em;
  text-transform:uppercase; color:var(--muted); text-align:right; line-height:1.5;
}

.sheet-body{ column-count:2; column-gap:9mm; column-fill:auto; }

h2{
  font-family:var(--mono); font-size:7.4pt; font-weight:700; letter-spacing:.15em;
  text-transform:uppercase; color:var(--accent);
  margin:9pt 0 3pt; padding-top:4pt; border-top:1px solid var(--line);
  break-after:avoid; break-inside:avoid;
}
h2:first-child{ margin-top:0; padding-top:0; border-top:0; }
p{ margin:0 0 4.5pt; orphans:2; widows:2; }
strong{ font-weight:700; }
em{ font-style:italic; }

/* The numbered steps carry the whole structure, so the numerals are the
   accent -- they let someone find "step 9" while talking. */
p > strong:first-child{ color:var(--accent); }

table{
  width:100%; border-collapse:collapse; margin:3pt 0 6pt;
  font-size:7.4pt; break-inside:avoid;
}
th{
  font-family:var(--mono); font-size:6.2pt; font-weight:500; letter-spacing:.12em;
  text-transform:uppercase; color:var(--muted); text-align:left;
  border-bottom:1px solid var(--ink); padding:2pt 5pt 2pt 0;
}
td{ border-bottom:.5px solid var(--line); padding:2.4pt 5pt 2.4pt 0; vertical-align:top; }
tr > *:last-child{ padding-right:0; }

hr{ display:none; }

.sheet-foot{
  column-span:all; margin-top:8pt; padding-top:5pt;
  border-top:1px solid var(--line);
  display:flex; justify-content:space-between; gap:12pt;
  font-family:var(--mono); font-size:6.4pt; letter-spacing:.1em;
  text-transform:uppercase; color:var(--muted);
}
"""

# ---------------------------------------------------------------------------
# The book. Single column, one chapter per page, running feet.
# ---------------------------------------------------------------------------
BOOK_CSS = """
@page {
  size: Letter; margin: 20mm 18mm 16mm;
  @bottom-center { content: counter(page); }
}
:root{
  --ink:#0A0A0A; --muted:#55534E; --line:#C9C5B9; --accent:#8C6900;
  --d4:#A14431; --d8:#346587; --d12:#436A48; --d20:var(--accent);
  --sans:"Familjen Grotesk",system-ui,sans-serif;
  --serif:"Literata",Georgia,serif;
  --display:"Archivo Black",Impact,sans-serif;
  --mono:"JetBrains Mono",ui-monospace,monospace;
}
*{ box-sizing:border-box; }
body{
  margin:0; color:var(--ink); font-family:var(--serif);
  font-size:10.5pt; line-height:1.55;
  -webkit-print-color-adjust:exact; print-color-adjust:exact;
}
.cover{
  /* Letter is 279.4mm tall; 20mm top and 16mm bottom margins leave a 243.4mm
     text block. 247mm here pushed the footer onto a blank second page. */
  height:238mm; display:flex; flex-direction:column; justify-content:space-between;
  break-after:page;
}
.cover-title{ font-family:var(--display); font-size:58pt; line-height:.92; margin-top:34mm; }
.cover-sub{
  font-family:var(--mono); font-size:9pt; letter-spacing:.2em; text-transform:uppercase;
  color:var(--accent); margin-top:10mm;
}
.cover-foot{ font-family:var(--mono); font-size:7.5pt; letter-spacing:.12em;
  text-transform:uppercase; color:var(--muted); line-height:1.9; }

.toc{ break-after:page; }
.toc h2{ font-family:var(--mono); font-size:8pt; letter-spacing:.18em;
  text-transform:uppercase; color:var(--muted); font-weight:500;
  border-bottom:1px solid var(--ink); padding-bottom:6pt; margin:0 0 14pt; }
.toc ol{ list-style:none; margin:0; padding:0; counter-reset:toc; }
.toc li{ counter-increment:toc; display:flex; align-items:baseline; gap:10pt;
  font-family:var(--sans); font-size:12pt; padding:9pt 0;
  border-bottom:.5px solid var(--line); }
.toc li::before{ content:counter(toc,decimal-leading-zero);
  font-family:var(--mono); font-size:9pt; color:var(--accent); }

.chapter{ break-before:page; }
.chapter:first-of-type{ break-before:avoid; }
h1{
  font-family:var(--display); font-size:26pt; line-height:1.02;
  margin:0 0 10pt; padding-bottom:7pt; border-bottom:2px solid var(--ink);
}
h2{
  font-family:var(--sans); font-size:12.5pt; font-weight:700;
  margin:16pt 0 4pt; break-after:avoid;
}
h3{ font-family:var(--sans); font-size:10.5pt; font-weight:700; margin:12pt 0 3pt; break-after:avoid; }
p{ margin:0 0 7pt; orphans:2; widows:2; }
ul,ol{ margin:0 0 8pt; padding-left:16pt; }
li{ margin:0 0 3pt; }
table{ width:100%; border-collapse:collapse; margin:8pt 0 12pt; font-family:var(--sans);
  font-size:9pt; break-inside:avoid; }
th{ font-family:var(--mono); font-size:7pt; font-weight:500; letter-spacing:.13em;
  text-transform:uppercase; color:var(--muted); text-align:left;
  border-bottom:1px solid var(--ink); padding:5pt 10pt 5pt 0; }
td{ border-bottom:.5px solid var(--line); padding:5pt 10pt 5pt 0; vertical-align:top; }
tr > *:last-child{ padding-right:0; }
code{ font-family:var(--mono); font-size:8.6pt; }
blockquote{ margin:8pt 0; padding-left:10pt; border-left:2px solid var(--accent);
  color:var(--muted); font-style:italic; }
hr{ border:0; border-top:1px solid var(--line); margin:12pt 0; }
img{ max-width:100%; }

/* The odds grid: win, tie and lose stacked in each cell, as on the site. */
.dpd-odds-grid td span{ display:block; line-height:1.3; }
.odds-w{ font-weight:700; }
.odds-t{ color:var(--accent); }
.odds-l{ color:var(--muted); }
.dpd-odds-key{ font-family:var(--sans); font-size:8.6pt; color:var(--muted); }
.dpd-odds-key span{ margin-right:6pt; }
.admonition{ border-left:2px solid var(--accent); padding:2pt 0 2pt 10pt; margin:8pt 0 10pt;
  break-inside:avoid; }
.admonition-title{ font-family:var(--mono); font-size:7pt; letter-spacing:.13em;
  text-transform:uppercase; color:var(--accent); margin:0 0 3pt; }

/* The odds grid keeps the site's dice colours: d4, d6, d8, d12, d20 in order,
   d6 in ink. */
.dpd-odds-grid tbody tr:nth-child(1) th,.dpd-odds-grid thead th:nth-child(2){ color:var(--d4); }
.dpd-odds-grid tbody tr:nth-child(3) th,.dpd-odds-grid thead th:nth-child(4){ color:var(--d8); }
.dpd-odds-grid tbody tr:nth-child(4) th,.dpd-odds-grid thead th:nth-child(5){ color:var(--d12); }
.dpd-odds-grid tbody tr:nth-child(5) th,.dpd-odds-grid thead th:nth-child(6){ color:var(--d20); }
"""


# ---------------------------------------------------------------------------
# The character sheet.
#
# The site page told people to print it from their browser, which is why it
# "wasn't printing": a documentation page rendered through a browser's print
# dialogue is not a character sheet, it is a documentation page with the
# navigation hidden. This is a purpose-built sheet -- one side of one page,
# fields big enough to actually write in with a pencil at a table, and the
# difficulty ladder printed on it so a new player never has to look anything up
# mid-game.
# ---------------------------------------------------------------------------
SHEET_CSS = """
@page { size: Letter; margin: 13mm 14mm 11mm; }
:root{
  --ink:#0A0A0A; --muted:#55534E; --line:#B8B4A8; --accent:#8C6900;
  --d4:#A14431; --d8:#346587; --d12:#436A48; --d20:var(--accent);
  --sans:"Familjen Grotesk",system-ui,sans-serif;
  --display:"Archivo Black",Impact,sans-serif;
  --mono:"JetBrains Mono",ui-monospace,monospace;
}
*{ box-sizing:border-box; }
body{
  margin:0; color:var(--ink); font-family:var(--sans); font-size:9.5pt;
  -webkit-print-color-adjust:exact; print-color-adjust:exact;
}
.head{
  display:flex; align-items:flex-end; justify-content:space-between; gap:14pt;
  border-bottom:2px solid var(--ink); padding-bottom:6pt; margin-bottom:11pt;
}
.title{ font-family:var(--display); font-size:21pt; line-height:.95; }
.sub{
  font-family:var(--mono); font-size:6.6pt; letter-spacing:.15em;
  text-transform:uppercase; color:var(--muted); text-align:right; line-height:1.6;
}
.lbl{
  font-family:var(--mono); font-size:6.6pt; letter-spacing:.14em;
  text-transform:uppercase; color:var(--accent); display:block; margin-bottom:2pt;
}
.lbl span{ color:var(--muted); letter-spacing:.06em; text-transform:none; }
/* A ruled line with real room above it: people write with a pencil, and a 6mm
   field is a field you cannot use. */
.rule{ border-bottom:.75pt solid var(--line); height:9.5mm; }
.rule.short{ height:8mm; }
.row{ display:flex; gap:12pt; }
.row > *{ flex:1; }
.block{ margin-bottom:8pt; }

table{ width:100%; border-collapse:collapse; margin:2pt 0 0; }
th{
  font-family:var(--mono); font-size:6.2pt; font-weight:500; letter-spacing:.13em;
  text-transform:uppercase; color:var(--muted); text-align:left;
  border-bottom:1pt solid var(--ink); padding:3pt 6pt 3pt 0;
}
td{ border-bottom:.5pt solid var(--line); padding:6.5pt 6pt 6.5pt 0; vertical-align:middle; }
td b{ font-size:10pt; }
td .hint{ color:var(--muted); font-size:8.4pt; }
.die{ width:18mm; text-align:center; font-family:var(--mono); font-size:12pt; color:var(--line); }
/* Floor: the lowest you can roll on that stat, from training. A small box,
   blank until training puts a number in it. */
.fl{ width:15mm; }
.fl span{ display:block; width:9mm; height:6.5mm; margin:0 auto;
  border:.75pt solid var(--line); border-radius:1pt; }
.train{ margin-top:9pt; }

.two{ display:grid; grid-template-columns:1fr 62mm; gap:14pt; align-items:start; }
/* Skills: what training has bought, beside the stats it builds on. */
.skl .rule.short{ height:7.6mm; }
/* Stamina: twenty boxes a stat, with the five dice marked where each one
   ends, so "cross out the boxes past your die" needs no arithmetic. */
.stam{ margin-top:11pt; }
.st-row{ display:flex; align-items:center; gap:8pt; margin-top:2.6pt; }
.st-row > b{ width:15mm; font-size:9.5pt; }
.bx{ display:grid; grid-template-columns:repeat(20, 6.3mm); column-gap:1.3mm; }
.bx i{ height:6.3mm; border:.75pt solid var(--line); border-radius:1pt; }
.bx i:nth-child(4){ border:1.3pt solid var(--d4); }
.bx i:nth-child(6){ border:1.3pt solid var(--ink); }
.bx i:nth-child(8){ border:1.3pt solid var(--d8); }
.bx i:nth-child(12){ border:1.3pt solid var(--d12); }
.bx i:nth-child(20){ border:1.3pt solid var(--d20); }
.st-hdr{ margin-top:4pt; }
.st-hdr em{ font-style:normal; font-family:var(--mono); font-size:6.4pt; font-weight:700;
  text-align:right; line-height:1; }
.st-hdr .m4{ color:var(--d4); } .st-hdr .m6{ color:var(--ink); } .st-hdr .m8{ color:var(--d8); }
.st-hdr .m12{ color:var(--d12); } .st-hdr .m20{ color:var(--d20); }
.foot{
  margin-top:9pt; padding-top:5pt; border-top:.75pt solid var(--line);
  display:flex; justify-content:space-between; gap:12pt;
  font-family:var(--mono); font-size:6pt; letter-spacing:.1em;
  text-transform:uppercase; color:var(--muted);
}
.stam ~ .foot{ margin-top:16pt; }
"""


def build_one_pager(site, chrome, out_dir):
    """The core rules on a single sheet."""
    body = article_of(os.path.join(site, "rules", "index.html"))
    # The h1 is replaced by the masthead, so drop it from the flow.
    body = re.sub(r"<h1\b.*?</h1>", "", body, count=1, flags=re.S)

    page = shell(
        '<link rel="stylesheet" href="assets/stylesheets/fonts.css">',
        "Does Play Dice -- the core rules",
        f"""
<div class="sheet-head">
  <div class="sheet-title">DOES<br>PLAY DICE</div>
  <div class="sheet-sub">The core rules<br>doesplaydice.com</div>
</div>
<div class="sheet-body">{body}
<div class="sheet-foot">
  <span>Does Play Dice by Jeff Adams</span>
  <span>Text licensed CC BY 4.0 &middot; name and logo excluded</span>
</div>
</div>""",
        ONE_PAGER_CSS,
    )
    return _render_in_site(site, chrome, page, out_dir, "does-play-dice-rules.pdf")



def build_character_sheet(site, chrome, out_dir):
    """A sheet someone can actually fill in at a table."""
    page = shell(
        '<link rel="stylesheet" href="assets/stylesheets/fonts.css">',
        "Does Play Dice -- character vitae",
        """
<div class="head">
  <div class="title">CHARACTER<br>VITAE</div>
  <div class="sub">Does Play Dice<br>doesplaydice.com</div>
</div>

<div class="row block">
  <div><span class="lbl">Character name</span><div class="rule"></div></div>
  <div><span class="lbl">Played by</span><div class="rule"></div></div>
</div>

<div class="block">
  <span class="lbl">Background <span>&mdash; where you're from, your place in the world</span></span>
  <div class="rule"></div><div class="rule"></div>
</div>

<div class="row block">
  <div><span class="lbl">School or job</span><div class="rule"></div></div>
  <div><span class="lbl">Connections <span>&mdash; who you know in the Party</span></span><div class="rule"></div></div>
</div>

<div class="block">
  <span class="lbl">Habits and quirks <span>&mdash; anything that makes you you</span></span>
  <div class="rule"></div><div class="rule"></div>
</div>

<div class="two">
  <div>
    <span class="lbl">Your three stats <span>&mdash; write in the die your Narrator gave you</span></span>
    <table>
      <tr><th>Stat</th><th>What it covers</th><th style="text-align:center">Die</th><th style="text-align:center">Floor</th></tr>
      <tr><td><b>Body</b><br>Physical</td><td class="hint">Strength, senses, fine motor skills, endurance</td><td class="die">d&nbsp;&nbsp;&nbsp;</td><td class="fl"><span></span></td></tr>
      <tr><td><b>Mind</b><br>Mental</td><td class="hint">Knowledge, memory, reasoning, aptitude</td><td class="die">d&nbsp;&nbsp;&nbsp;</td><td class="fl"><span></span></td></tr>
      <tr><td><b>Soul</b><br>Spiritual</td><td class="hint">Connection: intuition, empathy, persuasion, deception, nature</td><td class="die">d&nbsp;&nbsp;&nbsp;</td><td class="fl"><span></span></td></tr>
    </table>
    <div class="train">
      <span class="lbl">Training points <span>&mdash; to spend when the story gives you a chance to train</span></span>
      <div class="rule short"></div>
    </div>
  </div>
  <div class="skl">
    <span class="lbl">Skills <span>&mdash; what you've trained in</span></span>
    <div class="rule short"></div><div class="rule short"></div><div class="rule short"></div>
    <div class="rule short"></div><div class="rule short"></div><div class="rule short"></div>
  </div>
</div>

<div class="block stam">
  <span class="lbl">Stamina <span>&mdash; one box per side of the stat's die. Cross out the rest; tick one off for each point you lose</span></span>
  <div class="st-row st-hdr"><b></b><div class="bx"><em></em><em></em><em></em><em class="m4">d4</em><em></em><em class="m6">d6</em><em></em><em class="m8">d8</em><em></em><em></em><em></em><em class="m12">d12</em><em></em><em></em><em></em><em></em><em></em><em></em><em></em><em class="m20">d20</em></div></div>
  <div class="st-row"><b>Body</b><div class="bx"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div></div>
  <div class="st-row"><b>Mind</b><div class="bx"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div></div>
  <div class="st-row"><b>Soul</b><div class="bx"><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i><i></i></div></div>
</div>

<div class="block" style="margin-top:9pt">
  <span class="lbl">Notes <span>&mdash; what happened, what you're carrying, what you owe, what's left a mark</span></span>
  <div class="rule short"></div><div class="rule short"></div>
  <div class="rule short"></div><div class="rule short"></div>
</div>

<div class="foot">
  <span>Does Play Dice by Jeff Adams</span>
  <span>Text licensed CC BY 4.0 &middot; name and logo excluded</span>
</div>""",
        SHEET_CSS,
    )
    return _render_in_site(site, chrome, page, out_dir,
                           "does-play-dice-character-sheet.pdf")


# ---------------------------------------------------------------------------
# The player reference.
#
# Everything a player needs at the table on one side of one page, as lists,
# tables, arrows and small drawings rather than prose. The Basic Rules page
# teaches the game; this is what you glance at mid-scene. The dice glyphs are
# the masthead's, so the sheet and the site draw the same five shapes.
# ---------------------------------------------------------------------------
REFERENCE_CSS = """
@page { size: Letter; margin: 11mm 12mm 9mm; }
:root{
  --ink:#0A0A0A; --muted:#55534E; --line:#C9C5B9; --soft:#F3EFE4;
  --accent:#8C6900; --accent-ui:#B08400;
  --d4:#A14431; --d6:#0A0A0A; --d8:#346587; --d12:#436A48; --d20:#B08400;
  --sans:"Familjen Grotesk",system-ui,sans-serif;
  --display:"Archivo Black",Impact,sans-serif;
  --mono:"JetBrains Mono",ui-monospace,monospace;
}
*{ box-sizing:border-box; }
body{
  margin:0; color:var(--ink); font-family:var(--sans); font-size:8.6pt; line-height:1.36;
  -webkit-print-color-adjust:exact; print-color-adjust:exact;
  zoom:1.06;
}
b{ font-weight:700; }
.head{
  display:flex; align-items:flex-end; justify-content:space-between; gap:14pt;
  border-bottom:2px solid var(--ink); padding-bottom:5pt; margin-bottom:7pt;
}
.title{ font-family:var(--display); font-size:21pt; line-height:.95; }
.sub{
  font-family:var(--mono); font-size:6.6pt; letter-spacing:.15em;
  text-transform:uppercase; color:var(--muted); text-align:right; line-height:1.6;
}
h2{
  font-family:var(--mono); font-size:6.8pt; font-weight:700; letter-spacing:.15em;
  text-transform:uppercase; color:var(--accent); margin:0 0 5pt;
}
.box{ border-top:1px solid var(--ink); padding-top:5pt; margin-bottom:8pt; }
.head + .box{ border-top:0; padding-top:0; }
.cols{ display:grid; grid-template-columns:1fr 1fr; gap:14pt; }
.note{ margin:5pt 0 0; font-size:7.6pt; color:var(--muted); }
.note b{ color:var(--ink); }

/* Icons: outlines in ink, one filled shape in gold. */
.ico{ fill:none; stroke:var(--ink); stroke-width:2.2; stroke-linejoin:round; }
.ico-l{ fill:none; stroke:var(--ink); stroke-width:2.2; stroke-linecap:round; stroke-linejoin:round; }
.ico-f{ fill:var(--accent-ui); stroke:var(--accent-ui); stroke-width:2.2; }
svg.i{ width:22pt; height:22pt; display:block; margin-bottom:3pt; }
svg.i-s{ width:13pt; height:13pt; flex:none; }

/* The roll: four steps with arrows between. */
.flow{ display:flex; align-items:stretch; gap:4pt; }
.step{ flex:1; background:var(--soft); border-radius:4pt; padding:6pt 7pt; }
.step b{ display:block; font-size:9.6pt; margin-bottom:1pt; }
.step span{ display:block; font-size:7.8pt; color:var(--muted); }
.step em{ font-style:normal; font-weight:700; color:var(--accent); }
.arrow{ align-self:center; font-size:14pt; color:var(--accent-ui); }

/* stats */
table{ width:100%; border-collapse:collapse; }
td{ border-bottom:.5pt solid var(--line); padding:3pt 5pt 3pt 0; vertical-align:top; }
tr:last-child td{ border-bottom:0; }
.skills td:first-child{ width:19mm; }
.skills b{ display:block; font-size:9.4pt; }
.skills i{ font-style:normal; font-family:var(--mono); font-size:6.3pt; letter-spacing:.08em;
  text-transform:uppercase; color:var(--muted); }
.skills td:last-child{ font-size:8pt; }

/* The dice ladder */
.ladder{ display:flex; justify-content:space-between; gap:3pt; }
.rung{ flex:1; text-align:center; }
.rung svg{ width:22pt; height:22pt; display:block; margin:0 auto 2pt; }
.rung b{ display:block; font-family:var(--mono); font-size:9pt; }
.rung span{ display:block; font-size:7.2pt; color:var(--muted); line-height:1.2; }
.die-o{ fill:none; stroke:currentColor; stroke-width:2.6; stroke-linejoin:round; }
.die-c{ fill:none; stroke:currentColor; stroke-width:1.4; stroke-linejoin:round; stroke-linecap:round; }
.die-p{ fill:currentColor; }
.r4{ color:var(--d4); } .r6{ color:var(--d6); } .r8{ color:var(--d8); }
.r12{ color:var(--d12); } .r20{ color:var(--d20); }
.rung span{ color:var(--muted); }

/* Your turn */
.pips{ display:flex; align-items:center; gap:4pt; margin-bottom:4pt; font-size:8.4pt; }
.pips span{ width:10pt; height:10pt; border-radius:50%; background:var(--accent-ui); }
.pips b{ margin-left:3pt; font-size:9.6pt; }
ul.ar{ list-style:none; margin:0; padding:0; }
ul.ar li{ position:relative; padding:2.2pt 0 2.2pt 11pt; border-bottom:.5pt solid var(--line); }
ul.ar li:last-child{ border-bottom:0; }
ul.ar li::before{ content:"\\2192"; position:absolute; left:0; color:var(--accent-ui); font-weight:700; }
ul.ar li.hold{ display:flex; gap:4pt; align-items:center; padding-left:0; }
ul.ar li.hold::before{ content:none; }

/* Try again: a two-way fork */
.fork .q{ font-weight:700; font-size:9pt; margin-bottom:4pt; }
.paths{ display:grid; grid-template-columns:1fr 1.35fr; gap:5pt; }
.path{ background:var(--soft); border-radius:4pt; padding:5pt 6pt; font-size:8pt; }
.path em{ font-style:normal; font-weight:700; color:var(--accent); }
.path.push{ border-left:2.5pt solid var(--accent-ui); }
.crit{ margin-top:5pt; font-size:8pt; padding:4pt 6pt; border:1pt dashed var(--d4); border-radius:4pt; }
.crit b:first-child{ color:var(--d4); }

/* Fighting */
.fight{ display:grid; grid-template-columns:1fr 1fr; gap:14pt; align-items:start; }
.out td.k{ width:17mm; font-weight:700; white-space:nowrap; }
.out td{ font-size:8.2pt; }
.sd-title{ font-weight:700; font-size:8.6pt; margin-bottom:4pt; }
.sd-row{ display:flex; align-items:center; gap:4pt; margin-bottom:3pt; color:var(--accent-ui); font-weight:700; }
.sd-lbl{ width:27mm; color:var(--ink); font-weight:400; font-size:8pt; }
.sd{ font-family:var(--mono); font-size:8.4pt; border:1.2pt solid currentColor; border-radius:3pt; padding:0 4pt; }

/* Stamina and recovery */
.outs{ margin-top:4pt; }
.outs td{ font-size:7.9pt; padding:2pt 5pt 2pt 0; }
.outs td:first-child{ width:12mm; }
.rec td{ font-size:8pt; }
.rec td:first-child{ width:34mm; font-weight:700; }
.rec td.n{ width:9mm; font-family:var(--mono); font-weight:700; color:var(--accent); }

.foot{
  margin-top:2pt; padding-top:5pt; border-top:.75pt solid var(--line);
  display:flex; justify-content:space-between; gap:12pt;
  font-family:var(--mono); font-size:6pt; letter-spacing:.1em;
  text-transform:uppercase; color:var(--muted);
}
"""

REFERENCE_BODY = """
<svg width="0" height="0" style="position:absolute">
  <defs>
    <symbol id="d4" viewBox="0 0 40 40"><polygon points="20,4 3,35 37,35" class="die-o"/><path d="M20,4V35" class="die-c"/></symbol>
    <symbol id="d6" viewBox="0 0 40 40"><rect x="6" y="6" width="28" height="28" class="die-o"/><circle cx="20" cy="20" r="3" class="die-p"/></symbol>
    <symbol id="d8" viewBox="0 0 40 40"><polygon points="20,2 6,20 20,38 34,20" class="die-o"/><path d="M6,20H34" class="die-c"/></symbol>
    <symbol id="d12" viewBox="0 0 40 40"><polygon points="20,3 3,15.5 9.5,35.5 30.5,35.5 37,15.5" class="die-o"/><polygon points="20,12 11.5,18.2 14.7,28.2 25.3,28.2 28.5,18.2" class="die-c"/><path d="M20,12V3M11.5,18.2L3,15.5M14.7,28.2L9.5,35.5M25.3,28.2L30.5,35.5M28.5,18.2L37,15.5" class="die-c"/></symbol>
    <symbol id="d20" viewBox="0 0 40 40"><polygon points="20,2 4.4,11 4.4,29 20,38 35.6,29 35.6,11" class="die-o"/><polygon points="20,10 11,26 29,26" class="die-c"/><path d="M20,10V2M20,10L4.4,11M20,10L35.6,11M11,26L4.4,11M11,26L4.4,29M11,26L20,38M29,26L20,38M29,26L35.6,29M29,26L35.6,11" class="die-c"/></symbol>
    <symbol id="talk" viewBox="0 0 40 40"><path d="M6,8h28a3,3 0 0 1 3,3v15a3,3 0 0 1-3,3H17l-8,7v-7H6a3,3 0 0 1-3-3V11a3,3 0 0 1 3-3z" class="ico"/><path d="M11,16h18M11,21h12" class="ico-l"/></symbol>
    <symbol id="pick" viewBox="0 0 40 40"><circle cx="12" cy="13" r="6" class="ico"/><circle cx="28" cy="13" r="6" class="ico"/><circle cx="20" cy="28" r="6" class="ico-f"/></symbol>
    <symbol id="vs" viewBox="0 0 40 40"><rect x="3" y="11" width="15" height="15" class="ico" transform="rotate(-10 10.5 18.5)"/><polygon points="29,8 21,22 29,32 37,22" class="ico"/></symbol>
    <symbol id="win" viewBox="0 0 40 40"><path d="M12,6h16v8a8,8 0 0 1-16,0z" class="ico"/><path d="M12,9H6v3a6,6 0 0 0 6,6M28,9h6v3a6,6 0 0 1-6,6M20,22v7M13,34h14M15,29h10v5H15z" class="ico-l"/></symbol>
    <symbol id="hand" viewBox="0 0 40 40"><path d="M13,36c-4-3-8-9-9-13c-.6-2 1.6-3.2 3-1.8l4,4.2V9a2.2,2.2 0 0 1 4.4,0v10V5.5a2.2,2.2 0 0 1 4.4,0V19V7a2.2,2.2 0 0 1 4.4,0v12v-8.5a2.2,2.2 0 0 1 4.4,0V24c0,6-3,10-6,12z" class="ico"/></symbol>
  </defs>
</svg>

<div class="head">
  <div class="title">PLAYER<br>REFERENCE</div>
  <div class="sub">Does Play Dice<br>doesplaydice.com</div>
</div>

<section class="box">
  <h2>The roll</h2>
  <div class="flow">
    <div class="step"><svg class="i"><use href="#talk"/></svg><b>Say what you do</b><span>Easy things just happen. Hard things get a roll.</span></div>
    <div class="arrow">&rarr;</div>
    <div class="step"><svg class="i"><use href="#pick"/></svg><b>Pick a stat</b><span>Body, Mind or Soul: whichever fits how you try it.</span></div>
    <div class="arrow">&rarr;</div>
    <div class="step"><svg class="i"><use href="#vs"/></svg><b>Both roll</b><span>Your stat die against the Narrator's die.</span></div>
    <div class="arrow">&rarr;</div>
    <div class="step"><svg class="i"><use href="#win"/></svg><b>Highest wins</b><span><em>Tie:</em> both sides get something.</span></div>
  </div>
</section>

<div class="cols">
  <section class="box">
    <h2>Your three stats</h2>
    <table class="skills">
      <tr><td><b>Body</b><i>Physical</i></td><td>Strength, senses, fine motor skills, endurance</td></tr>
      <tr><td><b>Mind</b><i>Mental</i></td><td>Knowledge, memory, reasoning, aptitude</td></tr>
      <tr><td><b>Soul</b><i>Spiritual</i></td><td>Connection: intuition, empathy, persuasion, deception, nature</td></tr>
    </table>
    <p class="note">One die on each, from the three your Narrator hands out. Bigger is better.</p>
  </section>

  <section class="box">
    <h2>How hard is it?</h2>
    <div class="ladder">
      <div class="rung r4"><svg><use href="#d4"/></svg><b>d4</b><span>Easy</span></div>
      <div class="rung r6"><svg><use href="#d6"/></svg><b>d6</b><span>Moderate</span></div>
      <div class="rung r8"><svg><use href="#d8"/></svg><b>d8</b><span>Challenging</span></div>
      <div class="rung r12"><svg><use href="#d12"/></svg><b>d12</b><span>High</span></div>
      <div class="rung r20"><svg><use href="#d20"/></svg><b>d20</b><span>&ldquo;Impossible&rdquo;</span></div>
    </div>
    <p class="note">The Narrator picks the die. Against another character, they roll their stat instead.</p>
  </section>
</div>

<div class="cols">
  <section class="box">
    <h2>Your turn</h2>
    <div class="pips"><span></span><span></span><span></span><b>3 actions</b> every turn</div>
    <ul class="ar">
      <li><b>Who goes first?</b> Whoever started it. Everyone else rolls <b>Soul</b>; highest next.</li>
      <li><b>Free:</b> talking, noticing the obvious, dropping something.</li>
      <li><b>Bigger jobs</b> can cost 2 or 3 actions. The Narrator will say.</li>
      <li class="hold"><svg class="i-s"><use href="#hand"/></svg><span><b>Hold an action</b> to react after someone else's turn.</span></li>
      <li><b>New round:</b> everyone's actions refresh.</li>
    </ul>
  </section>

  <section class="box">
    <h2>Missed? Try again</h2>
    <div class="fork">
      <div class="q">Could you normally just try again?</div>
      <div class="paths">
        <div class="path"><b>Yes</b> &rarr; spend another action and roll again.</div>
        <div class="path push"><b>No</b> &rarr; <b>push your luck:</b> 1 action <em>+ 1 stamina</em> in that stat. Same check, same die.</div>
      </div>
      <div class="crit"><b>Fail a push</b> &rarr; <b>critical failure.</b> Worse than a miss, often double the effect. The Narrator decides.</div>
    </div>
  </section>
</div>

<section class="box">
  <h2>Fighting</h2>
  <div class="fight">
    <table class="out">
      <tr><td class="k">You win</td><td>&rarr; they lose <b>1 stamina</b> in the stat they used</td></tr>
      <tr><td class="k">They win</td><td>&rarr; <b>you</b> lose 1, even on your own turn</td></tr>
      <tr><td class="k">Tie</td><td>&rarr; both land</td></tr>
      <tr><td class="k">Hard hit</td><td>Win by more than their die has sides &rarr; <b>2 stamina</b></td></tr>
    </table>
    <div class="step-down">
      <div class="sd-title">Each one after the first steps down a die</div>
      <div class="sd-row"><span class="sd-lbl">Attacks, your turn</span><span class="sd r12">d12</span>&rarr;<span class="sd r8">d8</span>&rarr;<span class="sd r6">d6</span></div>
      <div class="sd-row"><span class="sd-lbl">Defences, per round</span><span class="sd r12">d12</span>&rarr;<span class="sd r8">d8</span>&rarr;<span class="sd r6">d6</span>&rarr;<span class="sd r4">d4</span></div>
      <p class="note">Never below d4. <b>Defending is free</b>: no action. Counts reset each round. <b>You can always leave:</b> say so and go.</p>
    </div>
  </div>
</section>

<div class="cols">
  <section class="box">
    <h2>Stamina</h2>
    <ul class="ar">
      <li>One track per stat, starting at the <b>sides on its die</b>: a d8 Body has 8.</li>
      <li>Losing it <b>never changes your rolls.</b></li>
      <li><b>0 in any stat &rarr; you're out.</b> Out isn't dead.</li>
    </ul>
    <table class="outs">
      <tr><td><b>Body</b></td><td>unconscious, winded, can't stand</td></tr>
      <tr><td><b>Mind</b></td><td>overwhelmed, can't hold a thought</td></tr>
      <tr><td><b>Soul</b></td><td>broken, can't face the room</td></tr>
    </table>
  </section>

  <section class="box">
    <h2>Getting it back</h2>
    <table class="rec">
      <tr><td>A full round of rest</td><td class="n">+1</td><td>any stat, only while it's <b>below half</b></td></tr>
      <tr><td>A night, with food and shelter</td><td class="n">All</td><td>Body, Mind and Soul</td></tr>
      <tr><td>Care, with tools or training</td><td class="n">+1</td><td>any stat: a healing kit, a counsellor, a spell</td></tr>
    </table>
    <p class="note"><b>Stamina isn't healing.</b> Broken bones, disease and serious wounds mend in the story, in their own time.</p>
  </section>
</div>

<div class="foot">
  <span>Does Play Dice by Jeff Adams</span>
  <span>Text licensed CC BY 4.0 &middot; name and logo excluded</span>
</div>
"""


def build_reference(site, chrome, out_dir):
    """The rules a player needs at the table, on one page."""
    page = shell(
        '<link rel="stylesheet" href="assets/stylesheets/fonts.css">',
        "Does Play Dice -- player reference",
        REFERENCE_BODY,
        REFERENCE_CSS,
    )
    return _render_in_site(site, chrome, page, out_dir,
                           "does-play-dice-reference.pdf")


def build_book(site, chrome, out_dir):
    """The rules and the character sheet as one document."""
    chapters, contents = [], []
    for rel, title in BOOK_PAGES:
        path = os.path.join(site, *rel.split("/"))
        if not os.path.isfile(path):
            print("  skipping %s (not built)" % rel)
            continue
        body = article_of(path)
        # The web sheet sat between the intro and a rule; with it gone the
        # rule would follow the intro directly.
        body = re.sub(r"(</p>)\s*<hr\s*/?>", r"\1", body, count=1) \
            if rel.startswith("rules/character-vitae/") else body
        chapters.append('<div class="chapter">%s</div>' % body)
        contents.append("<li>%s</li>" % title)
    # The designed character sheet is appended as the last page, after Chrome
    # has printed the rest; it has its own page margins and type.
    sheet = os.path.join(out_dir, "does-play-dice-character-sheet.pdf")
    if os.path.isfile(sheet):
        contents.append("<li>Character sheet</li>")

    toc = (
        '<div class="toc"><h2>Contents</h2><ol>%s</ol></div>' % "".join(contents)
        if contents else ""
    )

    page = shell(
        '<link rel="stylesheet" href="assets/stylesheets/fonts.css">',
        "Does Play Dice",
        """
<div class="cover">
  <div>
    <div class="cover-title">DOES<br>PLAY<br>DICE</div>
    <div class="cover-sub">Five dice. Fifteen minutes. A night out.</div>
  </div>
  <div class="cover-foot">
    Jeff Adams<br>
    doesplaydice.com<br>
    Text licensed CC BY 4.0 &middot; the name and logo are excluded
  </div>
</div>"""
        + toc
        + "".join(chapters),
        BOOK_CSS,
    )
    book = _render_in_site(site, chrome, page, out_dir, "does-play-dice-book.pdf")
    if os.path.isfile(sheet):
        from pypdf import PdfWriter  # requirements.txt; only the book needs it
        writer = PdfWriter()
        writer.append(book)
        writer.append(sheet)
        with open(book, "wb") as out:
            writer.write(out)
    return book


def _render_in_site(site, chrome, markup, out_dir, filename):
    """Render `markup` from inside the built site so relative asset paths work.

    The fonts are self-hosted and referenced relatively, so the temporary file
    has to live at the site root -- pointing Chrome at /tmp would silently fall
    back to system faces and the PDF would not match the site.
    """
    handle, tmp = tempfile.mkstemp(suffix=".html", prefix="_print-", dir=site)
    os.close(handle)
    pdf = os.path.abspath(os.path.join(out_dir, filename))
    try:
        with open(tmp, "w", encoding="utf-8") as out:
            out.write(markup)
        render(chrome, tmp, pdf)
    finally:
        os.unlink(tmp)

    if not os.path.isfile(pdf):
        raise SystemExit("Chrome produced no file for %s" % filename)
    return pdf


def page_count(path):
    """Count pages without a PDF library: /Type /Page objects in the raw file."""
    with open(path, "rb") as handle:
        blob = handle.read()
    count = len(re.findall(rb"/Type\s*/Page[^s]", blob))
    return count or None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site", default="wiki/site", help="built site directory")
    parser.add_argument("--chrome", help="path to Chrome or Chromium")
    parser.add_argument("--only", choices=["rules", "book"], help="build just one")
    args = parser.parse_args()

    if not os.path.isdir(args.site):
        sys.exit("no built site at %s -- run mkdocs build first" % args.site)

    chrome = find_chrome(args.chrome)
    out_dir = os.path.join(args.site, "downloads")
    os.makedirs(out_dir, exist_ok=True)

    jobs = []
    if args.only != "book":
        jobs.append(("one-page rules", build_one_pager))
        jobs.append(("character sheet", build_character_sheet))
        jobs.append(("player reference", build_reference))
    if args.only != "rules":
        jobs.append(("full book", build_book))

    for label, builder in jobs:
        pdf = builder(args.site, chrome, out_dir)
        pages = page_count(pdf)
        size = os.path.getsize(pdf) / 1024.0
        print(
            "  %-16s %-30s %6.0f KB  %s"
            % (label, os.path.basename(pdf), size,
               ("%d page%s" % (pages, "" if pages == 1 else "s")) if pages else "")
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())

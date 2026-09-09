#!/usr/bin/env python3
"""Generate the printable PDFs from the built site.

Two artefacts, and they are deliberately different things:

  does-play-dice-rules.pdf  The whole game on one sheet. This is the thing
                            people take home from a convention table, so it is
                            laid out for paper -- two columns, tight leading,
                            no navigation, no web furniture -- rather than
                            being a screenshot of the web page.

  does-play-dice-book.pdf   The game content as one document: rules, character
                            sheet, expansions, setting, narrator guidance.
                            Project-planning pages are excluded; they come down
                            at launch and were never part of the book.

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
    ("rules/character-vitae/index.html", "Character Vitae"),
    ("rules/expanded/index.html", "Expanded Rules"),
    ("world/index.html", "The World"),
    ("narrators/index.html", "For Narrators"),
]

# Classes stripped from every page before printing. These are scaffolding for
# the website or notes to ourselves, not part of the game.
STRIP_CLASSES = [
    "dpd-protobar",     # "this page is a container" banners
    "dpd-status",       # the Complete / Not written pills
    "admonition",       # includes every OPEN DECISION block
    "md-content__button",
    "headerlink",
    "dpd-timeline",
    "dpd-roller",       # an interactive widget means nothing on paper
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
  --ink:#0A0A0A; --muted:#55534E; --line:#C9C5B9; --accent:#A11F16;
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
  --ink:#0A0A0A; --muted:#55534E; --line:#C9C5B9; --accent:#A11F16;
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
"""


def build_one_pager(site, chrome, out_dir):
    """The whole game on a single sheet."""
    body = article_of(os.path.join(site, "rules", "index.html"))
    # The h1 is replaced by the masthead, so drop it from the flow.
    body = re.sub(r"<h1\b.*?</h1>", "", body, count=1, flags=re.S)

    page = shell(
        '<link rel="stylesheet" href="assets/stylesheets/fonts.css">',
        "Does Play Dice -- the complete rules",
        f"""
<div class="sheet-head">
  <div class="sheet-title">DOES<br>PLAY DICE</div>
  <div class="sheet-sub">The complete rules<br>doesplaydice.com</div>
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


def build_book(site, chrome, out_dir):
    """Rules, sheet, expansions, setting and narrator guidance as one document."""
    chapters, contents = [], []
    for rel, title in BOOK_PAGES:
        path = os.path.join(site, *rel.split("/"))
        if not os.path.isfile(path):
            print("  skipping %s (not built)" % rel)
            continue
        chapters.append('<div class="chapter">%s</div>' % article_of(path))
        contents.append("<li>%s</li>" % title)

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
    return _render_in_site(site, chrome, page, out_dir, "does-play-dice-book.pdf")


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

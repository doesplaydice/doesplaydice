#!/usr/bin/env python3
"""Draw the link preview card: wiki/docs/assets/img/og-card.v3.png (1200x630).

This is the picture Discord, BlueSky, Reddit and iMessage show when someone
pastes the link. It reuses the masthead (overrides/partials/masthead.html), so
the card says what the top of the site says: The Set wordmark on its dice
backdrop, in the dark palette, with the home page heading underneath.

The card is committed, not built in CI, so run this after changing the
masthead, the palette or the heading, and commit the new PNG. Bump the version
in its name (and in overrides/main.html) when you do: Discord and iMessage
cache a preview image by its URL.

    python3 tools/build_og_card.py [--chrome /path/to/chrome]
"""
import argparse
import os
import re
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(__file__))
from build_pdf import find_chrome  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MASTHEAD = os.path.join(ROOT, "wiki", "overrides", "partials", "masthead.html")
FONTS = os.path.join(ROOT, "wiki", "docs", "assets", "fonts")
OUT = os.path.join(ROOT, "wiki", "docs", "assets", "img", "og-card.v3.png")

# Keep in step with the home page heading (wiki/docs/index.md).
TAGLINE = "Five dice. Fifteen minutes. A lifetime of adventure."

# The dark palette and the masthead colours, from extra.v7.css.
CSS = """
@font-face{ font-family:"Archivo Black"; src:url("FONTS/archivo-black-normal-400-latin.woff2"); }
@font-face{ font-family:"JetBrains Mono"; font-weight:400 700;
  src:url("FONTS/jetbrains-mono-normal-400-700-latin.woff2"); }
:root{
  --bg:#050505; --ink:#F4F2EC; --muted:#9A978E; --accent:#F7BA00;
  --mh-d4:#c4553f; --mh-d8:#3f7aa3; --mh-d12:#5b8f62; --mh-d20:#f7ba00;
  --mh-dice:#f7ba00; --mh-dice-op:.45;
}
html,body{ margin:0; width:1200px; height:630px; overflow:hidden; background:var(--bg); }
.card{ position:relative; width:1200px; height:630px; }
.bd{ position:absolute; left:0; top:0; width:1200px; height:440px;
  -webkit-mask-image:linear-gradient(transparent, #000 12%, #000 70%, transparent);
  fill:none; stroke:var(--mh-dice); stroke-width:2; stroke-linejoin:round;
  opacity:var(--mh-dice-op); }
.mark{ position:absolute; left:58px; top:60px; height:330px; width:auto; }
.tag{ position:absolute; left:80px; top:470px; margin:0;
  font:700 30px/1 "JetBrains Mono",monospace; letter-spacing:.06em;
  text-transform:uppercase; color:var(--accent); }
.url{ position:absolute; left:80px; top:530px; margin:0;
  font:400 22px/1 "JetBrains Mono",monospace; letter-spacing:.14em;
  text-transform:uppercase; color:var(--muted); }
.mh-ink{ fill:var(--ink); stroke:var(--ink); }
.mh-d4{ fill:var(--mh-d4); stroke:var(--mh-d4); }
.mh-d8{ fill:var(--mh-d8); stroke:var(--mh-d8); }
.mh-d12{ fill:var(--mh-d12); stroke:var(--mh-d12); }
.mh-d20{ fill:var(--mh-d20); stroke:var(--mh-d20); }
.mh-cut{ stroke:var(--bg); }
.mh-pip{ fill:var(--bg); }
.mh-halo{ flood-color:var(--bg); }
"""


def card_html():
    src = open(MASTHEAD, encoding="utf-8").read()
    svgs = re.findall(r"<svg\b.*?</svg>", src, re.S)
    if len(svgs) != 2:
        sys.exit("Expected the backdrop and the wordmark in masthead.html")
    backdrop = svgs[0].replace('class="dpd-masthead-bd"', 'class="bd"')
    mark = svgs[1].replace("<svg ", '<svg class="mark" ', 1)
    css = CSS.replace("FONTS", "file://" + FONTS)
    return (
        "<!doctype html><meta charset=utf-8><style>%s</style>"
        '<div class="card">%s%s<p class="tag">%s</p><p class="url">doesplaydice.com</p></div>'
        % (css, backdrop, mark, TAGLINE)
    )


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--chrome")
    ap.add_argument("--out", default=OUT)
    args = ap.parse_args()
    try:
        from PIL import Image  # only this tool needs it: pip install pillow
    except ImportError:
        sys.exit("Needs Pillow: python3 -m pip install pillow")
    chrome = find_chrome(args.chrome)
    with tempfile.TemporaryDirectory() as tmp:
        page = os.path.join(tmp, "card.html")
        shot = os.path.join(tmp, "shot.png")
        with open(page, "w", encoding="utf-8") as f:
            f.write(card_html())
        subprocess.run(
            [chrome, "--headless=new", "--no-sandbox", "--disable-gpu",
             "--hide-scrollbars", "--force-device-scale-factor=1",
             "--window-size=1200,900", "--virtual-time-budget=3000",
             "--screenshot=" + shot, "file://" + page],
            check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        # Headless Chrome's viewport comes out shorter than --window-size by
        # however tall its invisible toolbar is, so shoot a taller window and
        # keep the top 1200x630.
        Image.open(shot).crop((0, 0, 1200, 630)).save(args.out, optimize=True)
    print("wrote", args.out)


if __name__ == "__main__":
    main()

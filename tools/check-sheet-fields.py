#!/usr/bin/env python3
"""Check that the Download button still writes onto the right ruled lines.

The character sheet PDF is regenerated from HTML by build_pdf.py on every
deploy. The browser-side filler in assets/js/sheet-pdf.js writes onto it at
hardcoded coordinates, because a PDF has no idea what a "field" is.

That is a silent-failure waiting to happen: nudge the sheet's CSS and the
answers land in the wrong place, or in the margin, and nothing complains. So
this reads the ruled lines back out of the generated PDF and fails the build if
any coordinate in sheet-pdf.js no longer sits on one.

Stdlib only, like everything else in here.

    python3 tools/check-sheet-fields.py [--site wiki/site]
"""

import argparse
import os
import re
import sys
import zlib

TOLERANCE = 1.5  # points; a rule that has moved less than this is still the rule


def content_stream(pdf):
    """The page's content stream, decompressed."""
    for m in re.finditer(rb'(\d+) 0 obj\s*(<<[^>]*?>>)\s*stream\r?\n', pdf, re.S):
        head = m.group(2)
        if b'/Length' not in head:
            continue
        raw = pdf[m.end():pdf.index(b'endstream', m.end())]
        if b'/FlateDecode' in head:
            try:
                text = zlib.decompress(raw)
            except zlib.error:
                continue
        else:
            text = raw
        # The page content is the one that draws the ruled lines.
        if b' re' in text and b'cm' in text:
            return text.decode('latin-1')
    raise SystemExit("could not find the page content stream")


def _mul(a, b):
    return (a[0] * b[0] + a[1] * b[2], a[0] * b[1] + a[1] * b[3],
            a[2] * b[0] + a[3] * b[2], a[2] * b[1] + a[3] * b[3],
            a[4] * b[0] + a[5] * b[2] + b[4], a[4] * b[1] + a[5] * b[3] + b[5])


def rules_in(stream):
    """Every thin wide rectangle, in page points. Those are the ruled lines."""
    ctm = (1, 0, 0, 1, 0, 0)
    stack, nums, rects = [], [], []
    for num, op in re.findall(r'(-?[\d.]+)|([A-Za-z*\'"]+)', stream):
        if num:
            nums.append(float(num))
            continue
        if op == 'q':
            stack.append(ctm)
        elif op == 'Q' and stack:
            ctm = stack.pop()
        elif op == 'cm' and len(nums) >= 6:
            ctm = _mul(tuple(nums[-6:]), ctm)
        elif op == 're' and len(nums) >= 4:
            x, y, w, h = nums[-4:]
            x0 = ctm[0] * x + ctm[2] * y + ctm[4]
            y0 = ctm[1] * x + ctm[3] * y + ctm[5]
            x1 = ctm[0] * (x + w) + ctm[2] * (y + h) + ctm[4]
            y1 = ctm[1] * (x + w) + ctm[3] * (y + h) + ctm[5]
            rects.append((min(x0, x1), min(y0, y1), abs(x1 - x0), abs(y1 - y0)))
        nums = []
    return [r for r in rects if r[3] <= 2.2 and r[2] > 40]


def boxes_in(stream):
    """The outline of every stroked shape, in page points. Chrome draws a
    bordered box (the Floor boxes, the stamina boxes) as a path rather than a
    rectangle, so this takes the bounding box of each path it strokes."""
    ctm = (1, 0, 0, 1, 0, 0)
    stack, nums, pts, boxes = [], [], [], []

    def at(x, y):
        return (ctm[0] * x + ctm[2] * y + ctm[4], ctm[1] * x + ctm[3] * y + ctm[5])

    for num, op in re.findall(r'(-?[\d.]+)|([A-Za-z*\'"]+)', stream):
        if num:
            nums.append(float(num))
            continue
        if op == 'q':
            stack.append(ctm)
        elif op == 'Q' and stack:
            ctm = stack.pop()
        elif op == 'cm' and len(nums) >= 6:
            ctm = _mul(tuple(nums[-6:]), ctm)
        elif op in ('m', 'l') and len(nums) >= 2:
            pts.append(at(*nums[-2:]))
        elif op == 'c' and len(nums) >= 6:
            pts.append(at(*nums[-2:]))
        elif op in ('S', 's', 'f', 'F', 'f*', 'B', 'B*', 'b', 'b*', 'n'):
            if pts and op in ('S', 's'):
                xs = [p[0] for p in pts]
                ys = [p[1] for p in pts]
                boxes.append((min(xs), min(ys), max(xs) - min(xs), max(ys) - min(ys)))
            pts = []
        nums = []
    return [b for b in boxes if b[2] > 10 and b[3] > 10]


def declared_stamina(js_path):
    """The stamina grid sheet-pdf.js crosses boxes out on."""
    src = open(js_path, encoding='utf-8').read()
    m = re.search(r'var STAMINA = \{\s*x:\s*([\d.]+),\s*step:\s*([\d.]+),\s*'
                  r'size:\s*([\d.]+),\s*rows:\s*\[([^\]]*)\]', src)
    if not m:
        raise SystemExit("could not find the STAMINA table in %s" % js_path)
    rows = [float(v) for v in m.group(4).split(',')]
    return float(m.group(1)), float(m.group(2)), float(m.group(3)), rows


def declared_rules(js_path):
    """The coordinates sheet-pdf.js will actually write at."""
    src = open(js_path, encoding='utf-8').read()
    block = re.search(r'var RULES = \{(.*?)\n  \};', src, re.S)
    if not block:
        raise SystemExit("could not find the RULES table in %s" % js_path)
    out = {}
    for name, x, y, w in re.findall(
            r"'([\w-]+)'\s*:\s*\[\s*([\d.]+)\s*,\s*([\d.]+)\s*,\s*([\d.]+)\s*\]",
            block.group(1)):
        out[name] = (float(x), float(y), float(w))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--site", default=os.path.join("wiki", "site"))
    ap.add_argument("--js", default=os.path.join(
        "wiki", "docs", "assets", "js", "sheet-pdf.js"))
    args = ap.parse_args()

    pdf_path = os.path.join(args.site, "downloads",
                            "does-play-dice-character-sheet.pdf")
    if not os.path.isfile(pdf_path):
        print("  skipping: %s is not built yet" % pdf_path)
        print("  (run tools/build_pdf.py first; CI does this on every push)")
        return 0

    stream = content_stream(open(pdf_path, "rb").read())
    found = rules_in(stream)
    boxes = boxes_in(stream)
    declared = declared_rules(args.js)

    def box_near(x, y):
        return any(abs(b[0] - x) <= TOLERANCE and abs(b[1] - y) <= TOLERANCE
                   for b in boxes)

    problems = []
    checked = 0
    for name, (x, y, _w) in sorted(declared.items()):
        if name.startswith("die-"):
            continue  # written on a printed glyph's baseline, not on a rule
        checked += 1
        if name.startswith("floor-"):
            if not box_near(x, y):
                problems.append((name, x, y))
            continue
        near = [r for r in found
                if abs(r[1] - y) <= TOLERANCE and r[0] - TOLERANCE <= x <= r[0] + r[2]]
        if not near:
            problems.append((name, x, y))

    sx, step, _size, rows = declared_stamina(args.js)
    for i, y in enumerate(rows):
        for b in range(20):
            checked += 1
            x = sx + b * step
            if not box_near(x, y):
                problems.append(("stamina-%d-%d" % (i + 1, b + 1), x, y))

    if problems:
        print("The character sheet has moved under the Download button.\n")
        print("These coordinates in %s no longer sit on the sheet's lines and boxes:\n" % args.js)
        for name, x, y in problems:
            print("  %-14s expected a %s at x=%.1f y=%.1f"
                  % (name, "rule" if name[:5] not in ("floor", "stami") else "box", x, y))
        print("\nThe ruled lines actually in the sheet now:\n")
        for x, y, w, _h in sorted(found, key=lambda r: (-r[1], r[0])):
            print("  x=%6.1f  y=%6.1f  width=%6.1f" % (x, y, w))
        print("\nThe boxes actually in the sheet now:\n")
        for x, y, w, h in sorted(boxes, key=lambda r: (-r[1], r[0])):
            print("  x=%6.1f  y=%6.1f  width=%6.1f  height=%6.1f" % (x, y, w, h))
        print("\nUpdate the RULES and STAMINA tables in sheet-pdf.js to match, then re-run this.")
        return 1

    print("Download button: all %d lines and boxes still where sheet-pdf.js expects."
          % checked)
    return 0


if __name__ == "__main__":
    sys.exit(main())

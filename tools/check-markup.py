#!/usr/bin/env python3
"""Reject dangerous raw HTML in documentation source.

Python-Markdown passes raw HTML straight through, and wiki/docs/community/ is
deliberately unowned -- CONTRIBUTING says community modules get "a light read".
So a merged pull request could put a <script> tag on doesplaydice.com.

Today that buys someone defacement. It gets worse later: the CMS at /admin/
runs on this same origin and will hold a GitHub token once its OAuth broker is
deployed, and any script on the origin can read that token from storage.

This is a blunt check on purpose. The site uses plenty of legitimate raw HTML
-- divs, spans, tables, inline SVG -- and none of that is touched. What is
rejected is the small set of constructs that can execute or embed.

    python3 tools/check-markup.py [docs_dir]
"""
import os
import re
import sys

# Each: (name, pattern, why it matters)
BANNED = [
    ("script tag", re.compile(r"<\s*script\b", re.I),
     "executes arbitrary JavaScript on the site's origin"),
    ("event handler", re.compile(r"<[^>]*?\son[a-z]+\s*=", re.I | re.S),
     "onerror/onclick/onload run arbitrary JavaScript"),
    ("iframe", re.compile(r"<\s*iframe\b", re.I),
     "embeds a third-party page and can be used for clickjacking"),
    ("object/embed", re.compile(r"<\s*(object|embed)\b", re.I),
     "embeds arbitrary plugin content"),
    ("javascript: url", re.compile(r"""=\s*["']?\s*javascript:""", re.I),
     "executes JavaScript when followed"),
    ("data: url in href/src", re.compile(r"""(?:href|src)\s*=\s*["']?\s*data:(?!image/)""", re.I),
     "can smuggle executable content past a naive review"),
]


def main(root="wiki/docs"):
    if not os.path.isdir(root):
        sys.exit("no such directory: %s" % root)

    hits = []
    scanned = 0
    for dirpath, _, filenames in os.walk(root):
        for name in sorted(filenames):
            if not name.endswith(".md"):
                continue
            path = os.path.join(dirpath, name)
            scanned += 1
            with open(path, encoding="utf-8", errors="replace") as handle:
                for lineno, line in enumerate(handle, 1):
                    for label, pattern, why in BANNED:
                        if pattern.search(line):
                            hits.append((path, lineno, label, why, line.strip()[:110]))

    if hits:
        print("%d disallowed construct(s) in documentation source:\n" % len(hits))
        for path, lineno, label, why, text in hits:
            print("  %s:%d" % (path, lineno))
            print("    %s -- %s" % (label, why))
            print("    %s\n" % text)
        print("Scanned %d markdown files." % scanned)
        return 1

    print("No disallowed HTML in %d markdown files." % scanned)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "wiki/docs"))

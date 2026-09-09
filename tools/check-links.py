#!/usr/bin/env python3
"""Check every internal link in the built site actually resolves.

Why this exists, given `mkdocs build --strict`:

    --strict fails on broken *markdown* links, because MkDocs resolves those
    itself. It never looks inside raw HTML. Several pages here are hand-written
    HTML blocks (the card grids, the file list), and every href in them is
    invisible to --strict. That is how six download links and one rules link
    shipped pointing at /downloads/downloads/*.pdf -- the page lives at
    /downloads/, so a relative "downloads/x.pdf" doubled the directory.

Run against the build output:

    python3 tools/check-links.py wiki/site
"""
import html
import os
import re
import sys
from urllib.parse import urljoin, urlparse

SKIP_SCHEMES = ("http:", "https:", "mailto:", "tel:", "data:", "javascript:")


def page_urls(root):
    """Yield (file path, the URL path the file is served at)."""
    for dirpath, _, filenames in os.walk(root):
        for name in filenames:
            if not name.endswith(".html"):
                continue
            path = os.path.join(dirpath, name)
            rel = os.path.relpath(path, root).replace(os.sep, "/")
            # foo/index.html is served at /foo/, anything else at its own name.
            served = "/" + (rel[: -len("index.html")] if rel.endswith("index.html") else rel)
            yield path, served


def resolves(root, url_path):
    target = os.path.join(root, url_path.lstrip("/"))
    return (
        os.path.isfile(target)
        or os.path.isfile(os.path.join(target, "index.html"))
        or os.path.isfile(target.rstrip("/") + ".html")
    )


def main(root):
    if not os.path.isdir(root):
        sys.exit(f"no such directory: {root} (build the site first)")

    broken, checked = [], 0
    for path, served in page_urls(root):
        markup = open(path, encoding="utf-8").read()
        # Only content links. Theme chrome is Material's problem, not ours, and
        # it legitimately emits things this checker would misread.
        article = re.search(r"<article\b[^>]*>(.*?)</article>", markup, re.S)
        if not article:
            continue
        for attr in re.findall(r'(?:href|src)="([^"]+)"', article.group(1)):
            attr = html.unescape(attr).strip()
            if not attr or attr.startswith("#") or attr.lower().startswith(SKIP_SCHEMES):
                continue
            if attr.startswith("//"):  # protocol-relative, still external
                continue
            checked += 1
            target = urlparse(urljoin(served, attr)).path
            if not resolves(root, target):
                broken.append((served, attr, target))

    if broken:
        print(f"{len(broken)} broken internal link(s):\n")
        current = None
        for served, attr, target in sorted(broken):
            if served != current:
                print(f"  page {served}")
                current = served
            print(f'    href="{attr}"  ->  {target}  (does not exist)')
        print(f"\nChecked {checked} internal links.")
        return 1

    print(f"All {checked} internal links resolve.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "wiki/site"))

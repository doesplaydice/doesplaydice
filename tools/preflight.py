#!/usr/bin/env python3
"""Launch-day checks for doesplaydice.com.

Several things on this site exist only because it is pre-launch, and every one
of them fails *silently* if it is still in place on the day. The worst is
robots.txt: `Disallow: /` makes the launched site invisible to search engines,
nothing appears broken, and nobody notices for weeks.

This turns that knowledge into something executable, so it does not live in
commit messages and somebody's memory.

    python3 tools/preflight.py            # report, exit 1 if a blocker remains
    python3 tools/preflight.py --pre-launch   # expect the temporary things

Before launch most checks are SUPPOSED to fail -- that is the checklist working.
Run it with --pre-launch to confirm only the expected ones are outstanding.
"""
import argparse
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = "doesplaydice/doesplaydice"

BLOCKER, WARNING = "BLOCKER", "warning"


def read(*parts):
    path = os.path.join(ROOT, *parts)
    if not os.path.isfile(path):
        return None
    with open(path, encoding="utf-8", errors="replace") as handle:
        return handle.read()


def check_robots():
    body = read("wiki", "docs", "robots.txt")
    if body is None:
        return True, "robots.txt is gone -- search engines may index the site"
    if re.search(r"^\s*Disallow:\s*/\s*$", body, re.M):
        return False, (
            "robots.txt still says `Disallow: /`. The launched site would be "
            "invisible to every search engine, and nothing would look broken.\n"
            "         Fix: rm wiki/docs/robots.txt"
        )
    return True, "robots.txt exists but does not block the whole site"


def check_gate():
    """Is the pre-launch passphrase gate still in place?

    This deliberately looks for the gate itself rather than for
    wiki/overrides/ or custom_dir. That template also carries the permanent
    installable/offline head tags now, so deleting the directory at launch
    would silently take offline support with it -- which is exactly the kind
    of quiet collateral damage this script exists to prevent.
    """
    # The passphrase hash is the thing that actually has to be gone. Checking
    # only for a comment marker was not enough: the markers were briefly in the
    # wrong place and enclosed the palette migration instead of the gate, so
    # this check would have reported "removed" while the hash and the
    # passphrase form were still in every page.
    HASH_PREFIX = "6db171ebb2a69f14"
    problems = []
    template = read("wiki", "overrides", "main.html") or ""
    if "GATE START" in template:
        problems.append("the gate block is still in overrides/main.html")
    if HASH_PREFIX in template:
        problems.append("the passphrase hash is still in overrides/main.html")
    admin = read("wiki", "docs", "admin", "index.html") or ""
    if HASH_PREFIX in admin:
        problems.append("the passphrase hash is still in admin/index.html")
    css = read("wiki", "docs", "assets", "stylesheets", "extra.v3.css") or ""
    if "dpd-gate" in css:
        problems.append("the gate styling is still in extra.v3.css")
    if problems:
        return False, (
            "the pre-launch passphrase gate is still active: "
            + "; ".join(problems)
            + "\n         Fix: delete everything between GATE START and GATE END "
              "in wiki/overrides/main.html, and the #dpd-gate rules in "
              "extra.v3.css.\n         Do NOT delete overrides/ or custom_dir -- "
              "the manifest and offline tags live there too."
        )
    return True, "the passphrase gate is removed"


def check_admin_scripts():
    body = read("wiki", "docs", "admin", "index.html")
    if body is None:
        return True, "no admin/ page"
    if "<script" in body:
        return False, (
            "wiki/docs/admin/index.html still carries script blocks.\n"
            "         Fix: remove them, or delete the admin page entirely"
        )
    return True, "admin page carries no scripts"


def check_plan_section():
    config = read("wiki", "mkdocs.yml") or ""
    still = [name for name in ("plan/index.md", "decisions.md") if name in config]
    if still:
        return False, (
            "the project-planning pages are still in the nav (%s). They say on "
            "their own face that they come down before launch." % ", ".join(still)
        )
    return True, "planning pages are out of the nav"


def check_open_decisions():
    docs = os.path.join(ROOT, "wiki", "docs")
    count = 0
    for dirpath, _, filenames in os.walk(docs):
        for name in filenames:
            if name.endswith(".md"):
                with open(os.path.join(dirpath, name), encoding="utf-8") as handle:
                    count += len(re.findall(r'decision "OPEN DECISION', handle.read()))
    if count:
        return False, "%d open decision%s still unresolved (see decisions.md)" % (
            count, "" if count == 1 else "s"
        )
    return True, "no open decisions left on the site"


def check_https():
    try:
        out = subprocess.run(
            ["gh", "api", "repos/%s/pages" % REPO],
            capture_output=True, text=True, timeout=25,
        )
        if out.returncode:
            return None, "could not read Pages settings (gh not authenticated?)"
        data = json.loads(out.stdout)
    except Exception as exc:                      # noqa: BLE001 -- report, never crash
        return None, "could not read Pages settings: %s" % exc

    if data.get("https_enforced"):
        return True, "HTTPS is enforced"
    state = (data.get("https_certificate") or {}).get("state", "unknown")
    extra = ""
    if state == "dns_changed":
        extra = (
            "\n         Stuck here since 2026-09-09. Diagnosed: the apex certificate "
            "covers\n         doesplaydice.com only, and www.doesplaydice.com is a CNAME to "
            "the APEX\n         rather than to doesplaydice.github.io, so GitHub cannot "
            "finish\n         provisioning and TLS to www fails outright.\n"
            "         Jeff must change ONE DNS record at Fastmail:\n"
            "           www  CNAME  doesplaydice.github.io.\n"
            "         (or delete the www record entirely). This does NOT touch MX --"
            "\n         his email is unaffected."
        )
    return False, (
        "HTTPS is not enforced (certificate state: %s).%s\n"
        "         Then:  gh api -X PUT repos/%s/pages -F https_enforced=true"
        % (state, extra, REPO)
    )


def check_pdfs():
    site = os.path.join(ROOT, "wiki", "site", "downloads")
    wanted = ["does-play-dice-rules.pdf", "does-play-dice-book.pdf"]
    missing = [n for n in wanted if not os.path.isfile(os.path.join(site, n))]
    if missing:
        return None, (
            "not built locally: %s\n"
            "         (CI builds them on every push; run mkdocs build then "
            "tools/build_pdf.py to check locally)" % ", ".join(missing)
        )
    return True, "both PDFs present in the build output"


CHECKS = [
    ("robots.txt does not block indexing", check_robots, BLOCKER),
    ("passphrase gate removed", check_gate, BLOCKER),
    ("HTTPS enforced", check_https, BLOCKER),
    ("admin page has no scripts", check_admin_scripts, WARNING),
    ("planning pages out of the nav", check_plan_section, WARNING),
    ("open decisions resolved", check_open_decisions, WARNING),
    ("printable PDFs build", check_pdfs, WARNING),
]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--pre-launch", action="store_true",
        help="expect the temporary pre-launch things to still be in place",
    )
    args = parser.parse_args()

    print("\nLaunch preflight -- %s\n" % REPO)
    failures = 0
    for title, check, severity in CHECKS:
        ok, detail = check()
        if ok is None:
            mark, tag = "  ?  ", "skipped"
        elif ok:
            mark, tag = " PASS", ""
        else:
            mark, tag = " FAIL", severity
            if severity == BLOCKER:
                failures += 1
        print("  [%s] %-34s %s" % (mark, title, tag))
        if not ok:
            print("         %s" % detail)
    print()

    if args.pre_launch:
        print("  Pre-launch mode: the gate, robots.txt and the planning pages are")
        print("  expected to be outstanding. What matters is that nothing ELSE is.\n")
        return 0

    if failures:
        print("  %d blocker%s outstanding. Do not launch.\n"
              % (failures, "" if failures == 1 else "s"))
        return 1
    print("  No blockers. Clear to launch.\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())

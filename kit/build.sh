#!/usr/bin/env bash
# Build the convention kit PDFs from the HTML sources.
#
# Uses headless Chrome, which is already on every Mac that has Chrome installed.
# No LaTeX, no WeasyPrint, no system libraries to fight with.

set -euo pipefail
cd "$(dirname "$0")"

CHROME="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
if [ ! -x "$CHROME" ]; then
  echo "Chrome not found at: $CHROME" >&2
  echo "Set CHROME=/path/to/chrome, or just open the files in src/ and use File > Print > Save as PDF." >&2
  exit 1
fi

mkdir -p dist
PIECES=(table-tent pregens scenario-frame handout session-brief feedback-slips)

for p in "${PIECES[@]}"; do
  printf 'Building %-16s ... ' "$p"
  "$CHROME" \
    --headless=new \
    --disable-gpu \
    --run-all-compositor-stages-before-draw \
    --virtual-time-budget=10000 \
    --no-pdf-header-footer \
    --print-to-pdf="dist/$p.pdf" \
    "file://$PWD/src/$p.html" 2>/dev/null
  printf 'ok (%s)\n' "$(du -h "dist/$p.pdf" | cut -f1 | tr -d ' ')"
done

echo
echo "Done. PDFs in kit/dist/"

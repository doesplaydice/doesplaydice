#!/usr/bin/env python3
"""Generate wiki/docs/rules/odds.md -- every outcome in the core mechanic.

The numbers are computed here rather than typed, for the same reason the
Platonic solids are computed rather than drawn: a table of 25 pairings with
three percentages each is 75 chances to make a transcription error that nobody
would ever catch by eye.

Everything is exact. Each cell enumerates all p*n equally likely (skill roll,
difficulty roll) pairs and counts them; no sampling, no floating point until
the final format.

    python3 tools/generate-odds.py
"""
from fractions import Fraction

DICE = [4, 6, 8, 12, 20]
DIFFICULTY = {4: "Easy", 6: "Moderate", 8: "Challenging", 12: "High difficulty",
              20: '"Impossible"'}
OUT = "wiki/docs/rules/odds.md"


def outcomes(skill, challenge):
    """Exact (win, tie, lose) probabilities for one pairing."""
    win = tie = 0
    for a in range(1, skill + 1):
        for b in range(1, challenge + 1):
            if a > b:
                win += 1
            elif a == b:
                tie += 1
    total = skill * challenge
    w = Fraction(win, total)
    t = Fraction(tie, total)
    return w, t, 1 - w - t


def fmt(value):
    """Format a number the way pct() formats a fraction."""
    return f"{value:.0f}" if abs(value - round(value)) < 0.05 else f"{value:.1f}"


def pct(fraction):
    value = float(fraction) * 100
    # No decimal on whole numbers: "25%" reads better than "25.0%" in a grid
    # this dense, and every one of these is exact anyway.
    return f"{value:.0f}" if abs(value - round(value)) < 0.05 else f"{value:.1f}"


def main():
    # The tie rule is the interesting one, so verify the closed form rather
    # than asserting it in prose: P(tie) should be exactly 1/max(skill, challenge).
    for s in DICE:
        for c in DICE:
            _, tie, _ = outcomes(s, c)
            assert tie == Fraction(1, max(s, c)), (s, c, tie)

    rows = []
    for skill in DICE:
        cells = []
        for challenge in DICE:
            w, t, l = outcomes(skill, challenge)
            # Round win and tie, then DERIVE lose from them. Rounding all
            # three independently made nine of the 25 cells display as 99.9 or
            # 100.1 -- while the page's own key promised "every column adds to
            # 100". The underlying fractions were always exact; only the
            # display lied.
            w_s, t_s = pct(w), pct(t)
            l_s = fmt(100 - float(w_s) - float(t_s))
            cells.append(
                '<td><span class="odds-w">%s</span>'
                '<span class="odds-t">%s</span>'
                '<span class="odds-l">%s</span></td>'
                % (w_s, t_s, l_s)
            )
        rows.append(
            '  <tr><th scope="row">d%d</th>%s</tr>' % (skill, "".join(cells))
        )

    head = "".join(
        '<th scope="col">d%d<span>%s</span></th>' % (d, DIFFICULTY[d]) for d in DICE
    )

    page = '''---
hide:
  - toc
---

# The odds

<p class="dpd-lede-sm">Every possible roll in the game, worked out exactly. Your Skill die
across the rows, the Narrator's Difficulty die across the columns.</p>

<div class="dpd-odds" markdown>

<table class="dpd-odds-grid">
  <thead>
    <tr><th scope="col"><span class="odds-corner">skill \\ challenge</span></th>%s</tr>
  </thead>
  <tbody>
%s
  </tbody>
</table>

<p class="dpd-odds-key">
  <span class="odds-w">win</span>
  <span class="odds-t">tie</span>
  <span class="odds-l">lose</span>
  &mdash; percentages, from the player's side. Every column adds to 100.
</p>

</div>

## The tie is governed by the bigger die

There is a clean rule hiding in that grid, and it is exact rather than
approximate:

!!! quote "The tie rule"

    **A tie happens exactly 1 &divide; (the larger of the two dice) of the time.**

    d4 against d4 ties one roll in four. d20 against d20 ties one in twenty.
    It does not matter what the smaller die is.

Which means the most generous rule in the game &mdash; *both sides get something*
&mdash; fires **most often for beginners attempting easy things**, and almost
disappears at the top of the range.

A new player with a d4 Skill trying something Easy triggers it on a quarter of
their rolls. Two experts in a d20 standoff trigger it on one roll in twenty.
The game gets more decisive exactly as the stakes rise, and it is at its most
collaborative exactly where new players are standing.

## An even match is never a coin flip

Matched dice do not split 50/50, because the tie takes its share out of the
middle first:

| Matched pair | Win | Tie | Lose |
| --- | --- | --- | --- |
%s

The tie is a real third outcome, not a rounding error. At the bottom of the
range it is a quarter of all play.

## Reading the grid

- **Down a column** &mdash; what one more point of Skill buys you against a fixed
  challenge. Against a d12, moving from d4 to d20 takes you from 12.5%% to 67.5%%.
- **Across a row** &mdash; how fast a challenge outruns you. A d8 Skill is favoured
  against Easy and Moderate, even against Challenging, and outmatched above that.
- **The diagonal** &mdash; an even contest, which is where the tie rule does most of
  its work.

!!! note "How these were produced"

    Computed, not measured. Each cell enumerates all possible pairs of rolls and
    counts them, so these are exact probabilities rather than the results of a
    simulation. The generator is `tools/generate-odds.py`, and it asserts the
    1 &divide; larger-die rule for all 25 pairings every time it runs.
''' % (head, "\n".join(rows), "\n".join(
        "| d%d vs d%d | %s%% | %s%% | %s%% |" % (
            d, d, pct(outcomes(d, d)[0]), pct(outcomes(d, d)[1]),
            fmt(100 - float(pct(outcomes(d, d)[0])) - float(pct(outcomes(d, d)[1]))),
        )
        for d in DICE
    ))

    with open(OUT, "w") as handle:
        handle.write(page)
    print("  wrote %s (%d pairings, tie rule verified)" % (OUT, len(DICE) ** 2))


if __name__ == "__main__":
    main()

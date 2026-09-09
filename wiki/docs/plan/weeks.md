# Week by week

<div class="dpd-timeline" data-con="2026-10-16">
  <div class="dpd-tl-count">
    <span class="dpd-tl-num">&mdash;</span>
    <span class="dpd-tl-label">&nbsp;</span>
  </div>
  <ol class="dpd-tl-steps">
    <li data-date="2026-09-10"><b>Sep 10</b><span>Decisions</span></li>
    <li data-date="2026-09-17"><b>Sep 17</b><span>Site goes real</span></li>
    <li data-date="2026-09-24"><b>Sep 24</b><span>Campaign rules</span></li>
    <li data-date="2026-10-01"><b>Oct 1</b><span>Feedback in</span></li>
    <li data-date="2026-10-08"><b>Oct 8</b><span>Print and freeze</span></li>
    <li data-date="2026-10-15"><b>Oct 15</b><span>Go, no-go</span></li>
    <li data-date="2026-10-16" class="dpd-tl-con"><b>Oct 16</b><span>Carnage Con</span></li>
  </ol>
</div>

Six Thursday sessions between now and the convention. Each one has a single job, and one thing
that must be true by the end of it.

!!! note "How to read this"

    **Jeff's column is the one that matters most.** Almost everything on the build side is
    already done or is straightforward. The schedule risk lives in the writing and the
    playtesting, and both of those are Jeff's.

    Items struck through are already finished &mdash; they're left visible so it's clear what
    moved rather than what vanished.

---

## Already done

Cleared ahead of the schedule below, so none of it needs discussing on a Thursday:

- **The licence is chosen and applied.** CC BY 4.0, with the name and logo excluded as
  trademarks. `LICENSE` and `NOTICE.md` are in the repository.
- **The repository is public**, at `doesplaydice/doesplaydice`, under Jeff's organisation.
- **The site is live** at doesplaydice.com, behind the temporary passphrase while it settles.
- **The printed kit exists** &mdash; all six pieces, and every one of them downloads.
- **Publishing is automatic.** Anything merged to `main` is live in about a minute, and broken
  links now fail the build rather than shipping.

---

## Thursday 10 September &mdash; Decisions

**The job:** clear everything that's blocking, so nothing waits on a question.

The [open decisions](../decisions.md) page is the agenda. Four are open; two more turned out to
have been settled back on 24 August and had been sitting on the site as questions Jeff had
already answered.

| Jeff | Llamassist |
| --- | --- |
| Confirm the Carnage Con registration actually went through | Walk through the site together, first look |
| ~~Make the licence call~~ &mdash; **done, CC BY 4.0** | ~~Apply the licence~~ &mdash; **done** |
| Agree the campaign rules table of contents &mdash; **structure only, not content** | Rob's answer on the writing pipeline |
| Settle the naming question: Narrator vs GM (Timaeus is already settled) | Ten minutes of practice editing a page together |
| Print the kit and take it to the next library night | |

**True by the end:** convention registration confirmed, the open decisions are closed or
consciously deferred, and playtesting has started.

!!! warning "One setting still to turn on"

    The frozen-core governance is agreed but not yet enforced. `CODEOWNERS` names Jeff as the
    owner of the one-page rules, and that only binds once branch protection on `main` requires
    code-owner review. Worth deciding together, because switching it on also stops direct
    pushes to `main` &mdash; which is how the site is currently updated.

---

## Thursday 17 September &mdash; The site stops being a preview

**The job:** the rules become something you can hand to a stranger on paper.

| Jeff | Llamassist |
| --- | --- |
| First two playtests done, sheets photographed | **PDF rulebook, generated from the site** |
| Start writing skills and combat | Passphrase gate comes off |
| | ~~Licence and trademark notice~~ &mdash; **done** |

**True by the end:** the one-page rules exist as a PDF anyone can print, and the site is open to
the public.

---

## Thursday 24 September &mdash; Campaign rules take shape

**The job:** Jeff's writing lands in the structure agreed on the 10th. Publishing is automatic,
so each section appears the moment it's finished.

| Jeff | Llamassist |
| --- | --- |
| Skills and combat drafted | Publish each section as it arrives |
| Playtests move on to testing the campaign rules | Character template layout, if the writing allows |

**True by the end:** an honest call on whether the campaign rules make the convention. If they
won't, they ship as a draft and nothing else changes.

---

## Thursday 1 October &mdash; Feedback into the rules

**The job:** six or so sessions of data. This is where playtesting earns its keep.

| Jeff | Llamassist |
| --- | --- |
| Fix what actually confused real tables | Update the kit with Jeff's characters and scenario |
| Write the one-shot scenario for the convention | Convention logistics: table setup, what to hand out |

**True by the end:** the one-page rules are frozen. No more changes except typos.

---

## Thursday 8 October &mdash; Print and freeze

**The job:** everything physical gets ordered with a week of slack.

| Jeff | Llamassist |
| --- | --- |
| Full dry run of a 40-minute convention slot | Final PDFs to print |
| Approve the final printed pieces | Everything frozen except typos |

**True by the end:** printing is ordered. Nothing remains that can slip.

---

## Thursday 15 October &mdash; Go, no-go

**The job:** confirm. Do not build.

- Printed materials in hand and checked
- Site up, QR codes scanned on a real phone
- Feedback slips printed and packed
- `tools/preflight.py` passes &mdash; the launch checks, run one last time

**True by the end:** Jeff drives to Carnage Con with everything he needs.

---

## 16&ndash;18 October &mdash; Carnage Con

Fifteen years of work, in front of strangers.

!!! warning "The one thing that would actually hurt"

    Another quiet fortnight. The gap in late August cost roughly four playtest sessions, and
    those are the scarcest thing in this plan &mdash; there are only about ten of them in total.

    **Keep the Thursday even when there's nothing to show.** A ten-minute call that says "no
    change this week" is worth more than a skipped one.

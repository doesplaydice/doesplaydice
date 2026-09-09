---
hide:
  - toc
---

# Open decisions <span class="dpd-status stub">4 open</span>

<div class="dpd-protobar" markdown>
**This page is the agenda, not the game.** Every unresolved question on the site is collected
here so nobody has to tour the whole thing to find them. It comes down before launch.
</div>

Four decisions are open. Two more were already settled on **24 August** and had been sitting
here as questions Jeff had answered months ago &mdash; they are recorded at the bottom rather
than deleted, so it is clear what moved.

Each one below says what it blocks and what we'd recommend. The recommendation is a starting
position to argue with, not a conclusion.

## At a glance

| # | Decision | Blocks | Decide by |
| --- | --- | --- | --- |
| 1 | [Is the Narrator's guide free?](#1-is-the-narrators-guide-free) | The licence boundary, permanently | **Before Jeff writes it** |
| 2 | [What is the Narrator called?](#2-what-is-the-narrator-called) | Terminology pass, printed kit | **Next session** |
| 3 | [How far does the character sheet go?](#3-how-far-does-the-character-sheet-go) | Print order | 24 Sep |
| 4 | [Which expansions matter first?](#4-which-expansions-matter-first) | Nothing for launch | 24 Sep |

---

## 1. Is the Narrator's guide free?

!!! danger "This one is irreversible, and it is the reason it's listed first"

    **CC BY 4.0 cannot be revoked.** Anything committed to this repository is permanently
    free for anyone to use, modify and sell, with attribution. That is the point of the
    licence and it is why it was the right call &mdash; but it runs one direction only.

    So the question is not really "is the Narrator's guide free". It is **"does the Narrator's
    guide go in this repository at all"** &mdash; because the moment it does, the answer is yes,
    forever.

Jeff's own Actuator notebook draws the commercial line here explicitly: *"core player content
must be free (or open-sourced, which ends up being the same thing), while content developed for
a GM or a streamer can remain proprietary and be sold commercially."*

**Our recommendation.** Keep everything in this repository free, Narrator guidance included, and
keep future commercial work &mdash; published adventures, streamer packs, a printed hardback
&mdash; as separate works in separate repositories. Two licence boundaries inside one repository
is how open-source projects end up with problems that take a lawyer to unpick, and Jeff would be
the lawyer.

That still leaves plenty to sell. The free rules are the thing that gets adopted; the products
are the things built on top.

**What we need from Jeff:** a yes or no on "the repository is entirely free", so the writing can
start without a licensing question attached to every paragraph.

---

## 2. What is the Narrator called?

Jeff flagged this himself in `Playing the Game.md`: *"Can't use DM; it's in sore need of an
update, plus it's trademarked. (Is it?) So, the usual alt is GM, but are there better options?
Director? MC? Narrator? Conductor? Moderator? Storyteller? Bard? The Voice?"*

**Our recommendation: Narrator, and close this tomorrow.** The live one-pager already says it,
the printed kit already says it, and this site already says it. It is the better word anyway
&mdash; it promises story-telling rather than dungeons, which is exactly the pitch. Most of the
older notes still say GM or DM, so what remains is one terminology pass, not a decision.

**Blocked behind it:** the pass itself, and the printed kit, which cannot go to the printer on
8 October with two words for the same role.

---

## 3. How far does the character sheet go?

The current draft covers exactly what the one-page rules require and no more. Jeff's
`Character resume.md` runs to 30,000 characters and describes a much richer document &mdash;
point-buy, training, backgrounds-as-organizations.

**Our recommendation: ship the minimal sheet for v1.** It is already drafted, it matches the
one-page rules exactly, and a convention player fills it in during the first two minutes of a
40-minute slot. The full CV is a v2 document that belongs with the expanded rules it depends on.

The v1 scope agreed on 24 August already points the same way: two rule sets only, with
character templates listed as post-launch. What is left to confirm is whether the blank sheet
that ships alongside them is this minimal one.

**A fillable PDF is explicitly a nice-to-have.** If the schedule allows it in early October,
good; if not, nothing is lost. It should not be on the critical path.

**Blocked behind it:** the print order on 8 October.

---

## 4. Which expansions matter first?

There are roughly 295,000 words of design notes across Jeff's folder and they disagree with each
other. `RPG dev notes.md` alone contains around fifteen different attribute schemes &mdash;
Body/Mind/Soul, Health/Fitness/Left-brain/Right-brain, STR/DEX/CON/INT/WIS/CHA,
Heart/Soul/Brains/Guts, and more.

Choosing between them is **authorship, not engineering**, and it is the single largest unbounded
cost in the project.

**The proposal, unchanged:** we build the machine that publishes chapters. Jeff decides which
version of each rule is canon and writes it. Chapters ship as they are finished rather than all
at once, so the launch never waits on the whole book.

**Our recommendation for what goes first: combat.** It is the thing convention players ask about
within the first five minutes, and it is the expansion most likely to be exercised in a
40-minute slot.

**What we need from Jeff:** does the split work? And which one or two expansions matter most for
the first six months?

---

## Already settled

Both of these were answered by Jeff on **24 August 2026** and stayed on the site as open
questions for weeks afterwards. The answers now live on the pages they belong to.

| Decision | Answer | Where it lives now |
| --- | --- | --- |
| Timaeus or Prota? | **Timaeus.** Prota was the working name for the same world, and is retired. | [The World](world/index.md) |
| Is the one-page ruleset frozen? | **Yes &mdash; frozen canon**, with a path to stewarded governance. `CODEOWNERS` names the owners, but branch protection is not on yet, so it is not enforced. | [Basic Rules](rules/index.md) |

## Closing a decision

When one is settled it comes off the list above, the answer goes into the page it came from, and
it gets a row down here. The count in the title should reach zero before the passphrase gate
comes off.

---
hide:
  - toc
---

# Open decisions <span class="dpd-status stub">6 open</span>

<div class="dpd-protobar" markdown>
**This page is the agenda, not the game.** Every unresolved question on the site is collected
here so nobody has to tour the whole thing to find them. It comes down before launch.
</div>

Six decisions are open. Four are Jeff's alone, and two of them should be closed on **Thursday 10
September** because other work is waiting behind them.

Each one below says what it blocks and what we'd recommend. The recommendation is a starting
position to argue with, not a conclusion.

## At a glance

| # | Decision | Blocks | Decide by |
| --- | --- | --- | --- |
| 1 | [Is the Narrator's guide free?](#1-is-the-narrators-guide-free) | The licence boundary, permanently | **Before Jeff writes it** |
| 2 | [What is the Narrator called?](#2-what-is-the-narrator-called) | Terminology pass, printed kit | **10 Sep** |
| 3 | [Timaeus or Prota?](#3-timaeus-or-prota) | The World section, con demo | **10 Sep** |
| 4 | [Is the one-page ruleset frozen?](#4-is-the-one-page-ruleset-frozen) | What contributors may change | 17 Sep |
| 5 | [How far does the character sheet go?](#5-how-far-does-the-character-sheet-go) | Print order | 24 Sep |
| 6 | [Which expansions matter first?](#6-which-expansions-matter-first) | Nothing for launch | 24 Sep |

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

## 3. Timaeus or Prota?

There are two setting names in the source material and they appear to describe the same kind of
place. **Timaeus** is the folder &mdash; 33 files, about 91,000 words. **Prota** is named in
`What is Free Worlds.md`: *"Prota, the first setting for Free Worlds which is included here."*

**Our recommendation: keep the name Timaeus, and ship v1 rules-only.**

Two separate calls, and they pull in different directions, so they're worth taking separately:

- **The name.** Timaeus is the Plato dialogue that assigns the Platonic solids to the elements.
  That means the five dice *are* the five elements &mdash; the mechanic and the cosmology are
  the same object. That is a genuinely good piece of design, it is already the best visual idea
  on the home page, and Prota does not do any of that work.
- **The scope.** 91,000 words of outlines and fragments is not five weeks of work. Shipping
  rules-only keeps v1 finishable, and it makes the "runs any genre" promise concrete rather than
  theoretical. The cost is showing up at a convention with no world to demo &mdash; which is
  survivable, because the one-shot scenario does that job instead.

**What we need from Jeff:** are they the same world? If yes, the name question is easy. If
they're two different settings, that's a longer conversation and it should not happen before
October.

---

## 4. Is the one-page ruleset frozen?

Everything else on this site is designed to expand. The one page is the promise that the game
stays learnable in one sitting &mdash; which only holds if it stops changing.

**Our recommendation: freeze it at v1.0, with explicit versioning.** Changes require a
deliberate version event with a date, not an edit. Expansions stay editable; the core does not.

This is what makes "backwards compatible forever" mean something rather than sound nice. It is
also what makes the game safe to fork: someone can build on v1.0 knowing the ground will not
move. And it gives contributors a clear answer about what they may send a pull request against
&mdash; which `CONTRIBUTING.md` currently cannot tell them.

**Blocked behind it:** the contributor guidance, and the versioning note on the rules page.

---

## 5. How far does the character sheet go?

The current draft covers exactly what the one-page rules require and no more. Jeff's
`Character resume.md` runs to 30,000 characters and describes a much richer document &mdash;
point-buy, training, backgrounds-as-organizations.

**Our recommendation: ship the minimal sheet for v1.** It is already drafted, it matches the
one-page rules exactly, and a convention player fills it in during the first two minutes of a
40-minute slot. The full CV is a v2 document that belongs with the expanded rules it depends on.

**A fillable PDF is explicitly a nice-to-have.** If the schedule allows it in early October,
good; if not, nothing is lost. It should not be on the critical path.

**Blocked behind it:** the print order on 8 October.

---

## 6. Which expansions matter first?

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

## Closing a decision

When one is settled, it comes off this page and the answer goes into the page it came from. The
count in the title above should reach zero before the passphrase gate comes off.

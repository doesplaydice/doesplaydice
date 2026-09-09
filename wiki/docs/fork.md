---
hide:
  - toc
---

# Take it

<p class="dpd-lede-sm">This page is not a formality. It is the reason the game exists in this
form, and it is meant to be used.</p>

## Why this page is here

In January 2023, Wizards of the Coast attempted to revoke the Open Gaming Licence &mdash; the
agreement the tabletop industry had built on for twenty years. Games that thousands of people
were actively playing were, briefly, at the mercy of a decision made in a boardroom.

Does Play Dice is Jeff Adams's answer to that. The point is not that the rules are free to read.
The point is that **nobody can take them back** &mdash; not a publisher, not a future owner, not
Jeff.

That claim is only worth something if you can check it. So: here is how to take the whole thing.

## What you are allowed to do

The text of this site is licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
In plain terms:

<div class="dpd-fork-grid" markdown>

<div class="dpd-fork-yes" markdown>
### You may

- **Copy it.** All of it, anywhere.
- **Change it.** Rewrite any rule. Contradict us.
- **Sell it.** Print it, bundle it, charge whatever you like.
- **Build on it.** Adventures, settings, apps, translations.
- **Keep your version closed** if you want to. There is no share-alike clause.
- **Do all of the above forever.** The licence is irrevocable.
</div>

<div class="dpd-fork-no" markdown>
### You must

- **Give credit.** Say the game is based on Does Play Dice by Jeff Adams, link the licence, and
  note if you changed things.
- **Use your own name.** *Does Play Dice* and the logo are held as trademarks and are **not**
  covered by the licence. That is deliberate: it is what stops someone shipping a different game
  under this name and confusing players &mdash; the same arrangement Ubuntu and Canonical use.
</div>

</div>

!!! quote "The attribution line, if you want one ready-made"

    Based on [Does Play Dice](https://doesplaydice.com) by Jeff Adams, licensed
    [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Changes were made.

## How to actually do it

This site is deliberately boring underneath: plain Markdown files in git, built by a static
site generator. There is no database, no server, nothing that only we can run. That is what
makes the promise real rather than rhetorical.

<div class="dpd-forksteps" markdown>

**1. Fork the repository.**
[github.com/doesplaydice/doesplaydice](https://github.com/doesplaydice/doesplaydice) &rarr; Fork.
You now have every word of the game, its full history, and the machinery that publishes it.

**2. Rename it.**
Change `site_name` in `wiki/mkdocs.yml` and the wordmark on the home page. This is the one step
that is not optional &mdash; the name is a trademark and it is not yours.

**3. Turn on Pages.**
Settings &rarr; Pages &rarr; Source: GitHub Actions. The workflow is already in the fork.

**4. Push.**
Your copy is live in about a minute, at your address, under your name, building from your
markdown. Nothing points back at us.

</div>

!!! success "That is the whole thing"

    No permission to ask. No key we hold. If this site vanished tomorrow, every fork keeps
    working, and the game survives in as many copies as people cared to make.

## If you would rather not use git

The licence does not require a GitHub account.

- [Download the full book as a PDF](../downloads/does-play-dice-book.pdf) &mdash; rules, character
  sheet, expansions, setting and narrator guidance in one document.
- [Download the one-page rules](../downloads/does-play-dice-rules.pdf) &mdash; the complete game on
  a single sheet.
- Print either one, photocopy it, hand it out. That is a fork too. It is just made of paper.

## We would like to know, but you do not owe us that

If you build something, [tell us](community/index.md) and we will link it. If you would rather
not, that is entirely your right, and the licence says so.

The measure of whether this worked is not how many people come back here. It is how many
versions of this game exist that we never hear about.

# Make it yours

The short version: **the whole game is yours to take.** Only the name and logo stay with us. This page explains what that means, and
how to do it.

## The text

Everything written on this site — the rules and the examples — is
**Does Play Dice**, licensed
<a href="https://creativecommons.org/licenses/by/4.0/" rel="license">CC BY 4.0</a>.

You can copy it, change it, print it, teach from it, and sell what you make from
it. You do not need permission and you do not owe anyone money. The license is
irrevocable: it cannot be taken back later, by us or by anyone who looks after
the project in future.

<div class="dpd-fork-grid" markdown>

<div class="dpd-fork-yes" markdown>
### You may

- **Copy it.** All of it, anywhere.
- **Change it.** Rewrite any rule. Contradict us.
- **Sell it.** Print it, bundle it, charge whatever you like.
- **Build on it.** Adventures, settings, apps, translations.
- **Keep your version closed** if you want to. There is no share-alike clause.
- **Do all of the above forever.** The license is irrevocable.
</div>

<div class="dpd-fork-no" markdown>
### You must

- **Give credit.** Say the game is based on Does Play Dice, link the license, and
  note if you changed things.
- **Use your own name.** *Does Play Dice* and the logo are held as trademarks and are **not**
  covered by the license. See [What is not covered](#what-is-not-covered).
</div>

</div>

The one condition is credit. Something like this is enough:

> Based on <a href="https://doesplaydice.com">Does Play Dice</a>,
> licensed <a href="https://creativecommons.org/licenses/by/4.0/" rel="license">CC BY 4.0</a>.
> Changes were made.

## No half measures

Many open game licenses only open up parts of a game. Both the OGL and the ORC license, for
example, split a game in two: open rules on one side, and on the other a closed list of "product
identity" or "reserved material." Iconic monsters, named NPCs and spells, campaign settings, and
artwork stay behind that wall.

**We don't split the game.** The only things held back are the name *Does Play Dice* and its
logo. Everything else is CC BY:

- the rules, and every example of them
- spells, skills and character templates
- story guides, their pregenerated characters, handouts and maps
- every download, and every page of this site
- the campaign setting, when it's released

You can keep your own work closed if you want to. We're not keeping ours.

## What is not covered

**The name "Does Play Dice" and the Does Play Dice logo are excluded.** They are
held as marks and are not part of the CC BY grant.

This is the one piece of deliberate friction in an otherwise open license, and
it exists for a specific reason: it means anyone can publish their own version
of these rules, but nobody can publish a *different* game under this game's
name. Call your version whatever you like, say what it is based on, and you are
well inside the line.

## Why this license

We wanted a license that was **familiar, tested and well supported**, and not one written
for a single industry. Creative Commons licenses are used across publishing, education, music
and the arts. Writers, publishers and lawyers already know what they mean, so nobody has to
learn a new set of terms to build on this game. That's why we chose CC BY.

We left out share-alike on purpose. It would have required anyone building on the game to open
their own work too. That sounds protective, but it would block exactly what we want to see:
people earning a living from what they make.

## How to take it

This site is deliberately boring underneath: plain Markdown files in git, built by a static
site generator. There is no database, no server, nothing that only we can run. That is what
makes the promise real rather than rhetorical.

<div class="dpd-forksteps" markdown>

**1. Fork the repository.**
[github.com/doesplaydice/doesplaydice](https://github.com/doesplaydice/doesplaydice) &rarr; Fork.
You now have every word of the game, its full history, and the machinery that publishes it.

**2. Rename it.**
Change `site_name` and the footer in `wiki/mkdocs.yml`, the logo in
`wiki/overrides/partials/masthead.html`, and the app name in `wiki/docs/manifest.webmanifest`.
This is the one step that is not optional &mdash; the name is a trademark and it is not yours.

**3. Turn on Pages.**
Settings &rarr; Pages &rarr; Source: GitHub Actions. The workflow is already in the fork.

**4. Push.**
Your copy is live in about a minute, at your address, under your name, building from your
markdown. Nothing points back at us.

</div>

!!! success "That is the whole thing"

    No permission to ask. No key we hold. If this site vanished tomorrow, every fork keeps
    working, and the game survives in as many copies as people cared to make.

### If you would rather not use git

The license does not require a GitHub account.

- <a href="../downloads/does-play-dice-book.pdf">Download the full book as a PDF</a> &mdash; the
  rules and the character sheet in one document.
- <a href="../downloads/does-play-dice-rules.pdf">Download the core rules</a> &mdash; one
  printable sheet.
- Print either one, photocopy it, hand it out. That is a fork too. It is just made of paper.

## We would like to know, but you do not owe us that

If you build something,
[tell us](https://github.com/doesplaydice/doesplaydice/issues). If you would rather not, that
is entirely your right, and the license says so.

The measure of whether this worked is not how many people come back here. It is how many
versions of this game exist that we never hear about.

## Built with

The site is a static one, and it makes no third-party requests — everything
below is served from this domain.

| What | License |
| --- | --- |
| [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) | MIT |
| [MkDocs](https://www.mkdocs.org/) | BSD 2-Clause |
| Archivo Black, Literata, Familjen Grotesk, JetBrains Mono | SIL Open Font License 1.1 |

Designed and built by <a href="https://llamassist.ai">Llamassist</a>.

# Contribute <span class="dpd-status stub">Needs decisions</span>

<div class="dpd-protobar" markdown>
**This page can't be written until three questions are answered.** They're below. This is the
page where Jeff's actual motivation for the whole project lives, so it's worth getting right.
</div>

> *"I have a vendetta against the Open Gaming License, and it's a problem to me that anyone can
> play chess, but not anyone can play D&D without buying an encyclopedia set of rule-books."*
>
> — Jeff, Actuator notebook, Week 0

The point of this project is that the game belongs to the people who play it. Write rules,
settings, adversaries, adventures, art — and keep what you make.

## How editing actually works

Two doors, which is what Jeff asked for on the call: *"go to the website and click a download
link, or if they are savvy, go to the GitHub site and mirror or fork."*

<div class="grid cards" markdown>

-   :material-pencil: **The easy door**

    ---

    Every page has an edit pencil in the top right. Click it, type, save. The site rebuilds
    itself and publishes in about a minute. No install, no command line.

    Or use the full editor at <a href="../admin/" target="_blank" rel="noopener"><code>/admin/</code></a>
    &mdash; sign in, write, and your change becomes a pull request automatically.

    This is also **how Jeff maintains the site** — it's the answer to "something I could easily
    update."

-   :material-source-fork: **The savvy door**

    ---

    The whole site is plain markdown files in a git repository. Clone it, fork it, mirror it,
    edit it in Obsidian, send a pull request. Nothing here is locked up.

</div>

---

## Three decisions block this page

!!! decision "1. Which license?"

    "Open source" means something specific for **software** and something different for a
    **game text**. MIT and GPL are the wrong shape for a book. The real options:

    | License | What it means here |
    | --- | --- |
    | **CC0** | Public domain. Anyone does anything, no credit required |
    | **CC BY** | Anyone does anything, must credit you |
    | **CC BY-SA** | Anyone does anything, must credit you, **and derivatives must stay equally open** (copyleft) |
    | **ORC License** | Purpose-built for TTRPGs post-OGL, backed by Paizo and others. Irrevocable by design — which is the specific thing the OGL crisis proved matters |

    Jeff's own table of contents says **"Copyleft"** — but copyleft constrains exactly the
    commercial add-on ecosystem he says he wants: *"I want people to be able to earn a living
    and to make money for their art and their contributions."* Under CC BY-SA, a paid module
    may have to be released under the same open terms.

    **That tension has to be resolved by Jeff, and only Jeff.** He's the lawyer, it's his
    vendetta, and it's the most consequential irreversible decision in the project.

!!! decision "2. What's the trademark position?"

    The standard model — the one Wizards and Paizo both use — is **free text, defended name**.
    The rules are open; the logo and the name are not. That's what lets you keep quality
    control over what calls itself official while the game itself stays genuinely free.

    **Questions for Jeff:** do you want a defended mark? Under which name (see the naming
    decision on the home page)? And does a compatibility badge exist — an "works with Does Play
    Dice" logo third parties can use under stated conditions?

!!! decision "3. Who owns canon?"

    Jeff said two things on the call that pull in opposite directions:

    - *"I don't want to be the sole person responsible for it. I want people to help out and to implement their own ideas."*
    - Everything must stay **backwards compatible** with the one page, forever.

    Those can both be true, but only with an explicit rule about what the community can change:

    - **Open core** — pull requests can alter the basic rules. Maximum community ownership, and the compatibility promise is only as strong as review.
    - **Frozen core, open everything else** — the one page is Jeff's and it's versioned deliberately; the community expands freely around it. Protects the promise, but Jeff stays the bottleneck on the part he says he doesn't want to be sole owner of.
    - **Stewarded** — Jeff holds canon now, with a named path to handing it to a group later.

    **Question for Jeff:** which one? This decides what `CONTRIBUTING.md` says, what the pull
    request template asks, and whether a stranger can change the game.

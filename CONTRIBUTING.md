# Contributing

Thanks for wanting to add to this game.

> **OPEN DECISION.** The governance model below is written to work under either answer to
> "who owns canon," with the switch marked. It needs Jeff's decision before launch.
> See the [Contribute](wiki/docs/contribute/index.md) page.

## Two kinds of contribution

**Modules** &mdash; adventures, settings, adversaries, optional rules, tools. Anything that
*adds* without changing the one page. **The front door is open.** Write one, send it, it lands.

**Core rules** &mdash; the one page itself. A change here can invalidate every character, module
and adventure anyone has already made, so it goes through review and it will be slow. That's
deliberate, not gatekeeping.

## How to contribute

**Without git.** Go to `/admin/` on the site, sign in with GitHub, and edit in the browser. Your
change becomes a pull request automatically &mdash; you don't need to know what that means.

**Trying it locally.** `/admin/` also offers *Work with Local Repository*: pick the project
folder and the editor writes straight to the markdown on disk. No account, no server, no OAuth
&mdash; useful for demos and for editing on a plane.

**With git.** Fork, branch, edit the markdown under `wiki/docs/`, open a PR. The whole site is
plain markdown; there's nothing else to learn.

## The compatibility rule

This is the one hard rule, and it's the reason the game exists in this shape:

> Anything you write must work at a table that only knows the one page.

A new adversary, a new setting, a new optional subsystem &mdash; fine. A change that means
someone has to re-learn the basics, or that makes an existing character sheet wrong, is not.
If your idea needs the core to change, open an issue and make the case before writing code.

## Review

<!-- ===================================================================== -->
<!-- GOVERNANCE SWITCH -- pick one at launch and delete the others.        -->
<!--                                                                       -->
<!--  [ ] FROZEN CORE  Jeff is sole approver on wiki/docs/rules/index.md.  -->
<!--                   Enforce with CODEOWNERS + branch protection.        -->
<!--                   Modules merge on any maintainer approval.           -->
<!--                                                                       -->
<!--  [ ] OPEN CORE    Any maintainer can approve core changes.            -->
<!--                   Relax CODEOWNERS to the maintainer team.            -->
<!--                                                                       -->
<!--  [ ] STEWARDED    Jeff approves today; a named group inherits later.  -->
<!--                   Same as frozen core, plus a written succession doc. -->
<!-- ===================================================================== -->

Modules get a light read: does it work, is it clear, is it yours to give. Core changes get
argued about.

## What you keep

You keep authorship of what you write.

Contributions are accepted under the project's licence, **CC BY 4.0** &mdash; the same terms the
rest of the game uses. In practice that means anyone may reuse what you contribute, including
commercially, as long as they credit it. By opening a pull request you confirm the work is yours
to give.

See [NOTICE.md](NOTICE.md) for what the licence does and doesn't cover.

**Do not submit** text, stat blocks, art, or tables copied from other games. That includes
paraphrases close enough to be recognisable. This project's whole argument is that you shouldn't
need someone else's rulebook &mdash; borrowing from one would be a poor start.

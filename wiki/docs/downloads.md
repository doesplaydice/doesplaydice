# Download <span class="dpd-status stub">Wired, not filled</span>

<div class="dpd-protobar" markdown>
**The plumbing works; the files aren't generated yet.** This page exists because Jeff named it
specifically on the call — *"go to the website and click a download link"* — and because a URL
on a sticker needs somewhere to land.
</div>

Everything here is free. No account, no email address, no cart.

<div class="grid cards" markdown>

-   :material-file-pdf-box: **The one-page rules** — PDF

    ---

    The complete game on a single sheet. Print it, fold it, put it in the box with your dice.

    *Not yet generated.*

-   :material-clipboard-account: **Character Vitae** — PDF

    ---

    Printable and fillable character sheet.

    *Draft exists — see [Character Vitae](rules/character-vitae.md).*

-   :material-book-open-page-variant: **The full book** — PDF / EPUB

    ---

    Everything on this site, as one document.

    *Blocked on the table of contents decision.*

-   :material-github: **The source**

    ---

    Every page here as markdown, in git. Fork it, mirror it, make it yours.

    *Repo not created yet.*

</div>

---

## Convention kit <span class="dpd-status ready">Built</span>

Print-ready pieces for running a table at a convention, a library, or a coffee shop. Designed to
survive black-and-white printing.

<div class="grid cards" markdown>

-   :material-table-furniture: [**Table tent**](downloads/table-tent.pdf)

    ---

    The core mechanic standing on the table. Fold once; both faces read upright, so players on
    either side can see it without asking.

-   :material-account-group: **Six pre-generated characters**

    ---

    Ready to play with no character creation. The six cover every possible spread of three dice
    across three Skills, so no two players are alike.

-   :material-clipboard-text-outline: **One-shot frame**

    ---

    A Narrator's single-page planning sheet, with a post-session half for capturing what actually
    happened at the table.

-   :material-card-account-details-outline: **Handout cards**

    ---

    Ten per sheet, business-card size, with a QR to this site. The whole game in three lines.

</div>

**Download the kit**

| Piece | File |
| --- | --- |
| Table tent | [table-tent.pdf](downloads/table-tent.pdf) |
| Six pre-generated characters | [pregens.pdf](downloads/pregens.pdf) |
| One-shot frame | [scenario-frame.pdf](downloads/scenario-frame.pdf) |
| Handout cards | [handout.pdf](downloads/handout.pdf) |
| Playtest session brief | [session-brief.pdf](downloads/session-brief.pdf) |
| Player feedback slips | [feedback-slips.pdf](downloads/feedback-slips.pdf) |

*Sources and build script live in `kit/`. Run `./kit/build.sh` to regenerate.*

---

## How this works once it's live

The PDFs are **built from the same markdown as the website**, automatically, every time a page
changes. There's no separate document to maintain and no way for the printed rules to drift out
of sync with the site. Jeff edits one place.

!!! decision "OPEN DECISION — what does the sticker point at?"

    Jeff has business cards and stickers, and wants to hand people a URL that says *"it's ready
    to play and ready to contribute."*

    **Questions for Jeff:** should that URL land here, on the [rules](rules/index.md), or on the
    home page? Should there be a short memorable path — `doesplaydice.com/play` — that's easy
    to say out loud across a convention table? And is a QR code on the sticker worth it?

!!! decision "OPEN DECISION — Foundry and virtual tabletops"

    Jeff plays on **Foundry VTT** and said he eventually wants the rules built there so people
    can play online. He also said advanced players will look for the game *"on platforms that
    they're already familiar with."*

    That's a real piece of software — a Foundry system module, not a document — and it's a
    separate phase with its own cost. Worth scoping separately once v1 is out.

# Does Play Dice — wiki prototype

Prototype built 24 Aug 2026 for the strategy call with Jeff Adams.

## What this is

A working MkDocs Material site, built from Jeff's own material, to make the follow-up
conversation concrete. **It is a conversation prop, not a deliverable.**

It is deliberately **decision-neutral**: every unresolved question is rendered as a visible
`OPEN DECISION` block rather than silently answered. The table of
contents, the setting, and the governance model are all Jeff's calls. The prototype asks them;
it does not make them.

## What's real vs. placeholder

| Page | State |
| --- | --- |
| `rules/index.md` | **Real.** Jeff's finished one-pager, verbatim from doesplaydice.com |
| `rules/character-vitae.md` | **Draft.** Derived only from steps 5–7 of the basic rules |
| Everything else | **Containers.** Structure + decision prompts only |

## Run it

```
.venv/bin/mkdocs serve -f wiki/mkdocs.yml -a 127.0.0.1:8777
```

Or `preview_start` the `dpd-wiki` config in `.claude/launch.json`.

## Setup from scratch

```
python3 -m venv .venv && .venv/bin/pip install mkdocs-material
```

## Known considerations

- `repo_url` in `wiki/mkdocs.yml` is a **placeholder**. It drives the "edit this page" pencil,
  which is the demo of "Jeff can update it himself." Point it at a real repo before sharing.
- The Material team has posted a warning about MkDocs 2.0 being backwards-incompatible with all
  plugins and theme overrides. Worth factoring into the platform decision before committing.
- `files-from-jeff/Rules/Examples/` contains large verbatim excerpts of other publishers'
  content (PF2, 4e, Daggerheart, LotFP). Fine as private research; **must not** be pushed to a
  public repo.

## Source material

`files-from-jeff/` — ~295,000 words across 121 markdown files, ~15 years of notes.
Not modified. Not published.

---

## What else is in here

### `kit/` &mdash; convention kit

Print-ready pieces for running the game at a table: a table tent, six pre-generated characters,
a Narrator's one-shot frame, and handout cards with a live QR. Built for black-and-white
printing. `./kit/build.sh` renders them to PDF via headless Chrome. See
[kit/README.md](kit/README.md).

The table tent and one-shot frame are derived entirely from the published rules. The six
characters are **setting-neutral samples** to be replaced. The scenario itself is deliberately
blank &mdash; that's authorship.

### Contributor CMS

A git-backed editor at `/admin/` (Sveltia CMS, Decap-compatible). Contributors get a real
browser editor; every edit becomes a **pull request**, never a direct commit.

That design is what makes it decision-neutral on the governance question: the frozen-core versus
open-core lever lives in [.github/CODEOWNERS](.github/CODEOWNERS) plus branch protection, **not**
in the CMS config. Answer the question, flip CODEOWNERS, nothing else changes.

To try it with no GitHub account: open `/admin/` and choose *Work with Local Repository*.

### CI

[.github/workflows/publish.yml](.github/workflows/publish.yml) builds every pull request with
`--strict` (so a broken link fails before review) and deploys `main` to GitHub Pages. This is
what makes "click the pencil, it's live in a minute" true.

### Repository

[`doesplaydice/doesplaydice`](https://github.com/doesplaydice/doesplaydice), owned by the
**doesplaydice** organization. Public, licensed CC BY 4.0.

### One real unknown still marked REPLACE-ME

- **The CMS OAuth broker URL** in `wiki/docs/admin/config.yml` — a small Cloudflare Worker that
  has to be deployed before browser sign-in works. Until then, `/admin/` still works locally via
  *Work with Local Repository*.

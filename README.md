# Does Play Dice

A storytelling game that's free to download, quick to learn, and only limited by your
imagination. This repository is the source of [doesplaydice.com](https://doesplaydice.com).

Does Play Dice is licensed [CC BY 4.0](LICENSE). The name and logo are held back
as marks; see [NOTICE.md](NOTICE.md) and the [license page](https://doesplaydice.com/license/).

## What's in here

- `wiki/` &mdash; the site, as plain markdown under `wiki/docs/`, built with
  [MkDocs Material](https://squidfunk.github.io/mkdocs-material/).
- `kit/` &mdash; print-ready pieces for running the game at a table: a table tent, pre-generated
  characters, a one-shot frame and handout cards. See [kit/README.md](kit/README.md).
- `tools/` &mdash; the checks CI runs on every pull request, and the PDF builder.

## Run it

```
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/mkdocs serve -f wiki/mkdocs.yml -a 127.0.0.1:8777
```

## Contribute or fork

Every page has an edit pencil that turns your change into a pull request. Or fork this repository and edit the markdown directly. See
[CONTRIBUTING.md](CONTRIBUTING.md), and the [license page](https://doesplaydice.com/license/) for how
to fork it.

Pull requests are built with `--strict`, so a broken link fails before review. Merges to `main`
deploy to GitHub Pages.

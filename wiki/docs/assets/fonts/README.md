# Self-hosted fonts

These are served from this repository so the site makes **no third-party
requests**. Nothing about the site depends on Google staying up, or on a
visitor's browser being allowed to reach it.

- **Open Sans** -- variable weight 300-700, roman and italic. One file per style.
- **IBM Plex Mono** -- 400 and 500.
- latin and latin-ext subsets only.

Both are under the SIL Open Font License, which permits redistribution.

Declarations live in `../stylesheets/fonts.css`. To refresh, re-download the
woff2 files Google Fonts serves for:

```
https://fonts.googleapis.com/css2?family=Open+Sans:ital,wght@0,300..700;1,300..700&family=IBM+Plex+Mono:wght@400;500&display=swap
```

(request it with a modern browser user-agent, or you get ttf instead of woff2)
and keep the `unicode-range` values in step.

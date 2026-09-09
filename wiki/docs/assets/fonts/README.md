# Self-hosted fonts

Served from this repository so the site makes **no third-party requests**.
Nothing here depends on Google staying up, or on a visitor's browser being
allowed to reach it.

| Family | Role | Notes |
| --- | --- | --- |
| **Archivo Black** | Display — wordmark, page titles | Single weight by design |
| **Literata** | Body prose, ledes | Variable 400–600, plus italic |
| **Familjen Grotesk** | UI — nav, buttons, labels, tables | Variable 400–700 |
| **JetBrains Mono** | Kickers, numbers, filenames | Variable 400–700 |

All four are SIL Open Font License, which permits redistribution.
latin and latin-ext subsets only.

Declarations live in `../stylesheets/fonts.css`. To refresh, request this from
Google Fonts **with a modern browser user-agent** (otherwise you get ttf, not
woff2), download each woff2, and keep the `unicode-range` values in step:

```
https://fonts.googleapis.com/css2?family=Archivo+Black&family=Literata:ital,opsz,wght@0,7..72,400..600;1,7..72,400&family=Familjen+Grotesk:ital,wght@0,400..700;1,400..700&family=JetBrains+Mono:wght@400..700&display=swap
```

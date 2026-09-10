# Handoff checklist

Things that are true only because this project is still being built by
Llamassist, and that must be undone when Jeff takes it over.

Each one is a deliberate, temporary loosening. None of them should outlive the
build phase. They are written down here because the failure mode is not that
someone objects — it is that everyone forgets, and a temporary exception
quietly becomes the permanent state.

## 1. Andrei's direct-push bypass — REMOVE AT HANDOFF

The `Canon review` ruleset requires a pull request for every change to `main`,
and requires a code owner's approval for files listed in `.github/CODEOWNERS`
— which is what makes Jeff's one-page rules genuinely frozen.

The **`build-phase` team bypasses that rule**, and Andrei (`amatei`) is its only
member. He can still push directly to `main` while the site is being built.

**What this does and does not protect.** It protects the frozen rules from
everyone except Andrei — which is the actual threat model today, since the
people who will start proposing rule changes are strangers at Carnage Con. It
is a governance control, not a security control: Andrei is a repository admin
and could remove the ruleset anyway, so the bypass does not lower the ceiling.

**To remove it:**

```sh
gh api -X DELETE orgs/doesplaydice/teams/build-phase/memberships/amatei
gh api -X DELETE orgs/doesplaydice/teams/build-phase
```

Deleting the team is enough; the ruleset then applies to everybody, Andrei
included, with no other change.

`tools/preflight.py` reports this bypass every time it runs, so it cannot go
quiet.

## 1b. HTTPS enforcement — WAITING ON GITHUB, not on us

**Status 2026-09-10: escalate. Everything we can do has been done.**

The apex works and will keep working. `https://doesplaydice.com` serves a valid
Let's Encrypt certificate (issued 8 Sep, expires 7 Dec) and returns 200. What is
missing is `www`, and `https_enforced`, which GitHub will not let us set while
the certificate state is `dns_changed`.

**The finding that settles it:** the Pages API's `https_certificate.domains`
array lists *only* the apex. GitHub is not requesting a certificate for `www` at
all, so this was never a validation failure we could fix by correcting records.

```
apex A         185.199.108.153 .109.153 .110.153 .111.153     correct
www CNAME      doesplaydice.github.io.                        correct, explicit record
CAA            none on apex; via www CNAME, github.io's own — permits letsencrypt
AAAA           none on apex; www inherits GitHub's IPv6
cert state     dns_changed          (unchanged since 2026-09-08)
cert covers    ["doesplaydice.com"]  <- www never requested
pages status   null
org verified   false; protected_domain_state null
```

Verified 2026-09-10 and all clean: four independent public resolvers (`8.8.8.8`,
`1.1.1.1`, `9.9.9.9`, `208.67.222.222`) all return the `www` CNAME, the CNAME
target resolves to the four Pages IPs, `www` is an explicit record rather than a
wildcard artefact, and `http://www` returns a clean `301` to the apex from
`Server: GitHub.com`. So GitHub receives `www` traffic and answers it. It simply
never asks for a certificate covering it.

### What has been tried, and did not work

- **Removing and re-adding the custom domain.** Done twice on 2026-09-09 and a
  third time on 2026-09-10 (Andrei's call, knowing this note advised against it —
  it was worth one attempt against the current DNS). State returned to
  `dns_changed` and stayed there through 60 minutes of polling at 3-minute
  intervals. The apex stayed up and served valid HTTPS throughout. **Do not do
  this a fourth time.**
- **Re-running the Pages deployment** to completion, in case a fresh deploy would
  re-trigger DNS evaluation. Succeeded; no change to state, `domains`, or
  `status`.

### Next step

Open a GitHub Support ticket. The write-up is ready to paste, with every command
and its output: **`GITHUB-PAGES-CERT-TICKET.md`** in this directory.

Lead with the `domains` array. There are really two anomalies and that is the
stronger one — even if GitHub's answer on `www` is "we no longer add that
automatically", a `dns_changed` state persisting for days against correct, stable
DNS still needs fixing, because it is what blocks enforcement.

### Deliberately NOT tried

Temporarily setting the custom domain to `www.doesplaydice.com` to force
provisioning, then switching back. The downside is asymmetric: the apex currently
has a working certificate, and this could end with a www-only certificate and a
broken apex — a worse position weeks before the con. It is also exactly what
support can do safely from their side. Keep it as the fallback if the ticket
stalls.

Once the state clears:

```sh
gh api -X PUT repos/doesplaydice/doesplaydice/pages -F https_enforced=true
```

Impact while it waits: narrow. Typing `www` without a scheme still lands safely,
because it redirects to the apex over http first. Only someone who explicitly
types `https://www.` gets a warning.

### Separately: the wildcard

`*.doesplaydice.com CNAME doesplaydice.com.` still exists (a Fastmail default).
It is **not** what breaks the certificate — `www` has its own record, which wins
— but it does mean every mistyped subdomain silently serves the site. Worth a
decision with Jeff. **Whoever goes into that DNS panel must leave the MX records
alone** (Fastmail, `messagingengine.com`).

## 2. The pre-launch passphrase gate — REMOVE AT LAUNCH

Bracketed with `GATE START` / `GATE END` markers in
`wiki/overrides/main.html`, plus the `#dpd-gate` rules in `extra.v3.css` and
the duplicated hash in `wiki/docs/admin/index.html`.

**Do not delete `wiki/overrides/` or drop `custom_dir`** — that file also
carries the permanent installable/offline head tags, and deleting it would take
offline support down with the gate.

## 3. `wiki/docs/robots.txt` — DELETE AT LAUNCH

It currently says `Disallow: /`. Correct while private. If it ships, the
launched site is invisible to every search engine and nothing looks broken.

## 4. The planning pages — TAKE OUT OF THE NAV AT LAUNCH

`Launch plan` and `Open decisions` say on their own face that they come down.

---

Run `python3 tools/preflight.py` before going public. It checks all of the
above and exits non-zero while any blocker remains.

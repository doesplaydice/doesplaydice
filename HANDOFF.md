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

Everything on our side and Jeff's side is correct. GitHub has not reissued the
certificate. Checked 2026-09-09, roughly six hours after the DNS fix:

```
apex A       185.199.108.153 .109.153 .110.153 .111.153   (correct)
www CNAME    doesplaydice.github.io.                       (correct, added by Jeff)
CAA          none on apex; www inherits GitHub's, which permits letsencrypt.org
AAAA         none on apex; www inherits GitHub's IPv6
Pages cname  doesplaydice.com
cert state   dns_changed
cert covers  ["doesplaydice.com"]     <- no www SAN, which is what blocks enforcement
```

Ruled out as causes: a CAA record forbidding Let's Encrypt, a stray IPv6 answer,
the ACME challenge path being unreachable, and the old wildcard shadowing `www`.
`www` itself works -- it 301s to the apex over http and lands on 200. It simply
has no certificate of its own.

**Do not remove and re-add the custom domain again.** That was done twice on
2026-09-09; each attempt restarts GitHub's own clock rather than advancing it.

**If it is still `dns_changed` after 24 hours from 2026-09-09 12:45 CDT**, open a
GitHub Support ticket and paste the block above. Then:

```sh
gh api -X PUT repos/doesplaydice/doesplaydice/pages -F https_enforced=true
```

Impact while it waits: none for visitors. `https://doesplaydice.com` serves
normally with a valid certificate. What is missing is the `www` variant over TLS
and the automatic http-to-https redirect.

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

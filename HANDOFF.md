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

## 1b. HTTPS enforcement — DONE 2026-09-28

The `www.doesplaydice.com` certificate problem is fixed, and **Enforce HTTPS is
on** (Jeff enabled it in Settings > Pages on 2026-09-28).

From 2026-09-08, GitHub's Pages certificate covered only the apex, and the Pages
API reported `https_certificate.state: dns_changed` against DNS that was correct.
Because of that stuck state, `https_enforced` could not be set. Removing and
re-adding the custom domain three times did not help, and neither did re-running
the deployment. The problem cleared on 2026-09-28. That day an HTTPS request to
`www` completed a verified handshake, where 45 minutes earlier it had failed with
a hostname mismatch.

If it ever recurs, `tools/preflight.py` checks the Pages certificate state and
`https_enforced`, and says what to do. The DNS the fix relies on is:

```
apex A         185.199.108.153 .109.153 .110.153 .111.153
www CNAME      doesplaydice.github.io.     (explicit record — keep it)
```

Do not temporarily switch the custom domain to `www` to force provisioning. It
risks leaving the apex without a certificate.

### Still open: the wildcard

`*.doesplaydice.com CNAME doesplaydice.com.` still exists (a Fastmail default).
It did not cause the certificate problem — `www` has its own record, which wins
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

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

# note

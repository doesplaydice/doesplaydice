# GitHub Pages: certificate never includes `www`, stuck in `dns_changed`

**Repo:** `doesplaydice/doesplaydice` (public, org-owned)
**Custom domain:** `doesplaydice.com` (apex)
**Evidence gathered:** 2026-09-10, ~09:40 UTC

## Summary

The apex certificate is issued and working. `www` has correct, authoritative DNS
but has never been added to the certificate, and the Pages API has reported
`dns_changed` continuously for roughly two days — including through a full
remove-and-re-add of the custom domain followed by an hour of polling.

The API shows GitHub is not *requesting* `www` at all, so this does not look like
a validation failure on our side.

## What the API reports

```
GET /repos/doesplaydice/doesplaydice/pages
{
  "cname": "doesplaydice.com",
  "status": null,
  "protected_domain_state": null,
  "pending_domain_unverified_at": null,
  "https_certificate": {
    "state": "dns_changed",
    "description": "Detected a change to DNS settings. Requesting a new certificate.",
    "domains": ["doesplaydice.com"],
    "expires_at": "2026-12-07"
  },
  "https_enforced": false
}
```

`domains` contains only the apex. `www.doesplaydice.com` is absent.

`GET /repos/doesplaydice/doesplaydice/pages/health` returns `200` with an empty
body `{}`.

## The live certificate

```
issuer=C=US, O=Let's Encrypt, CN=YR1
notBefore=Sep  8 20:54:04 2026 GMT
notAfter=Dec  7 20:54:03 2026 GMT
X509v3 Subject Alternative Name:
    DNS:doesplaydice.com
```

Single SAN. `https://doesplaydice.com` returns 200 and verifies cleanly.
`https://www.doesplaydice.com` fails verification (no certificate covers it).

## DNS, read from the authoritative nameservers

Nameservers are `ns1.messagingengine.com` / `ns2.messagingengine.com` (Fastmail).

```
$ dig @ns2.messagingengine.com www.doesplaydice.com CNAME +noall +answer
www.doesplaydice.com.  3600  IN  CNAME  doesplaydice.github.io.

$ dig +short doesplaydice.com A
185.199.108.153  185.199.109.153  185.199.110.153  185.199.111.153
```

The `www` record is explicit, not a wildcard artefact. A wildcard
`*.doesplaydice.com CNAME doesplaydice.com.` does exist, but `www` has its own
record, which takes precedence:

```
$ dig +short zzz-does-not-exist-9f3a.doesplaydice.com CNAME
doesplaydice.com.
$ dig +short www.doesplaydice.com CNAME
doesplaydice.github.io.
```

## CAA is not blocking issuance

The apex publishes no CAA records. The CAA visible through the `www` CNAME is
`github.io`'s own, and it permits Let's Encrypt for both `issue` and `issuewild`:

```
0 issue "letsencrypt.org"
0 issuewild "letsencrypt.org"
0 issue "digicert.com"
0 issuewild "digicert.com"
0 issue "sectigo.com"
0 issuewild "sectigo.com"
```

## GitHub is serving `www` correctly at the HTTP layer

```
$ curl -sI http://www.doesplaydice.com/
HTTP/1.1 301 Moved Permanently
Server: GitHub.com
Location: http://doesplaydice.com/
```

So `www` traffic reaches GitHub and GitHub answers it — it simply has no
certificate. The ACME challenge path on `www` also 301s to the apex:

```
$ curl -sI http://www.doesplaydice.com/.well-known/acme-challenge/probe-token
301 -> http://doesplaydice.com/.well-known/acme-challenge/probe-token
```

## What we already tried

- Removed the custom domain via `PUT /repos/.../pages` with `{"cname": null}`,
  then immediately re-added `{"cname": "doesplaydice.com"}`. State returned to
  `dns_changed` and stayed there for 60 minutes (polled every 3 minutes, 20
  samples, no change). The apex stayed up and served valid HTTPS throughout.
- Confirmed the `www` record predates the re-add, so it was present when the
  domain was re-verified.
- Ruled out org domain verification: the org's `is_verified` is `false` and
  `protected_domain_state` is `null`.
- Re-ran the Pages deployment workflow to completion (`success`), in case a fresh
  deployment would re-trigger DNS evaluation. No change: `state` is still
  `dns_changed`, `domains` still lists only the apex, and `status` is still `null`.
- Confirmed the DNS is not a propagation or resolver problem. Four independent
  public resolvers (`8.8.8.8`, `1.1.1.1`, `9.9.9.9`, `208.67.222.222`) all return
  `www.doesplaydice.com CNAME doesplaydice.github.io.`, the CNAME target resolves
  to the four Pages IPs, and there is no stray `AAAA` on the apex.

## What we are asking

Please re-trigger certificate provisioning for this Pages site so that the
request includes `www.doesplaydice.com` alongside the apex.

## Why it matters to us

The site launches publicly at a convention on 16 October 2026. Anyone typing
`https://www.doesplaydice.com` currently gets a certificate warning.

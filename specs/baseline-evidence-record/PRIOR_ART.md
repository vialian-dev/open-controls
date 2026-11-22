# Prior art

Draft 0.1 applies established techniques to the governance of an approved business baseline.

| Existing tool or practice | What it solves | What it does not solve | Draft contribution |
|---|---|---|---|
| `sha256sum` | Content digest | Metric meaning, owner, approval, revision governance and trusted time | Baseline governance semantics and evidence references |
| Signed Git tag | Signed revision reference | Trusted creation time, truthful source data and benefits semantics | Versioned decision record |
| RFC 3161 | Trusted assertion that a digest existed before a time | Business meaning, metric quality and owner | Future optional trusted-time anchor |
| Sigstore/Rekor | Transparency and append-only evidence | Benefits-baseline semantics and approval rationale | Future optional anchor |
| in-toto/SLSA | Provenance and signed claims | Business baseline, owner and realized benefit | Future evidence-profile compatibility |
| Benefits-management guidance | Need for a pre-implementation baseline | Machine-readable interoperable record | Draft profile, schema, revision protocol and example |

# AI-development attestation

| Field | Record |
|---|---|
| Release candidate | Baseline Evidence Record Profile Draft 0.1: the commit tagged `baseline-evidence-record-draft-0.1`. |
| Canonical platform | GitHub. |
| Verification | Local CI checks passed. Two independent pre-publication reviews were conducted using different AI providers. The maintainer prepared and verified the release candidate with AI assistance. |
| Maturity | Level 0. No independent external practitioner review has been recorded. |
| Publication approval | Approved on 2026-11-22. The maintainer recorded the decision to publish this release candidate with the documented [limitations](KNOWN_LIMITATIONS.md). |

## Scope and results

The review covered the JSON Schema, synthetic examples, artifact digests, documentation and local CI checks. Candidate validation passed locally on Python 3.12: schema validation, two positive examples, nine negative examples and their repairs, exact-byte SHA-256 checks for three artifacts, and local Markdown links. The strict JSON loader rejected duplicate keys in schema and example checks. The release tree scan found no personal names or addresses identified by the review and no private references flagged for removal.

Release verification is separate from the maintainer's approval. Verify hosted CI, including fixture integrity on Linux, Windows and macOS, and confirm the active tag ruleset. From a clean clone, verify the tagged schema URL and exact-byte SHA-256. Record the full commit SHA and verification results in the release notes. See the [AI-development disclosure](AI-DEVELOPMENT-DISCLOSURE.md) and [local validation commands](../../CONTRIBUTING.md).

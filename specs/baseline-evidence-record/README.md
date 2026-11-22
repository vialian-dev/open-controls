# Baseline Evidence Record Profile: Draft 0.1

Draft status: This profile is a public draft for review (Draft 0.1). Draft status is separate from the software licence; the repository remains MIT licensed.

Canonical platform: GitHub. Release reference: `baseline-evidence-record-draft-0.1`.

Maturity: Level 0. An independent external practitioner review has yet to be recorded.

Preserve the approved before-state for an AI-enabled or operational change while the evidence is still available. Start with the example to see what a decision owner preserves, then use the profile and review questions to assess the baseline and its revision history.

## Profile and example

- [Profile and revision protocol](PROFILE.md)
- [JSON Schema, Draft 2020-12](schema/baseline-evidence-record.schema.json)
- [Complete JSON record](examples/baseline-v1.json)
- [Valid pending draft with empty metrics and sources](examples/baseline-draft.json)
- [Aggregate sample CSV](examples/baseline-aggregates.csv)
- [Manually prepared illustrative report](examples/baseline-report.example.md)
- [SHA-256 sidecar for baseline-v1.json](examples/baseline-v1.sha256). The digest covers the exact preserved JSON bytes: UTF-8, no BOM, LF line endings, a final newline and exact formatting. Reformatting or reordering keys changes the hash. Draft 0.1 uses no JCS (JSON Canonicalization Scheme).

SHA-256 of the exact bytes of `baseline-evidence-record.schema.json`: `7e2a53ef3fababd4c3e06dc468bf63acb185097ac4b1060231982fb7eca0bdfc`

The schema checks record structure and conditional requirements. The negative fixtures illustrate nine records it must reject:

- [Revision 2 without a supersedes link](examples/negative/revision-2-no-supersedes.json)
- [Revision 2 without a revision reason](examples/negative/revision-2-no-revision-reason.json)
- [Invalid lifecycle status](examples/negative/invalid-lifecycle.json)
- [Draft lifecycle with approved approval](examples/negative/draft-with-approved-approval.json)
- [Approved lifecycle without an approver](examples/negative/approved-no-approver.json)
- [Approved lifecycle with pending approval](examples/negative/approved-with-pending-approval.json)
- [Draft with pending approval and an approval timestamp](examples/negative/draft-pending-with-approved-at.json)
- [Blank identifiers and source references](examples/negative/blank-identifiers-and-references.json)
- [Custom aggregation without a definition](examples/negative/custom-no-definition.json)

## Review and feedback

- [Prior art](PRIOR_ART.md)
- [Known limitations](KNOWN_LIMITATIONS.md)
- [Practitioner review questions and manual checks](REVIEW_QUESTIONS.md)
- [FAQ](FAQ.md)
- [AI-development disclosure](AI-DEVELOPMENT-DISCLOSURE.md)
- [AI-development attestation](AI-DEVELOPMENT-ATTESTATION.md)
- [Feedback and contributing](../../CONTRIBUTING.md)
- [Security reporting](../../SECURITY.md)

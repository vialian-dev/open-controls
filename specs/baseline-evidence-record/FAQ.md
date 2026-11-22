# FAQ

## Is this an industry standard?

No. This is a Draft 0.1 governance profile for practitioner review with no standards-body status.

## Is this just SHA-256?

SHA-256 gives reviewers a digest of the preserved bytes. The record carries the approved comparison, metric meaning, source references, ownership and revision history.

## Why is trusted time absent from Draft 0.1?

Draft 0.1 defines the baseline record and revision semantics. Trusted-time anchoring is deferred until the reference implementation has been tested and reviewed. A local timestamp is recorded metadata, not proof of time.

## Why not Git only?

Git provides version history and release references. The profile captures the business decision, the evidence it relies on, and what a later reviewer needs to compare.

## Who prepared the draft?

AI agents assisted under human direction. Human contributors defined the problem, scope, fields, review questions and publication decision. [AI-development disclosure](AI-DEVELOPMENT-DISCLOSURE.md)

Vialian will obtain IP advice before adopting a permanent disclosure policy.

## Does AI-assisted preparation imply reliability?

No. Use the schema and digest checks to verify the artifact and the manual review questions to assess its evidence and limitations.

## Who reviewed it?

Draft 0.1 is at Level 0. An independent external practitioner review has yet to be recorded. [AI-development attestation](AI-DEVELOPMENT-ATTESTATION.md)

## What personal data does it store?

The example uses synthetic aggregates and names roles only. The profile permits optional names for role holders and records whether a source contains personal data. The flag describes that source only; review free text and extensions for sensitive data before publication. Keep sensitive source files outside the profile package and treat their hashes as potentially sensitive metadata.

## Why publish a draft?

Practitioners can test whether the record gives a later reviewer enough context to reproduce a baseline and understand what was approved.

## How are revisions handled?

Preserve each revision's exact bytes. A new revision points to an earlier one by baseline ID, revision number and digest, gives a reason for the change and requires new approval before becoming current. The highest-numbered approved revision in the linear chain is current. [Revision protocol](PROFILE.md)

## What will Draft 0.2 add?

Candidate work includes a reference CLI, trusted-time anchoring and RFC 8785 JCS canonicalization, subject to implementation and review. A separate revision-chain index is also under consideration.

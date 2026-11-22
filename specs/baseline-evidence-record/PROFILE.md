# Baseline Evidence Record Profile

After go-live, workflow steps, queues, approval points and exception handling can change. Effort may be recorded differently, metric definitions can drift and original reports may become irreproducible. Preserve the approved before-state while the source evidence is still available so a later benefits review can test the intended comparison.

## Schema and release reference

The schema uses JSON Schema Draft 2020-12 (`https://json-schema.org/draft/2020-12/schema`). Its `$id` is the versioned URI below. A record's required `$schema` property is explicitly declared and must equal that URI. Validate against the local copy of the [schema](schema/baseline-evidence-record.schema.json).

`https://raw.githubusercontent.com/vialian-dev/open-controls/baseline-evidence-record-draft-0.1/specs/baseline-evidence-record/schema/baseline-evidence-record.schema.json`

A Git tag can be updated or deleted. The release procedure calls for a GitHub tag ruleset on `baseline-evidence-record-*` that disallows updates and deletion except through an explicitly authorized break-glass path. Verify the release reference against the commit SHA in the release notes and the published SHA-256 digests for the schema and example.

## Record fields

| Required field | Meaning |
|---|---|
| `$schema` | Versioned schema URI. |
| `profile`, `profile_version` | Fixed identifiers `vialian.baseline-evidence-record` and `draft-0.1`. |
| `baseline_id`, `revision` | Identifier shared across the chain and a positive integer revision number. |
| `lifecycle_status`, `created_at` | `draft` or `approved`, and the recorded creation date and time. |
| `purpose` | Change identifier, description and intended comparison. |
| `unit_of_work` | Name and operational definition, with the steps or cases included and excluded. |
| `measurement_window` | Start and exclusive end with an explicit UTC offset (`Z` or a numeric offset), a nonblank timezone and `start_inclusive_end_exclusive` interval semantics. Include the start and exclude the end. Confirm that the instants represent the named local business period. |
| `sample` | Population, nonnegative sample size, inclusion criteria and exclusion criteria. |
| `metrics` | Array of metric identifiers, names, definitions, values, aggregations, source references and metric-specific limitations. |
| `sources` | Array of evidence-source identifiers, descriptions, systems, references, storage modes, SHA-256 digests and `contains_personal_data` flags. |
| `ownership` | Accountable owner role and, for an approved lifecycle, approver role. A draft may omit the approver. Record the approval decision separately from the role assignment. Names are optional. |
| `approval` | `pending` or `approved`. An approved approval requires `decision_record_ref` and `scope`. |
| `planned_review` | Review date, comparison purpose and outcome evidence source. |
| `limitations` | Constraints on interpreting or reusing the baseline. |

The conditional or optional top-level fields are `supersedes`, `revision_reason` and `extensions`. The schema rejects additional top-level properties. Put extension properties inside the declared `extensions` object. Revision 1 forbids `supersedes`. Revisions 2 and later require both `supersedes` and `revision_reason`. When present, the revision reason must contain a non-whitespace character.

Use a `value` object with `type` set to `decimal_string`, a decimal string in `value`, and a nonblank `unit`. Record the aggregation as `count`, `sum`, `mean`, `median`, `ratio`, `percentage`, `minimum`, `maximum` or `custom`. The schema requires `aggregation_definition` when the aggregation is `custom`. When present, the definition must contain a non-whitespace character.

Each required identifier (`baseline_id`, including in `supersedes`, `change_id`, `metric_id` and `source_id`), each source `reference` and each `source_refs` entry must contain a non-whitespace character. Each entry in `source_refs` identifies a `source_id` in `sources`. Use `hash_only`, `external_reference` or `included_aggregate` to describe how source evidence is retained. The example gives a median cycle time of 72 hours, a mean human effort of 18 hours and a rework ratio of 0.12. All three metrics point to `SRC-001`, the included Jira aggregate CSV. [Example record](examples/baseline-v1.json) · [Aggregate CSV](examples/baseline-aggregates.csv)

The schema uses `allOf`, `if` and `then` for lifecycle and approval conditions. An `approved` lifecycle requires `approval.status` to be `approved`, an approver role and `approved_at`. An `approved` decision requires an `approved` lifecycle. A `pending` decision forbids `approved_at` but may include `decision_record_ref` and `scope` without implying approval. Role names in `role`, `decision_record_ref` and `scope` must each contain a non-whitespace character when present. Both `created_at` and `approved_at` are recorded metadata. Trusted-time proof is outside Draft 0.1.

An approved record requires at least one metric, at least one source and at least one `source_refs` entry per metric. A working draft may have empty `metrics`, `sources` and `source_refs` arrays. Reviewers manually resolve references to their declared sources.

## Exact-byte digests and revisions

Calculate `record_sha256` over the exact preserved bytes of the JSON file. Use 64 lowercase hexadecimal characters for SHA-256 digests in this profile. Use UTF-8 without a BOM, LF line endings and a final newline. Keep the exact formatting. Reformatting or changing key order changes the digest. Draft 0.1 hashes serialized file bytes. RFC 8785 JCS and semantic-content hashing are outside this draft.

1. Preserve revision 1 unchanged. Once its digest is published, never edit the file to add a lifecycle state or successor reference.
2. Create revision 2 in a new file as `draft` with approval `pending`. Record the `revision_reason`. In the new record's `supersedes`, give the prior record's `baseline_id`, revision number and SHA-256 of its exact preserved JSON bytes.
3. Review the changes and obtain a new approval before preserving the new revision as `approved`. Record the approver role, `approved_at`, decision record reference and approval scope.
4. Retain links to both preserved versions. Express supersession only through the new record's `supersedes` link. Keep every preserved revision unchanged and use the same procedure for later revisions.
5. Manually verify one linear chain per `baseline_id`. Each new revision must point to one earlier preserved revision, carry the same `baseline_id` as that revision, and match its recorded revision number and exact-byte digest. Check for branches, missing records or overwritten history. The current baseline is the highest-numbered approved revision in that chain. A pending draft leaves the current approved revision in effect.

Branching, merging and withdrawal states are outside Draft 0.1.

## Validation and review

Reject duplicate object keys at any depth when parsing the schema and records, before schema validation.

Validate in JSON Schema format assertion mode with support for both `date-time` and `date`. Both measurement-window bounds, `created_at` and `approval.approved_at` use RFC 3339 `date-time` and require `Z` or a numeric UTC offset. The schema rejects CR and LF in these timestamps. The CI validator does not support RFC 3339 leap-second notation (`:60`); do not use it in Draft 0.1 records. `planned_review.review_date` uses `date`. Annotation-only mode treats formats as metadata.

The schema validates one record at a time. Reviewers must reconcile the revision chain, identifier uniqueness, source references, chronology, actual sample and metric meaning with the approval and source evidence. See the [known limitations](KNOWN_LIMITATIONS.md) and [manual checks](REVIEW_QUESTIONS.md).

## Privacy and security

Keep source files outside the profile package unless they are safe aggregates. Use only aggregated, synthetic or anonymized example data. Use roles in place of personal names in examples and exclude raw timesheets and employee-level activity. Record `contains_personal_data` for each source. Treat hashes of sensitive source files as potentially sensitive metadata.

Draft 0.1 makes no security-product claim. See the repository's [security reporting instructions](../../SECURITY.md).

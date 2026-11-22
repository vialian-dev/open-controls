# Known limitations

Draft 0.1 is a public draft for review. JSON Schema checks one record's structure and specified conditional rules. It cannot enforce every cross-field rule and does not reliably establish:

- that a revision chain is linear across multiple files;
- that `supersedes.baseline_id` matches the current record across separate artifacts;
- uniqueness of `metric_id` when objects otherwise differ;
- uniqueness of `source_id`;
- validity of every `source_ref`;
- chronological comparison of arbitrary timestamp strings;
- truth of the declared sample size;
- truth or usefulness of metric definitions;
- integrity of external source systems.

Draft 0.1 has these additional limits:

- The CI `date-time` validator rejects RFC 3339 leap-second timestamps (`:60`). Other format validators may handle them differently.
- It does not prove source-data truth or evaluate whether a metric is useful.
- It does not establish trusted time or create or verify external anchors.
- It hashes exact serialized file bytes, not canonicalized semantic JSON.
- It does not provide regulatory compliance.
- It does not replace benefits governance, records-management or retention policy, or a model risk management (MRM) framework.
- It does not prevent a user from creating a misleading record or protect raw source data.

Use the [manual review checks](REVIEW_QUESTIONS.md) to assess claims the schema cannot verify.

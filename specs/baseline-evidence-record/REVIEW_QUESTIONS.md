# Review questions

1. Is the unit of work specific enough to reproduce?
2. Does the measurement window match the business period?
3. Is the sample representative?
4. Are metric definitions operationally testable?
5. Are queue time and rework visible?
6. Does each metric identify its evidence source?
7. Does the owner have decision rights over the benefit?
8. Is the approver authorized to accept the baseline?
9. Would a later reviewer understand every revision?
10. Does the revision chain remain linear, with no hidden branch or overwritten prior record?
11. Which field is missing for benefits realization?
12. Which field creates unnecessary bureaucracy?
13. Which part would fail in a regulated environment?

## Manual checks

- Follow each `supersedes` link across the preserved files. Check the referenced revision number and exact-byte digest, confirm the chain has no branches, cycles, missing referenced artifacts or overwritten records, and identify the highest-numbered approved revision.
- Compare each `supersedes.baseline_id` with the current record's `baseline_id` and with the identifier in the referenced artifact.
- Check for duplicate `metric_id` values even when the metric objects differ, and for duplicate `source_id` values.
- Resolve every entry in each metric's `source_refs` to one declared source. Confirm that the evidence from that source supports the metric.
- Compare the recorded times with their offsets and the named business timezone. Check that the window starts before its exclusive end and that creation, approval and planned review follow the intended sequence.
- Reconcile the declared sample size against the retained aggregate or authorized evidence and apply the stated inclusion and exclusion criteria.
- Reproduce the metric definitions against the evidence and assess whether each measure supports the intended benefits comparison.
- Confirm the provenance and integrity of external source systems and evidence exports with their custodians. Compare source digests where authorized and check the approver's decision and scope.

Record the evidence reviewed and any checks you could not complete. Submit findings through the [feedback channel](../../CONTRIBUTING.md).

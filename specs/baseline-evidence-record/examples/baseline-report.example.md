Illustrative example

This report was prepared manually to demonstrate a possible human-readable rendering of the Draft 0.1 record. Draft 0.1 does not include a report-generation CLI.

## Baseline and decision

`BL-2026-001`, revision 1, is the approved comparison baseline in the example for `AI-CHANGE-2026-014`, an AI-assisted delivery-evidence workflow. The comparison after go-live covers cycle time, human effort and rework. The unit of work is one complete delivery evidence package accepted by the authorized approver. [Example record](baseline-v1.json)

The measurement window runs from `2026-10-01T00:00:00-04:00` inclusive to `2026-11-01T00:00:00-04:00` exclusive (`America/Toronto`). The sample comprises 48 completed delivery-evidence requests accepted and completed within the window. Cancelled, training and test requests are excluded.

| Metric | Definition | Aggregation | Value |
|---|---|---|---|
| Cycle time | Elapsed time from accepted request to approved result | Median | 72 hours |
| Human effort | Direct staff effort per unit | Mean | 18 hours |
| Rework rate | Units requiring correction divided by units completed | Ratio | 0.12 |

Synthetic example: 6 of 48 completed units required correction; 6/48 = 0.125, rounded to two decimal places using ties-to-even = 0.12.

All metrics reference `SRC-001`, an included aggregate export from Jira marked `contains_personal_data: false`. [Aggregate CSV](baseline-aggregates.csv)

The Program Manager is the accountable owner. The Business Sponsor approved the example for use as the comparison baseline for the named AI change under `DEC-2026-042`, with recorded approval time `2026-11-23T09:00:00-05:00`. The planned review on `2027-02-23` uses the operational reporting system to measure realized changes.

## Limitations

Synthetic aggregate example; not evidence of realized benefits. The recorded approval time is metadata and does not establish trusted time. [Profile limitations](../KNOWN_LIMITATIONS.md)

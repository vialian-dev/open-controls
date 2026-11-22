import subprocess
import sys
from collections import Counter
from copy import deepcopy
from hashlib import sha256
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker
from referencing import Registry

from profile_json import load_json


def diagnosis(error):
    property_name = None
    if error.validator == "required":
        property_name = next(
            name for name in error.validator_value
            if error.message == f"{name!r} is a required property"
        )
    return tuple(error.absolute_path), error.validator, property_name


def set_field(record, path, value):
    parent = record
    for part in path[:-1]:
        parent = parent[part]
    parent[path[-1]] = value


def check_duplicate_keys():
    for data in (b'{"key": 1, "key": 2}', b'{"nested": {"key": 1, "key": 2}}'):
        try:
            load_json("duplicate-key test", data)
        except SystemExit as error:
            if str(error) != "duplicate-key test: duplicate JSON key 'key'":
                raise
        else:
            raise SystemExit(f"Duplicate-key test unexpectedly accepted {data!r}")
    print("Top-level and nested duplicate keys rejected")


def check_field_boundaries(validator, base):
    timestamp = "1990-12-31T18:59:59-05:00"
    timestamp_cases = (
        (timestamp, None),
        ("1990-12-31T23:59:59Z", None),
        (timestamp + "\n", "not"),
        (timestamp + "\r\n", "not"),
        ("1990-12-31T23:59:59", "format"),
        ("1990-12-31T23:59:60Z", "format"),
    )
    cases = {
        ("created_at",): timestamp_cases,
        ("approval", "approved_at"): timestamp_cases,
        ("measurement_window", "start"): timestamp_cases,
        ("measurement_window", "end_exclusive"): timestamp_cases,
        ("measurement_window", "timezone"): (("", "pattern"), (" \t", "pattern")),
        ("metrics", 0, "value", "unit"): (("", "pattern"), (" \t", "pattern")),
    }
    for path, field_cases in cases.items():
        for value, expected in field_cases:
            record = deepcopy(base)
            set_field(record, path, value)
            actual = {(tuple(error.absolute_path), error.validator) for error in validator.iter_errors(record)}
            if (expected is None and actual) or (expected is not None and (path, expected) not in actual):
                raise SystemExit(f"{path} = {value!r}: expected {expected!r}, got {actual}")
    print("Timestamp and nonblank-field boundary checks passed")


def negative_fixtures(base, draft, predecessor):
    source = base["sources"][0]
    metric = base["metrics"][0]
    blank_repairs = {
        ("baseline_id",): base["baseline_id"],
        ("supersedes", "baseline_id"): base["baseline_id"],
        ("purpose", "change_id"): base["purpose"]["change_id"],
        ("metrics", 0, "metric_id"): metric["metric_id"],
        ("metrics", 0, "source_refs", 0): source["source_id"],
        ("sources", 0, "source_id"): source["source_id"],
        ("sources", 0, "reference"): source["reference"],
    }
    return {
        "revision-2-no-supersedes.json": (
            [((), "required", "supersedes")],
            {("supersedes",): predecessor},
        ),
        "revision-2-no-revision-reason.json": (
            [((), "required", "revision_reason")],
            {("revision_reason",): "Metric definition clarified after data-quality review"},
        ),
        "invalid-lifecycle.json": (
            [(("lifecycle_status",), "enum", None)],
            {("lifecycle_status",): base["lifecycle_status"]},
        ),
        "draft-with-approved-approval.json": (
            [(("lifecycle_status",), "const", None), (("approval", "status"), "not", None)],
            {("lifecycle_status",): base["lifecycle_status"]},
        ),
        "approved-no-approver.json": (
            [(("ownership",), "required", "approver")],
            {("ownership", "approver"): base["ownership"]["approver"]},
        ),
        "custom-no-definition.json": (
            [(("metrics", 0), "required", "aggregation_definition")],
            {("metrics", 0, "aggregation_definition"): "Median elapsed time across completed units."},
        ),
        "approved-with-pending-approval.json": (
            [(("approval",), "required", "approved_at"), (("approval", "status"), "const", None)],
            {("approval",): base["approval"]},
        ),
        "draft-pending-with-approved-at.json": (
            [(("approval",), "not", None)],
            {("approval",): draft["approval"]},
        ),
        "blank-identifiers-and-references.json": (
            [(path, "pattern", None) for path in blank_repairs],
            blank_repairs,
        ),
    }


def main():
    check_duplicate_keys()
    profile = Path("specs/baseline-evidence-record")
    schema = profile / "schema/baseline-evidence-record.schema.json"
    examples = profile / "examples"
    negative_dir = examples / "negative"
    base_path = examples / "baseline-v1.json"
    draft_path = examples / "baseline-draft.json"

    schema_data = load_json(schema, schema.read_bytes())
    example_bytes = {path: path.read_bytes() for path in sorted(examples.rglob("*.json"))}
    records = {path: load_json(path, data) for path, data in example_bytes.items()}
    negative_paths = sorted(negative_dir.rglob("*.json"))
    positive_paths = sorted(records.keys() - set(negative_paths))
    base = records[base_path]
    predecessor = {
        "baseline_id": base["baseline_id"],
        "revision": base["revision"],
        "record_sha256": sha256(example_bytes[base_path]).hexdigest(),
    }
    fixtures = {
        negative_dir / name: test
        for name, test in negative_fixtures(base, records[draft_path], predecessor).items()
    }
    if set(negative_paths) != fixtures.keys():
        unregistered = sorted(path.as_posix() for path in set(negative_paths) - fixtures.keys())
        missing = sorted(path.as_posix() for path in fixtures.keys() - set(negative_paths))
        raise SystemExit(f"Negative fixture coverage mismatch: unregistered={unregistered}, missing={missing}")

    cli = [sys.executable, "-m", "check_jsonschema"]
    subprocess.run([*cli, "--check-metaschema", str(schema)], check=True)
    subprocess.run([*cli, "--schemafile", str(schema), *map(str, positive_paths)], check=True)

    checker = FormatChecker()
    missing_formats = {"date", "date-time"} - checker.checkers.keys()
    if missing_formats:
        raise SystemExit(f"Missing JSON Schema format checkers: {', '.join(sorted(missing_formats))}")
    validator = Draft202012Validator(schema_data, registry=Registry(), format_checker=checker)
    for path in positive_paths:
        validator.validate(records[path])
        print(f"{path}: valid")
    check_field_boundaries(validator, base)

    for path in negative_paths:
        expected, repairs = fixtures[path]
        record = records[path]
        actual = [diagnosis(error) for error in validator.iter_errors(record)]
        if Counter(actual) != Counter(expected):
            raise SystemExit(f"{path}: expected diagnostics {expected}, got {actual}")
        for repair_path, replacement in repairs.items():
            set_field(record, repair_path, replacement)
        remaining = [diagnosis(error) for error in validator.iter_errors(record)]
        if remaining:
            raise SystemExit(f"{path}: diagnostics after repair {remaining}")
        print(f"{path}: rejected as expected, valid after repair")


if __name__ == "__main__":
    main()

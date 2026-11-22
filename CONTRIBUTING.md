# Feedback and review

Send ordinary feedback through [GitHub Issues](https://github.com/vialian-dev/open-controls/issues). Identify the profile version, the relevant field or section, and the behavior or wording you propose. Use synthetic examples and omit personal information, internal source references and raw evidence.

Report suspected vulnerabilities through the [security reporting channel](SECURITY.md).

For a practitioner review, record which checks you performed, what evidence you could assess and where your conclusions are limited. You can use the same issue channel to share findings from the [review questions and manual checks](specs/baseline-evidence-record/REVIEW_QUESTIONS.md).

## Local validation

From the repository root, create and activate a Python 3.12 virtual environment:

```sh
python3.12 -m venv .venv
. .venv/bin/activate
```

On Windows, create it with `py -3.12 -m venv .venv`. Activate it with `.\.venv\Scripts\Activate.ps1` in PowerShell or `.venv\Scripts\activate.bat` in `cmd.exe`.

Install the CI dependencies and run the same checks as CI:

```sh
python -m pip install check-jsonschema==0.34.1 rfc3339-validator==0.1.4 "markdown-it-py[linkify]==4.2.0"
python scripts/validate_profile_examples.py
python scripts/check_fixture_integrity.py
python scripts/check_markdown_links.py
```

When adding a negative fixture, document it in the [profile README](specs/baseline-evidence-record/README.md) and register its expected diagnostics and repair in the example validator.

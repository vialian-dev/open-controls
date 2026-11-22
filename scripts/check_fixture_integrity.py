from codecs import BOM_UTF8
from hashlib import sha256
from pathlib import Path

from profile_json import load_json

def exact_bytes(path):
    data = path.read_bytes()
    data.decode("utf-8", errors="strict")
    if data.startswith(BOM_UTF8) or b"\r" in data or not data.endswith(b"\n"):
        raise SystemExit(f"{path}: expected UTF-8 without BOM, LF and final newline")
    return data

profile = Path("specs/baseline-evidence-record")
examples = profile / "examples"
csv = examples / "baseline-aggregates.csv"
record = examples / "baseline-v1.json"
sidecar = examples / "baseline-v1.sha256"
schema = profile / "schema/baseline-evidence-record.schema.json"
readme = profile / "README.md"

csv_bytes = exact_bytes(csv)
csv_digest = sha256(csv_bytes).hexdigest()
expected_csv = "f9b536d5d48ca418ddda6107a93d418789d29df22d8a0f8d34aa3000a2a8d884"
if len(csv_bytes) != 234 or csv_digest != expected_csv:
    raise SystemExit(f"{csv}: expected 234 bytes and SHA-256 {expected_csv}, got {csv_digest}")

record_bytes = exact_bytes(record)
record_digest = sha256(record_bytes).hexdigest()
if exact_bytes(sidecar) != f"{record_digest}  {record.name}\n".encode("ascii"):
    raise SystemExit(f"{sidecar}: expected SHA-256 {record_digest}, two spaces and {record.name}")

sources = [
    source for source in load_json(record, record_bytes)["sources"]
    if source.get("reference") == csv.name and source.get("storage") == "included_aggregate"
]
if len(sources) != 1 or sources[0].get("sha256") != csv_digest:
    raise SystemExit(f"{record}: sources SHA-256 for {csv.name} must equal {csv_digest}")

for fixture in sorted(examples.rglob("*.json")):
    if fixture == record:
        continue
    successor = load_json(fixture, exact_bytes(fixture))
    if "supersedes" in successor and successor["supersedes"].get("record_sha256") != record_digest:
        raise SystemExit(f"{fixture}: supersedes.record_sha256 must equal {record_digest}")

schema_digest = sha256(exact_bytes(schema)).hexdigest()
digest_lines = [
    line for line in exact_bytes(readme).decode("utf-8").splitlines()
    if "SHA-256" in line and f"`{schema.name}`" in line
]
expected_line = f"SHA-256 of the exact bytes of `{schema.name}`: `{schema_digest}`"
if digest_lines != [expected_line]:
    raise SystemExit(f"{readme}: expected one SHA-256 line for {schema.name} with {schema_digest}")

for artifact, digest in ((csv, csv_digest), (record, record_digest), (schema, schema_digest)):
    print(f"{artifact}: {digest}")

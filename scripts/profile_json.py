import json


def unique_object(pairs):
    obj = {}
    for key, value in pairs:
        if key in obj:
            raise ValueError(f"duplicate JSON key {key!r}")
        obj[key] = value
    return obj


def load_json(path, data):
    try:
        return json.loads(data, object_pairs_hook=unique_object)
    except ValueError as error:
        raise SystemExit(f"{path}: {error}") from None

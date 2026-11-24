"""Load a source inventory and verify quotations against exact line ranges."""
import hashlib
import json
import re
from pathlib import Path

def require(value, message):
    if not value:
        raise ValueError(message)

def load(path):
    def reject(value):
        raise ValueError(f"Nonfinite JSON number: {value}")
    def unique(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, f"Duplicate JSON key: {key}")
            result[key] = value
        return result
    return json.loads(Path(path).read_text(encoding="utf-8-sig"),
                      parse_constant=reject, object_pairs_hook=unique)

def dump(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n",
                    encoding="utf-8")

def normalize(value):
    return re.sub(r"\s+", " ", value).strip()

def index(rows, label):
    require(isinstance(rows, list), f"{label} must be a list")
    result = {}
    for row in rows:
        require(isinstance(row, dict), f"{label} entries must be objects")
        key = row.get("id")
        require(isinstance(key, str) and key.strip() and key not in result,
                f"Invalid or duplicate {label} identifier: {key}")
        result[key] = row
    return result

def source_identity(root, relative):
    path = (root / relative).resolve()
    require(path.is_relative_to(root) and path.is_file(), f"Invalid source path: {relative}")
    data = path.read_bytes()
    return data, hashlib.sha256(data).hexdigest()

def inventory(root, catalog):
    root = Path(root).resolve()
    sources = {}
    metadata = {}
    for sid, record in index(catalog, "source").items():
        data, digest = source_identity(root, record["path"])
        require(record.get("sha256", digest) == digest, f"Extracted source hash mismatch: {sid}")
        sources[sid] = data.decode("utf-8-sig").splitlines()
        metadata[sid] = {"path": record["path"], "sha256": digest}
        if "original_path" in record:
            _, digest = source_identity(root, record["original_path"])
            require(record.get("original_sha256", digest) == digest, f"Original source hash mismatch: {sid}")
            metadata[sid].update(original_path=record["original_path"], original_sha256=digest)
    return sources, metadata

def anchor(ref, sources):
    source = ref["source_id"]
    lines = sources[source]
    start, end = ref["start"], ref["end"]
    require(type(start) is int and type(end) is int and 1 <= start <= end <= len(lines),
            f"Invalid line range for {source}: {start}-{end}")
    quote = normalize(ref["quote"])
    require(quote and quote in normalize(" ".join(lines[start-1:end])),
            f"Quote absent from {source}:{start}-{end}")
    return {"source_id": source, "start": start, "end": end, "quote": ref["quote"]}

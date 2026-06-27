import json
import hashlib
from pathlib import Path

# Path to documents.json
REGISTRY_FILE = Path(__file__).resolve().parent.parent / "data" / "documents.json"


def calculate_hash(file_path):
    sha = hashlib.sha256()

    with open(file_path, "rb") as f:
        while True:
            data = f.read(8192)
            if not data:
                break
            sha.update(data)

    return sha.hexdigest()


def load_registry():
    if not REGISTRY_FILE.exists():
        return {}

    with open(REGISTRY_FILE, "r") as f:
        return json.load(f)


def save_registry(registry):
    with open(REGISTRY_FILE, "w") as f:
        json.dump(registry, f, indent=4)


def is_document_changed(file_path):

    registry = load_registry()

    file_name = Path(file_path).name

    current_hash = calculate_hash(file_path)

    if file_name not in registry:
        return True

    return registry[file_name]["hash"] != current_hash


def update_registry(file_path, pages, chunks):

    registry = load_registry()

    file_name = Path(file_path).name

    registry[file_name] = {
        "hash": calculate_hash(file_path),
        "pages": pages,
        "chunks": chunks
    }

    save_registry(registry)
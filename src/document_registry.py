import json
import hashlib
import re
from pathlib import Path


def get_registry_file(session_id=None):
    data_dir = Path(__file__).resolve().parent.parent / "data"
    if not session_id:
        return data_dir / "documents.json"
    
    registries_dir = data_dir / "registries"
    registries_dir.mkdir(exist_ok=True)
    clean_session_id = re.sub(r'[^a-z0-9_-]', '', session_id.lower())
    return registries_dir / f"registry_{clean_session_id}.json"


def calculate_hash(file_path):
    sha = hashlib.sha256()

    with open(file_path, "rb") as f:
        while True:
            data = f.read(8192)
            if not data:
                break
            sha.update(data)

    return sha.hexdigest()


def load_registry(session_id=None):
    registry_file = get_registry_file(session_id)
    if not registry_file.exists():
        return {}

    with open(registry_file, "r") as f:
        return json.load(f)


def save_registry(registry, session_id=None):
    registry_file = get_registry_file(session_id)
    with open(registry_file, "w") as f:
        json.dump(registry, f, indent=4)


def is_document_changed(file_path, session_id=None):

    registry = load_registry(session_id)

    file_name = Path(file_path).name

    current_hash = calculate_hash(file_path)

    if file_name not in registry:
        return True

    return registry[file_name]["hash"] != current_hash


def update_registry(file_path, pages, chunks, session_id=None):

    registry = load_registry(session_id)

    file_name = Path(file_path).name

    registry[file_name] = {
        "hash": calculate_hash(file_path),
        "pages": pages,
        "chunks": chunks
    }

    save_registry(registry, session_id)
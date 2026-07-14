from pathlib import Path

from document_registry import save_registry
from indexer import PROJECT_ROOT, index_document
from vectordb import collection


def collection_status():
    """Report whether stored vectors have citation-ready source metadata."""
    records = collection.get(include=["metadatas"])
    metadatas = records.get("metadatas", [])
    legacy_count = sum(
        1 for metadata in metadatas if not metadata or not metadata.get("source")
    )
    return {"vector_count": len(records.get("ids", [])), "legacy_count": legacy_count}


def rebuild_collection(document_paths):
    """Replace all stored vectors by indexing the supplied documents."""
    paths = [Path(path) for path in document_paths if path.strip()]
    resolved = [path if path.is_absolute() else PROJECT_ROOT / path for path in paths]
    if not resolved:
        raise ValueError("Provide at least one PDF or DOCX path.")
    missing = [path for path in resolved if not path.exists()]
    if missing:
        raise FileNotFoundError(f"File not found: {missing[0]}")

    # 1. Get existing IDs and delete them to wipe the collection
    existing_ids = collection.get(include=[]).get("ids", [])
    deleted_count = len(existing_ids)
    if existing_ids:
        collection.delete(ids=existing_ids)
    
    # 2. Reset the registry (empty state)
    save_registry({})

    # 3. Index the new documents
    for path in resolved:
        # This calls your indexer's function to parse & embed each document
        index_document(path)

    # 4. Return the expected dictionary structure
    return {
        "deleted_vectors": deleted_count,
        "status": collection_status()  # Fetch the fresh, updated status
    }
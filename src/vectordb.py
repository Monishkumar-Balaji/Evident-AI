# vectordb.py
import chromadb
import hashlib
import re
from config import CHROMA_PATH, COLLECTION_NAME

client = chromadb.PersistentClient(
    path=CHROMA_PATH
)

def clean_session_name(session_id):
    if not session_id:
        return COLLECTION_NAME
    # Ensure collection name is safe (lowercase, alphanumeric, underscores, hyphens)
    clean = re.sub(r'[^a-z0-9_-]', '', session_id.lower())
    if len(clean) < 3:
        clean = f"session_{clean}"
    return clean[:63]


def get_collection(session_id=None):
    name = clean_session_name(session_id)
    return client.get_or_create_collection(name=name)


def store_chunks(chunks, embeddings, session_id=None):
    ids = []
    documents = []
    metadatas = []

    for chunk in chunks:

        source_key = hashlib.sha256(chunk["source"].encode("utf-8")).hexdigest()[:16]
        ids.append(f"{source_key}_chunk_{chunk['id']}")

        documents.append(chunk["text"])

        metadatas.append({
            "page": chunk["page"],
            "chunk": chunk["chunk"],
            "length": chunk["length"],
            "source": chunk["source"]
        })

    collection = get_collection(session_id)
    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
        embeddings=embeddings if isinstance(embeddings, list) else embeddings.tolist()
    )

def delete_document(source, session_id=None):
    collection = get_collection(session_id)

    collection.delete(
        where={"source": source}
    )

    print(
        f"Deleted old vectors for {source} in session {session_id}",
        flush=True
    )

    
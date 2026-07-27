import time
from pathlib import Path

from parser import extract_text
from chunker import create_chunks
from embedder import generate_embeddings
from vectordb import delete_document, store_chunks
from document_registry import is_document_changed, update_registry


PROJECT_ROOT = Path(__file__).resolve().parent.parent


def index_document(pdf_path, session_id=None):

    total_start = time.perf_counter()

    pdf_path = PROJECT_ROOT / pdf_path

    if not pdf_path.exists():
        print(f"\n❌ File not found:\n{pdf_path}", flush=True)
        return

    # =========================================================
    # 1. CHECK + EXTRACT TEXT
    # =========================================================

    print("Extracting text...", flush=True)

    if not is_document_changed(pdf_path, session_id=session_id):
        print("Document already indexed.", flush=True)
        print("No changes detected.", flush=True)
        return

    start = time.perf_counter()

    pages = extract_text(str(pdf_path))

    print(
        f"⏱ Text extraction: {time.perf_counter() - start:.2f}s",
        flush=True
    )

    # =========================================================
    # 2. CREATE CHUNKS
    # =========================================================

    print("Creating chunks...", flush=True)

    start = time.perf_counter()

    chunks = create_chunks(pages, pdf_path)

    print(f"Created {len(chunks)} chunks", flush=True)

    print(
        f"⏱ Chunking: {time.perf_counter() - start:.2f}s",
        flush=True
    )

    texts = [chunk["text"] for chunk in chunks]

    # =========================================================
    # 3. GENERATE EMBEDDINGS
    # =========================================================

    print("Generating embeddings...", flush=True)

    start = time.perf_counter()

    embeddings = generate_embeddings(texts)

    print(
        f"⏱ Embedding generation: {time.perf_counter() - start:.2f}s",
        flush=True
    )

    # =========================================================
    # 4. DELETE EXISTING VECTORS
    # =========================================================

    print("Storing into ChromaDB...", flush=True)
    print("Deleting existing vectors...", flush=True)

    start = time.perf_counter()

    delete_document(
        Path(pdf_path).name,
        session_id=session_id
    )

    print(
        f"⏱ Vector deletion: {time.perf_counter() - start:.2f}s",
        flush=True
    )

    # =========================================================
    # 5. STORE NEW VECTORS
    # =========================================================

    print("Writing new vectors...", flush=True)

    start = time.perf_counter()

    store_chunks(
        chunks,
        embeddings,
        session_id=session_id
    )

    print(
        f"⏱ Vector storage: {time.perf_counter() - start:.2f}s",
        flush=True
    )

    # =========================================================
    # 6. UPDATE DOCUMENT REGISTRY
    # =========================================================

    print("Updating document registry...", flush=True)

    start = time.perf_counter()

    update_registry(
        pdf_path,
        pages=len(pages),
        chunks=len(chunks),
        session_id=session_id
    )

    print(
        f"⏱ Registry update: {time.perf_counter() - start:.2f}s",
        flush=True
    )

    # =========================================================
    # COMPLETE
    # =========================================================

    total_time = time.perf_counter() - total_start

    print(
        f"🚀 TOTAL INDEXING TIME: {total_time:.2f}s",
        flush=True
    )

    print("✅ Document indexed successfully.", flush=True)
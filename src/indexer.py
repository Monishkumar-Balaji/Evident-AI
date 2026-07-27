from pathlib import Path
from parser import extract_text
from chunker import create_chunks
from embedder import generate_embeddings
from vectordb import delete_document, store_chunks
from document_registry import (is_document_changed,update_registry)
import time 


PROJECT_ROOT = Path(__file__).resolve().parent.parent

def index_document(pdf_path, session_id=None):

    total_start = time.perf_counter()

    pdf_path = PROJECT_ROOT / pdf_path

    if not pdf_path.exists():
        print(f"\n❌ File not found:\n{pdf_path}")
        return

    # ---------------- PARSING ----------------
    start = time.perf_counter()

    print("Extracting text...", flush=True)

    if not is_document_changed(pdf_path, session_id=session_id):
        print("Document already indexed.", flush=True)
        return

    pages = extract_text(str(pdf_path))

    print(
        f"⏱ Text extraction: {time.perf_counter() - start:.2f}s",
        flush=True
    )

    # ---------------- CHUNKING ----------------
    start = time.perf_counter()

    print("Creating chunks...", flush=True)

    chunks = create_chunks(pages, pdf_path)

    print(f"Created {len(chunks)} chunks", flush=True)

    print(
        f"⏱ Chunking: {time.perf_counter() - start:.2f}s",
        flush=True
    )

    texts = [chunk["text"] for chunk in chunks]

    # ---------------- EMBEDDING ----------------
    start = time.perf_counter()

    print("Generating embeddings...", flush=True)

    embeddings = generate_embeddings(texts)

    print(
        f"⏱ Embedding generation: {time.perf_counter() - start:.2f}s",
        flush=True
    )

    # ---------------- CHROMADB ----------------
    start = time.perf_counter()

    print("Storing into ChromaDB...", flush=True)

    delete_document(
        Path(pdf_path).name,
        session_id=session_id
    )

    store_chunks(
        chunks,
        embeddings,
        session_id=session_id
    )

    print(
        f"⏱ ChromaDB storage: {time.perf_counter() - start:.2f}s",
        flush=True
    )

    # ---------------- REGISTRY ----------------

    update_registry(
        pdf_path,
        pages=len(pages),
        chunks=len(chunks),
        session_id=session_id
    )

    print(
        f"🚀 TOTAL INDEXING TIME: "
        f"{time.perf_counter() - total_start:.2f}s",
        flush=True
    )

    print("✅ Document indexed successfully.", flush=True)
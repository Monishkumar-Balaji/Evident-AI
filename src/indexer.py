from pathlib import Path
from parser import extract_text
from chunker import create_chunks
from embedder import generate_embeddings
from vectordb import delete_document, store_chunks
from document_registry import (is_document_changed,update_registry)

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def index_document(pdf_path):

    pdf_path = PROJECT_ROOT / pdf_path

    if not pdf_path.exists():
        print(f"\n❌ File not found:\n{pdf_path}")
        return

    print("Extracting text...")

    if not is_document_changed(pdf_path):
        print("\nDocument already indexed.")
        print("No changes detected.")
        return

    pages = extract_text(str(pdf_path))

    print("Creating chunks...")

    chunks = create_chunks(pages, pdf_path)

    print(f"Created {len(chunks)} chunks")

    texts = [chunk["text"] for chunk in chunks]

    print("Generating embeddings...")

    embeddings = generate_embeddings(texts)

    print("Storing into ChromaDB...")
    delete_document(Path(pdf_path).name)
    store_chunks(chunks, embeddings)

    update_registry(
        pdf_path,
        pages=len(pages),
        chunks=len(chunks)
    )

    print("✅ Document indexed successfully.")
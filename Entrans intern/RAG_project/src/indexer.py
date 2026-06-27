from pathlib import Path

from parser import extract_pdf_text
from chunker import create_chunks
from embedder import generate_embeddings
from vectordb import store_chunks


PROJECT_ROOT = Path(__file__).resolve().parent.parent


def index_document(pdf_path):

    pdf_path = PROJECT_ROOT / pdf_path

    if not pdf_path.exists():
        print(f"\n❌ File not found:\n{pdf_path}")
        return

    print("Extracting text...")

    pages = extract_pdf_text(str(pdf_path))

    print("Creating chunks...")

    chunks = create_chunks(pages)

    print(f"Created {len(chunks)} chunks")

    texts = [chunk["text"] for chunk in chunks]

    print("Generating embeddings...")

    embeddings = generate_embeddings(texts)

    print("Storing into ChromaDB...")

    store_chunks(chunks, embeddings)

    print("✅ Document indexed successfully.")
# vectordb.py
import chromadb
from config import CHROMA_PATH, COLLECTION_NAME

client = chromadb.PersistentClient(
    path=CHROMA_PATH
)

collection = client.get_or_create_collection(
    name=COLLECTION_NAME
)


def store_chunks(chunks, embeddings):
    ids = []
    documents = []
    metadatas = []

    for chunk in chunks:

        ids.append(f"chunk_{chunk['id']}")

        documents.append(chunk["text"])

        metadatas.append({
            "page": chunk["page"],
            "chunk": chunk["chunk"],
            "length": chunk["length"],
            "source": chunk["source"]
        })

    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
        embeddings=embeddings.tolist()
    )

def delete_document(source):

    results = collection.get(
        where={"source": source}
    )

    if results["ids"]:
        collection.delete(
            ids=results["ids"]
        )

        print(f"Deleted old vectors for {source}")
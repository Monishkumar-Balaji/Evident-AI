# retriever.py
from embedder import generate_embeddings
from vectordb import collection


def search(query, top_k=3):

    query_embedding = generate_embeddings([query])[0]

    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=top_k
    )

    docs = results["documents"][0]
    pages = results["metadatas"][0]
    distances = results["distances"][0]

    formatted_results = []

    for doc, page, distance in zip(docs, pages, distances):
        if distance < 0.75:   # Adjust this threshold after testing
            formatted_results.append({
                    "page": page["page"],
                    "chunk": page["chunk"],
                    "length": page["length"],
                    "distance": distance,
                    "text": doc
                })

    return formatted_results
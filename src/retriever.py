# retriever.py
from embedder import generate_embeddings
from vectordb import collection
from config import DEFAULT_TOP_K, MAX_RETRIEVAL_DISTANCE, MAX_TOP_K, MIN_TOP_K


def choose_top_k(query):
    """
    Choose retrieval depth from query length.
    Short factual questions need less context; broader questions need more.
    """

    word_count = len(query.split())

    if word_count <= 5:
        return MIN_TOP_K

    if word_count <= 12:
        return DEFAULT_TOP_K

    return MAX_TOP_K


def search(query, top_k=None):
    if top_k is None:
        top_k = choose_top_k(query)

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
        if distance <= MAX_RETRIEVAL_DISTANCE:
            formatted_results.append({
                "page": page["page"],
                "chunk": page["chunk"],
                "length": page["length"],
                "source": page.get("source"),
                "distance": distance,
                "text": doc
            })

    return formatted_results

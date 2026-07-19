# retriever.py
from config import DEFAULT_TOP_K, MAX_TOP_K, MIN_TOP_K


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

    from hybrid_retriever import hybrid_search
    return hybrid_search(query, top_k)

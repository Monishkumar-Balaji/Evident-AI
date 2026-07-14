from sklearn.metrics.pairwise import cosine_similarity

from embedder import generate_embeddings


def build_audit_trail(verification, evidence):
    """Map every answer claim to its closest retrieved evidence sentence."""
    candidates = [
        {
            "quote": sentence["text"],
            "source": item.get("source") or "Unknown source",
            "page": item.get("page"),
        }
        for item in evidence
        for sentence in item.get("sentences", [])
    ]
    if not verification or not candidates:
        return []

    candidate_embeddings = generate_embeddings(
        [candidate["quote"] for candidate in candidates]
    )
    claim_embeddings = generate_embeddings(
        [item["sentence"] for item in verification]
    )
    similarities = cosine_similarity(claim_embeddings, candidate_embeddings)

    trail = []
    for claim, scores in zip(verification, similarities):
        best_index = int(scores.argmax())
        support = candidates[best_index]
        trail.append({
            "claim": claim["sentence"],
            "supported": claim["verified"],
            "score": round(float(scores[best_index]), 3),
            "source": support["source"],
            "page": support["page"],
            "quote": support["quote"],
        })
    return trail

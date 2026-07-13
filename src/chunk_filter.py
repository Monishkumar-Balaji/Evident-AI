from config import MAX_CONTEXT_CHUNKS, MIN_CHUNK_FILTER_SCORE, SIMILARITY_THRESHOLD
from sentence_extractor import extract_best_sentences


def _distance_to_score(distance):
    return max(0, min(100, (1 - distance) * 100))


def _chunk_key(chunk):
    return (
        chunk.get("source"),
        chunk.get("page"),
        chunk.get("text")
    )


def _score_chunk(question, chunk):
    retrieval_score = _distance_to_score(chunk["distance"])
    evidence_sentences = extract_best_sentences(
        question,
        chunk["text"],
        top_k=2
    )

    if evidence_sentences:
        evidence_score = max(
            sentence["score"]
            for sentence in evidence_sentences
        ) * 100
        average_evidence_score = (
            sum(sentence["score"] for sentence in evidence_sentences)
            / len(evidence_sentences)
        ) * 100
    else:
        evidence_score = 0
        average_evidence_score = 0

    score = (
        retrieval_score * 0.60
        + evidence_score * 0.30
        + average_evidence_score * 0.10
    )

    return {
        "score": round(score, 2),
        "retrieval_score": round(retrieval_score, 2),
        "evidence_score": round(evidence_score, 2),
        "best_sentences": evidence_sentences
    }


def filter_chunks(question, retrieved_chunks, max_chunks=MAX_CONTEXT_CHUNKS):
    """
    Keep only the chunks most likely to answer the question.
    """

    report = {
        "retrieved_count": len(retrieved_chunks),
        "kept_count": 0,
        "removed_weak_count": 0,
        "removed_duplicate_count": 0,
        "removed_low_score_count": 0,
        "max_context_chunks": max_chunks,
        "kept_chunks": [],
        "reason": "No chunks were available to filter."
    }

    if not retrieved_chunks:
        return [], report

    candidates = []
    seen = set()

    for chunk in retrieved_chunks:
        if chunk["distance"] > SIMILARITY_THRESHOLD:
            report["removed_weak_count"] += 1
            continue

        key = _chunk_key(chunk)

        if key in seen:
            report["removed_duplicate_count"] += 1
            continue

        seen.add(key)

        scoring = _score_chunk(question, chunk)

        if scoring["score"] < MIN_CHUNK_FILTER_SCORE:
            report["removed_low_score_count"] += 1
            continue

        ranked_chunk = dict(chunk)
        ranked_chunk["filter_score"] = scoring["score"]
        ranked_chunk["retrieval_score"] = scoring["retrieval_score"]
        ranked_chunk["evidence_score"] = scoring["evidence_score"]
        ranked_chunk["filter_evidence"] = scoring["best_sentences"]

        candidates.append(ranked_chunk)

    candidates.sort(
        key=lambda item: (
            item["filter_score"],
            -item["distance"]
        ),
        reverse=True
    )

    filtered_chunks = candidates[:max_chunks]
    report["kept_count"] = len(filtered_chunks)
    report["kept_chunks"] = [
        {
            "source": chunk.get("source"),
            "page": chunk.get("page"),
            "distance": round(chunk["distance"], 3),
            "filter_score": chunk["filter_score"],
            "retrieval_score": chunk["retrieval_score"],
            "evidence_score": chunk["evidence_score"]
        }
        for chunk in filtered_chunks
    ]

    if filtered_chunks:
        report["reason"] = (
            f"Kept {len(filtered_chunks)} of {len(retrieved_chunks)} retrieved chunk(s) "
            f"after removing weak, duplicate, and low-score context."
        )
    else:
        report["reason"] = (
            "All retrieved chunks were removed because they were weak, "
            "duplicates, or below the chunk relevance score threshold."
        )

    return filtered_chunks, report

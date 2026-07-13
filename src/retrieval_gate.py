from config import SIMILARITY_THRESHOLD


def _clamp_score(score):
    return max(0, min(100, score))


def _distance_to_score(distance):
    return _clamp_score((1 - distance) * 100)


def assess_retrieval(retrieved_chunks):
    """
    Build a retrieval quality report and decide if generation is allowed.
    """

    if not retrieved_chunks:
        return {
            "should_generate": False,
            "score": 0,
            "level": "NONE",
            "reason": "No chunks were retrieved.",
            "best_distance": None,
            "strong_chunk_count": 0,
            "candidate_count": 0
        }

    distances = [
        chunk["distance"]
        for chunk in retrieved_chunks
    ]

    best_distance = min(distances)
    best_score = _distance_to_score(best_distance)

    strong_chunks = [
        chunk
        for chunk in retrieved_chunks
        if chunk["distance"] <= SIMILARITY_THRESHOLD
    ]

    if strong_chunks:
        average_score = sum(
            _distance_to_score(chunk["distance"])
            for chunk in strong_chunks
        ) / len(strong_chunks)
    else:
        average_score = 0

    coverage_score = min(
        len(strong_chunks) / 3,
        1
    ) * 100

    quality_score = (
        best_score * 0.50
        + average_score * 0.30
        + coverage_score * 0.20
    )

    should_generate = (
        best_distance <= SIMILARITY_THRESHOLD
        and quality_score >= 45
        and len(strong_chunks) >= 1
    )

    if quality_score >= 75:
        level = "STRONG"
    elif quality_score >= 55:
        level = "GOOD"
    elif quality_score >= 35:
        level = "WEAK"
    else:
        level = "POOR"

    if should_generate:
        reason = (
            f"Retrieval passed with {len(strong_chunks)} relevant chunk(s) "
            f"and best distance {best_distance:.3f}."
        )
    else:
        reason = (
            f"Retrieval was too weak: best distance {best_distance:.3f}, "
            f"{len(strong_chunks)} relevant chunk(s)."
        )

    return {
        "should_generate": should_generate,
        "score": round(quality_score, 2),
        "level": level,
        "reason": reason,
        "best_distance": round(best_distance, 3),
        "strong_chunk_count": len(strong_chunks),
        "candidate_count": len(retrieved_chunks)
    }


def should_generate_answer(retrieved_chunks):
    """
    Backward-compatible boolean gate for older callers.
    """

    return assess_retrieval(retrieved_chunks)["should_generate"]

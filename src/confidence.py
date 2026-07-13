def _clamp_score(score):
    return max(0, min(100, score))


def _distance_to_score(distance):
    """
    Convert ChromaDB distance into a 0-100 retrieval score.
    Lower distance means better retrieval.
    """

    return _clamp_score((1 - distance) * 100)


def _confidence_level(score):
    if score >= 85:
        return "HIGH"

    if score >= 70:
        return "MEDIUM"

    if score >= 50:
        return "LOW"

    return "VERY LOW"


def _calculate_evidence_score(evidence):
    if not evidence:
        return 0, 0

    scores = []

    for item in evidence:
        for sentence in item.get("sentences", []):
            scores.append(sentence.get("score", 0) * 100)

    if not scores:
        return 0, 0

    strong_count = sum(score >= 75 for score in scores)
    return sum(scores) / len(scores), strong_count


def _calculate_verification_score(verification):
    if not verification:
        return 0

    verified_count = sum(
        item.get("verified", False)
        for item in verification
    )

    return (verified_count / len(verification)) * 100


def calculate_confidence(
    chunks,
    evidence=None,
    verification=None,
    retrieval_quality=None
):
    """
    Calculate answer confidence from retrieval, evidence, and verification.
    """

    if not chunks:
        return {
            "score": 0,
            "level": "NONE",
            "explanation": "No relevant document chunks were retrieved.",
            "components": {
                "best_retrieval": 0,
                "average_retrieval": 0,
                "evidence": 0,
                "verification": 0
            }
        }

    retrieval_scores = [
        _distance_to_score(chunk["distance"])
        for chunk in chunks
    ]

    best_retrieval = max(retrieval_scores)
    average_retrieval = sum(retrieval_scores) / len(retrieval_scores)

    evidence_score, strong_evidence_count = _calculate_evidence_score(
        evidence
    )

    verification_score = _calculate_verification_score(
        verification
    )

    confidence = (
        best_retrieval * 0.35
        + average_retrieval * 0.25
        + evidence_score * 0.20
        + verification_score * 0.20
    )

    if verification and verification_score < 60:
        confidence -= 10

    if strong_evidence_count == 0:
        confidence -= 5

    if retrieval_quality:
        confidence = min(
            confidence,
            retrieval_quality["score"] + 20
        )

    confidence = _clamp_score(confidence)

    explanation = (
        f"Best retrieval {best_retrieval:.1f}%, "
        f"average retrieval {average_retrieval:.1f}%, "
        f"{strong_evidence_count} strong evidence sentence(s), "
        f"verification {verification_score:.1f}%."
    )

    return {
        "score": round(confidence, 2),
        "level": _confidence_level(confidence),
        "explanation": explanation,
        "components": {
            "best_retrieval": round(best_retrieval, 2),
            "average_retrieval": round(average_retrieval, 2),
            "evidence": round(evidence_score, 2),
            "verification": round(verification_score, 2)
        }
    }

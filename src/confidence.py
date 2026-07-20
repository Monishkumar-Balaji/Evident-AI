def _clamp_score(score):
    return max(0, min(100, score))


def _distance_to_score(distance):
    """
    Convert ChromaDB distance into a 0-100 retrieval score.
    Lower distance means better retrieval.
    """

    return _clamp_score((1 - distance) * 100)


def _confidence_level(score):
    if score >= 90:
        return "VERY HIGH"
    if score >= 75:
        return "HIGH"
    if score >= 60:
        return "MEDIUM"
    if score >= 40:
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


def _calculate_verification_metrics(verification):
    if not verification:
        return 0, 0

    verified_count = sum(
        item.get("verified", False)
        for item in verification
    )
    
    total_count = len(verification)
    verification_score = (verified_count / total_count) * 100 if total_count > 0 else 0
    return verification_score, verified_count


def calculate_confidence(
    chunks,
    evidence=None,
    verification=None,
    retrieval_quality=None
):
    """
    Calculate answer confidence prioritizing verification and evidence over raw retrieval.
    """

    if not chunks:
        return {
            "confidence_score": 0,
            "confidence_label": "NONE",
            "reason_codes": ["no_retrieval"],
            "reason_messages": ["⚠ No relevant document chunks were retrieved."],
            "score_breakdown": {
                "verification": 0,
                "retrieval": 0,
                "evidence": 0,
                "supported_claims": 0,
                "retrieval_quality": 0
            }
        }

    retrieval_scores = [
        _distance_to_score(chunk["distance"])
        for chunk in chunks
    ]

    best_retrieval = max(retrieval_scores) if retrieval_scores else 0
    evidence_score, strong_evidence_count = _calculate_evidence_score(evidence)
    verification_score, verified_count = _calculate_verification_metrics(verification)
    
    total_claims = len(verification) if verification else 0
    supported_claim_ratio = (verified_count / total_claims) * 100 if total_claims > 0 else 0
    rq_score = retrieval_quality["score"] if retrieval_quality else 0

    # Apply Weights
    w_verification = 0.40
    w_best_retrieval = 0.25
    w_evidence = 0.15
    w_supported_claims = 0.10
    w_retrieval_quality = 0.10

    c_verification = verification_score * w_verification
    c_best_retrieval = best_retrieval * w_best_retrieval
    c_evidence = evidence_score * w_evidence
    c_supported_claims = supported_claim_ratio * w_supported_claims
    c_retrieval_quality = rq_score * w_retrieval_quality

    confidence = (
        c_verification
        + c_best_retrieval
        + c_evidence
        + c_supported_claims
        + c_retrieval_quality
    )

    reason_codes = []
    reason_messages = []

    # Hard constraints & dynamic reasons
    if verification:
        if verification_score == 100:
            reason_codes.append("verified_answer")
            reason_messages.append("✓ Answer fully verified against retrieved evidence")
        elif verification_score >= 50:
            reason_codes.append("partially_verified")
            reason_messages.append("⚠ Some claims could not be verified")
            confidence -= 10
        else:
            reason_codes.append("verification_failed")
            reason_messages.append("⚠ Verification failed for most claims")
            confidence -= 20
    else:
        reason_codes.append("no_claims")
        reason_messages.append("⚠ No specific factual claims found to verify")

    if strong_evidence_count > 0:
        reason_codes.append("strong_evidence")
        reason_messages.append("✓ Strong supporting evidence found")
    else:
        reason_codes.append("weak_evidence")
        reason_messages.append("⚠ No strong supporting evidence sentence found")
        confidence -= 15

    if best_retrieval >= 75:
        reason_codes.append("high_retrieval")
        reason_messages.append("✓ High retrieval relevance")
    elif best_retrieval < 50:
        reason_codes.append("weak_retrieval")
        reason_messages.append("⚠ Weak retrieval similarity")
        confidence -= 15

    # Check for hallucination/unsupported claims
    if verification and total_claims > 0:
        unsupported = total_claims - verified_count
        if unsupported == 0:
            reason_codes.append("no_hallucination")
            reason_messages.append("✓ No unsupported claims detected")
        else:
            reason_codes.append("hallucination_detected")
            reason_messages.append(f"⚠ {unsupported} claim(s) could not be verified")
            confidence -= (10 * unsupported)

    # Never LOW override conditions
    if (verification_score == 100 
        and best_retrieval >= 75 
        and strong_evidence_count > 0 
        and (total_claims > 0 and total_claims == verified_count)):
        confidence = max(confidence, 75)

    confidence = _clamp_score(confidence)

    return {
        "confidence_score": round(confidence),
        "confidence_label": _confidence_level(confidence),
        "reason_codes": reason_codes,
        "reason_messages": reason_messages,
        "score_breakdown": {
            "verification": round(c_verification, 1),
            "retrieval": round(c_best_retrieval, 1),
            "evidence": round(c_evidence, 1),
            "supported_claims": round(c_supported_claims, 1),
            "retrieval_quality": round(c_retrieval_quality, 1)
        }
    }

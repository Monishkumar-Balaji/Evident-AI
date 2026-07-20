# rag.py
from retriever import search
from prompt import build_prompt
from generator import generate
from confidence import calculate_confidence
from evidence import build_evidence
from hallucination_detector import verify_answer
from audit import build_audit_trail
from retrieval_gate import assess_retrieval
from chunk_filter import filter_chunks


def empty_response(retrieval_quality=None, chunk_filter=None):
    """
    Standard response when no relevant information is found.
    """

    if retrieval_quality is None:
        retrieval_quality = {
            "should_generate": False,
            "score": 0,
            "level": "NONE",
            "reason": "No retrieval was performed.",
            "best_distance": None,
            "strong_chunk_count": 0,
            "candidate_count": 0
        }

    if chunk_filter is None:
        chunk_filter = {
            "retrieved_count": 0,
            "kept_count": 0,
            "removed_weak_count": 0,
            "removed_duplicate_count": 0,
            "removed_low_score_count": 0,
            "max_context_chunks": 0,
            "kept_chunks": [],
            "reason": "No chunk filtering was performed."
        }

    return {
        "answer": "I could not find this information in the uploaded documents.",
        "confidence": {
            "confidence_score": 0,
            "confidence_label": "NONE",
            "reason_codes": ["no_retrieval"],
            "reason_messages": [retrieval_quality["reason"]],
            "score_breakdown": {
                "verification": 0,
                "retrieval": 0,
                "evidence": 0,
                "supported_claims": 0,
                "retrieval_quality": 0
            }
        },
        "retrieval_quality": retrieval_quality,
        "chunk_filter": chunk_filter,
        "evidence": [],
        "audit_trail": [],
        "verification": [],
        "sources": []
    }


def ask(question):
    """
    Complete RAG pipeline:
    Retrieve -> Filter -> Generate -> Verify
    """

    retrieved_chunks = search(question)
    retrieval_quality = assess_retrieval(retrieved_chunks)

    if not retrieval_quality["should_generate"]:
        return empty_response(retrieval_quality)

    filtered_chunks, chunk_filter_report = filter_chunks(
        question,
        retrieved_chunks
    )

    if not filtered_chunks:
        return empty_response(
            retrieval_quality,
            chunk_filter_report
        )

    prompt = build_prompt(
        question,
        filtered_chunks
    )

    answer = generate(prompt)

    evidence = build_evidence(
        question,
        filtered_chunks
    )

    verification = verify_answer(
        answer,
        evidence
    )
    audit_trail = build_audit_trail(
        verification,
        evidence
    )

    confidence = calculate_confidence(
        filtered_chunks,
        evidence=evidence,
        verification=verification,
        retrieval_quality=retrieval_quality
    )

    return {
        "answer": answer,
        "confidence": confidence,
        "retrieval_quality": retrieval_quality,
        "chunk_filter": chunk_filter_report,
        "evidence": evidence,
        "verification": verification,
        "sources": filtered_chunks,
        "audit_trail": audit_trail,
    }

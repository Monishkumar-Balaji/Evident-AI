from sentence_extractor import extract_best_sentences


def build_evidence(question, chunks):
    """Construct evidence list from retrieved chunks.

    Each evidence dict includes the page number, distance score, source filename,
    and the most relevant sentences extracted for the given question.
    """
    evidence = []
    for chunk in chunks:
        evidence.append({
            "page": chunk["page"],
            "distance": round(chunk["distance"], 3),
            "source": chunk.get("source"),
            "sentences": extract_best_sentences(question, chunk["text"])
        })
    return evidence

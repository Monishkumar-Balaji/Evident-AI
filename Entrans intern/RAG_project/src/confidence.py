def calculate_confidence(chunks):
    """
    Calculate retrieval confidence from ChromaDB distances.
    Lower distance = Higher confidence.
    """

    if not chunks:
        return {
            "score": 0,
            "level": "NONE"
        }

    avg_distance = sum(
        chunk["distance"]
        for chunk in chunks
    ) / len(chunks)

    confidence = max(
        0,
        min(
            100,
            (1 - avg_distance) * 100
        )
    )

    if confidence >= 85:
        level = "HIGH"

    elif confidence >= 70:
        level = "MEDIUM"

    elif confidence >= 50:
        level = "LOW"

    else:
        level = "VERY LOW"

    return {
        "score": round(confidence, 2),
        "level": level
    }
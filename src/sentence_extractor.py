import re
from sklearn.metrics.pairwise import cosine_similarity
from embedder import generate_embeddings


def get_strength(score):
    """
    Convert similarity score into an ASCII star rating.
    """

    if score >= 0.90:
        return "[*****]"

    if score >= 0.80:
        return "[**** ]"

    if score >= 0.70:
        return "[***  ]"

    if score >= 0.60:
        return "[**   ]"

    return "[*    ]"


def extract_best_sentences(question, chunk, top_k=2):
    sentences = re.split(
        r'(?<=[.!?])\s+',
        chunk
    )

    sentences = [
        s.strip()
        for s in sentences
        if len(s.strip()) > 20
    ]

    if not sentences:
        return []

    question_embedding = generate_embeddings(
        [question]
    )

    sentence_embeddings = generate_embeddings(
        sentences
    )

    similarities = cosine_similarity(
        question_embedding,
        sentence_embeddings
    )[0]

    ranked = sorted(
        zip(sentences, similarities),
        key=lambda x: x[1],
        reverse=True
    )

    evidence = []

    for sentence, similarity in ranked[:top_k]:
        evidence.append({
            "text": sentence,
            "score": round(float(similarity), 3),
            "strength": get_strength(similarity)
        })

    return evidence

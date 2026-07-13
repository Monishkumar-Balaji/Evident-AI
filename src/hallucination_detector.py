import re

from sklearn.metrics.pairwise import cosine_similarity

from embedder import generate_embeddings


def split_sentences(text):
    """
    Split answer into individual sentences.
    """

    sentences = re.split(
        r'(?<=[.!?])\s+',
        text
    )

    return [
        s.strip()
        for s in sentences
        if len(s.strip()) > 10
    ]


def verify_answer(answer, evidence, threshold=0.75):
    """
    Verify every sentence of the generated answer
    against extracted evidence.
    """

    answer_sentences = split_sentences(answer)

    evidence_sentences = []

    for item in evidence:

        evidence_sentences.extend(
            sentence["text"]
            for sentence in item["sentences"]
        )

    if not evidence_sentences:

        return []

    evidence_embeddings = generate_embeddings(
        evidence_sentences
    )

    results = []

    for sentence in answer_sentences:

        sentence_embedding = generate_embeddings(
            [sentence]
        )

        similarities = cosine_similarity(
            sentence_embedding,
            evidence_embeddings
        )[0]

        best_score = float(max(similarities))

        results.append({

            "sentence": sentence,

            "score": round(best_score, 3),

            "verified": best_score >= threshold

        })

    return results
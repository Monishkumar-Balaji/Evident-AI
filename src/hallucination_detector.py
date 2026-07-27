import re

from sklearn.metrics.pairwise import cosine_similarity

from embedder import generate_embeddings


def split_sentences(text):
    """
    Split answer into individual sentences.
    """

    sentences = re.split(
        r'(?<=[.!?])\s+(?![a-z])',
        text
    )

    return [
        s.strip()
        for s in sentences
        if len(s.strip()) > 10
    ]


def verify_answer(answer, evidence, threshold=0.70):
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

    if not evidence_sentences or not answer_sentences:
        return []

    # Embed evidence + answer sentences in a single API request
    all_texts = evidence_sentences + answer_sentences
    all_embeddings = generate_embeddings(all_texts)

    evidence_count = len(evidence_sentences)

    evidence_embeddings = all_embeddings[:evidence_count]
    answer_embeddings = all_embeddings[evidence_count:]

    # Compare every answer sentence against all evidence sentences
    similarities = cosine_similarity(
        answer_embeddings,
        evidence_embeddings
    )

    results = []

    for i, sentence in enumerate(answer_sentences):
        best_score = float(max(similarities[i]))

        results.append({
            "sentence": sentence,
            "score": round(best_score, 3),
            "verified": best_score >= threshold
        })

    return results
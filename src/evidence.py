from sentence_extractor import extract_best_sentences

def build_evidence(question, chunks):

    evidence = []

    for chunk in chunks:

        evidence.append({

            "page": chunk["page"],

            "distance": round(
                chunk["distance"],
                3
            ),

            "sentences": extract_best_sentences(
                question,
                chunk["text"]
            )

        })

    return evidence            "source": chunk.get("source"),


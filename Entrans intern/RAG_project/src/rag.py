#rag.py
from retriever import search
from prompt import build_prompt
from generator import generate

# Maximum acceptable distance from ChromaDB
# Lower = more similar
DISTANCE_THRESHOLD = 0.55


def ask(question):

    # Retrieve chunks
    retrieved_chunks = search(question)

    # Filter low-quality chunks and remove duplicates
    filtered_chunks = []
    seen = set()

    for chunk in retrieved_chunks:

        # Ignore weak matches
        if chunk["distance"] > DISTANCE_THRESHOLD:
            continue

        # Remove duplicate chunks
        key = (chunk["page"], chunk["text"])

        if key in seen:
            continue

        seen.add(key)
        filtered_chunks.append(chunk)

    # If nothing relevant is found, don't call the LLM
    if len(filtered_chunks) == 0:
        return {
            "answer": "I could not find this information in the uploaded documents.",
            "sources": []
        }

    # Build prompt
    prompt = build_prompt(
        question,
        filtered_chunks
    )

    # Generate answer
    answer = generate(prompt)

    return {
        "answer": answer,
        "sources": filtered_chunks
    }
# prompy.py
def build_prompt(question, retrieved_chunks):
    """
    Build a prompt for the LLM using the retrieved document chunks.
    """

    context = ""

    for i, chunk in enumerate(retrieved_chunks, start=1):
        context += (
            f"Document Chunk {i}\n"
            f"Page: {chunk['page']}\n"
            "-------------------------\n"
            f"{chunk['text']}\n\n"
        )

    prompt = f"""
You are an expert Document Question Answering Assistant.

Your task is to answer the user's question ONLY using the information provided in the context below.

STRICT RULES:

1. Use ONLY the provided context.
2. NEVER use your own knowledge.
3. NEVER make assumptions.
4. NEVER fabricate information.
5. If the answer is not completely present in the context, reply EXACTLY:

"I could not find this information in the uploaded documents."

6. Keep the answer concise and accurate.
7. At the end of the answer, mention the page number(s) you used.

========================
CONTEXT
========================

{context}

========================
QUESTION
========================

{question}

========================
ANSWER
========================
"""

    return prompt
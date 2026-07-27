# embedder.py
from huggingface_hub import InferenceClient
from config import EMBEDDING_MODEL, HF_TOKEN
import numpy as np

print("Using Hugging Face remote embedding API...")

client = InferenceClient(
    provider="hf-inference",
    api_key=HF_TOKEN,
    timeout=60
)


def generate_embeddings(texts, batch_size=10):
    if not texts:
        return []

    all_embeddings = []

    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]

        embeddings = client.feature_extraction(
            batch,
            model=EMBEDDING_MODEL
        )

        embeddings = np.asarray(embeddings, dtype=np.float32)

        if embeddings.ndim == 1:
            embeddings = embeddings.reshape(1, -1)

        # Normalize each embedding
        norms = np.linalg.norm(
            embeddings,
            axis=1,
            keepdims=True
        )
        norms[norms == 0] = 1

        embeddings = embeddings / norms

        all_embeddings.extend(embeddings.tolist())

    return all_embeddings
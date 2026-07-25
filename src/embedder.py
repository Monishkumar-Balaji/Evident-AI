from huggingface_hub import InferenceClient
from config import EMBEDDING_MODEL, HF_TOKEN
import numpy as np

print("Using Hugging Face remote embedding API...")

client = InferenceClient(
    provider="hf-inference",
    api_key=HF_TOKEN
)


def generate_embeddings(texts):
    embeddings = []

    for text in texts:
        embedding = client.feature_extraction(
            text,
            model=EMBEDDING_MODEL
        )

        embedding = np.asarray(embedding, dtype=np.float32)

        # Ensure a single 1-D embedding
        if embedding.ndim > 1:
            embedding = embedding.mean(axis=0)

        # Normalize like SentenceTransformer(normalize_embeddings=True)
        norm = np.linalg.norm(embedding)
        if norm > 0:
            embedding = embedding / norm

        embeddings.append(embedding.tolist())

    return embeddings
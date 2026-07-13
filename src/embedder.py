# embedder.py
from sentence_transformers import SentenceTransformer
from config import EMBEDDING_MODEL

print("Loading embedding model...")

model = SentenceTransformer(EMBEDDING_MODEL)

print("Embedding model loaded.")

def generate_embeddings(texts):
    return model.encode(
        texts,
        normalize_embeddings=True
    )
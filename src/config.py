# config.py
import os
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"

COLLECTION_NAME = "documents"

CHROMA_PATH = "../chroma_db"

TOP_K = 3

MIN_TOP_K = 2

DEFAULT_TOP_K = 5

MAX_TOP_K = 8

MAX_CONTEXT_CHUNKS = 3

SIMILARITY_THRESHOLD = 0.65

MAX_RETRIEVAL_DISTANCE = 0.85

MIN_CHUNK_FILTER_SCORE = 45

LLM_MODEL = "microsoft/Phi-3-mini-4k-instruct"

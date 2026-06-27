# config.py
import os
from dotenv import load_dotenv

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"

COLLECTION_NAME = "documents"

CHROMA_PATH = "../chroma_db"

TOP_K = 3

SIMILARITY_THRESHOLD = 0.65

LLM_MODEL = "microsoft/Phi-3-mini-4k-instruct"


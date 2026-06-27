# llm.py
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
import os

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

client = InferenceClient(
    api_key=HF_TOKEN
)
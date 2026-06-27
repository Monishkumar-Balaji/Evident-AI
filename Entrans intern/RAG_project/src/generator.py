# generator.py
from huggingface_hub import InferenceClient
from huggingface_hub.utils import HfHubHTTPError
from config import HF_TOKEN, LLM_MODEL

client = InferenceClient(
    api_key=HF_TOKEN
)

def generate(prompt):
    try:
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You answer ONLY from the provided context. "
                        "If the answer is not present, say "
                        "'I could not find this information in the uploaded documents.'"
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0,
            max_tokens=300
        )

        return response.choices[0].message.content
    
    except HfHubHTTPError as e:
        return f"LLM Error: {e}"

    except Exception as e:
        return f"Unexpected Error: {e}"
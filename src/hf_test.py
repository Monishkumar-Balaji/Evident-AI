from huggingface_hub import InferenceClient
from config import HF_TOKEN

client = InferenceClient(
    api_key=HF_TOKEN
)

models = [
    "Qwen/Qwen2.5-7B-Instruct",
    "meta-llama/Llama-3.1-8B-Instruct",
    "mistralai/Mistral-7B-Instruct-v0.3"
]

for model in models:
    print(f"\nTesting: {model}")
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": "Say hello in one sentence."
                }
            ],
            max_tokens=30
        )
        print("Works!")
        print(response.choices[0].message.content)
    except Exception as e:
        print("Failed!")
        print(str(e)[:200])
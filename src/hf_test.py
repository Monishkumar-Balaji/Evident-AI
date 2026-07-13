from huggingface_hub import InferenceClient
from config import HF_TOKEN

client = InferenceClient(
    api_key=HF_TOKEN
)

models = [
    "microsoft/Phi-3-mini-4k-instruct",
    "google/gemma-2-2b-it",
    "Qwen/Qwen2.5-7B-Instruct",
    "meta-llama/Llama-3.2-3B-Instruct"
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

        print("✅ Works")
        print(response.choices[0].message.content)
        break

    except Exception as e:

        print("❌ Failed")
        print(e)
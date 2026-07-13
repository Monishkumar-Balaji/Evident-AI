# test.py
from retriever import search

results = search(
    "What is the aim of cricket?"
)

for i, result in enumerate(results, start=1):

    print(f"\nResult {i}")
    print(f"Page: {result['page']}")
    print(f"Distance: {result['distance']:.4f}")
    print(result['text'][:300])
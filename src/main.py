from indexer import index_document
from rag import ask


while True:

    print("\n===== RAG MENU =====")
    print("1. Index PDF")
    print("2. Ask Question")
    print("3. Exit")

    choice = input("\nEnter choice: ")

    if choice == "1":

        pdf_path = input("PDF Path: ")

        index_document(pdf_path)

    elif choice == "2":

        while True:

            question = input("\nAsk: ")

            if question.lower() == "exit":
                break

            result = ask(question)

            print("\nAnswer:\n")
            print(result["answer"])

            retrieval_quality = result.get("retrieval_quality")
            if retrieval_quality:
                print("\nRetrieval Quality")
                print("======================")
                print(
                    f"{retrieval_quality['score']}% "
                    f"({retrieval_quality['level']})"
                )
                print(retrieval_quality["reason"])

            chunk_filter = result.get("chunk_filter")
            if chunk_filter:
                print("\nChunk Filtering")
                print("======================")
                print(chunk_filter["reason"])
                print(
                    f"Retrieved: {chunk_filter['retrieved_count']} | "
                    f"Kept: {chunk_filter['kept_count']} | "
                    f"Weak: {chunk_filter['removed_weak_count']} | "
                    f"Duplicates: {chunk_filter['removed_duplicate_count']} | "
                    f"Low score: {chunk_filter['removed_low_score_count']}"
                )

                for kept in chunk_filter["kept_chunks"]:
                    source_name = kept.get("source") or "Unknown source"
                    print(
                        f"- {source_name} | Page {kept['page']} | "
                        f"Filter={kept['filter_score']} | "
                        f"Retrieval={kept['retrieval_score']} | "
                        f"Evidence={kept['evidence_score']}"
                    )

            print("\nConfidence")
            print("======================")
            print(
                f"{result['confidence']['score']}% "
                f"({result['confidence']['level']})"
            )

            if result["confidence"].get("explanation"):
                print(result["confidence"]["explanation"])

            print("\n======================")

            if result["evidence"]:
                print("Evidence")
                print("======================")

                for item in result["evidence"]:

                    print(f"\nPage : {item['page']}")
                    print(f"Chunk Distance : {item['distance']}")

                    for sentence in item["sentences"]:

                        print()
                        print(
                            sentence["strength"],
                            f"({sentence['score']})"
                        )
                        print(sentence["text"])

                print("\n======================")

            if result["verification"]:
                print("Verification")
                print("======================")

                for item in result["verification"]:
                    status = "VERIFIED" if item["verified"] else "UNSUPPORTED"
                    print()
                    print(status)
                    print(f"Similarity : {item['score']}")
                    print(item["sentence"])

            print("\nSources:")

            if len(result["sources"]) == 0:
                print("No supporting document found.")

            else:
                for source in result["sources"]:
                    source_name = source.get("source") or "Unknown source"
                    filter_score = source.get("filter_score", 0)
                    print(
                        f"{source_name} | Page {source['page']} "
                        f"(Distance={source['distance']:.3f}, "
                        f"Filter={filter_score})"
                    )

    elif choice == "3":
        break

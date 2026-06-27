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

            print("\nSources:")

            if len(result["sources"]) == 0:
                print("No supporting document found.")

            else:
                for source in result["sources"]:
                    print(
                        f"Page {source['page']} "
                        f"(Distance={source['distance']:.3f})"
                    )

    elif choice == "3":
        break
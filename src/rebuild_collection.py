from rebuild import collection_status, rebuild_collection

status = collection_status()
print(f"Current vectors: {status['vector_count']}")
print(f"Legacy vectors without source metadata: {status['legacy_count']}")
paths = input("PDF/DOCX paths (comma-separated): ")
confirmation = input("This removes all current vectors. Type REBUILD to continue: ")

if confirmation != "REBUILD":
    print("Rebuild cancelled.")
else:
    try:
        result = rebuild_collection(paths.split(","))
        print(
            f"Rebuild complete. Removed {result['deleted_vectors']} vector(s); "
            f"{result['status']['vector_count']} vector(s) stored."
        )
    except (FileNotFoundError, ValueError) as error:
        print(f"Rebuild failed: {error}")
    except Exception as error:
        print(f"An unexpected error occurred: {error}")
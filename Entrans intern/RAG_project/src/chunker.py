# chunker.py
from langchain_text_splitters import RecursiveCharacterTextSplitter
import re
from preprocessor import clean_text

splitter = RecursiveCharacterTextSplitter(
    chunk_size=350,
    chunk_overlap=50,
    separators=[
        "\n\n",   # paragraphs
        "\n",     # new lines
        ". ",     # sentences
        "? ",
        "! ",
        " ",      # words
        ""
    ]
)


def create_chunks(pages):
    chunk_counter = 0
    chunks = []

    for page_data in pages:

        page = page_data["page"]
        text = clean_text(page_data["text"])
        split_text = splitter.split_text(text)

        for chunk in split_text:
            chunk_counter += 1

            chunks.append({
                "id": chunk_counter,
                "page": page,
                "chunk": chunk_counter,
                "length": len(chunk),
                "text": chunk
            })

    return chunks
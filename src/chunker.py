# chunker.py
from langchain_text_splitters import RecursiveCharacterTextSplitter
import re
from preprocessor import clean_text
from pathlib import Path

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


def create_chunks(pages, source_file):
    chunk_id = -1
    chunks = []

    for page_data in pages:

        page = page_data["page"]
        text = clean_text(page_data["text"])
        split_text = splitter.split_text(text)

        for chunk in split_text:
            chunk_id += 1

            chunks.append({
                "id": chunk_id,
                "page": page,
                "chunk": chunk_id,
                "length": len(chunk),
                "source": Path(source_file).name,
                "text": chunk
            })

    return chunks
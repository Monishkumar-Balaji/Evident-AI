# preprocessor.py
import re


def clean_text(text):
    """
    Clean extracted text before chunking.
    """

    # Remove URLs
    text = re.sub(r"http\S+", "", text)

    # Replace multiple spaces with one
    text = re.sub(r"\s+", " ", text)

    # Remove multiple blank lines
    text = re.sub(r"\n{2,}", "\n\n", text)

    # Remove leading/trailing spaces
    text = text.strip()

    return text
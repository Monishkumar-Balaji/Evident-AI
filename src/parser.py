# parser.py
import fitz  # PyMuPDF
from docx import Document


def extract_pdf_text(pdf_path):
    pages = []

    pdf = fitz.open(pdf_path)

    for page_num in range(len(pdf)):
        page = pdf[page_num]

        pages.append({
            "page": page_num + 1,
            "text": page.get_text()
        })

    pdf.close()

    return pages


def extract_docx_text(docx_path):
    doc = Document(docx_path)

    text = "\n".join(
        paragraph.text
        for paragraph in doc.paragraphs
    )

    return text


def extract_text(file_path):
    if file_path.endswith(".pdf"):
        return extract_pdf_text(file_path)

    elif file_path.endswith(".docx"):
        return extract_docx_text(file_path)

    else:
        raise ValueError("Unsupported file type")
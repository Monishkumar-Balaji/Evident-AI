import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from docx import Document

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from chunker import create_chunks
from parser import extract_text


class IngestionTests(unittest.TestCase):
    def test_chunks_have_sequential_ids(self):
        chunks = create_chunks(
            [{"page": 1, "text": "Sentence. " * 100}],
            "example.pdf",
        )

        self.assertGreater(len(chunks), 1)
        self.assertEqual([item["id"] for item in chunks], list(range(len(chunks))))

    def test_docx_extraction_uses_page_contract(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "sample.docx"
            document = Document()
            document.add_paragraph("Readable DOCX text.")
            document.save(path)
            pages = extract_text(str(path))


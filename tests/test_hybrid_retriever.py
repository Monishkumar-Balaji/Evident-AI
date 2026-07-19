import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from keyword_retriever import tokenize, BM25
from hybrid_retriever import hybrid_search
from retriever import search


class HybridSearchTests(unittest.TestCase):
    def test_tokenize(self):
        text = "Hello, World! Welcome to RAG (Hybrid Search) 101."
        tokens = tokenize(text)
        expected = ["hello", "world", "welcome", "to", "rag", "hybrid", "search", "101"]
        self.assertEqual(tokens, expected)

    def test_bm25_scoring(self):
        corpus = [
            ["aim", "of", "cricket", "is", "to", "score", "runs"],
            ["cricket", "is", "played", "with", "a", "bat", "and", "ball"],
            ["weather", "is", "nice", "today"]
        ]
        bm25 = BM25(corpus)
        
        # Query with keyword "cricket"
        scores = bm25.get_scores(["cricket"])
        
        # "cricket" appears in doc 0 and doc 1, but not doc 2
        self.assertGreater(scores[0], 0.0)
        self.assertGreater(scores[1], 0.0)
        self.assertEqual(scores[2], 0.0)
        
        # Doc 0 is shorter than Doc 1 (7 words vs 8 words), so under BM25,
        # the shorter document gets a slightly higher score for the same term frequency.
        self.assertGreater(scores[0], scores[1])

    def test_hybrid_search_integration(self):
        # Verify that hybrid_search runs successfully and returns the expected schema
        results = hybrid_search("cricket", top_k=2)
        
        # There should be results since cricket.pdf is indexed in the database
        self.assertGreater(len(results), 0)
        for result in results:
            self.assertIn("page", result)
            self.assertIn("chunk", result)
            self.assertIn("length", result)
            self.assertIn("source", result)
            self.assertIn("distance", result)
            self.assertIn("text", result)
            self.assertLessEqual(result["distance"], 0.85)

    def test_retriever_interface_integration(self):
        # Verify that retriever's search function delegates correctly and behaves identically
        results = search("cricket")
        self.assertGreater(len(results), 0)
        for result in results:
            self.assertIn("distance", result)
            self.assertIn("text", result)

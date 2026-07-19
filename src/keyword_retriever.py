# keyword_retriever.py
import re
import math
from vectordb import collection

class BM25:
    """
    Standard BM25Okapi implementation for keyword scoring.
    """
    def __init__(self, corpus, k1=1.5, b=0.75):
        self.k1 = k1
        self.b = b
        self.corpus_size = len(corpus)
        self.doc_len = [len(doc) for doc in corpus]
        self.avgdl = sum(self.doc_len) / self.corpus_size if self.corpus_size > 0 else 0.0
        
        self.doc_freqs = []
        self.idf = {}
        
        nd = {}  # term -> document frequency
        for doc in corpus:
            frequencies = {}
            for word in doc:
                frequencies[word] = frequencies.get(word, 0) + 1
            self.doc_freqs.append(frequencies)
            
            for word in frequencies:
                nd[word] = nd.get(word, 0) + 1
                
        for word, freq in nd.items():
            # Standard BM25 IDF formula with smoothing to avoid negative IDF
            self.idf[word] = math.log(1 + (self.corpus_size - freq + 0.5) / (freq + 0.5))
            
    def get_scores(self, query):
        scores = []
        for i in range(self.corpus_size):
            score = 0.0
            doc_len = self.doc_len[i]
            frequencies = self.doc_freqs[i]
            for word in query:
                if word in frequencies:
                    freq = frequencies[word]
                    numerator = self.idf.get(word, 0) * freq * (self.k1 + 1)
                    denominator = freq + self.k1 * (1.0 - self.b + self.b * doc_len / self.avgdl)
                    score += numerator / denominator
            scores.append(score)
        return scores


def tokenize(text):
    """
    Tokenize text into lowercase alphanumeric words.
    """
    return re.findall(r"\w+", text.lower())


# Global cache for BM25 index and chunk metadata
_bm25_instance = None
_cached_ids = set()
_cached_chunks = []  # List of dictionaries containing chunk details

def get_bm25_retriever():
    """
    Loads/rebuilds the BM25 index and chunk cache dynamically.
    Checks the document IDs in ChromaDB to determine if the cache is stale.
    """
    global _bm25_instance, _cached_ids, _cached_chunks
    
    # Fast check of collection IDs to determine if collection has changed
    db_records = collection.get(include=[])
    db_ids = db_records.get("ids", [])
    db_ids_set = set(db_ids)
    
    if _bm25_instance is None or _cached_ids != db_ids_set:
        # Fetch all documents, metadatas, and embeddings from ChromaDB
        full_records = collection.get(include=["documents", "metadatas", "embeddings"])
        
        ids = full_records.get("ids", [])
        documents = full_records.get("documents", [])
        metadatas = full_records.get("metadatas", [])
        embeddings = full_records.get("embeddings", [])
        
        tokenized_corpus = []
        _cached_chunks = []
        
        for idx in range(len(ids)):
            text = documents[idx]
            tokenized_corpus.append(tokenize(text))
            _cached_chunks.append({
                "id": ids[idx],
                "text": text,
                "metadata": metadatas[idx],
                "embedding": embeddings[idx]
            })
            
        _bm25_instance = BM25(tokenized_corpus)
        _cached_ids = db_ids_set
        
    return _bm25_instance, _cached_chunks


def keyword_search(query, top_k=5):
    """
    Perform a BM25 keyword search over all documents in the vector database.
    """
    bm25, cached_chunks = get_bm25_retriever()
    if not cached_chunks:
        return []
        
    tokenized_query = tokenize(query)
    scores = bm25.get_scores(tokenized_query)
    
    results = []
    for idx, score in enumerate(scores):
        if score > 0.0:
            results.append({
                "chunk_id": cached_chunks[idx]["id"],
                "score": score,
                "text": cached_chunks[idx]["text"],
                "metadata": cached_chunks[idx]["metadata"],
                "embedding": cached_chunks[idx]["embedding"]
            })
            
    # Sort descending by BM25 score
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]

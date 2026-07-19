# hybrid_retriever.py
import numpy as np
from config import HYBRID_ALPHA, MAX_RETRIEVAL_DISTANCE
from embedder import generate_embeddings
from vectordb import collection
from keyword_retriever import keyword_search

def hybrid_search(query, top_k=None):
    """
    Hybrid search combining ChromaDB semantic search with a custom BM25 keyword search.
    Scores are normalized and merged into a hybrid distance metric.
    """
    num_items = collection.count()
    if num_items == 0:
        return []
        
    if top_k is None:
        from retriever import choose_top_k
        top_k = choose_top_k(query)
        
    top_k = min(top_k, num_items)
    
    # 1. Fetch semantic search results
    query_embedding = generate_embeddings([query])[0]
    
    vector_results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=top_k
    )
    
    v_ids = vector_results.get("ids", [[]])[0]
    v_docs = vector_results.get("documents", [[]])[0]
    v_metadatas = vector_results.get("metadatas", [[]])[0]
    v_distances = vector_results.get("distances", [[]])[0]
    
    # 2. Fetch keyword search results
    kw_candidates = keyword_search(query, top_k=top_k)
    
    # 3. Merge candidates and calculate distances
    merged = {}
    
    # Add vector candidates
    for idx in range(len(v_ids)):
        cid = v_ids[idx]
        meta = v_metadatas[idx]
        merged[cid] = {
            "id": cid,
            "text": v_docs[idx],
            "page": meta["page"],
            "chunk": meta["chunk"],
            "length": meta["length"],
            "source": meta.get("source"),
            "vector_distance": v_distances[idx],
            "bm25_score": 0.0
        }
        
    # Add/update keyword candidates
    q_emb = np.array(query_embedding)
    for candidate in kw_candidates:
        cid = candidate["chunk_id"]
        if cid in merged:
            merged[cid]["bm25_score"] = candidate["score"]
        else:
            # Candidate only found in BM25 search: compute its exact vector distance
            chunk_emb = np.array(candidate["embedding"])
            vector_distance = float(np.sum((q_emb - chunk_emb) ** 2))
            
            meta = candidate["metadata"]
            merged[cid] = {
                "id": cid,
                "text": candidate["text"],
                "page": meta["page"],
                "chunk": meta["chunk"],
                "length": meta["length"],
                "source": meta.get("source"),
                "vector_distance": vector_distance,
                "bm25_score": candidate["score"]
            }
            
    # 4. Normalize BM25 scores
    bm25_scores = [c["bm25_score"] for c in merged.values()]
    max_bm25 = max(bm25_scores) if bm25_scores else 0.0
    
    # 5. Blend metrics and filter results
    alpha = HYBRID_ALPHA
    formatted_results = []
    
    for cid, candidate in merged.items():
        v_dist = candidate["vector_distance"]
        b_score = candidate["bm25_score"]
        
        # Scale BM25 score to [0, 1]
        s_bm25 = (b_score / max_bm25) if max_bm25 > 0.0 else 0.0
        
        # Convert BM25 score to a distance metric
        d_bm25 = 1.0 - s_bm25
        
        # Linear combination of the two distance metrics
        d_hybrid = alpha * v_dist + (1.0 - alpha) * d_bm25
        d_hybrid = max(0.0, min(2.0, d_hybrid))
        
        if d_hybrid <= MAX_RETRIEVAL_DISTANCE:
            formatted_results.append({
                "page": candidate["page"],
                "chunk": candidate["chunk"],
                "length": candidate["length"],
                "source": candidate["source"],
                "distance": d_hybrid,
                "text": candidate["text"]
            })
            
    # 6. Sort by hybrid distance (ascending) and return top_k
    formatted_results.sort(key=lambda x: x["distance"])
    return formatted_results[:top_k]

import json 
from rank_bm25 import BM25Okapi

def keyword_search(query, k=5):
    """
    Keyword search using BM25 - reloads chunks each time to get latest uploads
    """
    try:
        # Reload chunks each time (not at import time)
        with open("data/chunks.json", "r", encoding="utf-8") as f:
            chunks = json.load(f)
        
        if not chunks:
            print("No chunks available for keyword search")
            return []
        
        print(f"Keyword searching in {len(chunks)} chunks...")
        
        corpus = [c["text"].split() for c in chunks]
        bm25 = BM25Okapi(corpus)
        
        tokenized_query = query.split()
        scores = bm25.get_scores(tokenized_query)
        ranked = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
        results = [chunks[i] for i in ranked[:k]]
        
        print(f"Keyword search returned {len(results)} results")
        return results
        
    except Exception as e:
        print(f"Error in keyword_search: {str(e)}")
        return []
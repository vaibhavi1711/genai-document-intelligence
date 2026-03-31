import faiss
import numpy as np
import json
from sentence_transformers import SentenceTransformer

INDEX_FILE = "data/vector.index"
CHUNKS_FILE = "data/chunks.json"

model = SentenceTransformer('all-MiniLM-L6-v2')


def retrieve(query, k=5):
    """
    Vector search using FAISS - reloads index and chunks each time
    """
    try:
        # Reload index and chunks each time (not at import time)
        index = faiss.read_index(INDEX_FILE)
        
        with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
            chunks = json.load(f)
        
        if index is None or len(chunks) == 0:
            print("No documents indexed yet. Please upload PDFs first.")
            return []
        
        print(f"Vector searching in {len(chunks)} chunks...")
        
        query_embedding = model.encode([query])
        D, I = index.search(np.array(query_embedding, dtype=np.float32), k)
        
        results = []
        for idx in I[0]:
            if idx < len(chunks):
                results.append(chunks[idx])
        
        print(f"Vector search returned {len(results)} results")
        return results
        
    except Exception as e:
        print(f"Error in retrieve: {str(e)}")
        import traceback
        traceback.print_exc()
        return []
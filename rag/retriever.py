import faiss
import numpy as np
import json
from sentence_transformers import SentenceTransformer

INDEX_FILE = "data/vector.index"
CHUNKS_FILE = "data/chunks.json"

model = SentenceTransformer('all-MiniLM-L6-v2')

index = faiss.read_index(INDEX_FILE)

with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
    chunks = json.load(f)
    

def retrieve(query, k=5):
    
    query_embedding = model.encode([query])
    
    D, I = index.search(np.array(query_embedding), k)
    
    results = []
    
    for idx in I[0]:
         results.append(chunks[idx])
    return results
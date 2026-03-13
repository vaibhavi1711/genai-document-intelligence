from sentence_transformers import SentenceTransformer
import json
import numpy as np

INPUT_FILE = "data/chunks.json"
OUTPUT_FILE = "data/embeddings.npy"


def create_embeddings():
    
    # load chunks
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        chunks = json.load(f)
        
    texts = [c["text"] for c in chunks]
    
    # Load embedding model  
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # create embeddings
    embeddings = model.encode(texts, show_progress_bar=True)
    
    np.save(OUTPUT_FILE, embeddings)
    
    print(f"Embeddings created")
    
    
if __name__ == "__main__":
    create_embeddings()
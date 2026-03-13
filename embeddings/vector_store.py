import faiss
import numpy as np

EMBEDDING_FILE = "data/embeddings.npy"
INDEX_FILE = "data/vector.index"

def build_faiss_index():
    
    # Load embeddings
    embeddings = np.load(EMBEDDING_FILE)
     
    dimension = embeddings.shape[1]
    
    # Build FAISS index
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    
    # Save index to disk
    faiss.write_index(index, INDEX_FILE)
    
    print(f"FAISS index created with {index.ntotal} vectors.")
    
if __name__ == "__main__":
    build_faiss_index()
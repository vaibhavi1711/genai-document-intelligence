from .pdf_loader import load_pdf
from .cleaner import clean_text
from .chunker import chunk_text
import json
import numpy as np
import os

CHUNKS_FILE = "data/chunks.json"
EMBEDDINGS_FILE = "data/embeddings.npy"


def process_uploaded_file(filepath):
    print(f"Processing uploaded file: {filepath}")

    try:
        docs = load_pdf(filepath)  # returns list of dicts
        print(f"Loaded {len(docs)} document(s)")
        
        cleaned_docs = []

        for doc in docs:
            print(f"Cleaning text from {doc['source']}...")
            text = doc["text"]  # get the text string
            print(f"Text type: {type(text)}, length: {len(text) if isinstance(text, str) else 'N/A'}")
            
            cleaned_text = clean_text(text)  # clean the text
            print(f"Cleaned text type: {type(cleaned_text)}")
            
            cleaned_docs.append({
                "text": cleaned_text,
                "source": doc["source"]  # preserve source
            })

        all_chunks = []
        for doc in cleaned_docs:
            print(f"Chunking {doc['source']}...")
            print(f"Chunk input - type: {type(doc['text'])}, is string: {isinstance(doc['text'], str)}")
            
            chunks = chunk_text(doc["text"])  # FIX: Pass only the text string, not the dict
            print(f"Created {len(chunks)} chunks")
            
            for chunk_idx, chunk_content in enumerate(chunks):
                all_chunks.append({
                    "text": chunk_content,
                    "source": doc["source"],
                    "chunk_id": chunk_idx
                })

        # Load existing chunks and append new ones
        existing_chunks = []
        if os.path.exists(CHUNKS_FILE):
            with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
                existing_chunks = json.load(f)
        
        # Combine and save all chunks
        all_chunks = existing_chunks + all_chunks
        with open(CHUNKS_FILE, "w", encoding="utf-8") as f:
            json.dump(all_chunks, f, indent=2)
        
        print(f"Added {len(all_chunks) - len(existing_chunks)} new chunks. Total chunks: {len(all_chunks)}")

        # Regenerate embeddings and FAISS index
        regenerate_embeddings_and_index(all_chunks)
        
        print("File processed successfully!")
    
    except Exception as e:
        print(f"ERROR in process_uploaded_file: {str(e)}")
        import traceback
        traceback.print_exc()
        raise


def regenerate_embeddings_and_index(chunks):
    """Regenerate embeddings and FAISS index for all chunks"""
    try:
        from sentence_transformers import SentenceTransformer
        import faiss
        
        if not chunks:
            print("No chunks to embed")
            return
        
        print(f"Generating embeddings for {len(chunks)} chunks...")
        
        # Get texts from chunks
        texts = [c["text"] for c in chunks]
        print(f"Extracted {len(texts)} texts")
        
        # Load embedding model
        model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Create embeddings
        embeddings = model.encode(texts, show_progress_bar=True)
        print(f"Embeddings shape: {embeddings.shape}")
        
        # Save embeddings
        np.save(EMBEDDINGS_FILE, embeddings)
        print(f"Embeddings saved: {embeddings.shape}")
        
        # Build FAISS index
        print("Building FAISS index...")
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(embeddings.astype(np.float32))
        
        # Save index
        faiss.write_index(index, "data/vector.index")
        print(f"FAISS index created with {index.ntotal} vectors")
        
    except Exception as e:
        print(f"ERROR in regenerate_embeddings_and_index: {str(e)}")
        import traceback
        traceback.print_exc()
        raise
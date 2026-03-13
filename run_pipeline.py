from pipeline.pdf_loader import load_pdfs
from pipeline.cleaner import clean_documents
from pipeline.chunker import chunk_documents
from embeddings.embedder import create_embeddings
from embeddings.vector_store import build_faiss_index

def run_pipeline():
    
    print("Loading PDFs...")
    load_pdfs()
    
    print("Cleaning documents...")
    clean_documents()
    
    print("Chunking documents...")
    chunk_documents()
    
    print("Creating embeddings...")
    create_embeddings()
    
    print("Building FAISS index...")
    build_faiss_index()
    
    print("Pipeline completed successfully")
    
if __name__ == "__main__":
    run_pipeline()
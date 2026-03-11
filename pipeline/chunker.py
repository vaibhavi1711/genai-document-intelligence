import json 

INPUT_FILE = "data/cleaned_documents.json"
OUTPUT_FILE = "data/chunks.json"

CHUNK_SIZE = 300


def chunk_text(text):
    
    words = text.split()
    chunks = []
    
    for i in range(0, len(words), CHUNK_SIZE):
        chunk = " ".join(words[i:i + CHUNK_SIZE])
        chunks.append(chunk)
        
    return chunks

def chunk_documents():
    
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        documents = json.load(f)
        
    all_chunks = []
    
    for doc in documents:
        chunks = chunk_text(doc)
        all_chunks.extend(chunks)
        
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2)
           
    print("Documents chunked successfully")
    
if __name__ == "__main__":
    chunk_documents()
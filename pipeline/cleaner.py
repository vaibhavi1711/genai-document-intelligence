import json
import re

INPUT_FILE = "data/raw_documents.json"
OUTPUT_FILE = "data/cleaned_documents.json"


def clean_text(text):
    
    # remove extra spaces
    text = re.sub(r'\s+', ' ', text)
    
    # remove strange charachters
    text = re.sub(r'[^\w\s.,!?()-]', '', text)
    
    return text.strip()

def clean_documents():
    
    with open(INPUT_FILE, "r") as f:
        documents = json.load(f)
        
    cleaned_docs = []
    
    for doc in documents:
        cleaned_docs.append(clean_text(doc))
        
    with open(OUTPUT_FILE, "w") as f:
        json.dump(cleaned_docs, f)
        
    print("Documents cleaned successfully")
    
    
if __name__ == "__main__":
    clean_documents()
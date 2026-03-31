from pypdf import PdfReader
import os
import json

PDF_FOLDER = "data/pdfs/"
OUTPUT_FILE = "data/raw_documents.json"


def load_pdfs():

    documents = []

    for file in os.listdir(PDF_FOLDER):

        if file.endswith(".pdf"):

            path = os.path.join(PDF_FOLDER, file)
            reader = PdfReader(path)

            text = ""

            for page in reader.pages:
                text += page.extract_text() + "\n"

            documents.append({
                "text": text,
                "source": file
            })

    with open(OUTPUT_FILE, "w") as f:
        json.dump(documents, f)

    print("PDFs loaded successfully")
    
    
    
def load_pdf(filepath):
    """
    Load a single PDF file and return a list of page documents.
    Each document is a dict with 'text' and 'source'.
    """
    from pypdf import PdfReader
    import os

    reader = PdfReader(filepath)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return [{"text": text, "source": os.path.basename(filepath)}]


if __name__ == "__main__":
    load_pdfs()
    

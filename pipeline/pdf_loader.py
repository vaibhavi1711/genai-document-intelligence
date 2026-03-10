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

            documents.append(text)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(documents, f)

    print("PDFs loaded successfully")


if __name__ == "__main__":
    load_pdfs()
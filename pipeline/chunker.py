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

    with open(INPUT_FILE) as f:
        documents = json.load(f)

    all_chunks = []

    for doc in documents:

        text = doc["text"]      # extract text
        source = doc["source"]  # keep metadata

        chunks = chunk_text(text)

        for i, chunk in enumerate(chunks):

            all_chunks.append({
                "text": chunk,
                "source": source,
                "chunk_id": i
            })

    with open(OUTPUT_FILE, "w") as f:
        json.dump(all_chunks, f)

    print("Documents chunked successfully")


if __name__ == "__main__":
    chunk_documents()
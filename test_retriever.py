from rag.retriever import retrieve

query = "What is attention in transformers?"

results = retrieve(query)

for r in results:

    print("\n---")
    print("Chunk:", r["text"][:200])
    print("Source:", r["source"])
    print("Chunk ID:", r["chunk_id"])
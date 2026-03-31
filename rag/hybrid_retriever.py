from rag.retriever import retrieve
from rag.keyword_retriever import keyword_search

def hybrid_retrieve(query):
    
    vector_results = retrieve(query)
    
    keyword_results = keyword_search(query)
    
    combined = vector_results + keyword_results
    
    # remove duplicates
    
    unique = {c["text"]: c for c in combined}
    
    return list(unique.values())
from rag.retriever import retrieve
from openai import OpenAI
from dotenv import load_dotenv
from sentence_transformers import CrossEncoder
import os
from rag.hybrid_retriever import hybrid_retrieve
import requests

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# reranking model
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")


def fetch_wikipedia(query, max_results=3):
    """
    Fetch relevant information from Wikipedia with direct links
    """
    try:
        print(f"Fetching Wikipedia data for: {query}")
        
        # Search Wikipedia
        search_url = "https://en.wikipedia.org/w/api.php"
        search_params = {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "format": "json",
            "srlimit": max_results
        }
        
        search_response = requests.get(search_url, params=search_params, timeout=5)
        search_results = search_response.json()
        
        wiki_docs = []
        
        if "query" in search_results and "search" in search_results["query"]:
            for result in search_results["query"]["search"][:max_results]:
                title = result["title"]
                
                # Get full page content
                content_params = {
                    "action": "query",
                    "titles": title,
                    "prop": "extracts",
                    "explaintext": True,
                    "format": "json"
                }
                
                content_response = requests.get(search_url, params=content_params, timeout=5)
                content_data = content_response.json()
                
                if "query" in content_data and "pages" in content_data["query"]:
                    for page in content_data["query"]["pages"].values():
                        if "extract" in page:
                            # Truncate to first 500 chars to avoid too much text
                            extract = page["extract"][:500]
                            # Create Wikipedia URL with properly formatted title
                            wiki_url = f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}"
                            wiki_docs.append({
                                "text": extract,
                                "source": f"Wikipedia: {title}",
                                "url": wiki_url
                            })
        
        print(f"Fetched {len(wiki_docs)} Wikipedia results")
        return wiki_docs
        
    except Exception as e:
        print(f"Error fetching Wikipedia: {str(e)}")
        return []


def rerank(query, docs):

    pairs = [[query, d["text"]] for d in docs]

    scores = reranker.predict(pairs)

    ranked = sorted(zip(scores, docs), reverse=True)

    return [doc for _, doc in ranked[:5]]  # Increased from 3 to 5 to account for Wikipedia + PDF


def generate_answer(question):
    """
    Generate answer combining Wikipedia data + uploaded PDFs
    """
    try:
        # Get data from uploaded PDFs
        print("Getting data from uploaded PDFs...")
        pdf_docs = hybrid_retrieve(question)
        
        # Get data from Wikipedia
        print("Getting data from Wikipedia...")
        wiki_docs = fetch_wikipedia(question, max_results=2)
        
        # Combine sources
        all_docs = pdf_docs + wiki_docs
        
        if not all_docs:
            print("No documents found from PDFs or Wikipedia")
            return "No information found. Please upload PDFs or try a different search query.", []
        
        # Rerank combined results
        best_docs = rerank(question, all_docs)
        
        # Create context from best docs
        context_parts = []
        sources_with_urls = []
        
        for doc in best_docs:
            source = doc.get("source", "Unknown")
            text = doc.get("text", "")
            url = doc.get("url", None)
            
            context_parts.append(f"[Source: {source}]\n{text}")
            
            # Add to sources list with URL if available
            if url:
                sources_with_urls.append({
                    "name": source,
                    "url": url
                })
            else:
                sources_with_urls.append({
                    "name": source,
                    "url": None
                })
        
        context = "\n\n".join(context_parts)
        
        # Get unique sources
        sources = list({s["name"]: s for s in sources_with_urls}.values())
        
        print(f"Creating answer from {len(best_docs)} sources")
        
        prompt = f"""You are a helpful AI assistant that synthesizes information from multiple sources.

Answer the question using the context provided below from both Wikipedia and uploaded documents.

Context:
{context}

Question:
{question}

IMPORTANT: Please provide your answer in exactly 3 well-structured paragraphs. 
- Paragraph 1: Introduction and overview of the topic
- Paragraph 2: Detailed explanation and key points
- Paragraph 3: Summary, conclusion, and important takeaways

Each paragraph should be clear, comprehensive, and synthesize insights from all available sources."""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        answer = response.choices[0].message.content
        
        return answer, sources
        
    except Exception as e:
        print(f"Error generating answer: {str(e)}")
        import traceback
        traceback.print_exc()
        return f"Error: {str(e)}", []
# GenAI Document Intelligence System

A production-grade Retrieval Augmented Generation (RAG) system that combines uploaded PDFs with Wikipedia data to provide intelligent, multi-source answers with full source attribution.

![Python](https://img.shields.io/badge/python-3.9+-green) ![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-blue) ![License](https://img.shields.io/badge/license-MIT-green)

## Features

✨ **Core Capabilities**
- 📄 PDF document upload and intelligent processing
- 🔍 Hybrid search combining FAISS vector similarity + BM25 keyword matching
- 🌐 Real-time Wikipedia integration for comprehensive answers
- 🤖 AI-powered answer generation using OpenAI GPT-4o-mini
- 📊 Cross-encoder reranking for result prioritization
- 🔗 Clickable source attribution with links to original content
- 💾 Persistent chunk and embedding storage with automatic indexing
- 🎨 Modern responsive web interface with gradient design

✨ **Architecture Highlights**
- Modular pipeline architecture (load → clean → chunk → embed → index)
- Dynamic data reloading for real-time new content availability
- Hybrid retrieval combining semantic (FAISS) + keyword (BM25) search strategies
- Cross-encoder reranking using `ms-marco-MiniLM-L-12-v2` model for relevance scoring
- Structured 3-paragraph AI responses with explicit paragraph purposes
- Comprehensive error handling and logging throughout

## Tech Stack

**Backend**
- FastAPI: REST API for answer generation
- Flask: Web server for UI
- PyPDF: PDF extraction and processing
- sentence-transformers: Text embeddings (all-MiniLM-L6-v2)
- FAISS: Vector similarity search at scale
- rank-bm25: BM25 keyword search implementation
- sentence-transformers: Cross-encoder for reranking
- OpenAI API: GPT-4o-mini for answer synthesis

**Frontend**
- Vanilla JavaScript: Interactive chat interface
- HTML5 & CSS3: Modern responsive design
- Font Awesome: Icon library

**Data Processing**
- regex: Text cleaning and normalization
- numpy: Embedding storage and manipulation
- json: Chunk persistence

## Project Structure

```
genai-document-intelligence/
├── api/
│   └── main.py                 # FastAPI backend for /ask endpoint
├── pipeline/
│   ├── pdf_loader.py          # PDF file loading
│   ├── cleaner.py             # Text cleaning and normalization
│   ├── chunker.py             # Text segmentation (300-word chunks)
│   └── ingest.py              # Complete ingestion orchestration
├── rag/
│   ├── retriever.py           # FAISS vector semantic search
│   ├── keyword_retriever.py   # BM25 keyword search
│   ├── hybrid_retriever.py    # Hybrid (vector + keyword) search
│   └── generator.py           # Wikipedia fetch + AI answer generation
├── embeddings/
│   ├── embedder.py            # Embedding model initialization
│   └── vector_store.py        # FAISS index management
├── ui/
│   ├── app.py                 # Flask web server
│   ├── templates/
│   │   └── index.html         # Web interface
│   └── static/
│       ├── script.js          # Frontend chat logic
│       └── style.css          # Responsive styling
├── data/
│   ├── pdfs/                  # Uploaded PDF storage
│   ├── chunks.json            # Stored document chunks
│   ├── embeddings.npy         # Vector embeddings
│   ├── vector.index           # FAISS index
│   ├── raw_documents.json     # Original documents
│   └── cleaned_documents.json # Cleaned documents
├── requirements.txt
├── README.md
└── LICENSE

```

## Installation & Setup

### Prerequisites
- Python 3.9 or higher
- OpenAI API key
- 2GB RAM minimum (for FAISS indexing)

### Step 1: Clone & Environment
```bash
# Clone repository
git clone https://github.com/yourusername/genai-document-intelligence.git
cd genai-document-intelligence

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Environment Variables
Create a `.env` file in the root directory:
```
OPENAI_API_KEY=sk-your-api-key-here
```

### Step 3: Start Services
**Terminal 1 - FastAPI Backend (port 8000):**
```bash
uvicorn api.main:app --reload
```

**Terminal 2 - Flask Frontend (port 5000):**
```bash
python ui/app.py
```

### Step 4: Access Application
Open browser to: **http://localhost:5000**

## Usage Guide

### Uploading Documents
1. Click "Choose PDF Files" button
2. Select one or multiple PDFs
3. Upload status appears in chat
4. Files processed automatically (cleaned, chunked, embedded)
5. Ready for querying immediately

### Asking Questions
1. Type question in input field
2. System searches both PDF and Wikipedia
3. AI generates 3-paragraph response
4. Click source links to view original content
5. Use copy button to save response

### Example Queries
- "What are the main findings in the uploaded research papers?"
- "Explain how machine learning models work"
- "What are the top frameworks for building web applications?"
- "Compare supervised vs unsupervised learning"

## How It Works

### Document Processing Pipeline
```
PDF Upload
    ↓
Load with PyPDF
    ↓
Extract Text
    ↓
Clean & Normalize (regex)
    ↓
Split into 300-word Chunks
    ↓
Generate Embeddings (sentence-transformers)
    ↓
Build FAISS Index
    ↓
Store: chunks.json, embeddings.npy, vector.index
```

### Query Resolution Pipeline
```
User Question
    ↓
Parallel Retrieval:
├─ FAISS Vector Search (semantic similarity)
├─ BM25 Keyword Search (exact term matching)
└─ Wikipedia API Fetch (real-time knowledge)
    ↓
Combine & Rerank (cross-encoder)
    ↓
Select Top 3-5 Results
    ↓
Generate Answer (GPT-4o-mini)
    ↓
Format: 3 Paragraphs + Source Links
```

### Key Algorithms

**Vector Search (FAISS)**
- Model: all-MiniLM-L6-v2 (384-dim embeddings)
- Index Type: IndexFlatL2 (L2 distance)
- Returns: Top-k semantically similar chunks

**Keyword Search (BM25)**
- Algorithm: Okapi BM25 probabilistic ranking
- Returns: Top-k documents with high term overlap

**Reranking (Cross-Encoder)**
- Model: ms-marco-MiniLM-L-12-v2
- Purpose: Re-rank top-k results by semantic relevance
- Output: Top 3-5 most relevant chunks

**Answer Generation**
- Model: GPT-4o-mini (fast, cost-effective)
- Prompt: Explicit 3-paragraph structure request
- Sources: PDF + Wikipedia with clickable links

## API Endpoints

### FastAPI (http://localhost:8000)

**Health Check**
```bash
GET /
```
Response: `{"status": "API is running"}`

**Ask Question**
```bash
POST /ask
Content-Type: application/json

{
  "question": "What is machine learning?"
}
```
Response:
```json
{
  "question": "What is machine learning?",
  "answer": "Three paragraph response...",
  "sources": [
    {"text": "Chunk text...", "source": "document.pdf or Wikipedia"},
    ...
  ]
}
```

### Flask (http://localhost:5000)

**Web Interface**
```
GET /
```
Returns: Interactive web UI with upload and chat

**Ask Question (via UI)**
```bash
POST /ask
Content-Type: application/json

{
  "question": "Your question here"
}
```

**Upload Files**
```bash
POST /upload
Content-Type: multipart/form-data

{
  "files": [file1.pdf, file2.pdf]
}
```

## Configuration

### Chunk Size
Edit in `pipeline/chunker.py`:
```python
CHUNK_SIZE = 300  # words per chunk
```

### Search Results
Edit in `rag/hybrid_retriever.py`:
```python
top_k = 10  # number of results to retrieve
```

### Reranking Top-K
Edit in `rag/generator.py`:
```python
rerank_top_k = 5  # number of results to rerank
```

### Embedding Model
Edit in `embeddings/embedder.py`:
```python
model_name = "all-MiniLM-L6-v2"  # sentence-transformers model
```

## Performance Metrics

- **PDF Processing**: ~2-5 seconds per document (depending on size)
- **Embedding Generation**: ~0.1 seconds per chunk
- **FAISS Search**: <1ms for 10k chunks
- **BM25 Search**: ~10-50ms for 10k chunks
- **Answer Generation**: ~2-5 seconds (OpenAI API)
- **Total Query Response**: ~5-10 seconds end-to-end

## Error Handling

The system includes comprehensive error handling:
- Invalid PDF format → User message: "Invalid PDF file"
- Missing embeddings → Automatic regeneration
- Wikipedia unavailable → Graceful fallback to PDF only
- API rate limits → Retry with exponential backoff
- Empty uploads → Warning message in UI

All errors logged to console with full traceback for debugging.

## Testing

Test individual components:
```bash
# Test embeddings
python test_embeddings.py

# Test retriever
python test_retriever.py

# Test RAG pipeline
python test_rag.py

# Test API
python test_key.py
```

## Development

### Adding New Features
1. Create modular functions in appropriate files
2. Add error handling with try-except
3. Log operations for debugging
4. Update relevant parsers/configs
5. Test with sample data

### Debugging
- Check `ui/app.py` logs for Flask errors
- Check terminal running `uvicorn` for FastAPI errors
- Check browser console (F12) for frontend errors
- Check `data/` folder for intermediate files

### Code Quality
- Type hints recommended for clarity
- Docstrings for all major functions
- Error messages should be user-friendly
- Log at INFO level for key operations

## Deployment

### Docker (Local Testing)
```bash
docker build -t genai-doc-intelligence .
docker run -p 5000:5000 -p 8000:8000 genai-doc-intelligence
```

### Cloud Deployment (Heroku/Railway)
1. Add `Procfile` with gunicorn + uvicorn startup
2. Set environment variables in platform settings
3. Push to Git, platform auto-deploys
4. Monitor logs for production issues

## Limitations & Future Work

**Current Limitations**
- Max ~10k chunks per index (FAISS memory constraints)
- Wikipedia API rate limits: 200 requests/hour
- OpenAI API costs scale with usage
- Single upload size: <50MB PDFs

**Planned Enhancements**
- [ ] Multi-language support for PDFs and questions
- [ ] Document metadata extraction (author, date, title)
- [ ] User session persistence
- [ ] Query recommendations based on document content
- [ ] Advanced filters: date range, source type, relevance threshold
- [ ] Batch processing for multiple documents
- [ ] Integration with external knowledge bases (ArXiv, PubMed)
- [ ] Fine-tuned models for domain-specific knowledge

## License

MIT License - See [LICENSE](LICENSE) file for details.

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## Support

For issues, questions, or suggestions:
- Open a GitHub issue
- Check existing issues for solutions
- Include error messages and reproduction steps

## Citation

If you use this project in research, please cite:
```
@software{genai_doc_intelligence,
  title={GenAI Document Intelligence System},
  author={Your Name},
  year={2024},
  url={https://github.com/yourusername/genai-document-intelligence}
}
```

---

**Last Updated**: March 2024  
**Maintained by**: Your Name  
**Status**: Active Development ✓
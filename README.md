# 📚 GenAI Document Intelligence

An AI-powered document intelligence system that combines Wikipedia insights with your uploaded PDFs to provide comprehensive, well-sourced answers using advanced retrieval-augmented generation (RAG).

## ✨ Features

### 📄 PDF Upload & Processing
- **Easy Upload**: Upload PDFs directly through the web interface
- **Automatic Processing**: PDFs are automatically extracted, cleaned, and chunked
- **Real-time Feedback**: Visual status messages during processing
- **Batch Upload**: Upload multiple PDFs at once

### 🔍 Hybrid Retrieval System
- **Vector Search**: Semantic similarity using FAISS and sentence-transformers
- **Keyword Search**: BM25-based keyword matching for exact terms
- **Intelligent Ranking**: Cross-encoder reranking for best results
- **Dynamic Loading**: Automatically detects new uploads without restart

### 📚 Multi-Source Intelligence
- **Wikipedia Integration**: Automatically fetches relevant Wikipedia articles
- **PDF Combination**: Seamlessly combines Wikipedia with your uploaded documents
- **Source Attribution**: Clickable links to Wikipedia articles
- **Smart Synthesis**: AI combines insights from multiple sources

### 🤖 AI-Powered Responses
- **GPT-4o-mini**: Uses OpenAI's advanced language model
- **Structured Output**: Returns answers in 3 well-formatted paragraphs
  - Paragraph 1: Introduction and overview
  - Paragraph 2: Detailed explanation with key points
  - Paragraph 3: Summary and important takeaways
- **Context Awareness**: Considers both PDF content and Wikipedia data

### 🎨 Modern User Interface
- **Gradient Design**: Beautiful purple-blue gradient theme
- **Chat Interface**: Real-time conversation with AI
- **Copy Functionality**: 📋 Copy AI responses to clipboard
- **Upload Status**: Visual feedback for file uploads
- **Responsive Design**: Works on desktop and mobile

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- OpenAI API key (get it from [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys))
- pip package manager

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/genai-document-intelligence.git
cd genai-document-intelligence
```

2. **Create virtual environment**
```bash
# Windows
python -m venv venv
.\venv\Scripts\Activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
# Create .env file in project root
echo OPENAI_API_KEY=your-api-key-here > .env
```

5. **Run the application**

Open 2 terminals in the project directory:

**Terminal 1 - FastAPI Backend (Port 8000):**
```bash
uvicorn api.main:app --reload --host 127.0.0.1 --port 8000
```

**Terminal 2 - Flask UI (Port 5000):**
```bash
python ui/app.py
```

6. **Open in browser**
```
http://127.0.0.1:5000
```

## 📁 Project Structure

```
genai-document-intelligence/
│
├── api/
│   ├── __init__.py
│   └── main.py                 # FastAPI endpoints (/ask)
│
├── ui/
│   ├── app.py                  # Flask server
│   ├── templates/
│   │   └── index.html          # Web interface
│   └── static/
│       ├── script.js           # Chat and upload logic
│       └── style.css           # Modern styling
│
├── pipeline/
│   ├── __init__.py
│   ├── pdf_loader.py           # Extract text from PDFs
│   ├── cleaner.py              # Clean and normalize text
│   ├── chunker.py              # Split text into chunks
│   └── ingest.py               # Full ingestion pipeline
│
├── rag/
│   ├── __init__.py
│   ├── retriever.py            # Vector search with FAISS
│   ├── keyword_retriever.py    # BM25 keyword search
│   ├── hybrid_retriever.py     # Combine both retrieval methods
│   └── generator.py            # Wikipedia fetch + answer generation
│
├── embeddings/
│   ├── embedder.py             # Create embeddings from chunks
│   └── vector_store.py         # Build FAISS index
│
├── data/
│   ├── chunks.json             # Processed document chunks
│   ├── embeddings.npy          # Vector embeddings (NumPy)
│   ├── vector.index            # FAISS index file
│   ├── raw_documents.json      # Original PDF content
│   ├── cleaned_documents.json  # Cleaned text
│   └── pdfs/                   # Uploaded PDF storage
│
├── uploads/                    # Temporary upload folder
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (create this)
├── .gitignore
└── README.md
```

## 🔄 How It Works

### Step-by-Step Process

```
1. PDF Upload
   ↓
2. Text Extraction (pypdf)
   ↓
3. Text Cleaning (remove noise, standardize)
   ↓
4. Text Chunking (300-word chunks)
   ↓
5. Embedding Generation (sentence-transformers)
   ↓
6. FAISS Indexing (fast vector search)
   ↓
7. User Query
   ↓
8. Dual Search:
   ├─ Vector Search (semantic similarity)
   └─ Keyword Search (BM25)
   ↓
9. Wikipedia Fetch (via API)
   ↓
10. Results Ranking (cross-encoder)
   ↓
11. Context Creation (combine top results)
   ↓
12. AI Synthesis (GPT-4o-mini)
   ↓
13. 3-Paragraph Response with Sources
```

### Core Components

**PDF Processing Pipeline**
- Loads PDFs using PyPDF
- Cleans text using regex and NLP
- Chunks into overlapping segments
- Generates embeddings using all-MiniLM-L6-v2 model

**Retrieval System**
- **Vector Search**: Uses FAISS for fast similarity search (k=5)
- **Keyword Search**: Uses BM25Okapi for exact matches
- **Hybrid Combination**: Merges results and removes duplicates
- **Reranking**: Cross-encoder ranks top 5 results

**Answer Generation**
- Fetches Wikipedia articles related to query
- Combines Wikipedia + PDF content
- Uses GPT-4o-mini to synthesize response
- Returns 3-paragraph structured answer

## 💻 Technologies Used

| Component | Technology |
|-----------|-----------|
| **Backend API** | FastAPI 0.135.1 |
| **Frontend Server** | Flask 3.1.3 |
| **LLM** | OpenAI GPT-4o-mini |
| **Embeddings** | sentence-transformers (all-MiniLM-L6-v2) |
| **Vector Database** | FAISS (CPU) 1.13.2 |
| **Keyword Search** | rank-bm25 0.2.2 |
| **PDF Parsing** | PyPDF 6.8.0 |
| **Reranking** | cross-encoder (ms-marco-MiniLM-L-6-v2) |
| **Frontend** | HTML5, CSS3, JavaScript (vanilla) |
| **APIs** | Wikipedia API, OpenAI API |

## 📖 Usage Examples

### Example 1: Medical Research
**Upload**: Medical AI research paper
**Query**: "What are the latest AI applications in medical diagnosis?"
**Result**: Combines Wikipedia's AI overview + your paper's specific techniques + GPT-4o synthesis

### Example 2: Technical Documentation
**Upload**: Your project documentation
**Query**: "How does the RAG system work?"
**Result**: Blends Wikipedia's general RAG explanation + your implementation details

### Example 3: News Analysis
**Upload**: News articles about a topic
**Query**: "What is the historical context of this event?"
**Result**: Wikipedia history + article details + comprehensive synthesis

## 🔧 Configuration

### Environment Variables (.env)
```env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxx
```

### API Endpoints

**FastAPI (http://localhost:8000)**
- `GET /` - Health check
- `POST /ask` - Submit question and get AI response
  - Request: `{"question": "Your question"}`
  - Response: `{"question": "...", "answer": "...", "sources": [...]}`

**Flask (http://localhost:5000)**
- `GET /` - Web interface
- `POST /upload` - Upload PDF files
- `POST /ask` - Forward questions to FastAPI

## ⚡ Performance Metrics

- PDF Processing: ~2-3 seconds per document
- Vector Search: <100ms for 1000+ chunks
- Wikipedia Fetch: ~1-2 seconds
- AI Response Generation: ~5-10 seconds
- Total Query Response: ~10-15 seconds

## 🐛 Troubleshooting

### Issue: "Upload failed" error
**Solution**: 
- Check Flask terminal for detailed error
- Ensure PDF is valid and not corrupted
- Try smaller PDF first

### Issue: "Error connecting to AI backend"
**Solution**:
- Verify FastAPI server is running (`uvicorn api.main:app --reload`)
- Check OPENAI_API_KEY is set in .env
- Verify OpenAI API has available credits

### Issue: No documents retrieved
**Solution**:
- Ensure PDFs are uploaded and processed
- Check `data/chunks.json` exists and has content
- Try uploading at least one PDF before asking

### Issue: Wikipedia links not working
**Solution**:
- Links should open Wikipedia in new tab
- Check browser pop-up settings
- Verify internet connection

## 🚦 API Keys & Credentials

### Getting OpenAI API Key
1. Go to [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Sign up or log in
3. Create new secret key
4. Add to `.env` file as `OPENAI_API_KEY`

### Rate Limits
- OpenAI: Default is 3 RPM (requests per minute) on free tier
- Wikipedia: No authentication needed
- FAISS: Local, no limits

## 📈 Future Enhancements

- [ ] Support additional file types (DOCX, TXT, PPTX)
- [ ] Multi-language support
- [ ] Custom domain-specific knowledge graphs
- [ ] Real-time document collaboration
- [ ] Advanced PDF annotations
- [ ] Export summaries to PDF/Word
- [ ] Integration with Semantic Scholar and arXiv
- [ ] Fine-tuned models for specific domains
- [ ] Conversation history and persistence
- [ ] Document similarity comparison
- [ ] Batch processing for large document sets
- [ ] REST API documentation with Swagger

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see LICENSE file for details

## 👨‍💻 Author

Created with ❤️ by Vaibhavi Rane

## 🙏 Acknowledgments

- OpenAI for GPT-4o-mini API
- Hugging Face for sentence-transformers
- Facebook for FAISS
- Wikipedia for knowledge base
- The open-source community

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check existing documentation
- Review troubleshooting section

---

**Last Updated:** March 31, 2026  
**Version:** 1.0.0
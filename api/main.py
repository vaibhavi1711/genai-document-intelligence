from fastapi import FastAPI
from pydantic import BaseModel
from rag.generator import generate_answer

app = FastAPI(title="GenAI Document Intelligence API")


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {"message": "GenAI Document Intelligence API is running"}


@app.post("/ask")
def ask_question(request: QuestionRequest):
    try:
        print(f"Received question: {request.question}")
        answer, sources = generate_answer(request.question)
        
        # Format sources with URLs if available
        formatted_sources = []
        if sources:
            for source in sources:
                if isinstance(source, dict):
                    formatted_sources.append(source)
                else:
                    formatted_sources.append({"name": source, "url": None})
        
        return {
            "question": request.question,
            "answer": answer,
            "sources": formatted_sources
        }
    except Exception as e:
        print(f"ERROR in /ask endpoint: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            "question": request.question,
            "answer": f"Error: {str(e)}",
            "sources": []
        }
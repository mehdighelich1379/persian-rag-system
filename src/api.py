from fastapi import FastAPI
from pydantic import BaseModel
from .generator import generate

app = FastAPI(
    title="Persian RAG System",
    description="RAG API for Persian HR & Resume Guidance",
    version="1.0.0"
)


class QueryRequest(BaseModel):
    query: str


class QueryResponse(BaseModel):
    answer: str


@app.post("/generate", response_model=QueryResponse)
def generate_answer(req: QueryRequest):
    """
    Generate an answer using the Persian RAG system.
    """
    answer = generate(req.query)
    return {"answer": answer}

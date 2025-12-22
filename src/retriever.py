import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from .config import EMBEDDING_MODEL, TOP_K, COSINE_THRESHOLD


# Embedding model
embedder = SentenceTransformer(EMBEDDING_MODEL)


# Load Vector Store
index = faiss.read_index("vector_store/index.faiss")
with open("vector_store/docs.json", encoding="utf-8") as f:
    docs = json.load(f)


def retrieve(query: str):
    """
    Retrieve relevant documents using cosine similarity.
    Returns empty list if query is out-of-domain.
    """
    emb = embedder.encode([query]).astype("float32")
    faiss.normalize_L2(emb)

    scores, idxs = index.search(emb, TOP_K)

    avg_score = scores[0].mean()
    print("AVG COSINE SCORE:", avg_score)

    # Guardrail for out-of-domain queries
    if avg_score < COSINE_THRESHOLD:
        return []

    return [docs[i] for i in idxs[0]]

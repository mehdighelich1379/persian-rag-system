import os
import json
import faiss
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer

DATA_PATH = "data/fine_tune_FINAL.jsonl"
OUT_DIR = Path("vector_store")
OUT_DIR.mkdir(exist_ok=True)


embedder = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

documents = []
vectors = []

with open(DATA_PATH, "r", encoding="utf-8") as f:
    for idx, line in enumerate(f):
        row = json.loads(line)
        messages = row["messages"]

        user_msg = next(m["content"] for m in messages if m["role"] == "user")
        assistant_msg = next(m["content"] for m in messages if m["role"] == "assistant")

        emb = embedder.encode(user_msg)
        vectors.append(emb)

        documents.append({
            "id": idx,
            "query": user_msg,
            "answer": assistant_msg
        })

vectors = np.array(vectors, dtype="float32")

# Cosine similarity
faiss.normalize_L2(vectors)
index = faiss.IndexFlatIP(vectors.shape[1])
index.add(vectors)

faiss.write_index(index, str(OUT_DIR / "index.faiss"))

with open(OUT_DIR / "docs.json", "w", encoding="utf-8") as f:
    json.dump(documents, f, ensure_ascii=False, indent=2)

print(f"Vector DB ساخته شد | {len(documents)} سند")

"""
Global configuration for the Persian RAG system
"""

EMBEDDING_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"

TOP_K = 5

# Cosine similarity threshold
# Below this value, query is considered out-of-domain
COSINE_THRESHOLD = 0.25



# LLM
LLM_MODEL = "gpt-4o-mini"



# Prompt / Generation
TEMPERATURE = 0.7
MAX_CONTEXT_CHARS = 3000

# services/vector_store.py
"""
Vector Store Service
--------------------
Handles embedding generation, FAISS index creation, and similarity search.
Used by AnalystAgent to find semantically relevant financial instruments.
"""

from sentence_transformers import SentenceTransformer
import numpy as np
import faiss
import json
from typing import List, Dict, Any
from services.tools import log_event, timeit


class VectorStore:
    """
    Semantic search layer for knowledge retrieval.
    """

    def __init__(self, corpus_path: str = "knowledge/corpus.json"):
        log_event("VectorStore", "Initializing vector store...")
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.corpus_path = corpus_path
        self.corpus = self._load_corpus()
        self.index, self.embeddings = self._build_index()

    # -----------------------------------------------------
    def _load_corpus(self) -> List[Dict[str, Any]]:
        with open(self.corpus_path, "r", encoding="utf-8") as f:
            return json.load(f)

    # -----------------------------------------------------
    @timeit
    def _build_index(self):
        """
        Encode all descriptions and build a FAISS index for fast similarity search.
        """
        texts = [item["description"] for item in self.corpus]
        embeddings = self.model.encode(texts, show_progress_bar=False)
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatL2(dimension)
        index.add(np.array(embeddings).astype("float32"))
        log_event("VectorStore", f"Indexed {len(self.corpus)} documents.")
        return index, embeddings

    # -----------------------------------------------------
    @timeit
    def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
        Perform vector similarity search and return top-k matching items.
        """
        query_vector = self.model.encode([query], show_progress_bar=False)
        D, I = self.index.search(np.array(query_vector).astype("float32"), top_k)
        results = [self.corpus[i] for i in I[0]]
        log_event("VectorStore", f"Search query: '{query}' → Top {top_k} results: {[r['name'] for r in results]}")
        return results

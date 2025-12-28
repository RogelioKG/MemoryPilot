from __future__ import annotations

from abc import ABC, abstractmethod

from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import VectorStore


class VectorDatabase(ABC):
    def __init__(
        self,
        db_url: str,
        collection_name: str,
        embedding_model: Embeddings,
    ) -> None:
        self.db_url = db_url
        self.collection_name = collection_name
        self.embedding_model = embedding_model
        self._store: VectorStore | None = None

    @property
    def store(self) -> VectorStore:
        if self._store is None:
            raise RuntimeError("Vector Database not initialized. Call init() first.")
        return self._store

    def init(self) -> None:
        if self._store is not None:
            return

        self._store = self._init_vector_store()

    @abstractmethod
    def _init_vector_store(self) -> VectorStore: ...

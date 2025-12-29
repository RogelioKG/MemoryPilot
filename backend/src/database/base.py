from abc import ABC, abstractmethod
from functools import cached_property

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
            raise RuntimeError("Vector Database not initialized. Call init_store() first.")
        return self._store

    @cached_property
    def vector_size(self) -> int:
        return len(self.embedding_model.embed_query("test"))

    @abstractmethod
    def init_store(self) -> None: ...

    @abstractmethod
    def destroy_store(self) -> None: ...

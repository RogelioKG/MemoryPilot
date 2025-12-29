from __future__ import annotations

from functools import cached_property, lru_cache
from typing import TYPE_CHECKING

from ..config import get_config
from ..model.embedding import get_embedding_model
from .base import VectorDatabase

if TYPE_CHECKING:
    from langchain_postgres import PGEngine  # pyright: ignore[reportMissingImports]
    from qdrant_client import QdrantClient  # pyright: ignore[reportMissingImports]


class PGVectorDatabase(VectorDatabase):
    @cached_property
    def engine(self) -> PGEngine:
        from langchain_postgres import PGEngine  # pyright: ignore[reportMissingImports]

        return PGEngine.from_connection_string(url=self.db_url)

    def init_store(self) -> None:
        from langchain_postgres import PGVectorStore  # pyright: ignore[reportMissingImports]

        # create collection
        try:
            self.engine.init_vectorstore_table(
                table_name=self.collection_name,
                vector_size=self.vector_size,
            )
        except Exception:
            pass

        # create store
        self._store = PGVectorStore.create_sync(
            engine=self.engine,
            table_name=self.collection_name,
            embedding_service=self.embedding_model,
        )

    def destroy_store(self) -> None:
        # delete collection
        self.engine.drop_table(self.collection_name)

        # delete store
        self._store = None


class QdrantDatabase(VectorDatabase):
    @cached_property
    def client(self) -> QdrantClient:
        from qdrant_client import QdrantClient  # pyright: ignore[reportMissingImports]

        return QdrantClient(url=self.db_url)

    def init_store(self) -> None:
        from langchain_qdrant import QdrantVectorStore  # pyright: ignore[reportMissingImports]
        from qdrant_client import models  # pyright: ignore[reportMissingImports]

        # create collection
        try:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(size=self.vector_size, distance=models.Distance.COSINE),
            )
        except Exception:
            pass

        # create store
        self._store = QdrantVectorStore(
            client=self.client,
            collection_name=self.collection_name,
            embedding=self.embedding_model,
        )

    def destroy_store(self) -> None:
        # delete collection
        self.client.delete_collection(self.collection_name)

        # delete store
        self._store = None


@lru_cache
def get_vector_db() -> VectorDatabase:
    db_url = get_config().VECTOR_DB_URL
    db_provider = get_config().VECTOR_DB_PROVIDER
    db_collection_name = get_config().VECTOR_DB_COLLECTION

    vector_db: VectorDatabase

    if db_provider == "postgres":
        vector_db = PGVectorDatabase(
            db_url=db_url,
            collection_name=db_collection_name,
            embedding_model=get_embedding_model(),
        )
    elif db_provider == "qdrant":
        vector_db = QdrantDatabase(
            db_url=db_url,
            collection_name=db_collection_name,
            embedding_model=get_embedding_model(),
        )
    else:
        raise ValueError(f"Unsupported vector database provider: {db_provider}")

    vector_db.init_store()

    return vector_db

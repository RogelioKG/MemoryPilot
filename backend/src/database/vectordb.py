from __future__ import annotations

from functools import lru_cache
from typing import TYPE_CHECKING

from ..config import get_config
from ..model.embedding import get_embedding_model
from .base import VectorDatabase

if TYPE_CHECKING:
    from langchain_postgres import PGVectorStore  # pyright: ignore[reportMissingImports]
    from langchain_qdrant import QdrantVectorStore  # pyright: ignore[reportMissingImports]


class PGVectorDatabase(VectorDatabase):
    def _init_vector_store(self) -> PGVectorStore:
        # lazy import
        from langchain_postgres import PGEngine, PGVectorStore  # pyright: ignore[reportMissingImports]

        # vector size
        vector_size = len(self.embedding_model.embed_query("test"))

        # engine
        engine = PGEngine.from_connection_string(url=self.db_url)

        # create collection
        try:
            engine.init_vectorstore_table(
                table_name=self.collection_name,
                vector_size=vector_size,
            )
        except Exception:
            pass

        # vector store
        return PGVectorStore.create_sync(
            engine=engine,
            table_name=self.collection_name,
            embedding_service=self.embedding_model,
        )


class QdrantDatabase(VectorDatabase):
    def _init_vector_store(self) -> QdrantVectorStore:
        # lazy import
        from langchain_qdrant import QdrantVectorStore  # pyright: ignore[reportMissingImports]
        from qdrant_client import QdrantClient, models  # pyright: ignore[reportMissingImports]
        from qdrant_client.http.exceptions import UnexpectedResponse  # pyright: ignore[reportMissingImports]

        # client
        client = QdrantClient(url=self.db_url)

        # create collection
        try:
            client.get_collection(self.collection_name)
        except (UnexpectedResponse, ValueError):
            vector_size = len(self.embedding_model.embed_query("test"))

            client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(size=vector_size, distance=models.Distance.COSINE),
            )

        # vector store
        return QdrantVectorStore(
            client=client,
            collection_name=self.collection_name,
            embedding=self.embedding_model,
        )


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

    vector_db.init()

    return vector_db

from functools import lru_cache

from langchain_core.embeddings import Embeddings
from langchain_openai import OpenAIEmbeddings
from langchain_postgres import PGEngine, PGVectorStore

from ..config import get_config
from ..database.base import VectorDatabase


class PGVectorDatabase(VectorDatabase):
    def __init__(
        self,
        db_url: str,
        table_name: str,
        embedding_model: Embeddings,
    ):
        self.db_url = db_url
        self.table_name = table_name
        self.embedding_model = embedding_model
        self._engine: PGEngine | None = None
        self._store: PGVectorStore | None = None

    @property
    def store(self) -> PGVectorStore:
        if self._store is None:
            raise RuntimeError("Vector Database not initialized. Call init() first.")
        return self._store

    def init(self) -> None:
        if self._store is not None:
            return

        # Embedding model
        vector_size = len(self.embedding_model.embed_query("hello"))

        # PG Engine
        self._engine = PGEngine.from_connection_string(url=self.db_url)

        # Create table
        try:
            self._engine.init_vectorstore_table(
                table_name=self.table_name,
                vector_size=vector_size,
            )
        except Exception:
            pass

        # PGVectorStore instance
        self._store = PGVectorStore.create_sync(
            engine=self._engine,
            table_name=self.table_name,
            embedding_service=self.embedding_model,
        )


@lru_cache
def get_vector_db() -> VectorDatabase:
    vector_db = PGVectorDatabase(
        db_url=get_config().POSTGRES_URI,
        table_name=get_config().VECTOR_TABLE_NAME,
        embedding_model=OpenAIEmbeddings(model=get_config().EMBEDDING_MODEL),
    )
    vector_db.init()
    return vector_db

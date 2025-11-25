from abc import ABC, abstractmethod

from langchain_core.vectorstores import VectorStore


class VectorDatabase(ABC):
    """
    向量資料庫
    """

    @abstractmethod
    async def init(self) -> None:
        """
        初始化向量資料庫
        """
        ...

    @property
    @abstractmethod
    def store(self) -> VectorStore:
        """
        VectorStore
        """
        ...

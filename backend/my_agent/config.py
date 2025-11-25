import os
from functools import lru_cache


class Config:
    def __init__(self):
        self.OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
        self.EMBEDDING_MODEL = os.environ["EMBEDDING_MODEL"]
        self.CHAT_MODEL = os.environ["CHAT_MODEL"]
        self.POSTGRES_URI = os.environ["POSTGRES_URI"]
        self.VECTOR_TABLE_NAME = os.environ["VECTOR_TABLE_NAME"]
        self.BACKEND_PORT = int(os.environ["BACKEND_PORT"])


@lru_cache
def get_config():
    return Config()

from functools import lru_cache
from typing import cast

from langchain_core.embeddings import Embeddings

from ..config import get_config


@lru_cache
def get_embedding_model() -> Embeddings:
    config = get_config()
    provider = config.EMBEDDING_PROVIDER
    model_name = config.EMBEDDING_MODEL

    if provider == "openai":
        from langchain_openai import OpenAIEmbeddings  # pyright: ignore[reportMissingImports]

        embedding_model = OpenAIEmbeddings(model=model_name, api_key=config.OPENAI_API_KEY)

    elif provider == "huggingface":
        from langchain_huggingface import HuggingFaceEmbeddings  # pyright: ignore[reportMissingImports]

        embedding_model = HuggingFaceEmbeddings(model_name=model_name)

    elif provider == "ollama":
        from langchain_ollama import OllamaEmbeddings  # pyright: ignore[reportMissingImports]

        embedding_model = OllamaEmbeddings(model=model_name, base_url=config.OLLAMA_BASE_URL)

    elif provider == "google":
        from langchain_google_genai import GoogleGenerativeAIEmbeddings  # pyright: ignore[reportMissingImports]

        embedding_model = GoogleGenerativeAIEmbeddings(model=model_name, api_key=config.GOOGLE_API_KEY)

    else:
        raise ValueError(f"Unsupported embedding provider: {provider}")

    return cast(Embeddings, embedding_model)

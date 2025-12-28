from functools import lru_cache
from typing import cast

from langchain_core.language_models import BaseChatModel

from ..config import get_config


@lru_cache
def get_llm_model() -> BaseChatModel:
    config = get_config()
    provider = config.LLM_PROVIDER
    model_name = config.LLM_MODEL

    if provider == "openai":
        from langchain_openai import ChatOpenAI  # pyright: ignore[reportMissingImports]

        llm = ChatOpenAI(model=model_name, api_key=config.OPENAI_API_KEY)

    elif provider == "google":
        from langchain_google_genai import ChatGoogleGenerativeAI  # pyright: ignore[reportMissingImports]

        llm = ChatGoogleGenerativeAI(model=model_name, api_key=config.GOOGLE_API_KEY)

    elif provider == "anthropic":
        from langchain_anthropic import ChatAnthropic  # pyright: ignore[reportMissingImports]

        llm = ChatAnthropic(model=model_name, api_key=config.ANTHROPIC_API_KEY)

    elif provider == "groq":
        from langchain_groq import ChatGroq  # pyright: ignore[reportMissingImports]

        llm = ChatGroq(model=model_name, api_key=config.GROQ_API_KEY)

    elif provider == "ollama":
        from langchain_ollama import ChatOllama  # pyright: ignore[reportMissingImports]

        llm = ChatOllama(model=model_name, base_url=config.OLLAMA_BASE_URL)

    else:
        raise ValueError(f"Unsupported chat provider: {provider}")

    return cast(BaseChatModel, llm)

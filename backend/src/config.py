from functools import lru_cache
from typing import Literal

from pydantic import SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    # basic
    BACKEND_PORT: int

    # vector database
    VECTOR_DB_URL: str
    VECTOR_DB_PROVIDER: str
    VECTOR_DB_COLLECTION: str

    # embedding
    EMBEDDING_PROVIDER: Literal["openai", "huggingface", "ollama", "google"]
    EMBEDDING_MODEL: str

    # llm
    LLM_PROVIDER: Literal["openai", "google", "anthropic", "groq", "ollama"]
    LLM_MODEL: str
    OPENAI_API_KEY: SecretStr | None = None
    GOOGLE_API_KEY: SecretStr | None = None
    ANTHROPIC_API_KEY: SecretStr | None = None
    GROQ_API_KEY: SecretStr | None = None
    OLLAMA_BASE_URL: str | None = None

    # .env
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @model_validator(mode="after")
    def validate_provider_credentials(self):
        key_requirements = {
            "openai": (self.OPENAI_API_KEY, "OPENAI_API_KEY"),
            "google": (self.GOOGLE_API_KEY, "GOOGLE_API_KEY"),
            "anthropic": (self.ANTHROPIC_API_KEY, "ANTHROPIC_API_KEY"),
            "groq": (self.GROQ_API_KEY, "GROQ_API_KEY"),
        }

        active_providers = {self.LLM_PROVIDER, self.EMBEDDING_PROVIDER}

        for provider, (api_key, key_name) in key_requirements.items():
            if provider in active_providers and not api_key:
                raise ValueError(f"Provider '{provider}' is active but {key_name} is missing.")

        return self


@lru_cache
def get_config() -> Config:
    return Config()  # pyright: ignore[reportCallIssue]

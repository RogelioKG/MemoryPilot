# MemoryPilot
![Version: 1.0.0](https://img.shields.io/badge/version-1.0.0-blue)
[![Licence: AGPL-3.0](https://img.shields.io/github/license/RogelioKG/MemoryPilot?style=flat)](./LICENSE)

## ⚡ Brief

A memory-powered AI agent with a live chatroom for conversational retrieval, using pgvector for vectors database, FastAPI backend and Vue frontend.

## ⚒️ Setup

### remote llm

1. install dependencies
    > You may choose other remote LLM providers (e.g., OpenAI, Anthropic, Grok).\
    > Please ensure the corresponding packages are installed.
    ```
    cd backend
    uv add langchain-google-genai
    uv export --locked --no-hashes --no-annotate --format requirements.txt > requirements.txt
    ```
2. environment variables (`.env`)
    > Remember to update the model configuration section accordingly!
    ```ini
    # backend
    BACKEND_PORT="8000"
    BACKEND_BASE_URL="http://localhost:${BACKEND_PORT}"

    # database
    POSTGRES_USER="postgres"
    POSTGRES_PASSWORD="postgres123"
    POSTGRES_HOST="db"
    POSTGRES_PORT="5432"
    POSTGRES_DB="langchain"
    VECTOR_DB_URL="postgresql+asyncpg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}"
    VECTOR_DB_PROVIDER="postgres"
    VECTOR_DB_COLLECTION="documents"
    
    # model
    EMBEDDING_PROVIDER="google"
    EMBEDDING_MODEL="text-embedding-004"
    LLM_PROVIDER="google"
    LLM_MODEL="gemini-2.5-flash"
    GOOGLE_API_KEY="..."
    ```
3. build & run app
    ```
    docker compose --profile remote-llm up
    ```

### local llm
1. install dependencies
    ```
    cd backend
    uv add langchain-ollama
    uv export --locked --no-hashes --no-annotate --format requirements.txt > requirements.txt
    ```
2. environment variables (`.env`)
    ```ini
    # backend
    BACKEND_PORT="8000"
    BACKEND_BASE_URL="http://localhost:${BACKEND_PORT}"

    # database
    POSTGRES_USER="postgres"
    POSTGRES_PASSWORD="postgres123"
    POSTGRES_HOST="db"
    POSTGRES_PORT="5432"
    POSTGRES_DB="langchain"
    VECTOR_DB_URL="postgresql+asyncpg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}"
    VECTOR_DB_PROVIDER="postgres"
    VECTOR_DB_COLLECTION="documents"

    # model
    EMBEDDING_PROVIDER="ollama"
    EMBEDDING_MODEL="nomic-embed-text"
    LLM_PROVIDER="ollama"
    LLM_MODEL="llama3.1"
    OLLAMA_PORT="11434"
    OLLAMA_BASE_URL="http://ollama:${OLLAMA_PORT}"
    ```
3. build & run app
    ```
    docker compose --profile local-llm up
    ```
4. install local llm
    ```
    docker exec -it memorypilot-ollama ollama pull nomic-embed-text
    docker exec -it memorypilot-ollama ollama pull llama3.1
    ```
# MemoryPilot

## ⚡ Brief

A memory-powered AI agent with a live chatroom for conversational retrieval, using pgvector for vectors database, FastAPI backend and Vue frontend.

## ⚒️ Setup

### remote llm

1. install dependencies
    ```
    cd backend
    uv add langchain-openai
    uv export --format requirements.txt > requirements.txt --no-hashes --no-annotate
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
    EMBEDDING_PROVIDER="openai"
    EMBEDDING_MODEL="text-embedding-3-small"
    LLM_PROVIDER="openai"
    LLM_MODEL="gpt-5"
    OPENAI_API_KEY="..."
    ```
3. build & run app
    ```
    docker compose up
    ```

### local llm
1. install dependencies
    ```
    cd backend
    uv add langchain-ollama
    uv export --format requirements.txt > requirements.txt --no-hashes --no-annotate
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
    docker exec -it memorypilot-ollama-1 ollama pull nomic-embed-text
    docker exec -it memorypilot-ollama-1 ollama pull llama3.1
    ```


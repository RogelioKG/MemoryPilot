# MemoryPilot

## ⚡ Brief

A memory-powered AI agent with a live chatroom for conversational retrieval, using pgvector for vectors database, FastAPI backend and Vue frontend.

## ⚒️ Setup

### remote llm

1. install dependencies
    ```
    cd backend
    uv add langchain-google-genai
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

### local test
1. install dependencies
    ```
    cd backend
    uv sync --group test
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
    OPENAI_API_KEY="..."  # judge model is GPT-4o
    OLLAMA_PORT="11434"
    OLLAMA_BASE_URL="http://ollama:${OLLAMA_PORT}"
    ```
3. build & run app
    ```
    docker compose --profile local-test up
    ```
4. install local llm
    ```
    docker exec -it memorypilot-ollama-1 ollama pull nomic-embed-text
    docker exec -it memorypilot-ollama-1 ollama pull llama3.1
    ```
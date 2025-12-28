import asyncio
import sys
from contextlib import asynccontextmanager
from typing import Annotated

import uvicorn
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from src.agent.chat import ChatAgent, get_chat_agent
from src.config import get_config
from src.database.vectordb import get_vector_db
from src.schemas import ChatResponse
from src.services.document import get_document_service
from src.utils.logger import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_dotenv()  # 載入環境變數
    if sys.platform == "win32":  # 兼容 Windows
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    setup_logging()  # 初始化日誌
    get_vector_db()  # 初始化資料庫
    get_chat_agent()  # 初始化模型
    get_document_service()  # 初始化檔案轉換服務
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/chat", response_model=ChatResponse)
async def chat(
    chat_agent: Annotated[ChatAgent, Depends(get_chat_agent)],
    thread_id: Annotated[str, Form()],
    query: Annotated[str, Form()],
    files: list[UploadFile] | None = None,
):
    response = await chat_agent.ainvoke(query, files, thread_id=thread_id)
    return ChatResponse(answer=response)


@app.post("/chat/stream")
async def chat_stream(
    chat_agent: Annotated[ChatAgent, Depends(get_chat_agent)],
    thread_id: Annotated[str, Form()],
    query: Annotated[str, Form()],
    files: list[UploadFile] | None = None,
):
    return StreamingResponse(
        (chunk.encode("utf-8") async for chunk in chat_agent.astream(query, files, thread_id=thread_id)),
        media_type="text/plain; charset=utf-8",
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=get_config().BACKEND_PORT)

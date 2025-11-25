from collections.abc import AsyncGenerator
from functools import lru_cache
from typing import Any, cast

from fastapi import UploadFile
from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware
from langchain_core.messages import AIMessage, BaseMessageChunk, HumanMessage, ToolMessage
from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.checkpoint.memory import InMemorySaver

from .config import get_config
from .database.vector import get_vector_db
from .services.document import get_document_service
from .utils.tools import query_weather, save_memory, search_memory
from .utils.types import ChatContext, ChatMiddleware, ChatState


class ChatAgent:
    def __init__(self, *, model: str, checkpointer: BaseCheckpointSaver):
        self.model = model
        self.checkpointer = checkpointer
        self.agent = self._create_agent()

    def _create_agent(self):
        tools = [
            save_memory,
            search_memory,
            query_weather,
        ]

        system_prompt = """
        你是一個會使用工具的助理。依照以下原則決定是否呼叫工具：

        【工具使用規則】
        - save_memory：使用者「提供檔案」，並要求「記住 / 儲存 / 加到知識庫」。
        - search_memory：當使用者「提出問題」，並要求「從知識庫找」相關訊息。
        - query_weather
        - 其他情況：直接回答，不使用工具。

        【範例】
        1. 使用者：「幫我把這份 PDF 加進知識庫」
        → 呼叫 save_memory

        2. 使用者：「我之前給你的 Python 筆記檔案，內容是什麼？」
        → 呼叫 search_memory
        → 必須和使用者說，這是根據他之前給你的檔案或資料

        3. 使用者：「台北今天幾度？」
        → 呼叫 query_weather

        4. 使用者：「你覺得我該怎麼開始學程式？」
        → 一般聊天，不用工具

        請依上述規則推理，不要誤用工具。
        請使用純文字回覆，不要採用 Markdown 格式，可以使用 Emoji。
        """

        return create_agent(
            model=self.model,
            tools=tools,
            system_prompt=system_prompt,
            state_schema=ChatState,
            context_schema=ChatContext,
            checkpointer=self.checkpointer,
            middleware=[
                ChatMiddleware(),
                SummarizationMiddleware(
                    model=self.model,
                    max_tokens_before_summary=1000,
                    messages_to_keep=5,
                ),  # type: ignore
            ],
        )

    async def ainvoke(
        self,
        query: str,
        files: list[UploadFile] | None,
        *,
        thread_id: str,
    ) -> str:
        results = await self.agent.ainvoke(
            {"messages": [HumanMessage(query)]},
            {"configurable": {"thread_id": thread_id}},
            context=ChatContext(
                vector_db=get_vector_db(),
                document_service=get_document_service(),
                files=files,
            ),
        )

        message: AIMessage = results["messages"][-1]
        return message.content  # type: ignore

    async def astream(
        self,
        query: str,
        files: list[UploadFile] | None,
        *,
        thread_id: str,
    ) -> AsyncGenerator[str]:
        stream = self.agent.astream(
            {"messages": [HumanMessage(query)]},
            {"configurable": {"thread_id": thread_id}},
            context=ChatContext(
                vector_db=get_vector_db(),
                document_service=get_document_service(),
                files=files,
            ),
            stream_mode="messages",
        )

        async for chunk in stream:
            message, metadata = cast(tuple[BaseMessageChunk | ToolMessage, dict[str, Any]], chunk)
            if metadata["langgraph_node"] == "model":
                yield message.content  # type: ignore
            elif metadata["langgraph_node"] == "tools":
                yield ""
            else:
                yield ""


@lru_cache
def get_chat_agent():
    return ChatAgent(
        model=get_config().CHAT_MODEL,
        checkpointer=InMemorySaver(),
    )

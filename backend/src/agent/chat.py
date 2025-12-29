from collections.abc import AsyncGenerator
from functools import lru_cache
from typing import Any, cast

from fastapi import UploadFile
from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessageChunk, HumanMessage, ToolMessage
from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.checkpoint.memory import InMemorySaver

from ..model.llm import get_llm_model
from .tools import query_weather, save_memory, search_memory
from .types import ChatContext, ChatMiddleware, ChatState


class ChatAgent:
    def __init__(self, *, model: BaseChatModel, checkpointer: BaseCheckpointSaver):
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
        你是一個會使用工具的助理。
        當使用者的需求可以透過工具解決時，**必須**呼叫工具，禁止自行編造數據。
        依照以下原則決定是否呼叫工具：

        【工具】
        - save_memory：使用者「提供檔案/內容」，並要求「記住/儲存/加到知識庫」時使用。
        - search_memory：使用者詢問「自己之前提供的資料」、「我的檔案」或提到「查詢知識庫/記憶」時使用。
        - query_weather：詢問天氣狀況時使用。
            - 例如：當使用者問「現在天氣」時 -> location="Taipei", current=["temperature_2m"]
            - 例如：當使用者問「未來天氣」-> location="Taipei", daily=["temperature_2m_max"], forecast_days=3
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
        請勿採用 Markdown 格式回覆，但可以使用 Emoji。
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

    def _extract_text_from_content(self, content: Any) -> str:
        if content is None:
            return ""

        if isinstance(content, str):
            return content

        if isinstance(content, list):
            text_parts = []
            for part in content:
                text_parts.append(self._extract_text_from_content(part))
            return "".join(text_parts)

        if isinstance(content, dict):
            if content.get("type") == "text":
                return content.get("text", "")
            return ""

        return str(content)

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
            context=ChatContext(files=files),
        )
        message: AIMessage = results["messages"][-1]
        return self._extract_text_from_content(message.content)

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
            context=ChatContext(files=files),
            stream_mode="messages",
        )

        async for chunk in stream:
            message, metadata = cast(tuple[BaseMessageChunk | ToolMessage, dict[str, Any]], chunk)
            if metadata["langgraph_node"] == "model":
                yield self._extract_text_from_content(message.content)
            elif metadata["langgraph_node"] == "tools":
                yield ""
            else:
                yield ""


@lru_cache
def get_chat_agent():
    return ChatAgent(
        model=get_llm_model(),
        checkpointer=InMemorySaver(),
    )

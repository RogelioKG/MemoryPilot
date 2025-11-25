from typing import Any

import requests
from langchain.tools import ToolRuntime, tool
from langchain_core.messages import ToolMessage
from langgraph.types import Command

from .misc import geocode
from .types import ChatContext, ChatState, WeatherQueryInput


@tool
async def save_memory(
    runtime: ToolRuntime[ChatContext, ChatState],
) -> Command:
    """將文件內容存進向量資料庫"""
    tool_call_id = runtime.tool_call_id
    document_service = runtime.context.document_service
    vector_db = runtime.context.vector_db
    files = runtime.context.files

    try:
        assert files is not None
        docs = await document_service.load_documents(files)
        await vector_db.store.aadd_documents(docs)
    except Exception:
        new_state: ChatState = {
            "messages": [ToolMessage("Fail: 使用者沒有傳入檔案", tool_call_id=tool_call_id)],
        }
    else:
        new_state: ChatState = {
            "messages": [ToolMessage("Success: 檔案已加入知識庫", tool_call_id=tool_call_id)],
        }

    return Command(update=new_state)


@tool
async def search_memory(
    runtime: ToolRuntime[ChatContext, ChatState],
    query: str,
) -> Command:
    """從向量資料庫做 RAG 查詢"""
    tool_call_id = runtime.tool_call_id
    vector_db = runtime.context.vector_db
    results = await vector_db.store.asimilarity_search(query, k=4)

    if not results:
        new_state = {"messages": [ToolMessage("Fail: 知識庫中找不到與問題相關的內容", tool_call_id=tool_call_id)]}
    else:
        memory = "\n".join(doc.page_content for doc in results)
        new_state = {"messages": [ToolMessage(f"Success: {memory}", tool_call_id=tool_call_id)]}

    return Command(update=new_state)


@tool(args_schema=WeatherQueryInput)
def query_weather(
    runtime: ToolRuntime[ChatContext, ChatState],
    location: str,
    current: list[str] | None = None,
    hourly: list[str] | None = None,
    daily: list[str] | None = None,
    forecast_days: int = 1,
) -> Command:
    """查詢即時或預報天氣（使用 Open-Meteo API）"""

    tool_call_id = runtime.tool_call_id

    if not (geo := geocode(location)):
        new_state: ChatState = {"messages": [ToolMessage(f"Fail: 找不到地點：{location}", tool_call_id=tool_call_id)]}
        return Command(update=new_state)

    params: dict[str, Any] = {
        "latitude": geo["latitude"],
        "longitude": geo["longitude"],
        "timezone": geo["timezone"],
        "current": current,
        "hourly": hourly,
        "daily": daily,
        "forecast_days": forecast_days,
    }

    try:
        response = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params=params,
            timeout=10,
        )
        response.raise_for_status()
    except Exception as err:
        new_state: ChatState = {"messages": [ToolMessage(f"Fail: 天氣 API 呼叫失敗：{err}", tool_call_id=tool_call_id)]}
        return Command(update=new_state)
    else:
        new_state: ChatState = {"messages": [ToolMessage(f"Success: {response.json()}", tool_call_id=tool_call_id)]}
        return Command(update=new_state)

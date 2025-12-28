import logging
from typing import Any

import requests
from langchain.tools import ToolRuntime, tool
from langchain_core.messages import ToolMessage
from langgraph.types import Command
from pydantic import BaseModel, Field

from ..utils.misc import geocode
from .types import ChatContext, ChatState


class WeatherQueryInput(BaseModel):
    """氣象查詢輸入格式"""

    location: str = Field(
        description="地點、城市之英文名稱",
    )
    current: list[str] | None = Field(
        default=None,
        description="欲查詢天氣參數（即時）"
        "例如：apparent_temperature、temperature_2m、relative_humidity_2m、"
        "wind_speed_10m、precipitation、rain、snowfall 等等",
    )
    hourly: list[str] | None = Field(
        default=None,
        description="欲查詢天氣參數（逐小時預報）"
        "例如：temperature_2m、relative_humidity_2m、wind_speed_10m、rain、visibility 等等",
    )
    daily: list[str] | None = Field(
        default=None,
        description="欲查詢天氣參數（逐日預報）"
        "例如：temperature_2m_max、temperature_2m_min、precipitation_sum、rain、uv_index_max 等等",
    )
    forecast_days: int = Field(
        default=1,
        ge=1,
        le=7,
        description="預報天數（mode 為 hourly 或 daily 時使用）",
    )


@tool
async def save_memory(
    runtime: ToolRuntime[ChatContext, ChatState],
) -> Command:
    """將文件內容存進向量資料庫"""
    logging.info("Tool [save_memory]: triggered")

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
    logging.info("Tool [search_memory]: triggered")

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
    logging.info("Tool [query_weather]: triggered")
    logging.info(f"Tool [query_weather]: {location=}")

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
    logging.info(f"Tool [query_weather]: {params=}")

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
        result = response.json()
        new_state: ChatState = {"messages": [ToolMessage(f"Success: {result}", tool_call_id=tool_call_id)]}
        logging.info(f"Tool [query_weather]: {result=}")
        return Command(update=new_state)

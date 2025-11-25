from dataclasses import dataclass

from fastapi import UploadFile
from langchain.agents import AgentState
from langchain.agents.middleware import AgentMiddleware
from pydantic import BaseModel, Field

from ..database.base import VectorDatabase
from ..services.document import DocumentService


class ChatResponse(BaseModel):
    answer: str


@dataclass
class ChatContext:
    vector_db: VectorDatabase
    document_service: DocumentService
    files: list[UploadFile] | None


class ChatState(AgentState): ...


class ChatMiddleware(AgentMiddleware[ChatState, ChatContext]): ...


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

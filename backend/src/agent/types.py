from dataclasses import dataclass

from fastapi import UploadFile
from langchain.agents import AgentState
from langchain.agents.middleware import AgentMiddleware
from pydantic import BaseModel

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

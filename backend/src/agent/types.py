from dataclasses import dataclass

from fastapi import UploadFile
from langchain.agents import AgentState
from langchain.agents.middleware import AgentMiddleware


@dataclass
class ChatContext:
    document_files: list[UploadFile] | None


class ChatState(AgentState): ...


class ChatMiddleware(AgentMiddleware[ChatState, ChatContext]): ...

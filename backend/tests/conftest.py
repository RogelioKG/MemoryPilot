import time
from collections.abc import AsyncGenerator, Awaitable, Callable

import pytest
import pytest_asyncio
from deepeval.models import GPTModel
from deepeval.test_case import LLMTestCase
from langchain_core.document_loaders import Blob
from langchain_core.messages import AIMessage, ToolMessage
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.checkpoint.memory import InMemorySaver

from src.agent.chat import ChatAgent, ChatContext
from src.database.vectordb import VectorDatabase, get_vector_db
from src.model.llm import get_llm_model
from src.services.document import get_document_service


@pytest.fixture(scope="session")
def eval_model():
    """
    Judge Model
    """
    return GPTModel(model="gpt-4o")


@pytest.fixture(scope="function")
def chat_agent() -> ChatAgent:
    """
    LangGraph Agent
    """
    # 確保在測試時 cache 不被重複使用
    get_llm_model.cache_clear()
    return ChatAgent(
        model=get_llm_model(),
        checkpointer=InMemorySaver(),
    )


@pytest_asyncio.fixture(scope="function")
async def vector_db() -> AsyncGenerator[VectorDatabase, None]:
    """
    Vector Database
    """
    # 確保在測試時 cache 不被重複使用
    get_vector_db.cache_clear()
    db = get_vector_db()
    yield db
    db.destroy_store()


@pytest_asyncio.fixture(scope="function")
async def file_knowledge_base(vector_db: VectorDatabase) -> None:
    """
    檔案資料 RAG
    """

    blob = Blob.from_path("./tests/data/MidtermMakeupExam.pdf")

    document_services = get_document_service()
    docs = document_services.blob_to_documents(blob)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=40)
    splits = text_splitter.split_documents(docs)

    await vector_db.store.aadd_documents(splits)


@pytest.fixture(scope="function")
def rag_tester(chat_agent: ChatAgent, vector_db: VectorDatabase) -> Callable[[str], Awaitable[LLMTestCase]]:
    """
    發送 Query -> 執行 Agent -> 解析 Message -> 產出 LLMTestCase
    """

    async def _runner(input: str, expected_output: str | None = None) -> LLMTestCase:
        # 準備 Context
        context = ChatContext(files=None)

        # 執行 Agent
        inputs = {"messages": [("user", input)]}
        config = {"configurable": {"thread_id": f"test_{hash(input)}"}}

        # 呼叫 Agent
        start_time = time.perf_counter()
        result_state = await chat_agent.agent.ainvoke(inputs, config=config, context=context)  # type: ignore
        messages = result_state["messages"]
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        print(messages)

        # 提取 Actual Output
        actual_output = ""
        if isinstance(messages[-1], AIMessage):
            actual_output = chat_agent._extract_text_from_content(messages[-1].content)

        # 提取 Retrieval Context
        retrieval_context = []
        for msg in messages:
            if isinstance(msg, ToolMessage) and "Success:" in str(msg.content):
                clean_text = str(msg.content).replace("Success:", "").strip()
                retrieval_context.append(clean_text)

        # 回傳 DeepEval test case
        return LLMTestCase(
            input=input,
            actual_output=actual_output,
            expected_output=expected_output,
            retrieval_context=retrieval_context,
            additional_metadata={"inference_speed": elapsed_time},
        )

    return _runner

import asyncio
from collections.abc import Callable, Iterable
from functools import lru_cache
from io import BytesIO

from fastapi import UploadFile
from langchain_core.document_loaders import Blob
from langchain_core.documents import Document
from pypdf import PdfReader

MimeHandler = Callable[[Blob], list[Document]]


class DocumentService:
    def __init__(self) -> None:
        self._handlers: dict[str, MimeHandler] = {}
        # 註冊 handler
        self.register_handlers(["application/pdf"], self._handle_pdf)
        self.register_handlers(["text/*"], self._handle_text)

    def register_handlers(
        self,
        mime_patterns: Iterable[str],
        handler: MimeHandler,
    ) -> None:
        for mime_pattern in mime_patterns:
            self._handlers[mime_pattern] = handler

    async def load_documents(self, files: list[UploadFile]) -> list[Document]:
        blobs = await asyncio.gather(*(self.file_to_blob(f) for f in files))

        docs: list[Document] = []
        for blob in blobs:
            docs.extend(self.blob_to_documents(blob))

        return docs

    async def file_to_blob(self, file: UploadFile) -> Blob:
        data = await file.read()

        return Blob.from_data(
            data=data,
            mime_type=file.content_type,
            encoding="utf-8",
            path=file.filename,
            metadata={
                "filename": file.filename,
                "content_type": file.content_type,
                "size": len(data),
            },
        )

    def blob_to_documents(self, blob: Blob) -> list[Document]:
        mime = (blob.mimetype or "").lower()

        # 1. exact match
        handler = self._handlers.get(mime)

        # 2. wildcard match
        if handler is None:
            for key, h in self._handlers.items():
                if key.endswith("/*") and mime.startswith(key[:-1]):
                    handler = h
                    break

        # 3. no handler found
        if handler is None:
            raise ValueError(f"No handler for MIME type: {mime!r}")

        return handler(blob)

    def _handle_pdf(self, blob: Blob) -> list[Document]:
        pdf_bytes = blob.as_bytes()
        reader = PdfReader(BytesIO(pdf_bytes))
        total = len(reader.pages)

        docs: list[Document] = []
        source = blob.metadata.get("filename") if isinstance(blob.metadata, dict) else blob.path

        for i, page in enumerate(reader.pages):
            text = page.extract_text() or ""
            docs.append(
                Document(
                    page_content=text,
                    metadata={
                        "source": source,
                        "page": i,
                        "total_pages": total,
                    },
                )
            )
        return docs

    def _handle_text(self, blob: Blob) -> list[Document]:
        try:
            text = blob.as_bytes().decode(blob.encoding or "utf-8")
        except UnicodeDecodeError:
            text = blob.as_bytes().decode("utf-8", errors="replace")

        return [
            Document(
                page_content=text,
                metadata=blob.metadata,
            )
        ]


@lru_cache
def get_document_service() -> DocumentService:
    return DocumentService()

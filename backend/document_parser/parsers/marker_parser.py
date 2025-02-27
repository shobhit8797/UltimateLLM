import uuid
from enum import Enum

from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
)
from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.output import text_from_rendered

from document_parser.parsers.base import BaseParser
from ultimate_llm.utilities.schema import Document


class TableOutputType(Enum):
    MARKDOWN = "markdown"
    HTML = "html"
    JSON = "json"


class MarkerParser(BaseParser):
    chunk_size = 1000
    chunk_overlap = 250
    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
    ]

    def __init__(self, file_path) -> None:
        self.file_path = file_path
        self.pdf_parts = None

    def parse(self):
        converter = PdfConverter(
            artifact_dict=create_model_dict(),
        )
        rendered = converter(str(self.file_path))
        text, _, _ = text_from_rendered(rendered)
        text = self.clean_elements(text)

        return text

    def pre_process_elements(self, file_checksum: str) -> list[Document]:
        parsed_text = self.parse()

        markdown_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=self.headers_to_split_on, strip_headers=False
        )
        md_header_splits = markdown_splitter.split_text(parsed_text)

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap
        )

        doc_splited = text_splitter.split_documents(md_header_splits)
        for doc in doc_splited:
            doc.metadata["file_checksum"] = file_checksum
            doc.id = uuid.uuid4().hex

        return doc_splited

    def get_documents(self, file_checksum: str) -> list[Document]:
        return self.pre_process_elements(file_checksum)

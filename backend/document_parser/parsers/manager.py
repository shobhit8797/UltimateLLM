import logging
import os
from pathlib import Path
from typing import List

from langchain_core.documents import Document

from document_parser.models import DocumentStore, ParsedElement
from document_parser.parsers.marker_parser import MarkerParser
from document_parser.parsers.pypdf_parser import PyPdfParser
from document_parser.parsers.unstructured_parser import UnstructuredParser
from document_parser.utils import compute_file_hash
from ultimate_llm.utilities.schema import SupportedParsers

logger = logging.getLogger(__name__)


class ContextParser:
    model_name: str = "yolox"
    partition_pdf_strategy: str = "hi_res"
    infer_table_structure: bool = True
    extract_image_block_types: list[str] = ["Table"]
    pdf_image_dpi: int = 300

    def __init__(
        self, file_path: Path, parser: SupportedParsers = SupportedParsers.Marker
    ) -> None:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        self.file_path = file_path
        self.package = parser
        self.doc_parser = None
        self._check_db()

    def set_package(self, parser: SupportedParsers) -> None:
        self.package = parser

    def _check_db(self):
        self._doc_checksum = compute_file_hash(self.file_path)
        self.db_document = (
            DocumentStore.objects.prefetch_related("parsed_elements")
            .filter(file_checksum=self._doc_checksum)
            .first()
        )
        if self.db_document and not self.db_document.parsed_elements.exists():
            self.db_document = None

    def _load_parser(self):
        if self.doc_parser:
            return  # Already initialized

        if self.package == SupportedParsers.PyPdf:
            self.doc_parser = self._parse_pypdf()
        elif self.package == SupportedParsers.Unstructured:
            self.doc_parser = self._parse_unstructured()
        elif self.package == SupportedParsers.Marker:
            self.doc_parser = self._parse_marker()

    def _parse_pypdf(self):
        return PyPdfParser(self.file_path)

    def _parse_unstructured(self):
        return UnstructuredParser(self.file_path)

    def _parse_marker(self):
        return MarkerParser(self.file_path)

    def _return_elements(self):
        return ParsedElement.objects.filter(document=self.db_document).values_list()

    def get_documents(self, fresh: bool = False) -> list[Document]:
        try:
            if not fresh and self.db_document:
                parsed_elements = ParsedElement.objects.filter(
                    document=self.db_document
                ).only("element_id", "content", "metadata")
                return [element.get_document() for element in parsed_elements]

            self._load_parser()
            document_store, _ = DocumentStore.objects.get_or_create(
                file_checksum=self._doc_checksum,
                defaults={"file_path": self.file_path, "title": self.file_path.name},
            )
            docs = self.doc_parser.get_documents(self._doc_checksum)

            # Delete existing parsed elements if fresh is True
            if fresh and self.db_document:
                ParsedElement.objects.filter(document=self.db_document).delete()

            elements = [
                ParsedElement(
                    element_id=doc.id,
                    content=doc.page_content,
                    metadata=doc.metadata,
                    document=document_store,
                )
                for doc in docs
            ]
            parsed_element_saved = ParsedElement.objects.bulk_create(
                elements, batch_size=500
            )
            return docs
        except Exception as e:
            print(f"exception in get_documents {e}: {e.__traceback__.tb_lineno}")
            raise e

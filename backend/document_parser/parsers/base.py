import abc
from abc import ABC, abstractmethod
from pathlib import Path

from langchain_core.documents import Document
from unstructured.cleaners.core import clean
from unstructured.documents.elements import Element


class BaseParser(ABC):
    def __init__(self, file_path: Path) -> None:
        if not file_path.exists():
            raise ValueError(f"The file path {file_path} does not exist.")
        self.file_path = file_path

    @staticmethod
    def clean_elements(text: str) -> str:
        """
        Cleans the input text by removing extra whitespace, dashes,
        and trailing punctuation.
        """
        return clean(
            text,
            extra_whitespace=True,
            dashes=True,
            trailing_punctuation=True,
        )

    # @abstractmethod
    # def chunk(self):
    #     """Splits the document into smaller chunks."""
    #     pass

    @abstractmethod
    def pre_process_elements(self) -> list[Document]:
        """Pre-processes the document elements."""
        raise NotImplementedError

    @abstractmethod
    def parse(self) -> list[Element | Document]:
        """Parses the document into structured elements."""
        raise NotImplementedError

    @abstractmethod
    def get_documents(self):
        """Runs the parser."""
        raise NotImplementedError

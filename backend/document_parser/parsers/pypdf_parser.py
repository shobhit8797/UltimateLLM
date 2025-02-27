import re
import sys
import uuid
from pathlib import Path

import pytesseract
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pdf2image import convert_from_path
from PIL import Image, ImageEnhance
from pypdf import PdfReader

from document_parser.parsers.base import BaseParser


def get_keywords(text: str) -> dict:
    patterns = {
        "insurer": r"Insurer:\s*(.+)",
        "insured_person": r"Insured (?:Person|Members|Persons|Member):\s*(.+)",
        "policy_name": r"Policy Name:\s*(.+)",
        "sum_insured": r"Sum Insured:\s*(.+)",
        "policy_number": r"Policy Number:\s*(.+)",
        "policy_period": r"Policy Period:\s*(.+)",
        "premium_amount": r"Premium Amount:\s*(.+)",
        "coverage_details": r"Coverage Details:\s*(.+)",
        "hospital_network": r"Hospital Network:\s*(.+)",
        "exclusions": r"Exclusions:\s*(.+)",
        "contact_details": r"Contact Details:\s*(.+)",
        "claim_process": r"Claim Process:\s*(.+)",
    }

    keywords = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            keywords[key] = match.group(1).strip()

    if keywords:
        print("-" * 100)
        print("Extracted Text:", text)
        print("Extracted Keywords:", keywords)
        print("-" * 100)

        return keywords


class PyPdfParser(BaseParser):
    chunk_size = 1000
    chunk_overlap = 250

    def __init__(self, file_path: Path) -> None:
        super().__init__(file_path)
        self.pdf_parts = []

    def is_scanned_pdf(self):
        """Returns True if the PDF is likely scanned, otherwise False."""
        reader = PdfReader(self.file_path)
        text = "".join(
            page.extract_text() or "" for page in reader.pages
        )  # Extract text from all pages
        return len(text.strip()) == 0  # If no text, it's scanned

    def chunk(self):
        """Splits the document into smaller chunks."""
        pass

    def parse(self) -> list:
        """
        Parses the PDF file into structured elements.
        Detects if the PDF is scanned or text-based before processing.
        """
        if self.is_scanned_pdf():
            print("Calling PDF OCR")
            return self.pdf_ocr()
        else:
            return self.pdf_text_extract()

    def pdf_text_extract(self):
        """Extracts text from a text-based PDF using PyPDFLoader."""
        _pages = PyPDFLoader(str(self.file_path)).lazy_load()
        self.pdf_parts = [page for page in _pages if page.page_content]
        return self.pdf_parts

    def pdf_ocr(self):
        """Extracts text from a scanned PDF using Tesseract OCR."""
        _pages = convert_from_path(self.file_path, dpi=300)
        for page_number, page in enumerate(_pages):
            img = self.preprocess_image(page)
            page_text = pytesseract.image_to_string(img)
            self.pdf_parts.append(
                {"page_content": page_text, "metadata": {"page": page_number}}
            )
        return self.pdf_parts

    @staticmethod
    def preprocess_image(image: Image.Image) -> Image.Image:
        """Preprocess the image to RGB format."""
        image = image.convert("L")
        enhancer = ImageEnhance.Contrast(image)
        contrast_image = enhancer.enhance(2.0)

        return contrast_image

    def pre_process_elements(self, file_checksum: str) -> list[Document]:
        """Extracts the text content from the PDF file."""
        if not hasattr(self, "pdf_parts") or not self.pdf_parts:
            self.parse()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap
        )

        # Split text for each page and flatten chunks
        chunks = []
        for page in self.pdf_parts:
            chunks.append(
                (
                    text_splitter.split_text(self.clean_elements(page.page_content)),
                    page.metadata["page"],
                )
            )

        if not chunks:
            raise ValueError("No text could be extracted from PDF file.")

        # Create Document objects from chunks
        documents = [
            Document(
                page_content=chunk_part,
                metadata={
                    "source": "pdf",
                    "file_checksum": file_checksum,
                    "page_no": chunk[1],
                    "keywords": get_keywords(chunk_part),
                },
                id=uuid.uuid4().hex,
            )
            for chunk in chunks
            for chunk_part in chunk[0]
        ]

        return documents

    def get_documents(self, file_checksum: str) -> list[Document]:
        return self.pre_process_elements(file_checksum)

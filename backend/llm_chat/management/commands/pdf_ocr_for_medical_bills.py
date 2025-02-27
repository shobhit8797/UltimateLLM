import pandas as pd
import pytesseract
from django.core.management.base import BaseCommand
from pdf2image import convert_from_path

from document_parser.utils import compute_file_hash
from llm_chat.rag import RagPipeline
from ultimate_llm.settings.base import TEMP_DIR
from ultimate_llm.utilities.schema import SupportedParsers


class Command(BaseCommand):
    help = "OCR for scanned PDFs."
    file = "02 47FINAL BILL.pdf"

    def handle(self, *args, **options):
        # Convert to image using resolution 300 dpi
        path = TEMP_DIR / self.file
        pdf_to_image_path = TEMP_DIR / self.file.split(".")[0]
        pdf_to_image_path.mkdir(parents=True, exist_ok=True)

        policy_checksum = compute_file_hash(path)

        rag_pipeline = RagPipeline()

        rag_pipeline.indexing_pipeline(path, SupportedParsers.PyPdf)

        questions = [
            # "Subtotal of individual doctor-related charges in tabular view?",
            "Please provide the claim amount and categorise in tabular form",
        ]

        for question in questions:
            answer = rag_pipeline.retrieval_pipeline(policy_checksum, question)
            print(f"Answer to '{question}': {answer}")

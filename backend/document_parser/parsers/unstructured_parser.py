import os
from pathlib import Path

from langchain_core.documents import Document
from unstructured.documents.elements import Element
from unstructured.partition.pdf import partition_pdf

from document_parser.parsers.base import BaseParser
from ultimate_llm.settings.base import TEMP_DIR
from ultimate_llm.utilities.resources import GlobalResources

# from llm_chat.pipelines.retrival_pipeline import parse_response, table_summary_prompt


class UnstructuredParser(BaseParser):
    def __init__(
        self,
        file_path: Path,
        model_name: str = "yolox",
        partition_pdf_strategy: str = "hi_res",
        infer_table_structure: bool = True,
        extract_image_block_types: list[str] = None,
        pdf_image_dpi: int = 300,
        language: str = "eng",
    ) -> None:
        super().__init__(file_path)
        self.pdf_parts = None
        self.partition_pdf_strategy = partition_pdf_strategy
        self.unstructured_model_name = model_name
        self.infer_table_structure = infer_table_structure
        self.extract_image_block_types = extract_image_block_types or ["Table"]
        self.pdf_image_dpi = pdf_image_dpi
        self.language = language

    def chunk(self):
        """Splits the document into smaller chunks."""
        pass

    def parse(self) -> list[Element]:
        """
        Parses the PDF file into structured elements using the unstructured library.
        """
        image_output_dir_path = TEMP_DIR / "images" / self.file_path.stem
        image_output_dir_path.mkdir(parents=True, exist_ok=True)

        try:
            self.pdf_parts = partition_pdf(
                strategy=self.partition_pdf_strategy,
                filename=str(self.file_path),
                hi_res_model_name=self.unstructured_model_name,
                infer_table_structure=self.infer_table_structure,
                extract_image_block_types=self.extract_image_block_types,
                extract_image_block_output_dir=image_output_dir_path,
                languages=[self.language],
                pdf_image_dpi=self.pdf_image_dpi,
                chunking_strategy="by_title",
                max_characters=1300,
                new_after_n_chars=1000,
                overlap=300,
            )
        except Exception as e:
            raise RuntimeError(f"Failed to parse PDF: {e}")

        return self.pdf_parts

    def pre_process_elements(self, file_checksum: str) -> list[Document]:
        """
        Pre-processes elements parsed from the PDF, converting them to `Document` objects.
        """
        if not self.pdf_parts:
            self.parse()

        document_list = []
        count = 0

        for element in self.pdf_parts:
            if element.category in ["Table", "Text"]:
                document_list.append(self._process_element(element, file_checksum))
                count += 1

        print(f"Table and Text elements parsed are: {count}")
        return document_list

    def _process_element(self, element: Element, file_checksum: str) -> Document:
        """
        Processes a single element to create a `Document` object.
        """
        metadata = {
            "filetype": element.metadata.filetype,
            "filename": element.metadata.filename,
            # "coordinates": element.metadata.coordinates, #TODO: make this json serializable and then save
            "file_checksum": file_checksum,
        }

        if element.category == "Table":
            return self._process_table_element(element, metadata)
        else:
            return Document(
                id=element._element_id,
                page_content=self.clean_elements(element.text),
                metadata=metadata,
            )

    def _process_table_element(self, element: Element, metadata: dict) -> Document:
        """
        Processes a table element to create a summarized `Document` object.
        """
        try:
            llm = GlobalResources.get_chat_llm()

            html_table = element.metadata.text_as_html
            text = element.text

            # _table_summary_prompt = table_summary_prompt(text, html_table)
            messages = [{"role": "user", "content": _table_summary_prompt}]
            res = llm.invoke(messages)
            # _, response = parse_response(res)

            metadata["context"] = self.clean_elements(element.text)
            document = Document(
                id=element._element_id,
                page_content=self.clean_elements(response),
                metadata=metadata,
            )

            # Write the table prompt, table text, table HTML, and LLM response to a file
            with open("table_summaries.txt", "a") as f:
                f.write("----- Table Summary -----\n")
                f.write(f"Prompt: {_table_summary_prompt}\n")
                f.write(f"Table Text: {text}\n")
                f.write(f"Table HTML: {html_table}\n")
                f.write(f"LLM Response: {response}\n")
                f.write("-------------------------\n\n")

            return document
        except Exception as e:
            raise RuntimeError(f"Failed to process table element: {e}")

    def get_documents(self, file_checksum: str) -> list[Document]:
        """
        Executes the full parsing pipeline and returns pre-processed documents.
        """
        return self.pre_process_elements(file_checksum)

import json
import logging
from pathlib import Path

from document_parser.parsers.manager import ContextParser
from llm_chat.llms.base import BaseLLM
from ultimate_llm.settings.base import TEMP_DIR
from ultimate_llm.utilities.resources import GlobalResources
from ultimate_llm.utilities.schema import Document, SupportedParsers

logger = logging.getLogger(__name__)
META_PROMPT = """### You are a Health Insurance Policy Decoder

Given a health insurance policy document and a user query, generate a precise response based only on the provided context.  
- Simple Answers: Concise paragraph.  
- Detailed Responses: Bullet points or a table for clarity.  
- Structured Data: JSON (without code blocks) if requested.

## Notes  
- If info is missing: _"Policy does not cover this."_  
- Prioritize clarity; avoid assumptions.
"""


def table_summary_prompt(extracted_table: str, html_table: str) -> str:
    """
    Generate a prompt to summarize a table's content.

    Args:
        extracted_table (str): Extracted text representation of the table.
        html_table (str): HTML content of the table.

    Returns:
        str: A prompt for summarizing the table.
    """
    return f"""
        You are given the table text and its content in HTML format. Extract the key points from the table content and summarize them clearly and concisely.
        Ensure the summary includes all important names, dates, numbers, relationships, and policy details while avoiding repetition and irrelevant details.

        Respond only with the summary, no additional comment.
        Do not start your message by saying "Here is a summary" or anything like that.
        Just give the summary as it is.

        Table Text: {extracted_table}
        Table Content: {html_table}
        """


def qna_prompt(context: str) -> str:
    """
        Generate a prompt to answer a question based on a given context.

        Args:
            context (str): The context (text or table) to base the answer on.

        Returns:
            str: A prompt for answering the question.

        If the question asks for the total of anything, it means to look for the exact term "total [something]" in the context and not to calculate it by summing values.
            If the exact term "total [something]" is not found in the context, look for the individual "[something]" value (e.g., "sum insured") and provide that instead. If you find multiple values for individual "[something]" give the max value.
            If neither the total nor the individual value is found, state that the information is not available in the context.
    Example:
            Question: What is the total sum insured?
            Think: Look for the term "total sum insured" in the context. If not found, look for "sum insured" and provide that value. If neither is found, state that the information is not available.

    """
    return f"""{context}"""


def prepare_context(retrieved_docs: list) -> str:
    """
    Prepare the context by concatenating retrieved documents.

    Args:
        retrieved_docs (list): A list of retrieved documents.

    Returns:
        str: The formatted context string.
    """
    context = "\n".join([doc.page_content for doc in retrieved_docs])
    return qna_prompt(context)


def parse_response(response: str) -> tuple[str, str]:
    res = response.content.split("</think>")
    return res[0].split("<think>")[1], res[1]


def question_answer(
    initial_context: str, question: str, llm: BaseLLM, file_checksum: str
) -> tuple[str, str]:
    """
    Process a single question and retrieve an answer from the LLM.

    Args:
        initial_context (str): The initial context for answering the question.
        question (str): The question to answer.
        llm: The language model instance for processing.

    Returns:
        str: The answer to the question.
    """
    try:
        context_with_question = initial_context + "\n" + question
        if not initial_context:
            print("::NO Context::")
            return ""

        messages = [
            {"role": "system", "content": META_PROMPT},
            #             {
            #                 "role": "assistant",
            #                 "content": """
            # ## Examples
            # Example 1
            # User Query: _"Does this policy cover emergency room visits?"_
            # Policy Excerpt: _"Emergency room visits are covered with a $200 copay unless deemed non-emergency, in which case the deductible applies."_
            # Response:
            # Yes, emergency room visits are covered. However:
            # - A $200 copay applies.
            # - If the visit is deemed non-emergency, the deductible will apply instead.
            # Example 2
            # User Query: _"Is dental surgery covered under this policy?"_
            # Policy Excerpt: _"Dental procedures are excluded except for reconstructive surgery due to an accident."_
            # Response:
            # No, dental surgery is not covered unless it is reconstructive surgery due to an accident.
            # """,
            #             },
            {"role": "user", "content": context_with_question},
        ]

        response = llm.invoke(messages)
        qna_dir = TEMP_DIR / "qna_data"
        qna_dir.mkdir(parents=True, exist_ok=True)
        with open(f"{qna_dir / file_checksum}.txt", "a") as f:
            f.write("*" * 100 + "\n")
            f.write(f"Context: {initial_context}\n")
            f.write(f"Question: {question}\n")
            f.write(f"Response: {response.content}\n")
            f.write("Response Meta:\n")
            json.dump(response.response_metadata, f, indent=4)
            f.write("\n" + "*" * 100 + "\n")

        print("*" * 100)
        print("Context: ", initial_context)
        print("Question: ", question)
        print("Response:", response.content)
        print("Response Meta:", json.dumps(response.response_metadata, indent=4))
        print("*" * 100)
        return response.content
        # return parse_response(response)
    except Exception as e:
        logger.error(
            f"Error during question-answer processing: {e} {e.__traceback__.tb_lineno}"
        )
        raise
    from pathlib import Path


class RagPipeline:
    def indexing_pipeline(self, file_path: Path, parser: SupportedParsers) -> list[str]:
        # Load the document
        doc_parser = ContextParser(file_path, parser)
        docs = doc_parser.get_documents(fresh=True)

        # Index the Document in Vector Store
        vector_store = GlobalResources.get_vectorstore()
        return vector_store.add_document(docs)

    def retrieval_pipeline(
        self,
        file_checksum: str,
        question: str,
        top_k: int = 2,
        page_no_limit: int = None,
        page_no_begning: int = None,
    ) -> list[str]:
        """
        Retrieve relevant documents and answer the question.

        Args:
            file_checksum (str): The checksum of the file to filter documents.
            question (str): The question to answer.
            top_k (int, optional): Number of top documents to retrieve. Defaults to 2.

        Returns:
            list[str]: The retrieved documents.
        """
        try:
            _reranker = GlobalResources.get_reranker()
            _llm = GlobalResources.get_chat_llm()

            _filter = {"file_checksum": file_checksum, "page_no": {}}

            # if page_no_limit is not None:
            #     _filter["page_no"]["$lte"] = page_no_limit
            # if page_no_begning is not None:
            #     _filter["page_no"]["$gte"] = page_no_begning

            if not _filter["page_no"]:
                del _filter["page_no"]

            retrieved_docs: list[Document] = _reranker.invoke(question, _filter)

            # Prepare the context
            initial_context = prepare_context(retrieved_docs)

            # Answer the question using the prepared context
            answer = question_answer(initial_context, question, _llm, file_checksum)
            return answer

        except Exception as e:
            logger.error(f"Error in retrieval pipeline: {e}")
            raise

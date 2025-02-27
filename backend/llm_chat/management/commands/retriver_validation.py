from django.core.management.base import BaseCommand

from document_parser.utils import compute_file_hash
from llm_chat.rag import RagPipeline
from ultimate_llm.settings.base import TEMP_DIR
from ultimate_llm.utilities.schema import Document, SupportedParsers


class Command(BaseCommand):
    help = "Validate Retriever."
    file = "p2.pdf"
    filess = ["p1.pdf", "p2.pdf", "p3.pdf", "p4.pdf"]

    questions_list = [
        ("Who is the insurer of this policy?", "Who is the insurance provider?"),
        (
            "List the insured members.",  # in the policy.",
            "List the insured persons.",  # in the policy.",
        ),
        ("What is the total sum insured amount?", "What is the total sum insured?"),
        (
            "What is the room rent amount or category included in the policy?",
            "What is the room rent amount included in the policy?",
        ),
        (
            "What is the ICU room rent amount included in the policy?",
            "What is the ICU room rent amount included in the policy?",
        ),
        (
            "Does the policy include maternity coverage? If yes, what is the sum insured?",
            "Does the policy include maternity coverage? If yes, what is the sum insured?",
        ),
        (
            "Does the policy have a copay? If yes, what is the copay percentage?",
            "Does the policy have a co-payment? If yes, what is the co-payment percentage?",
        ),
    ]

    def answer_parser(self, answer):
        return answer.content.split("</think>")

    def process_and_update_chat(self, question, policy_checksum, page_limit):
        """Handles retrieval, processing, and chat history update."""
        _question = question[0]
        rag_pipeline = RagPipeline()

        answer = rag_pipeline.retrieval_pipeline(
            policy_checksum, _question, page_no_limit=page_limit
        )

        if "is not available" in self.answer_parser(answer)[1]:
            _question = question[1]
            print(f"Retrieving answer for question: {_question}")
            answer = rag_pipeline.retrieval_pipeline(
                policy_checksum, _question, page_no_begning=3
            )

        return self.answer_parser(answer)

    def print_doc(self, doc: Document):
        print(f"Document MetaData: {doc.metadata}")
        print(f"Content: {doc.page_content}")
        print("-" * 50)

    def pretty_print_docs(self, docs):
        print(
            f"\n{'-' * 100}\n".join(
                [f"Document {i+1}:\n\n" + d.page_content for i, d in enumerate(docs)]
            )
        )

    def handle(self, *args, **options):
        # for file in self.filess:
        file_path = TEMP_DIR / self.file
        checksum = compute_file_hash(file_path)

        RagPipeline().indexing_pipeline(file_path, SupportedParsers.Marker)
        print(f"indexing_pipeline completed")
        thinking_process, ans = self.process_and_update_chat(
            self.questions_list[2], checksum, 3
        )

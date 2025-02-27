from pathlib import Path

import pandas as pd
from django.core.management.base import BaseCommand

from document_parser.utils import compute_file_hash
from llm_chat.rag import RagPipeline
from ultimate_llm.settings.base import TEMP_DIR
from ultimate_llm.utilities.schema import SupportedParsers


class Command(BaseCommand):
    help = "Export QnA pairs to an Excel file"
    files = ["p1.pdf", "p2.pdf", "p3.pdf", "p4.pdf"]

    MODEL_VALIDATION_DIR = TEMP_DIR / "model_validation"
    EXCEL_FILE_PATH = MODEL_VALIDATION_DIR / "openai_benchmark.xlsx"

    PREDEFINED_QUESTIONS = [
        ("Who is the insurer of this policy?", "Who is the insurance provider?"),
        ("List the insured members.", "List the insured persons."),
        ("What is the sum insured amount?", "What is the total sum insured?"),
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
            "Does the policy include maternity coverage? If yes, what is the sum insured? If you don’t find any information, please give the answer 'No'.",
        ),
        (
            "Does the policy have copay or co-payment? If yes, what is the copay or co-payment percentage?",
            "Does the policy have copay or co-payment? If yes, what is the co-payment percentage? Respond with 'Yes' followed by the percentage if applicable; otherwise, respond with 'No'.",
        ),
    ]

    def delete_policy_from_excel(self, policy_checksum):
        if not self.EXCEL_FILE_PATH.exists():
            return

        df = pd.read_excel(self.EXCEL_FILE_PATH, sheet_name="Sheet1")
        df = df[df["Policy Checksum"] == policy_checksum]

        df.to_excel(self.EXCEL_FILE_PATH, index=False)

    def update_excel(self, policy_checksum, file_path: Path, question, answer):
        # Load existing data if the file exists
        if self.EXCEL_FILE_PATH.exists():
            df = pd.read_excel(self.EXCEL_FILE_PATH, sheet_name="Sheet1")
        else:
            df = pd.DataFrame(
                columns=["Policy Checksum", "File Path", "Question", "Answer"]
            )

        # Create new entry
        new_entry = pd.DataFrame(
            [
                {
                    "Policy Checksum": policy_checksum,
                    "File Path": str(file_path.name),
                    "Question": question,
                    "Answer": answer,
                }
            ]
        )

        # Concatenate instead of append (append is deprecated)
        df = pd.concat([df, new_entry], ignore_index=True)

        # Save back to Excel
        df.to_excel(self.EXCEL_FILE_PATH, index=False)
        print(f"Updated {self.EXCEL_FILE_PATH} successfully.")

    def present_in_excel(self, policy_checksum, question=None):
        """
        Checks if the question is already present in the Excel file.
        """
        if not self.EXCEL_FILE_PATH.exists():
            return False

        df = pd.read_excel(self.EXCEL_FILE_PATH, sheet_name="Sheet1")
        return (
            (
                df[
                    (df["Policy Checksum"] == policy_checksum)
                    & (df["Question"] == question)
                ].shape[0]
                > 0
            )
            if question
            else (df[(df["Policy Checksum"] == policy_checksum)].shape[0] > 0)
        )

    def process_and_update_chat(
        self, question, policy_checksum, page_limit, file_path, force_add=False
    ):
        if self.present_in_excel(policy_checksum, question[0]) and not force_add:
            print(f"File already exists: {policy_checksum}")
            return
        _question = question[0]
        rag_pipeline = RagPipeline()
        answer = rag_pipeline.retrieval_pipeline(
            policy_checksum, _question, page_no_limit=page_limit
        )

        if (
            "not available" in answer.lower()
            or "policy does not cover this" in answer.lower()
        ):
            _question = question[1]
            answer = rag_pipeline.retrieval_pipeline(
                policy_checksum, _question, top_k=4
            )

        self.update_excel(policy_checksum, file_path, question[0], answer)
        return answer

    def handle(self, *args, **kwargs):
        try:
            pdf_folder = TEMP_DIR / "Policy_wordings"
            self.MODEL_VALIDATION_DIR.mkdir(parents=True, exist_ok=True)
            for file in pdf_folder.glob("*.pdf"):
                file_path: Path = TEMP_DIR / file
                print(f"file_path: {file_path}")
                if not file_path.exists():
                    print(f"File not found: {file_path}")
                    continue

                policy_checksum = compute_file_hash(file_path)

                # if policy_checksum in [
                #     "5299b5412722bab6e0a042311ff44bf6a83dffe243fc36137f6ec496a4cf9d71",
                #     "56679fac6bc3db69eb28adece95a5461de90233d6271c24ada06c92d14547aee",
                #     "59a1c9cf62942aaa8acb1752f9810bb0341e832f1c6053a74ffcd2f5955af92c",
                #     "5d1f3670a4458348691d502ba882c66caaf6f522bea270f862368e6bc393728c",
                #     "657be8820d563ddaf23f6cef7fb9f4b5c11f204fb3e4b1308fdabbf9ae248bd5",
                #     "675b5013dc1cba873d46212fb48a71400d6516fd16efdcb10b61e72fad3eeadc",
                #     "6ab39ef38a61b55e23c32ed5ad1f8f23a417d0ec9587c4ddd0501f09565ba550",
                #     "6b7097e02b3c50787366c67a05a19aea528ef9c1d91f18d2aefe9e78fd4d2492",
                #     "74a0bb1d7575d8f433e15e852b0057fb2b6011fc04b39552bf300af7dc56f940",
                #     "76670e97f96e6b609ee1f37aa3c539580b92f6c6ee538fa2db944972d9cdbb09",
                #     "7d62313fc0b20907a1fa6d31ad4b77aebd21beeb168cf671b3b305ac5bb47b05",
                #     "8ea180ad7495e0757560d3d176cb5db6dd6a81c2713ce004e1852af51f3eb1eb",
                #     "94eccce7f18eaf1e088a452d290e7a0fccc88a614434fb016d8d4da3340e6632",
                #     "963476acf4c49b8d478664dc1d20bfc019488ae50b07a07e4baa292810e839c1",
                #     "96f62b16cb3877b0fce1369b7edbc2af766835f69d3a5d5df4e3abbcd488392e",
                #     "9d8fa9d86c106a06fc7446d0340319dd9ec31621d53befd895864434c4343c4c",
                #     "b120259c8d0df8f8ca4f3c69b8193f25f2f19f4f671244206efc3c9ac729c638",
                #     "b3c85af482188968fc1c0ac0b5b7819a816994770bda956583aabd1475b2dc23",
                #     "bdc8b8629230804d0c34be9ffd9450a83a240f77aefe0bcc850c648c2bb9182d",
                #     "c843ebb84a1422c56c87e2b8d9c42623d2d65e93776f96676d997d8400372073",
                #     "ded61bee54452d7099ad07190d8e5c8b7f917f20fc81af788291e84f22baeae9",
                #     "f1d1ca216e5b109acffd52e488b26cd45f8f85d66e55590953e08b98d7d1fa8e",
                # ]:
                # self.delete_policy_from_excel(
                #     policy_checksum
                # )

                if self.present_in_excel(
                    policy_checksum, "What is the sum insured amount?"
                ):
                    print(f"File already exists: {policy_checksum}")
                    continue

                if policy_checksum in [
                    "f629adf2f0d782a8d560a5b968a1535a527d8b80c721000c14c9acf23f1cd68b",
                    "22f143bb2e3a40a6bf22a88dacf2417094366e71017ffa372551ded1233ca74f",
                    "10672855812df68e4719bb72deac05b37bf2c6401b121ae755f5fd511c2c32a3",
                    "7789fa7c4d09371536488d212c51734d38ae692f7ba704764b3403d5a45550a5",  # Scanned AADHAAR CARD in begning
                    "c49dd076e6a190932d75c6de80d5b6b77369336e62adff3417f9afe4609c31f6",  # ICICI Lombard
                    "2776f0af7e7d565032183b9e01d13f10d02b6e480ebef3cc33c4a8d788041a6b",  # Scanned
                    "10672855812df68e4719bb72deac05b37bf2c6401b121ae755f5fd511c2c32a3",  # ICICI Lombard
                    "9248f26ca4a6cb8955d3de6c8c965c82a96c291ec39da7dc55eac8a03fb3b4c4",  # ICICI Lombard
                    "ad5a48f2268608df42e3bfd4c4ac6361946eeb6e4ff2da65f3569070d87b6aed",  # ICICI Lombard
                ]:
                    continue

                RagPipeline().indexing_pipeline(file_path, SupportedParsers.Marker)
                for index, question in enumerate(self.PREDEFINED_QUESTIONS):
                    if self.present_in_excel(policy_checksum, question[0]):
                        print(f"File already exists: {policy_checksum}")
                        continue
                    # indexing_pipeline(file_path, SupportedParsers.Marker)
                    try:
                        page_limit = 3 if index <= 2 else 12
                        self.process_and_update_chat(
                            question, policy_checksum, page_limit, file_path
                        )
                    except Exception as e:
                        print(
                            f"Error answering question '{question[0]}': {e} ~ {e.__traceback__.tb_lineno}"
                        )
        except Exception as e:
            print(f"Error: {e} ~ {e.__traceback__.tb_lineno}")
            raise e

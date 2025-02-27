import logging
import time
from threading import Lock

from langchain_huggingface import ChatHuggingFace, HuggingFacePipeline

from ultimate_llm.utilities.log import log_time

logger = logging.getLogger(__name__)


class LLMConverseAI:
    _instance = None
    _lock = Lock()

    def __new__(
        cls,
        model_id="google/gemma-2-2b-it",
        pipeline_kwargs={
            "max_new_tokens": 150,
            "top_k": 50,
            "temperature": 0.3,
        },
        verbose=False,
    ):
        with cls._lock:
            if not cls._instance:
                if not model_id:
                    raise ValueError(
                        "model_id must be provided for the first instantiation."
                    )
                cls._instance = super().__new__(cls)
                cls._instance.model_id = model_id
                cls._instance.pipeline_kwargs = pipeline_kwargs or {}
                cls._instance.verbose = verbose
                cls._instance.logger = logging.getLogger(__name__)
                cls._instance.llm = cls._instance._initialize_llm()
            elif (
                model_id != cls._instance.model_id
                or pipeline_kwargs != cls._instance.pipeline_kwargs
            ):
                raise ValueError(
                    "Cannot change model_id or pipeline_kwargs after instantiation."
                )
            return cls._instance

    def _initialize_llm(self):
        """Initializes the LLM model."""
        self.logger.info("Initializing LLM")
        start_time = time.time()
        try:
            llm = HuggingFacePipeline.from_model_id(
                model_id=self.model_id,
                task="text-generation",
                pipeline_kwargs=self.pipeline_kwargs,
                # cache=True,
            )
        except Exception as e:
            self.logger.error(f"Error initializing LLM: {e}")
            raise  # Re-raise after logging
        log_time("LLM initialization", start_time)
        return llm

    def get_llm(self):
        return self.llm

    def table_summary(self, text: str, html_table: str) -> str:
        table_summary_prompt = f"""
        You are given the table text and its content in HTML format. Extract the key points from the table content and summarize them clearly and concisely.
        Ensure the summary includes all important names, dates, numbers, relationships, and policy details while avoiding repetition and irrelevant details.

        Respond only with the summary, no additionnal comment.
        Do not start your message by saying "Here is a summary" or anything like that.
        Just give the summary as it is.

        Table Text: {text}
        Table Content: {html_table}
        """

        return table_summary_prompt

    def create_chat(self, context):
        messages = [{"role": "user", "content": context}]

        return messages

    def invoke(self, message):
        self.llm: HuggingFacePipeline
        return self.llm(message)

    def prepare_context(self, retrieved_docs):
        """Prepares the initial chat context from retrieved documents."""
        self.logger.info("Preparing chat context")
        start_time = time.time()
        # Include metadata in context preparation
        context = "\n".join([f"{doc.page_content}" for doc in retrieved_docs])
        initial_context = f"""
        Answer the question based only on the following context, which can include text, tables.
        Do not give any additional information.
        Context: {context}
        """
        log_time("Chat context preparation", start_time)
        return initial_context

    def chat(self, messages):
        """Invokes a chat session with the LLM using the provided messages."""
        start_time = time.time()
        chat = ChatHuggingFace(llm=self.llm, verbose=self.verbose)
        try:
            response = chat.invoke(messages)
        except Exception as e:
            self.logger.error(f"Error during chat invocation: {e}")
            raise
        return response

    def parse_response(self, response):
        """Parses the chat response."""
        start_time = time.time()
        try:
            question = response.split("<start_of_turn>user")[-1].split("<end_of_turn>")[
                0
            ]
            final_response = response.split("<start_of_turn>model")[-1]
        except IndexError as e:  # Catching potential index errors
            self.logger.error(f"Error parsing response: {e}. Raw Response: {response}")
            raise
        log_time("Response parsing", start_time)
        return question, final_response

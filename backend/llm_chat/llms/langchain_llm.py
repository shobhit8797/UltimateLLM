import logging
from typing import List

from langchain_core.messages import BaseMessage
from langchain_huggingface import HuggingFacePipeline

from llm_chat.llms.base import BaseLLM

logger = logging.getLogger(__name__)


class BaseMessage:
    """
    Base class for all messages.
    """

    def __init__(self, content: str):
        self.content = content

    def to_openai_format(self) -> dict:
        raise NotImplementedError("This method must be implemented by subclasses.")


class SystemMessage(BaseMessage):
    """
    System message class.
    """

    def to_openai_format(self) -> dict:
        return {"role": "system", "content": self.content}


class AIMessage(BaseMessage):
    """
    AI message class.
    """

    def to_openai_format(self) -> dict:
        return {"role": "assistant", "content": self.content}


class HumanMessage(BaseMessage):
    """
    Human message class.
    """

    def to_openai_format(self) -> dict:
        return {"role": "user", "content": self.content}


class LLMInterface:
    """
    Interface for LLM responses.
    """

    def __init__(
        self,
        text: str = "",
        candidates: List[str] = None,
        completion_tokens: int = -1,
        total_tokens: int = -1,
        prompt_tokens: int = -1,
        total_cost: float = 0,
        logits: List[List[float]] = None,
        messages: List[AIMessage] = None,
        logprobs: List[float] = None,
    ):
        self.text = text
        self.candidates = candidates or []
        self.completion_tokens = completion_tokens
        self.total_tokens = total_tokens
        self.prompt_tokens = prompt_tokens
        self.total_cost = total_cost
        self.logits = logits or []
        self.messages = messages or []
        self.logprobs = logprobs or []


class LC_HF_LLM(BaseLLM):
    """
    LangChain Hugging Face LLM implementation.
    """

    def __init__(
        self,
        model_id: str = "google/gemma-2-9b-it",
        pipeline_kwargs: dict = {
            "max_new_tokens": 150,
            "top_k": 50,
            "temperature": 0.3,
        },
        task: str = "text-generation",
    ) -> None:
        self.model_id = model_id
        self.pipeline_kwargs = pipeline_kwargs
        self.task = task

        self.model: None = None
        self.load_model()

    def load_model(self) -> None:
        """
        Load the Hugging Face model.
        """
        if not self.model:
            logger.info(
                f"""
                Loading Hugging Face model with
                    - model_id: {self.model_id}
                    - task: {self.task}
                    - pipeline_kwargs: {self.pipeline_kwargs}
                """
            )
            self.model: HuggingFacePipeline = HuggingFacePipeline.from_model_id(
                model_id=self.model_id,
                task=self.task,
                pipeline_kwargs=self.pipeline_kwargs,
            )

    def get(self) -> HuggingFacePipeline:
        if not self.model:
            raise ValueError("Model not loaded yet...")
        return self.model

    def run(
        self, messages: str | BaseMessage | List[BaseMessage], **kwargs
    ) -> LLMInterface:
        input_ = self.prepare_message(messages)
        pred = self.model(messages=[input_], **kwargs)
        return self.prepare_response(pred)

    def prepare_message(
        self, messages: str | BaseMessage | List[BaseMessage]
    ) -> List[BaseMessage]:
        if isinstance(messages, str):
            return [HumanMessage(content=messages)]
        elif isinstance(messages, BaseMessage):
            return [messages]
        return messages

    def prepare_response(self, pred) -> LLMInterface:
        all_text = [each.text for each in pred.generations[0]]
        all_messages = [each.message for each in pred.generations[0]]

        completion_tokens = pred.llm_output.get("token_usage", {}).get(
            "completion_tokens", 0
        )
        total_tokens = pred.llm_output.get("token_usage", {}).get("total_tokens", 0)
        prompt_tokens = pred.llm_output.get("token_usage", {}).get("prompt_tokens", 0)

        return LLMInterface(
            text=all_text[0] if all_text else "",
            candidates=all_text,
            completion_tokens=completion_tokens,
            total_tokens=total_tokens,
            prompt_tokens=prompt_tokens,
            messages=all_messages,
            logits=[],
        )

    def __str__(self):
        return super().__str__() + f" | {self.model_id} | {self.task}"

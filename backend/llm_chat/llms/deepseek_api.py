from typing import List

from langchain_deepseek import ChatDeepSeek

from llm_chat.llms.base import BaseLLM
from llm_chat.llms.langchain_llm import BaseMessage


class DeepSeekLLM(BaseLLM):

    def __init__(self, model_id: str = "deepseek-chat", **kwargs):
        self.model_id = model_id
        self.temperature = kwargs.get("temperature", 0.2)
        self.max_tokens = kwargs.get("output_tokens", 256)

        self._llm = None

        self.load_model()

    def load_model(self) -> None:
        print("Loading DeepSeek model...")
        if self._llm is None:
            print(f"Loading Ollama model with model_id: {self.model_id}")
            self._llm = ChatDeepSeek(
                model=self.model_id,
                temperature=self.temperature,
            )

    def get(self):
        if not self._llm:
            raise ValueError("Model not loaded yet...")
        return self._llm

    def invoke(self, messages: List[BaseMessage]) -> str:
        return self._llm.invoke(messages)

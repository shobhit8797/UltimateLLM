from typing import List

from langchain_openai import ChatOpenAI

from llm_chat.llms.base import BaseLLM
from llm_chat.llms.langchain_llm import BaseMessage
from ultimate_llm.settings.base import OPENAI_API_KEY


class OpenAiLLM(BaseLLM):

    def __init__(self, model_id: str = "gpt-4o-mini", **kwargs):
        self.model_id = model_id
        self.temperature = kwargs.get("temperature", 0.2)
        self.max_tokens = kwargs.get("output_tokens", 256)

        self._llm = None

        self.load_model()

    def load_model(self) -> None:
        print("Loading DeepSeek model...")
        if self._llm is None:
            print(f"Loading Ollama model with model_id: {self.model_id}")
            self._llm = ChatOpenAI(
                model=self.model_id,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                timeout=None,
                max_retries=2,
                api_key=OPENAI_API_KEY,
            )

    def get(self):
        if not self._llm:
            raise ValueError("Model not loaded yet...")
        return self._llm

    def invoke(self, messages: List[BaseMessage]) -> str:
        return self._llm.invoke(messages)

    def stream(self, input: str):
        return self._llm.stream(input)

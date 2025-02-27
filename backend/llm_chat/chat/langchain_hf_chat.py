from langchain_huggingface import ChatHuggingFace, HuggingFacePipeline

from llm_chat.llms.langchain_llm import LC_HF_LLM


class LC_HF_Chat:
    verbose: bool = True

    def __init__(self, llm: LC_HF_LLM):
        _llm: HuggingFacePipeline = llm.get()
        self._chat = ChatHuggingFace(llm=llm, verbose=self.verbose)

    def ainvoke(self, messages, **kwargs):
        return self._chat.ainvoke(messages, **kwargs)

    def invoke(self, messages, **kwargs):
        return self._chat.invoke(messages, **kwargs)

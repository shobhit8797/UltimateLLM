from ultimate_llm.utilities.schema import Document


class BaseEmbeddings:
    def run(
        self, text: str | list[str] | Document | list[Document], *args, **kwargs
    ) -> list:
        return self.invoke(text, *args, **kwargs)

    def invoke(
        self, text: str | list[str] | Document | list[Document], *args, **kwargs
    ) -> list:
        raise NotImplementedError

    async def ainvoke(
        self, text: str | list[str] | Document | list[Document], *args, **kwargs
    ) -> list:
        raise NotImplementedError

    def prepare_input(
        self, text: str | list[str] | Document | list[Document]
    ) -> list[Document]:
        if isinstance(text, (str, Document)):
            return [Document(content=text)]
        elif isinstance(text, list):
            return [Document(content=_) for _ in text]
        return text


class LCEmbeddingMixin:
    def _get_lc_class(self):
        raise NotImplementedError(
            "Please return the relevant Langchain class in in _get_lc_class"
        )

    def __init__(self, **params):
        # self._lc_class = self._get_lc_class()
        self._obj = self._lc_class(**params)
        self._kwargs: dict = params

        super().__init__()

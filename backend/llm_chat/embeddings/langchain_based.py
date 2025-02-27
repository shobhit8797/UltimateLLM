from llm_chat.embeddings.base import BaseEmbeddings, LCEmbeddingMixin


class LCHuggingFaceEmbeddings(LCEmbeddingMixin, BaseEmbeddings):
    """Wrapper around Langchain's HuggingFace embedding, focusing on key parameters
    Model name to use (https://huggingface.co/models?pipeline_tag=sentence-similarity&sort=trending)
    Popular Models:
    - sentence-transformers/all-mpnet-base-v2
    - sentence-transformers/all-MiniLM-L6-v2
    - BAAI/bge-large-en-v1.5
    """

    model_name: str

    def __init__(
        self,
        model_name: str = "sentence-transformers/all-mpnet-base-v2",
        **params,
    ):
        super().__init__(
            model_name=model_name,
            **params,
        )

    def _get_lc_class(self):
        from langchain_huggingface.embeddings import HuggingFaceEmbeddings

        return HuggingFaceEmbeddings

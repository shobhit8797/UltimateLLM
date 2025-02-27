from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CrossEncoderReranker
from langchain_community.cross_encoders import HuggingFaceCrossEncoder
from langchain_core.vectorstores import VectorStoreRetriever
from sentence_transformers import CrossEncoder

from ultimate_llm.utilities.resources import GlobalResources
from ultimate_llm.utilities.schema import Document


class CrossEncoder:
    def __init__(self, top_n: int = 15):
        self.top_n = top_n

        self.retriever: VectorStoreRetriever = (
            GlobalResources.get_vectorstore().get_retriever()
        )
        print("self.retriever: ", self.retriever)

        model = HuggingFaceCrossEncoder(model_name="BAAI/bge-reranker-base")
        compressor = CrossEncoderReranker(model=model, top_n=self.top_n)

        self._reranker = ContextualCompressionRetriever(
            base_compressor=compressor, base_retriever=self.retriever
        )

    def invoke(self, query: str, _filter):
        try:
            self.retriever.search_kwargs.update({"filter": _filter})

            return self._reranker.invoke(query)

        except Exception as e:
            print("Error: ", e, e.__traceback__.tb_lineno)
            raise

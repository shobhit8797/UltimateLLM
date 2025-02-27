from llm_chat.llms.base import BaseLLM
from llm_chat.storage.vectorstores.base import BaseVectorStore


class GlobalResources:
    """
    Singleton class to manage global resources such as vector stores, LLMs, docstores, and embeddings.
    """

    _faiss_instance = None
    _llm_instance = None
    _docstore = None
    _embedding = None
    _reranker = None

    @classmethod
    def get_vectorstore(cls) -> BaseVectorStore:
        """
        Retrieve or initialize the vector store instance.

        Returns:
            BaseVectorStore: Instance of the vector store.
        """
        if cls._faiss_instance is None:
            cls._faiss_instance = cls.initialize_faiss()
        return cls._faiss_instance

    @classmethod
    def get_chat_llm(cls) -> BaseLLM:
        print("Getting chat llm")
        if cls._llm_instance is None:
            print("Initializing chat llm")
            cls._llm_instance = cls.initialize_llm()
            print("Chat llm initialized")

        print("Returning chat llm")
        return cls._llm_instance

    @classmethod
    def get_docstore(cls):
        """
        Retrieve or initialize the document store instance.

        Returns:
            InMemoryDocstore: Instance of the document store.
        """
        if cls._docstore is None:
            cls._docstore = cls.initialize_docstore()
        return cls._docstore

    @classmethod
    def get_embedding(cls):
        """
        Retrieve or initialize the embedding instance.

        Returns:
            HuggingFaceEmbeddings: Instance of the embeddings.
        """
        if cls._embedding is None:
            cls._embedding = cls.initialize_embedding()
        return cls._embedding

    @classmethod
    def get_reranker(cls):
        """
        Retrieve or initialize the cross-encoder reranker instance.

        Returns:
            CrossEncoderReranker: Instance of the cross-encoder reranker.
        """
        if cls._reranker is None:
            cls._reranker = cls.initialize_reranker()
        return cls._reranker

    @staticmethod
    def initialize_embedding():
        """
        Initialize the embedding instance using Hugging Face embeddings.

        Returns:
            HuggingFaceEmbeddings: Configured embedding instance.
        """
        from langchain_huggingface import HuggingFaceEmbeddings

        # from langchain_openai import OpenAIEmbeddings
        # BAAI/bge-m3 | sentence-transformers/all-mpnet-base-v2
        return HuggingFaceEmbeddings(
            model_name="BAAI/bge-m3",
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": False},
        )
        # return OpenAIEmbeddings(model="text-embedding-3-small")

    @staticmethod
    def initialize_docstore():
        """
        Initialize an in-memory document store instance.

        Returns:
            InMemoryDocstore: Configured document store instance.
        """
        from langchain_community.docstore.in_memory import InMemoryDocstore

        return InMemoryDocstore()

    @staticmethod
    def initialize_faiss():
        """
        Initialize the FAISS-based vector store instance.

        Returns:
            FaissStore: Configured FAISS vector store instance.
        """

        from llm_chat.storage.vectorstores.faiss_store import FaissStore

        return FaissStore(
            embedding=GlobalResources.get_embedding(),
            docstore=GlobalResources.get_docstore(),
        )

    @staticmethod
    def initialize_llm() -> BaseLLM:
        """
        Initialize the LLM instance for chat functionality.

        Returns:
            LC_HF_Chat: Configured chat LLM instance.
        """
        from llm_chat.llms.openai_api import OpenAiLLM

        _chat_llm = OpenAiLLM()

        return _chat_llm

    @staticmethod
    def initialize_reranker():
        from llm_chat.rerankers.cross_encoder import CrossEncoder

        return CrossEncoder()

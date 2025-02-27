from abc import ABC, abstractmethod
from typing import Optional


class BaseVectorStore(ABC):
    @abstractmethod
    def __init__(self, *args, **kwargs): ...

    @abstractmethod
    def add_document(
        self,
        embeddings: list[list[float]],  # TODO: UPdate the type
        metadatas: Optional[list[dict]] = None,
        ids: Optional[list[str]] = None,
    ) -> list[str]:
        """Add vector embeddings to vector stores

        Args:
            embeddings: List of embeddings
            metadatas: List of metadata of the embeddings
            ids: List of ids of the embeddings
            kwargs: meant for vectorstore-specific parameters

        Returns:
            List of ids of the embeddings
        """
        ...

    @abstractmethod
    def query(
        self,
        input: str,
        top_k: int,
        filter: Optional[dict[str]] = None,
        **kwargs,
    ) -> tuple[list[list[float]], list[float], list[str]]:
        """Return the top k most similar vector embeddings

        Args:
            embedding: List of embeddings
            top_k: Number of most similar embeddings to return
            ids: List of ids of the embeddings to be queried

        Returns:
            the matched embeddings, the similarity scores, and the ids
        """
        ...

    @abstractmethod
    def delete(self, ids: list[str], **kwargs):
        """Delete vector embeddings from vector stores

        Args:
            ids: List of ids of the embeddings to be deleted
            kwargs: meant for vectorstore-specific parameters
        """
        ...

    @abstractmethod
    def drop(self):
        """Drop the vector store"""
        ...

import json
import os
from typing import Literal, Optional

import faiss
from langchain_community.vectorstores.faiss import FAISS

from llm_chat.embeddings.base import BaseEmbeddings
from llm_chat.storage.vectorstores.base import BaseVectorStore
from ultimate_llm.utilities.schema import Document


class FaissStore(BaseVectorStore):
    _indexed_ids: set = set()
    search_type: Literal["mmr", "similarity_score_threshold", "similarity"] = (
        "similarity"
    )
    search_k = 20  # Default number of results to retrieve
    mapping_file = "faiss_mappings.json"

    def __init__(self, *args, **kwargs):
        """Initializes FAISS store with persistence support."""
        embedding: BaseEmbeddings = kwargs.get("embedding")
        docstore = kwargs.get("docstore")
        self.index_file = kwargs.get(
            "index_file", "faiss_index.bin"
        )  # Default FAISS index file
        self._store = None
        self.index_to_docstore_id = {}

        # if os.path.exists(self.index_file):
        #     print(f"🔄 Loading FAISS index from {self.index_file}")
        #     self._store = self._load_faiss_index(embedding, docstore)
        # else:
        print("❌ No existing FAISS index found. Creating a new one...")
        self._initialize_faiss(embedding, docstore)

    def _load_faiss_index(self, embedding, docstore):
        """Loads FAISS index and ensures mappings are correct."""
        index = faiss.read_index(self.index_file)
        if os.path.exists(self.mapping_file):
            with open(self.mapping_file, "r") as f:
                self.index_to_docstore_id = json.load(f)

        faiss_size = index.ntotal
        mapping_size = len(self.index_to_docstore_id)

        if faiss_size != mapping_size:
            self._rebuild_mappings(index, embedding, docstore)

        return FAISS(
            embedding_function=embedding,
            index=index,
            docstore=docstore,
            index_to_docstore_id=self.index_to_docstore_id,
        )

    def _initialize_faiss(self, embedding, docstore):
        """Creates a new FAISS index with the correct dimension."""
        dimension = len(embedding.embed_query("test query"))
        index = faiss.IndexFlatL2(dimension)
        self._store = FAISS(
            embedding_function=embedding,
            index=index,
            docstore=docstore,
            index_to_docstore_id={},
        )
        self.index_to_docstore_id = {}
        faiss.write_index(index, self.index_file)
        print(f"✅ New FAISS index saved to {self.index_file}")

    def _rebuild_mappings(self, index, embedding, docstore):
        """Rebuilds FAISS index-to-docstore mappings if they are missing."""

        self.index_to_docstore_id = {}
        dimension = len(embedding.embed_query("test query"))
        index = faiss.IndexFlatL2(dimension)
        self._store = FAISS(
            embedding_function=embedding,
            index=index,
            docstore=docstore,
            index_to_docstore_id=self.index_to_docstore_id,
        )

        self._save_mappings()
        self.save_vectorstore()

    def _save_mappings(self):
        """Saves FAISS index-to-document mappings."""
        with open(self.mapping_file, "w") as f:
            json.dump(self.index_to_docstore_id, f)

    def add_document(self, documents: list[Document]) -> list[str]:
        """Adds documents to FAISS and ensures they are stored in docstore."""
        documents_to_add = [doc for doc in documents if doc.id not in self._indexed_ids]
        if not documents_to_add:
            return []

        # Validate document structure
        for doc in documents_to_add:
            if not hasattr(doc, "page_content"):
                raise AttributeError(
                    f"Document {doc.id} is missing 'page_content' attribute"
                )

        added_ids = self._store.add_documents(documents_to_add)

        # Update indexed IDs and FAISS mappings
        for i, doc in enumerate(documents_to_add):
            faiss_id = len(self.index_to_docstore_id)  # Ensure new index is correct
            self.index_to_docstore_id[str(faiss_id)] = (
                doc.id
            )  # Mapping FAISS index to document ID

        self._indexed_ids.update(added_ids)
        self._save_mappings()

        return added_ids

    def query(
        self,
        input: str,
        top_k: int = 2,
        filter: Optional[dict[str]] = None,
        **kwargs,
    ) -> list[Document]:
        results = self._store.similarity_search(
            input, k=top_k, filter=filter, fetch_k=20
        )

        return results if results else []

    def get_retriever(self):
        """Returns the FAISS retriever with configured search parameters."""
        return self._store.as_retriever(search_kwargs={"k": self.search_k})

    def save_vectorstore(self):
        """Saves the FAISS index and mappings for persistence."""
        faiss.write_index(self._store.index, self.index_file)
        self._save_mappings()
        print(f"✅ FAISS index saved to {self.index_file}")

    def delete(self, ids: list[str], **kwargs):
        """Delete documents from FAISS. Not implemented yet."""
        raise NotImplementedError("Delete function is not implemented.")

    def drop(self):
        """Drop the entire FAISS index. Not implemented yet."""

        raise NotImplementedError("Drop function is not implemented.")

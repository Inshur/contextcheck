from abc import ABC, abstractmethod
from typing import List

from pydantic import BaseModel


class RagApiWrapperBase(BaseModel, ABC):
    top_k: int = 5

    @abstractmethod
    def list_documents(self) -> List[dict[str, str]]:
        """
        List documents from the RAG API.
        Returns a list of dictionaries, each containing the document ID and the document title.
        """
        pass

    @abstractmethod
    def get_document_chunks(self, document_id: str) -> List[str]:
        """
        Retrieve document chunks by document ID from the RAG API.
        Returns a list of strings, each representing a chunk of the document.
        Chunks should be ordered as they appear in the document.
        """
        pass

    @abstractmethod
    def query_semantic_db(self, query: str) -> List[str]:
        """
        Query the semantic database through the RAG API.
        Returns a list of strings, each representing a result of the query.
        """
        pass

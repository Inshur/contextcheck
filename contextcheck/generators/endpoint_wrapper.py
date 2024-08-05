from abc import ABC, abstractmethod
from typing import List

from pydantic import BaseModel


class RagApiWrapperBase(BaseModel, ABC):

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
    def query_semantic_db(self, query: str, **kwargs) -> List[str]:
        """
        Query the semantic database through the RAG API.
        Returns a list of strings, each representing a result of the query.
        """
        pass

    @abstractmethod
    def query_qa(self, question: str, **kwargs) -> List[str]:
        """
        Query the question answering model through the RAG API.
        Returns a list of strings, each representing an answer to the question.
        """
        pass
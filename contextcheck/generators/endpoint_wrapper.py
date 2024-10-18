from abc import ABC, abstractmethod

from pydantic import BaseModel, Field


# NOTE RB: For list[dict] return types I'd create a pydantic model, as otherwise it is confusing
# Or at least a TypedDict
class RagApiWrapperBase(BaseModel, ABC):
    timeout: int = Field(default=60, description="A timeout set for a request")

    @abstractmethod
    def list_documents(self) -> list[dict[str, str]]:
        """
        List documents from the RAG API.
        Returns a list of dictionaries, each containing the document ID and the document title.
        """

    @abstractmethod
    def get_document_chunks(self, document_id: str) -> list[str]:
        """
        Retrieve document chunks by document ID from the RAG API.
        Returns a list of strings, each representing a chunk of the document.
        Chunks should be ordered as they appear in the document.
        """

    @abstractmethod
    def query_semantic_db(self, query: str, **kwargs) -> list[dict]:
        """
        Query the semantic database through the RAG API.
        Returns a list of dicts, each representing a semantic search result.
        """

    @abstractmethod
    def query_qa(self, query: str, **kwargs) -> list[dict]:
        """
        Query the question answering model through the RAG API.
        Returns a list of dicts, each representing an answer to the query.
        """

import os
from typing import List

import dotenv
import requests

from contextcheck.generators.endpoint_wrapper import RagApiWrapperBase

dotenv.load_dotenv()


class ContextClueApiWrapper(RagApiWrapperBase):
    endpoint_base_url: str = os.environ["ENDPOINT_BASE_URL"]
    header_key: str = os.environ["HEADER_KEY"]
    header_value: str = os.environ["HEADER_VALUE"]

    @property
    def headers(self) -> dict[str, str]:
        return {self.header_key: self.header_value}

    def list_documents(self) -> List[dict[str, str]]:
        response = requests.get(f"{self.endpoint_base_url}/documents/", headers=self.headers)
        response.raise_for_status()

        return [{"id": file["id"], "name": file["name"]} for file in response.json()["documents"]]

    def get_document_chunks(self, document_id: str) -> List[str]:
        response = requests.get(
            f"{self.endpoint_base_url}/documents/{document_id}/", headers=self.headers
        )
        response.raise_for_status()

        return response.json()["document"]["chunks"]

    def query_semantic_db(self, query: str) -> List[str]:
        response = requests.post(
            f"{self.endpoint_base_url}/semantic_search/get_relevant_documents",
            data={"query": query, "top_k": self.top_k},
            headers=self.headers,
        )
        response.raise_for_status()

        chunks = response.json()["relevant_documents"]["collection_retriever_entries"]
        return [chunk["chunk"] for chunk in chunks]

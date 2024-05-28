from pydantic import model_serializer

from contextcheck.connectors.connector_http import ConnectorHTTP
from contextcheck.endpoints.endpoint import EndpointBase
from contextcheck.models.request import RequestBase


class EndpointCCPromptLLM(EndpointBase):
    class RequestModel(RequestBase):
        @model_serializer
        def serialize(self) -> dict:
            return {"prompt": self.message}

    def model_post_init(self, __context) -> None:
        self.connector = ConnectorHTTP(
            url=self.config.url,
            additional_headers=self.config.additional_headers,
        )
